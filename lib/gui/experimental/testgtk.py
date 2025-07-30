import math
from typing import Tuple, Optional
import gi

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk
import moderngl
from pyglm import glm

import numpy as np

import PIL.Image
import pathlib

from ...stitch_plan import StitchPlan, Stitch

basedir = pathlib.Path(__file__).parent

class MyGLArea(Gtk.GLArea):
    __gtype_name__ = "GLPreview"

    def __init__(self):
        Gtk.GLArea.__init__(self)

        self.ctx: Optional[moderngl.Context] = None
        self.stitch_plan: Optional[StitchPlan] = None

        self.set_allowed_apis(Gdk.GLAPI.GL)
        self.connect("realize", self.on_realize)
        self.connect("render", self.on_render)
        self.connect("resize", self.on_resize)

        self.mode = 0

        self.light_azimuth = 135
        self.light_elevation = 45
        self._update_light_vector()

        self.vbo = None

        self.k_a = 0
        self.k_d = 1.0
        self.k_s = 1.0
        self.specular_exponent = 20.0
        self.zoom = 1.0

        self.progress = 0

    def _update_light_vector(self):
        azimuth_radians = math.radians(-self.light_azimuth)
        elevation_radians = math.radians(self.light_elevation)
        ce = math.cos(elevation_radians)
        self.light_vector = [
            math.cos(azimuth_radians)*ce,
            math.sin(azimuth_radians)*ce,
            math.sin(elevation_radians)
        ]
        self.queue_draw()

    def set_light_azimuth(self, azimuth):
        self.light_azimuth = azimuth
        self._update_light_vector()

    def set_light_elevation(self, elevation):
        self.light_elevation = elevation
        self._update_light_vector()

    def on_realize(self, area):
        gdk_ctx = self.get_context()
        assert gdk_ctx
        gdk_ctx.make_current()
        ctx = self.ctx = moderngl.get_context()

        self.prog = ctx.program(
            vertex_shader="""
                #version 330

                uniform mat4 projection;
                uniform mat4 transform;

                in vec2 in_vert;
                in vec2 in_uv;
                in vec3 in_t;
                in vec3 in_b;
                in vec3 in_n;
                in vec3 in_color;

                out vec2 v_uv;
                out vec3 v_t;
                out vec3 v_b;
                out vec3 v_n;
                out vec3 v_color;

                void main() {
                    v_uv = in_uv;
                    v_t = in_t;
                    v_b = in_b;
                    v_n = in_n;
                    v_color = in_color;
                    gl_Position = projection * transform * vec4(in_vert, 0.0, 1.0);
                }
            """,
            fragment_shader="""
                #version 330

                #define saturate(x) clamp(x, 0.0, 1.0)

                uniform int mode;

                uniform float k_a;
                uniform float k_d;
                uniform float k_s;
                uniform float specular_exponent;
                uniform sampler2D tex;

                uniform vec3 light_vec;

                in vec2 v_uv;
                in vec3 v_t;
                in vec3 v_b;
                in vec3 v_n;
                in vec3 v_color;

                out vec4 f_color;

                void main() {
                    vec4 normal_alpha = texture(tex, v_uv);
                    // if (normal_alpha.a < 0.5) {
                    //     discard;
                    // }
                    mat3 TBN = transpose(mat3(v_t, v_b, v_n));
                    vec3 normal = TBN * (normal_alpha.xyz-0.5)*2.0;
                    if (mode == 0) {
                        vec3 H = normalize(normalize(light_vec) + vec3(0.0,0.0,1.0));
                        float specular = k_s * pow(saturate(dot(normal, H)), specular_exponent);
                        float diffuse = k_d * saturate(dot(normal, normalize(light_vec))); 
                        f_color = vec4(saturate((k_a + diffuse)*v_color + vec3(specular)), normal_alpha.a);
                    } else {
                        f_color = vec4((normal.xyz+1.0)/2.0, normal_alpha.a);
                    }
                }
            """,
        )

        with PIL.Image.open(basedir / "texture/normals-fixed.png") as i:
          self.tex = ctx.texture((i.width, i.height), 4, i.tobytes())
          self.tex.build_mipmaps()
          self.tex.repeat_y = False
        
        self._generate_stitches()


    def _generate_stitches(self):
        ctx = self.ctx
        assert ctx

        STITCH_HEIGHT = 1.398  # From rendering.py

        if self.stitch_plan is None:
            return

        buf = bytearray()
        ibuf = bytearray()
        cur_index = 0

        for color_block in self.stitch_plan.color_blocks:
            if color_block.color is not None:
                color = color_block.color.rgb_normalized
            else:
                color = (0.0,0.0,0.0)

            start_stitch: Stitch
            end_stitch: Stitch
            for start_stitch, end_stitch in zip(color_block[:-1], color_block[1:]):
                if end_stitch.trim or end_stitch.stop or end_stitch.color_change or end_stitch.jump:
                    # Break the line from a trim/stop/color change.
                    # For now, fill the 6 indices for this stitch with two degenerate triangles, so that the
                    # progress indicator works as expected.
                    indices = np.array([
                        0, 0, 0,
                        0, 0, 0,
                    ], dtype=np.uint16)
                    ibuf.extend(indices.tobytes())

                else:
                    # This is a normal stitch, generate geometry and indices
                    start = glm.vec2(start_stitch.x, start_stitch.y)
                    end = glm.vec2(end_stitch.x, end_stitch.y)
                    delta = (end-start)
                    length = glm.length(delta)
                    if length > 0.00001:
                        along = delta/length
                        across = glm.vec2(along[1], -along[0])
                    else:
                        along = glm.vec2(0.0, 0.0)
                        across = glm.vec2(0.0, 0.0)
                    

                    ue = end + across * (STITCH_HEIGHT/2)
                    le = end - across * (STITCH_HEIGHT/2)
                    us = start + across * (STITCH_HEIGHT/2)
                    ls = start - across * (STITCH_HEIGHT/2)

                    # Tangent/Bitangent/Normal vectors used for normal mapping
                    # The Tangent runs in the general direction of the stitch
                    # The Bitangent runs across the stitch
                    # The Normal points towards the viewer
                    tangent = glm.vec3(along, 0.0)
                    bitangent = glm.vec3(across, 0.0)
                    normal = glm.vec3(0.0, 0.0, 1.0)

                    repeats = length/STITCH_HEIGHT/2
                    vertices = np.array([
                        *ue, repeats, 0.0, *tangent, *bitangent, *normal, *color,
                        *us, 0.0,     0.0, *tangent, *bitangent, *normal, *color, 
                        *le, repeats, 1.0, *tangent, *bitangent, *normal, *color,
                        *ls, 0.0,     1.0, *tangent, *bitangent, *normal, *color,
                    ], dtype=np.float32)
                    buf.extend(vertices.tobytes())

                    indices = np.array([
                        cur_index    , cur_index + 1, cur_index + 2,
                        cur_index + 1, cur_index + 2, cur_index + 3,
                    ], dtype=np.uint16)
                    ibuf.extend(indices.tobytes())
                    cur_index = cur_index + 4

        if self.vbo is None:
            self.vbo = ctx.buffer(buf)
            self.ibo = ctx.buffer(ibuf)
        else:
            self.vbo.write(buf)
            self.ibo.write(ibuf)
        
        self.vao = ctx.vertex_array(
            self.prog, 
            self.vbo, "in_vert", "in_uv", "in_t", "in_b", "in_n", "in_color", 
            index_buffer = self.ibo, index_element_size=2, mode=moderngl.TRIANGLES
        )
        pass

    def on_resize(self, area, width, height):
        self.prog["projection"].write(glm.scale(glm.vec3(height/width, 1, 1)))
        
    def on_render(self, area, gdk_ctx):
        ctx = self.ctx
        assert ctx

        fb = self.ctx.detect_framebuffer()

        fb.use()
        fb.clear(0,0,0,0)

        scale = self.base_scale*self.zoom
        xform = glm.scale(glm.vec3(scale, -scale, 1)) @ glm.translate(self.pan)

        self.prog["k_a"] = self.k_a
        self.prog["k_d"] = self.k_d
        self.prog["k_s"] = self.k_s
        self.prog["specular_exponent"] = self.specular_exponent
        self.prog["light_vec"] = self.light_vector
        self.prog["transform"].write(xform)

        self.prog["mode"] = self.mode

        ctx.enable(ctx.BLEND)
        ctx.blend_func = (ctx.SRC_ALPHA, ctx.ONE_MINUS_SRC_ALPHA)

        self.tex.use(location=0)
        vertices = min(self.progress*6, self.vao.vertices)
        self.vao.render(vertices=vertices)

        return True
    
    def set_stitch_plan(self, stitch_plan: StitchPlan):
        self.stitch_plan = stitch_plan
        if self.ctx is not None:
            self._generate_stitches()

        self.progress = stitch_plan.num_stitches

        minx, miny, maxx, maxy = self.stitch_plan.bounding_box
        self.pan = glm.vec3(-(minx+maxx)/2, -(miny+maxy)/2, 0)
        self.base_scale = 1.9/(maxy-miny)

@Gtk.Template(filename=str(basedir / "test-gl.ui"))
class RenderWindow(Gtk.ApplicationWindow):
    __gtype_name__ = "RenderWindow"


    area: MyGLArea = Gtk.Template.Child("area")

    @Gtk.Template.Callback()
    def change_zoom(self, scale: Gtk.Scale, type: Gtk.ScrollType, data: float):
        self.area.zoom = data
        self.area.queue_render()

    @Gtk.Template.Callback()
    def change_light_angle(self, scale: Gtk.Scale, type: Gtk.ScrollType, data: float):
        self.area.set_light_azimuth(data)

    @Gtk.Template.Callback()
    def change_light_elevation(self, scale: Gtk.Scale, type: Gtk.ScrollType, data: float):
        self.area.set_light_elevation(data)

    @Gtk.Template.Callback()
    def change_ambient(self, scale: Gtk.Scale, type: Gtk.ScrollType, data: float):
        self.area.k_a = data
        self.area.queue_render()

    @Gtk.Template.Callback()
    def change_diffuse(self, scale: Gtk.Scale, type: Gtk.ScrollType, data: float):
        self.area.k_d = data
        self.area.queue_render()

    @Gtk.Template.Callback()
    def change_specular(self, scale: Gtk.Scale, type: Gtk.ScrollType, data: float):
        self.area.k_s = data
        self.area.queue_render()

    @Gtk.Template.Callback()
    def change_specular_exponent(self, scale: Gtk.Scale, type: Gtk.ScrollType, data: float):
        self.area.specular_exponent = data
        self.area.queue_render()

    progress: Gtk.Scale = Gtk.Template.Child("progress")

    @Gtk.Template.Callback()
    def change_progress(self, scale: Gtk.Scale, type: Gtk.ScrollType, data: float):
        self.area.progress = int(data)
        self.area.queue_render()

    def set_stitch_plan(self, stitch_plan: StitchPlan):
        self.area.set_stitch_plan(stitch_plan)
        self.progress.set_range(0, stitch_plan.num_stitches)
        self.progress.set_value(stitch_plan.num_stitches)

    def on_mode_changed(self, dropdown, param):
        self.area.mode = self.mode.props.selected
        self.area.queue_draw()

    mode: Gtk.DropDown = Gtk.Template.Child("mode")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.mode.connect("notify::selected", self.on_mode_changed)

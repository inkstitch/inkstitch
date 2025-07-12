# Temporary rendering code, adapted/cribbed from skia docs
import skia
import typing

def make_image(context: typing.Optional[skia.GrDirectContext], effect: skia.Shader, info: skia.ImageInfo):
    if context is not None:
        surface = skia.Surface.MakeRenderTarget(context, skia.Budgeted.kNo, info)
    else:
        surface = skia.Surfaces.Raster(info)
    canvas = surface.getCanvas()
    shader = effect.makeShader(None)
    assert shader is not None
    paint = skia.Paint()
    paint.setShader(shader)
    paint.setBlendMode(skia.BlendMode.kSrc)
    canvas.drawPaint(paint)
    return surface.makeImageSnapshot()

def render(context: typing.Optional[skia.GrDirectContext], canvas: skia.Canvas):
    imageinfo = skia.ImageInfo.MakeN32Premul(128, 128)
    imageshader = skia.RuntimeEffect.MakeForShader(r"""
     vec4 main(vec2 p) {
       p = (p / 128) * 2 - 1;
       float len2 = dot(p, p);
       vec3 v = (len2 > 1) ? vec3(0, 0, 1) : vec3(p, sqrt(1 - len2));
       return (v * 0.5 + 0.5).xyz1;
     }""")

    normalimage = make_image(context, imageshader, imageinfo)
    canvas.drawImage(normalimage, 0, 128)

    liteffect = skia.RuntimeEffect.MakeForShader(r"""
     uniform shader normals;
     vec4 main(vec2 p) {
       vec3 n = normalize(normals.eval(p).xyz * 2 - 1);
       vec3 l = normalize(vec3(-1, -1, 0.5));
       return saturate(dot(n, l)).xxx1;
     }""")
    builder = skia.RuntimeShaderBuilder(liteffect)
    paint = skia.Paint()
    builder.setChild('normals', normalimage.makeShader(skia.SamplingOptions()))
    paint.setShader(builder.makeShader())
    canvas.drawRect(skia.Rect(0,0,128,128), paint)
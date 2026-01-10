# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import sys
from base64 import b64encode
from re import findall
from tempfile import TemporaryDirectory
from typing import Optional, Tuple

from inkex import BaseElement, Boolean, Image, errormsg

from ..commands import add_layer_commands
from ..i18n import _
from ..marker import set_marker
from ..stitch_plan import stitch_groups_to_stitch_plan
from ..svg import render_stitch_plan
from ..svg.tags import (INKSCAPE_GROUPMODE, INKSTITCH_ATTRIBS,
                        SODIPODI_INSENSITIVE, SVG_GROUP_TAG, SVG_PATH_TAG,
                        XLINK_HREF)
from .base import InkstitchExtension
from .stitch_plan_preview_undo import reset_stitch_plan
from .utils.inkex_command import inkscape


class StitchPlanPreview(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--notebook")
        self.arg_parser.add_argument("-s", "--move-to-side", type=Boolean, default=True, dest="move_to_side")
        self.arg_parser.add_argument("-v", "--layer-visibility", type=str, default="unchanged", dest="layer_visibility")
        self.arg_parser.add_argument("-n", "--needle-points", type=Boolean, default=False, dest="needle_points")
        self.arg_parser.add_argument("-i", "--insensitive", type=Boolean, default=False, dest="insensitive")
        self.arg_parser.add_argument("-c", "--visual-commands", type=Boolean, default="symbols", dest="visual_commands")
        self.arg_parser.add_argument("-j", "--render-jumps", type=Boolean, default=True, dest="render_jumps")
        self.arg_parser.add_argument("-m", "--render-mode", type=str, default="simple", dest="mode")
        self.arg_parser.add_argument("-l", "--ignore-layer", type=Boolean, default=True, dest="ignore_layer")
        self.arg_parser.add_argument("-o", "--overwrite", type=Boolean, default=True, dest="overwrite")

    def effect(self):
        realistic, dpi = self.parse_mode()

        # delete old stitch plan
        self.remove_old()

        # create new stitch plan
        if not self.get_elements():
            return

        svg = self.document.getroot()
        visual_commands = self.options.visual_commands
        self.metadata = self.get_inkstitch_metadata()
        collapse_len = self.metadata['collapse_len_mm']
        min_stitch_len = self.metadata['min_stitch_len_mm']
        stitch_groups = self.elements_to_stitch_groups(self.elements)
        stitch_plan = stitch_groups_to_stitch_plan(stitch_groups, collapse_len=collapse_len, min_stitch_len=min_stitch_len)

        layer = render_stitch_plan(svg, stitch_plan, realistic, visual_commands, render_jumps=self.options.render_jumps)
        if self.options.ignore_layer and not self.options.mode[-1].isdigit():
            add_layer_commands(layer, ["ignore_layer"])
        layer = self.rasterize(svg, layer, dpi)

        # update layer visibility (unchanged, hidden, lower opacity)
        groups = self.document.getroot().findall(SVG_GROUP_TAG)
        self.set_invisible_layers_attribute(groups, layer)
        self.set_visibility(groups, layer)

        self.set_sensitivity(layer)
        self.translate(svg, layer)
        self.set_needle_points(layer)

    def parse_mode(self) -> Tuple[bool, Optional[int]]:
        """
        Parse the "mode" option and return a tuple of a bool indicating if realistic rendering should be used,
        and an optional int indicating the dpi value to use for rasterization, or None if rasterization should not be used.
        """
        realistic = False
        dpi: Optional[int] = None
        render_mode = self.options.mode
        if render_mode == "simple":
            pass
        elif render_mode.startswith("realistic-"):
            realistic = True
            dpi_option = render_mode.split('-')[1]
            if dpi_option != "vector":
                try:
                    dpi = int(dpi_option)
                except ValueError:
                    errormsg(f"Invalid raster mode {dpi_option}")
                    sys.exit(1)
        else:
            errormsg(f"Invalid render mode {render_mode}")
            sys.exit(1)

        return (realistic, dpi)

    def remove_old(self):
        svg = self.document.getroot()
        if self.options.overwrite:
            reset_stitch_plan(svg)
        else:
            reset_stitch_plan(svg, False)
            layer = svg.find(".//*[@id='__inkstitch_stitch_plan__']")
            if layer is not None:
                layer.set('id', svg.get_unique_id('inkstitch_stitch_plan_'))

    def rasterize(self, svg: BaseElement, layer: BaseElement, dpi: Optional[int]) -> BaseElement:
        if dpi is None:
            # Don't rasterize if there's no reason to.
            return layer
        else:
            with TemporaryDirectory() as tempdir:
                # Inkex's command functionality also writes files to temp directories like this.
                temp_svg_path = f"{tempdir}/temp.svg"
                temp_png_path = f"{tempdir}/temp.png"
                with open(temp_svg_path, "wb") as f:
                    f.write(svg.tostring())

                # We need the bounding box of the stitch layer so we can place the rasterized version in the same place.
                # however, layer.bounding_box() is pure python, so it can be very slow for more complex stitch previews.
                # Instead, especially because we need to invoke Inkscape anyway to perform the rasterization, we get
                # the bounding box with query commands before we perform the export. This is quite cheap.
                try:
                    out = inkscape(temp_svg_path, actions="; ".join([
                        f"select-by-id: {layer.get_id()}",
                        "query-x",
                        "query-y",
                        "query-width",
                        "query-height",
                        f"export-id: {layer.get_id()}",
                        "export-id-only",
                        "export-type: png",
                        f"export-dpi: {dpi}",
                        "export-png-color-mode: RGBA_16",
                        f"export-filename: {temp_png_path}",
                        "export-do"  # Inkscape docs say this should be implicit at the end, but it doesn't seem to be.
                    ]))
                except PermissionError:
                    # Windows-specific issue: antivirus, UAC, or MS Store installation privileges
                    errormsg(_(
                        "Permission denied when calling Inkscape.\n\n"
                        "This can happen due to:\n"
                        "• Antivirus software blocking the operation\n"
                        "• Windows security settings\n"
                        "• Inkscape installed from Microsoft Store (try the standalone installer instead)\n\n"
                        "Try running Inkscape as Administrator, or use the vector preview mode instead."
                    ))
                    return layer  # Return the non-rasterized layer as fallback

                # Extract numbers from returned string. It can include other information such as warnings about the usage of AppImages
                out = findall(r"(?m)^-?\d+\.?\d*$", out)

                # Parse the returned coordinates out into viewport units
                x, y, width, height = map(lambda x: svg.viewport_to_unit(f'{x}px'), out)

                # Embed the rasterized stitch plan into the SVG, and replace the original stitch plan
                with open(temp_png_path, "rb") as f:
                    image = Image(attrib={
                        XLINK_HREF: f"data:image/png;base64,{b64encode(f.read()).decode()}",
                        "x": str(x),
                        "y": str(y),
                        "height": str(height),
                        "width":  str(width),
                    })
                    layer.replace_with(image)
                    return image

    def set_invisible_layers_attribute(self, groups, layer):
        invisible_layers = []
        for g in groups:
            if g.get(INKSCAPE_GROUPMODE) == "layer" and 'display' in g.style and g.style['display'] == 'none':
                invisible_layers.append(g.get_id())
        layer.set(INKSTITCH_ATTRIBS['invisible_layers'], ",".join(invisible_layers))
        layer.set(INKSTITCH_ATTRIBS['layer_visibility'], self.options.layer_visibility)

    def set_visibility(self, groups, layer):
        if self.options.layer_visibility == "hidden":
            self.hide_all_layers()
            layer.style['display'] = "inline"
        elif self.options.layer_visibility == "lower_opacity":
            for g in groups:
                style = g.specified_style()
                # check groupmode and exclude stitch_plan layer
                # exclude objects which are not displayed at all or already have opacity < 0.4
                if (g.get(INKSCAPE_GROUPMODE) == "layer" and not g == layer and
                        float(style.get('opacity', 1)) > 0.4 and not style.get('display', 'inline') == 'none'):
                    g.style['opacity'] = 0.4

    def set_sensitivity(self, layer):
        if self.options.insensitive is True:
            layer.set(SODIPODI_INSENSITIVE, True)
        else:
            layer.pop(SODIPODI_INSENSITIVE)

    def translate(self, svg, layer):
        if self.options.move_to_side:
            # translate stitch plan to the right side of the canvas
            translate = svg.get('viewBox', '0 0 800 0').split(' ')[2]
            layer.transform = layer.transform.add_translate(translate)

    def set_needle_points(self, layer):
        if self.options.needle_points:
            for element in layer.iterdescendants(SVG_PATH_TAG):
                set_marker(element, 'start', 'needle-point')
                set_marker(element, 'mid', 'needle-point')
                set_marker(element, 'end', 'needle-point')

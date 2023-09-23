# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import inkex
import numpy as np
from scipy.spatial import KDTree

from ..commands import add_layer_commands
from ..i18n import _
from ..stitch_plan import stitch_groups_to_stitch_plan
from ..svg import PIXELS_PER_MM
from ..svg.tags import INKSCAPE_GROUPMODE, INKSCAPE_LABEL, SVG_GROUP_TAG
from ..svg.units import get_viewbox_transform
from ..utils import cache
from .base import InkstitchExtension


class DensityMap(InkstitchExtension):
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("-v", "--layer-visibility", type=int, default=0, dest="layer_visibility")
        self.arg_parser.add_argument("-l", "--num-neighbors-red", type=int, default=6, dest="num_neighbors_red")
        self.arg_parser.add_argument("-r", "--density-radius-red", type=float, default=0.5, dest="radius_red")
        self.arg_parser.add_argument("-m", "--num-neighbors-yellow", type=int, default=3, dest="num_neighbors_yellow")
        self.arg_parser.add_argument("-s", "--density-radius-yellow", type=float, default=0.5, dest="radius_yellow")

    def effect(self):
        # delete old stitch plan
        svg = self.document.getroot()
        reset_density_plan(svg)

        # create new stitch plan
        if not self.get_elements():
            return

        self.metadata = self.get_inkstitch_metadata()
        collapse_len = self.metadata['collapse_len_mm']
        patches = self.elements_to_stitch_groups(self.elements)
        stitch_plan = stitch_groups_to_stitch_plan(patches, collapse_len=collapse_len)

        layer = svg.find(".//*[@id='__inkstitch_density_plan__']")
        color_groups = create_color_groups(layer)
        density_options = [{'max_neighbors': self.options.num_neighbors_red, 'radius': self.options.radius_red},
                           {'max_neighbors': self.options.num_neighbors_yellow, 'radius': self.options.radius_yellow}]
        color_block_to_density_markers(svg, color_groups, stitch_plan, density_options)

        # update layer visibility 0 = unchanged, 1 = hidden, 2 = lower opacity
        groups = self.document.getroot().findall(SVG_GROUP_TAG)
        if self.options.layer_visibility == 1:
            self.hide_all_layers()
            layer.style['display'] = "inline"
        elif self.options.layer_visibility == 2:
            for g in groups:
                style = g.specified_style()
                # check groupmode and exclude density layer
                # exclude objects which are not displayed at all or already have opacity < 0.4
                if (g.get(INKSCAPE_GROUPMODE) == "layer" and not g == layer and
                        float(style.get('opacity', 1)) > 0.4 and not style.get('display', 'inline') == 'none'):
                    g.style['opacity'] = 0.4


def reset_density_plan(svg):
    layer = svg.find(".//*[@id='__inkstitch_density_plan__']")
    if layer is None:
        layer = inkex.Group(attrib={
            'id': '__inkstitch_density_plan__',
            INKSCAPE_LABEL: _('Density Plan'),
            INKSCAPE_GROUPMODE: 'layer'
        })
        svg.append(layer)
        add_layer_commands(layer, ["ignore_layer"])
    else:
        # delete old density plan
        del layer[:]

        # make sure the layer is visible
        layer.set('style', 'display:inline')


def create_color_groups(layer):
    color_groups = []
    colors = [_("Red"), _("Yellow"), _("Green")]
    for color in colors:
        color_group = inkex.Group(attrib={
            'id': '__%s_density_layer__' % color.lower(),
            INKSCAPE_LABEL: _('%s density') % color,
        })
        layer.append(color_group)
        color_groups.append(color_group)
    return color_groups


def color_block_to_density_markers(svg, groups, stitch_plan, density_options):
    num_neighbors = []
    for option in density_options:
        radius = option['radius'] * PIXELS_PER_MM
        num_neighbors.append(get_stitch_density(stitch_plan, radius))

    red_group, yellow_group, green_group = groups
    for red_neighbors, yellow_neighbors, coord in zip(num_neighbors[0][0], num_neighbors[1][0], num_neighbors[0][1]):
        color = "green"  # green
        group = green_group
        if density_options[0]['max_neighbors'] <= red_neighbors:
            color = "red"
            group = red_group
        elif density_options[1]['max_neighbors'] <= yellow_neighbors:
            color = "yellow"
            group = yellow_group
        density_marker = inkex.Circle(attrib={
            'id': svg.get_unique_id("density_marker"),
            'style': "fill: %s; stroke: #7e7e7e; stroke-width: 0.02%%;" % color,
            'cx': "%s" % coord[0],
            'cy': "%s" % coord[1],
            'r': str(0.5),
            'transform': get_correction_transform(svg)
        })
        group.append(density_marker)


def get_stitch_density(stitch_plan, radius):
    stitches = []
    for color_block in stitch_plan:
        for stitch in color_block:
            stitches.append((stitch.x, stitch.y))

    # get density per stitch
    tree = KDTree(np.array(stitches))
    neighbors = tree.query_ball_tree(tree, radius)
    density = [len(i) for i in neighbors], stitches

    return density


@cache
def get_correction_transform(svg):
    transform = get_viewbox_transform(svg)

    # we need to correct for the viewbox
    transform = -inkex.transforms.Transform(transform)

    return str(transform)

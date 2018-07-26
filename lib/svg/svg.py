import simpletransform, simplestyle, inkex

from .units import get_viewbox_transform
from .tags import SVG_GROUP_TAG, INKSCAPE_LABEL, INKSCAPE_GROUPMODE, SVG_PATH_TAG, SVG_DEFS_TAG
from .realistic_rendering import realistic_stitch, realistic_filter
from ..i18n import _
from ..utils import cache


def color_block_to_point_lists(color_block):
    point_lists = [[]]

    for stitch in color_block:
         if stitch.trim:
              if point_lists[-1]:
                  point_lists.append([])
                  continue

         if not stitch.jump and not stitch.color_change:
              point_lists[-1].append(stitch.as_tuple())

    return point_lists


@cache
def get_correction_transform(svg):
    transform = get_viewbox_transform(svg)

    # we need to correct for the viewbox
    transform = simpletransform.invertTransform(transform)
    transform = simpletransform.formatTransform(transform)

    return transform


def color_block_to_realistic_stitches(color_block, svg):
    paths = []

    for point_list in color_block_to_point_lists(color_block):
        if not point_list:
            continue

        color = color_block.color.visible_on_white.darker.to_hex_str()
        start = point_list[0]
        for point in point_list[1:]:
            paths.append(inkex.etree.Element(
                SVG_PATH_TAG,
                {'style': simplestyle.formatStyle(
                    {
                        'fill': color,
                        'stroke': 'none',
                        'filter': 'url(#realistic-stitch-filter)'
                    }),
                'd': realistic_stitch(start, point),
                'transform': get_correction_transform(svg)
                }))
            start = point

    return paths

def color_block_to_paths(color_block, svg):
    paths = []
    # We could emit just a single path with one subpath per point list, but
    # emitting multiple paths makes it easier for the user to manipulate them.
    for point_list in color_block_to_point_lists(color_block):
        color = color_block.color.visible_on_white.to_hex_str()
        paths.append(inkex.etree.Element(
            SVG_PATH_TAG,
            {'style': simplestyle.formatStyle(
                {'stroke': color,
                'stroke-width': "0.4",
                'fill': 'none'}),
            'd': "M" + " ".join(" ".join(str(coord) for coord in point) for point in point_list),
            'transform': get_correction_transform(svg),
            'embroider_manual_stitch': 'true',
            'embroider_trim_after': 'true',
            }))

    # no need to trim at the end of a thread color
    if paths:
        paths[-1].attrib.pop('embroider_trim_after')

    return paths

def render_stitch_plan(svg, stitch_plan, realistic=False):
    layer = svg.find(".//*[@id='__inkstitch_stitch_plan__']")
    if layer is None:
        layer = inkex.etree.Element(SVG_GROUP_TAG,
                                    {'id': '__inkstitch_stitch_plan__',
                                     INKSCAPE_LABEL: _('Stitch Plan'),
                                     INKSCAPE_GROUPMODE: 'layer'})
    else:
        # delete old stitch plan
        del layer[:]

        # make sure the layer is visible
        layer.set('style', 'display:inline')

    for i, color_block in enumerate(stitch_plan):
        group = inkex.etree.SubElement(layer,
                                       SVG_GROUP_TAG,
                                       {'id': '__color_block_%d__' % i,
                                        INKSCAPE_LABEL: "color block %d" % (i + 1)})
        if realistic:
            group.extend(color_block_to_realistic_stitches(color_block, svg))
        else:
            group.extend(color_block_to_paths(color_block, svg))

    svg.append(layer)

    if realistic:
        defs = svg.find(SVG_DEFS_TAG)

        if defs is None:
            defs = inkex.etree.SubElement(svg, SVG_DEFS_TAG)

        defs.append(inkex.etree.fromstring(realistic_filter))

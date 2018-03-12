import simpletransform, simplestyle, inkex
from . import _, get_viewbox_transform, cache, SVG_GROUP_TAG, INKSCAPE_LABEL, INKSCAPE_GROUPMODE, SVG_POLYLINE_TAG

def color_block_to_point_lists(color_block):
    point_lists = [[]]

    for stitch in color_block:
         if stitch.trim:
              if point_lists[-1]:
                  point_lists.append([])
                  continue

         if not stitch.jump and not stitch.stop:
              point_lists[-1].append(stitch.as_tuple())

    return point_lists


@cache
def get_correction_transform(svg):
    transform = get_viewbox_transform(svg)

    # we need to correct for the viewbox
    transform = simpletransform.invertTransform(transform)
    transform = simpletransform.formatTransform(transform)

    return transform


def color_block_to_polylines(color_block, svg):
    polylines = []
    for point_list in color_block_to_point_lists(color_block):
        color = color_block.color.to_hex_str()
        polylines.append(inkex.etree.Element(
            SVG_POLYLINE_TAG,
            {'style': simplestyle.formatStyle(
                {'stroke': color,
                'stroke-width': "0.4",
                'fill': 'none'}),
            'points': " ".join(",".join(str(coord) for coord in point) for point in point_list),
            'transform': get_correction_transform(svg)
            }))

    return polylines


def render_stitch_plan(svg, stitch_plan):
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
        group.extend(color_block_to_polylines(color_block, svg))

    svg.append(layer)

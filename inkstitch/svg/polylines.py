from .. import get_viewbox_transform, cache
import simpletransform, simplestyle, inkex

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
        color = color_block.color or '#000000'
        polylines.append(inkex.etree.Element(
            inkex.addNS('polyline', 'svg'),
            {'style': simplestyle.formatStyle(
                {'stroke': color,
                'stroke-width': "0.4",
                'fill': 'none'}),
            'points': " ".join(",".join(str(coord) for coord in point) for point in point_list),
            'transform': get_correction_transform(svg)
            }))

    return polylines


def render_stitch_plan(layer, stitch_plan):
    svg = layer.getroottree().getroot()
    for color_block in stitch_plan:
        layer.extend(color_block_to_polylines(color_block, svg))

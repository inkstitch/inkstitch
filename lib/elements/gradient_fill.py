from math import pi

from inkex import DirectedLineSegment, Transform
from shapely import geometry as shgeo
from shapely.affinity import affine_transform, rotate
from shapely.ops import split

from ..svg import get_correction_transform


def gradient_shapes_and_attributes(element, shape):
    # e.g. url(#linearGradient872) -> linearGradient872
    color = element.color[5:-1]
    xpath = f'.//svg:defs/svg:linearGradient[@id="{color}"]'
    gradient = element.node.getroottree().getroot().findone(xpath)
    gradient.apply_transform()
    point1 = (float(gradient.get('x1')), float(gradient.get('y1')))
    point2 = (float(gradient.get('x2')), float(gradient.get('y2')))
    # get 90° angle to calculate the splitting angle
    line = DirectedLineSegment(point1, point2)
    angle = line.angle - (pi / 2)
    # Ink/Stitch somehow turns the stitch angle
    stitch_angle = angle * -1
    # create bbox polygon to calculate the length necessary to make sure that
    # the gradient splitter lines will cut the entire design
    bbox = element.node.bounding_box()
    bbox_polygon = shgeo.Polygon([(bbox.left, bbox.top), (bbox.right, bbox.top),
                                  (bbox.right, bbox.bottom), (bbox.left, bbox.bottom)])
    # gradient stops
    offsets = gradient.stop_offsets
    stop_styles = gradient.stop_styles
    # now split the shape according to the gradient stops
    polygons = []
    colors = []
    attributes = []
    previous_color = None
    end_row_spacing = None
    for i, offset in enumerate(offsets):
        shape_rest = []
        split_point = shgeo.Point(line.point_at_ratio(float(offset)))
        length = split_point.hausdorff_distance(bbox_polygon)
        split_line = shgeo.LineString([(split_point.x - length - 2, split_point.y),
                                       (split_point.x + length + 2, split_point.y)])
        split_line = rotate(split_line, angle, origin=split_point, use_radians=True)
        transform = -Transform(get_correction_transform(element.node))
        transform = list(transform.to_hexad())
        split_line = affine_transform(split_line, transform)
        offset_line = split_line.parallel_offset(1, 'right')
        polygon = split(shape, split_line)
        color = stop_styles[i]['stop-color']
        # does this gradient line split the shape
        offset_outside_shape = len(polygon.geoms) == 1
        for poly in polygon.geoms:
            if isinstance(poly, shgeo.Polygon) and element.shape_is_valid(poly):
                if poly.intersects(offset_line):
                    if previous_color:
                        polygons.append(poly)
                        colors.append(previous_color)
                        attributes.append({'angle': stitch_angle, 'end_row_spacing': end_row_spacing, 'color': previous_color})
                    polygons.append(poly)
                    attributes.append({'angle': stitch_angle + pi, 'end_row_spacing': end_row_spacing, 'color': color})
                else:
                    shape_rest.append(poly)
        shape = shgeo.MultiPolygon(shape_rest)
        previous_color = color
        end_row_spacing = element.row_spacing * 2
    # add left over shape(s)
    if shape:
        if offset_outside_shape:
            for s in shape.geoms:
                polygons.append(s)
                attributes.append({'color': stop_styles[-2]['stop-color'], 'angle': stitch_angle, 'end_row_spacing': end_row_spacing})
            stitch_angle += pi
        else:
            end_row_spacing = None
        for s in shape.geoms:
            polygons.append(s)
            attributes.append({'color': stop_styles[-1]['stop-color'], 'angle': stitch_angle, 'end_row_spacing': end_row_spacing})
    return polygons, attributes

# Authors: see git history
#
# Copyright (c) 2026 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from collections import defaultdict
from inkex import Color, Group, Path, PathElement
from shapely import make_valid, unary_union
from ..stitches.utils.cross_stitch import CrossGeometries
from ..svg import PIXELS_PER_MM, get_correction_transform
from .geometry import ensure_multi_polygon


def pixelate_element(element, settings):
    ''' Takes a fill element and returns a multipolygon with its pixelated shape
    '''
    geometries = CrossGeometries(
        element.shrink_or_grow_shape(element.shape, 0.1),
        (settings['box_x'] * PIXELS_PER_MM, settings['box_y'] * PIXELS_PER_MM),
        settings['coverage'],
        'simple_cross',
        _get_grid_offset(settings),
        settings['align_with_canvas']
    )

    outline = _prepare_outline(geometries.boxes, settings)
    return outline


def pixelate_multiple(destination_group, fills, settings):
    ''' Pixelate multiple fill areas and generate path elements
        Returns the given destination_group with color sorted pixelated fill elements
    '''
    colored_boxes = _get_colored_boxes(fills, settings)
    if not colored_boxes:
        return destination_group

    for color, boxes in colored_boxes.items():
        color_group = Group()
        color_group.label = color
        # setup the path
        outline = _prepare_outline(boxes, settings)
        for polygon in outline.geoms:
            path = Path(list(polygon.exterior.coords))
            for interior in polygon.interiors:
                interior_path = Path(list(interior.coords))
                interior_path.close()
                path += interior_path
            path.close()

            path_element = PathElement()
            path_element.set('d', str(path))
            path_element.transform = get_correction_transform(fills[-1].node)
            path_element.style['fill'] = color_group.label
            color_group.append(path_element)
        if len(color_group) > 1:
            destination_group.append(color_group)
        else:
            destination_group.append(color_group[0])

    return destination_group


def _prepare_outline(boxes, settings):
    outline = unary_union(boxes)
    # add a small buffer to connect otherwise unconnected elements
    outline = outline.buffer(0.001)
    # the buffer has added some unwanted nodes at corners
    # remove them with simplify
    outline = outline.simplify(0.1)
    outline = make_valid(outline)
    # simplify has removed nodes at grid intersections.
    # the user chose to have some additional nodes (to pull the shape out, let's add some nodes back in
    if settings['nodes']:
        outline = outline.segmentize(settings['box_x'] * PIXELS_PER_MM + 0.002)
    return ensure_multi_polygon(outline)


def _get_grid_offset(settings):
    grid_offset = settings['grid_offset'].split(' ')
    try:
        grid_offset = settings['grid_offset'].split(' ')
        if len(grid_offset) == 1:
            offset = float(grid_offset[0]) * PIXELS_PER_MM
            return (offset, offset)
        elif len(grid_offset) == 2:
            return (float(grid_offset[0]) * PIXELS_PER_MM, float(grid_offset[1] * PIXELS_PER_MM))
    except ValueError:
        pass
    return (0, 0)  # Fallback


def _get_colored_boxes(fills, settings):
    ''' Gets all fill while also removing overlaps.
        Combines all fills and genereates a bunch of little boxes to fill the entire area.
        Then assigns most prominent color to each box.
    '''
    fill_areas = []
    fill_areas_by_color = defaultdict(list)
    # Walk in reversed order through the fill shapes, so we can remove visually covered areas easily
    for fill in reversed(fills):
        # subtract areas already filled with a color
        area = unary_union(fill_areas)
        adapted_shape = fill.shape.difference(area)
        if not adapted_shape.is_empty:
            color = Color(fill.fill_color).to('named')
            fill_areas_by_color[color].append(fill.shape.difference(area))
        # add a little expand value to connect otherwise unconnected
        fill_areas.append(fill.shrink_or_grow_shape(fill.shape, 0.1))

    # combine all selected fill shape areas to generate all squares at once
    full_area = ensure_multi_polygon(unary_union(fill_areas))
    # get squares
    grid_offset = _get_grid_offset(settings)
    geometries = CrossGeometries(
        full_area,
        (settings['box_x'] * PIXELS_PER_MM, settings['box_y'] * PIXELS_PER_MM),
        settings['coverage'],
        'simple_cross',
        grid_offset,
        settings['align_with_canvas']
    )

    color_shape_dict = {}
    for color, shapes in fill_areas_by_color.items():
        color_shape_dict[color] = make_valid(unary_union(shapes))

    colored_boxes = defaultdict(list)
    for box in geometries.boxes:
        current_color = None
        highest_overlap = 0
        for color, shape in color_shape_dict.items():
            overlap = box.intersection(shape).area
            if overlap > highest_overlap:
                current_color = color
                highest_overlap = overlap
        if current_color is not None:
            colored_boxes[current_color].append(box)
    return colored_boxes

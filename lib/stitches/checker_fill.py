# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from math import ceil, floor
from typing import TYPE_CHECKING, List, Optional, Tuple, Union

from networkx import is_empty
from shapely import get_point, line_merge, minimum_bounding_radius, segmentize
from shapely.affinity import rotate, scale, translate
from shapely.geometry import Point, Polygon
from .fill import intersect_region_with_grating, stitch_row
from ..stitches import auto_fill
from ..utils.list import is_all_zeroes
from ..utils.threading import check_stop_flag

from ..stitch_plan import Stitch, StitchGroup
from ..svg import PIXELS_PER_MM
if TYPE_CHECKING:
    from ..elements import FillStitch

def make_quadrilateral(quad_coord: tuple[int, int], 
                       grid_offset: tuple[float, float], 
                       grid_row_spacing: float, 
                       grid_column_spacing: float,
                       width: float,
                       height: float) -> Polygon:
    bottom_left = (grid_offset[0] + grid_column_spacing * quad_coord[0], grid_offset[1] + grid_row_spacing * quad_coord[1])
    bottom_right = (bottom_left[0] + width, bottom_left[1])
    top_left = (bottom_left[0], bottom_left[1] + height)
    top_right = (bottom_left[0] + width, bottom_left[1] + height)
    return Polygon((top_left, top_right, bottom_right, bottom_left, top_left))

class Checker:
    coords: tuple[int, int]
    areas: list[Polygon]

def checker_fill(fill: 'FillStitch', outline: Polygon,
                 starting_point: Union[tuple, Stitch, None], ending_point: Union[tuple, Stitch, None]) -> list[StitchGroup]:
    """
    Main method to fill the checker element with checker grid fill stitches

    :param fill: FillStitch element
    :param outline: the outline of the fill
    :param starting_point: the starting point (or None)
    :param ending_point: the ending point (or None)
    :returns: stitch_groups forming the checker pattern
    """

    # Get the shape dimensions in quads so we know maximum how many checkers we need
    (minx, miny, maxx, maxy) = outline.bounds
    shape_width_in_quad: int = ceil(abs(maxx - minx) / fill.checker_grid_column_spacing)
    shape_height_in_quad: int = ceil(abs(maxy - miny) / fill.checker_grid_row_spacing)
    
    quad_width: float = fill.checker_grid_column_spacing
    quad_height: float = fill.checker_grid_row_spacing
    shape_base_coord: tuple[int, int] = (floor(minx / fill.checker_grid_column_spacing), floor(miny / fill.checker_grid_column_spacing))

    checkers : list[Checker] = []

    for quad_x in range(shape_width_in_quad):
        for quad_y in range(shape_height_in_quad):
            check_stop_flag()
            checker = Checker()
            checker.coords = (shape_base_coord[0] + quad_x, shape_base_coord[1] + quad_y)
            quad: Polygon = make_quadrilateral(checker.coords, 
                                               (0.,0.), 
                                               fill.checker_grid_row_spacing, 
                                               fill.checker_grid_column_spacing, 
                                               quad_width, quad_height)
            
            res = quad.intersection(outline)

            # We're gonna ignore any geometry that doesn't have an area to fill
            if res.geom_type in ["Point", "MultiPoint", "MultiLineString", "LinearRing", "LineString"] or res.is_empty:
                continue
            # We parse geometry collections to extract only the individual polygons
            elif res.geom_type == "GeometryCollection":
                checker.areas = [geo for geo in res.geoms if geo.geom_type == "Polygon"]
                checker.areas.extend([list(geo) for geo in res.geoms if geo.geom_type == "MultiPolygon"])
            elif res.geom_type == "MultiPolygon":
                checker.areas = list(res.geoms)
            elif res.geom_type == "Polygon":
                checker.areas = [res]
            
            checkers.append(checker)

    stitch_groups : list[StitchGroup] = []

    for checker in checkers:
        check_stop_flag()
        # Type A checkers have the same parity of their grid coordinates, like (1,1) or (4,2)
        is_type_a: bool = (checker.coords[0] % 2 == 0) == (checker.coords[1] % 2 == 0)
        angle: float = fill.checker_A_angle if is_type_a else fill.checker_B_angle
        row_spacing: float = fill.checker_A_row_spacing if is_type_a else fill.checker_B_row_spacing

        stitches : list[Point] = []
        for area in checker.areas:
            stitches.extend(auto_fill(area, angle, row_spacing,
                    fill.end_row_spacing, fill.max_stitch_length, fill.running_stitch_length, fill.running_stitch_tolerance,
                    fill.staggers, fill.skip_last, 
                    None, None, False,
                    fill.gap_fill_rows, fill.enable_random_stitch_length, fill.random_stitch_length_jitter, fill.random_seed,
                    fill.pull_compensation_px, fill.pull_compensation_percent / 100,
                    ))

        stitch_groups.append(StitchGroup(
            color=fill.color,
            tags=("auto_fill", "auto_fill_top"),
            force_lock_stitches=fill.force_lock_stitches,
            lock_stitches=fill.lock_stitches,
            stitches=stitches
        ))

    return stitch_groups

# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from math import ceil, floor
from typing import TYPE_CHECKING, Tuple, List, Union

from shapely.geometry import Point, Polygon
from .fill import intersect_region_with_grating, stitch_row
from ..stitches import auto_fill
from ..utils.threading import check_stop_flag

from ..stitch_plan import Stitch, StitchGroup
from ..svg import PIXELS_PER_MM
if TYPE_CHECKING:
    from ..elements import FillStitch

def make_quadrilateral(quad_coord: Tuple[int, int], 
                       grid_offset: Tuple[float, float], 
                       grid_column_spacing: float,
                       grid_row_spacing: float, 
                       width: float,
                       height: float) -> Polygon:
    bottom_left = (grid_offset[0] + grid_column_spacing * quad_coord[0], grid_offset[1] + grid_row_spacing * quad_coord[1])
    bottom_right = (bottom_left[0] + width, bottom_left[1])
    top_left = (bottom_left[0], bottom_left[1] + height)
    top_right = (bottom_left[0] + width, bottom_left[1] + height)
    return Polygon((top_left, top_right, bottom_right, bottom_left, top_left))

class Checker:
    coords: Tuple[int, int]
    areas: List[Polygon]

def intersect_checker(fill: 'FillStitch', outline: Polygon, checker_coords: Tuple[int, int]) -> Checker:
        quad: Polygon = make_quadrilateral(checker_coords, 
                                            (0.,0.), 
                                            fill.checker_grid_column_spacing,
                                            fill.checker_grid_row_spacing, 
                                            fill.checker_grid_column_spacing, 
                                            fill.checker_grid_row_spacing)
        
        res = quad.intersection(outline)
        if res.is_empty:
            return None

        checker = Checker()
        checker.coords = checker_coords
        # Each polygon is a checker area.
        if res.geom_type == "GeometryCollection":
            # We parse geometry collections to extract only the individual polygons.
            checker.areas = [geo for geo in res.geoms if geo.geom_type == "Polygon"]
            checker.areas.extend([list(geo) for geo in res.geoms if geo.geom_type == "MultiPolygon"])
        elif res.geom_type == "MultiPolygon":
            checker.areas = list(res.geoms)
        elif res.geom_type == "Polygon":
            checker.areas = [res]
        else:
            # Any other type of geometry (Point, LineString, LinearRing) don't have areas to fill
            return None
        
        return checker

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
    
    shape_base_coord: Tuple[int, int] = (floor(minx / fill.checker_grid_column_spacing), floor(miny / fill.checker_grid_row_spacing))
    shape_max_coord: Tuple[int, int] = (ceil(maxx / fill.checker_grid_column_spacing), ceil(maxy / fill.checker_grid_row_spacing))

    shape_width_in_quad: int = shape_max_coord[0] - shape_base_coord[0]
    shape_height_in_quad: int = shape_max_coord[1] - shape_base_coord[1]

    checkers : List[Checker] = []

    for quad_x in range(shape_width_in_quad):
        for quad_y in range(shape_height_in_quad):
            check_stop_flag()
            checker: Checker = intersect_checker(fill, outline,
                                                (shape_base_coord[0] + quad_x, shape_base_coord[1] + quad_y))
            if checker is None:
                continue

            checkers.append(checker)

    stitch_groups : List[StitchGroup] = []

    for checker in checkers:
        check_stop_flag()
        # Type A checkers have the same parity of their grid coordinates, like (1,1) or (4,2)
        is_type_a: bool = (checker.coords[0] % 2 == 0) == (checker.coords[1] % 2 == 0)
        angle: float = fill.checker_A_angle if is_type_a else fill.checker_B_angle
        row_spacing: float = fill.checker_A_row_spacing if is_type_a else fill.checker_B_row_spacing

        stitches : List[Point] = []
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

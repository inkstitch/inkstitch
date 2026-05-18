# Authors: see git history
#
# Copyright (c) 2026 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
import zlib
import base64
import json
import logging
from typing import Dict, Tuple, Optional
from lxml import etree
import inkex

from .grid_state import GridStateManager, Cell, DEFAULT_THREAD_COLOR
from .grid_mapper import grid_to_svg
from .region_merger import merge_runs, Rect

logger = logging.getLogger(__name__)

EXPORT_GROUP_ID = "inkstitch-cross-stitch-canvas"
MAX_EXPORT_RECTS = 5000

# 15% inset keeps the stitch arms clear of cell borders,
# matching typical cross-stitch thread thickness at standard scales.
_CROSS_MARGIN_RATIO = 0.15

# Stroke width as a fraction of cell size; approximates real thread thickness visually.
# Must match _STROKE_WIDTH_RATIO in grid_visualizer.py.
_STROKE_WIDTH_RATIO = 0.13


def _serialize_state(grid_state: GridStateManager) -> str:
    """Serialize the current grid state to a compressed base64 string."""
    sparse_list = []
    for (row, col), cell in grid_state.cells.items():
        sparse_list.append([
            row, col,
            cell.thread_id,
            cell.stitch_type,
            cell.direction,
            cell.locked
        ])

    data = {
        "version": 1,
        "rows": grid_state.rows,
        "cols": grid_state.cols,
        "cells": sparse_list
    }
    json_bytes = json.dumps(data, separators=(',', ':')).encode('utf-8')
    compressed = zlib.compress(json_bytes)
    return base64.b64encode(compressed).decode('utf-8')


def _build_cross_path(r: Rect, cell_size: float) -> str:
    """Generate SVG path data for an X cross-stitch across a merged run.

    Each cell gets two diagonal lines forming an X. The margin keeps
    stitches visually separate from adjacent cells.
    """
    margins = cell_size * _CROSS_MARGIN_RATIO
    segments = []
    for col in range(r.col, r.col + r.width):
        x, y = grid_to_svg(r.row, col, cell_size)
        x1, y1 = x + margins, y + margins
        x2, y2 = x + cell_size - margins, y + cell_size - margins
        segments.append(f"M{x1},{y1} L{x2},{y2}")
        segments.append(f"M{x1},{y2} L{x2},{y1}")
    return " ".join(segments)


def build_export_group(
    grid_state: GridStateManager,
    cell_size: float,
    correction_transform: Optional[inkex.Transform] = None
) -> etree.Element:
    """Build the root SVG group containing the cross-stitch elements.

    Generates cross-stitch diagonal paths for each cell, organized by thread color.
    Serializes the grid state metadata and attaches it to the group.

    Args:
        grid_state: Current grid manager holding sparse cell coordinates and states.
        cell_size: Visual width/height of a single cell in SVG user units.
        correction_transform: Transform matrix to correct document scaling.

    Returns:
        The generated lxml etree.Element representing the root export group.
    """
    root_group = inkex.Group()
    root_group.set("id", EXPORT_GROUP_ID)

    if correction_transform:
        root_group.transform = correction_transform

    if not grid_state.cells:
        # Save serialized empty state over the root
        root_group.set("inkstitch:grid-state", _serialize_state(grid_state))
        return root_group

    threads: Dict[str, Dict[Tuple[int, int], Cell]] = {}
    for pos, cell in grid_state.cells.items():
        tid = cell.thread_id or DEFAULT_THREAD_COLOR
        if tid not in threads:
            threads[tid] = {}
        threads[tid][pos] = cell

    total_runs = 0

    for tid in sorted(threads.keys()):
        thread_group = inkex.Group()
        if tid:
            thread_group.set("inkstitch:thread", tid)

        rects = merge_runs(threads[tid], horizontal_only=True)
        total_runs += len(rects)

        for r in rects:
            cross_path = _build_cross_path(r, cell_size)
            stroke_w = max(1.0, cell_size * _STROKE_WIDTH_RATIO)
            cross_elem = inkex.PathElement(attrib={
                "d": cross_path,
                "style": f"fill:none;stroke:{tid};stroke-width:{stroke_w:.2f};stroke-linecap:round;stroke-opacity:0.9"
            })
            thread_group.append(cross_elem)

        root_group.append(thread_group)

    if total_runs > MAX_EXPORT_RECTS:
        logger.warning(
            "DOM SCALING WARNING: Extracted %d SVG runs. Render performance will degrade.",
            total_runs
        )

    ser_state = _serialize_state(grid_state)
    root_group.set("inkstitch:grid-state", ser_state)

    if len(ser_state) > 50000:
        logger.warning(
            "SERIALIZATION BUDGET WARNING: Artifact payload reached %d bytes",
            len(ser_state)
        )

    return root_group


def export_to_svg(
    svg_doc: etree._ElementTree,
    layer: inkex.Layer,
    grid_state: GridStateManager,
    cell_size: float,
    correction_transform: Optional[inkex.Transform] = None
) -> None:
    """Write the cross-stitch grid into the Inkscape SVG document layer.

    Replaces any existing export group (identified by EXPORT_GROUP_ID) with
    a freshly built one. If the canvas is empty, removes the old group and
    returns without adding anything.

    Args:
        svg_doc: The lxml root SVG document tree, used for xpath lookup of old groups.
        layer: The inkex Layer where the group should be appended.
        grid_state: Current canvas state to serialize and render.
        cell_size: Size of each grid cell in SVG user units.
        correction_transform: Optional transform applied to the root group,
            used to align the export with the Inkscape document's coordinate system.
    """
    new_group = build_export_group(grid_state, cell_size, correction_transform)

    # Locate existing EXPORT_GROUP_ID using standard lxml xpath
    old_groups = svg_doc.xpath(f"//*[@id='{EXPORT_GROUP_ID}']")
    old_group = old_groups[0] if old_groups else None

    if not grid_state.cells:
        logger.info("Canvas is empty; exporting empty placeholder group to preserve grid metadata.")

    # Normal replacement path
    if old_group is not None:
        old_group.getparent().remove(old_group)

    layer.append(new_group)
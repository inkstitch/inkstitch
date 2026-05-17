"""
Integration layer for exporting GridState into the working SVG DOM.
"""

import zlib
import base64
import json
import logging
from lxml import etree
import inkex

from .grid_state import GridStateManager, Cell
from .grid_mapper import grid_to_svg
from .region_merger import merge_runs

logger = logging.getLogger(__name__)

EXPORT_GROUP_ID = "inkstitch-cross-stitch-canvas"
MAX_EXPORT_RECTS = 5000


def _serialize_state(grid_state: GridStateManager) -> str:
    """
    Produce highly compact representation of the sparse state:
    [ [row, col, thread_id, stitch_type, direction, locked], ... ]
    """
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


def build_export_group(grid_state: GridStateManager, cell_size: float, correction_transform=None) -> etree.Element:
    """
    Builds the SVG structure for the grid.
    Returns: <g id="inkstitch-cross-stitch-canvas">
    """
    # Create the root group for our output
    root_group = inkex.Group()
    root_group.set("id", EXPORT_GROUP_ID)
    
    if correction_transform:
        # Apply layer correction transformations if they exist
        root_group.transform = correction_transform

    if not grid_state.cells:
        # Save serialized empty state over the root
        root_group.set("inkstitch:grid-state", _serialize_state(grid_state))
        return root_group
        
    # Group cells by thread_id
    threads = {}
    for pos, cell in grid_state.cells.items():
        tid = cell.thread_id or "#444444"  # Default color for unset values
        if tid not in threads:
            threads[tid] = {}
        threads[tid][pos] = cell
    
    total_runs = 0
    # Process each grouped thread in predictable sorted order
    for tid in sorted(threads.keys()):
        thread_group = inkex.Group()
        if tid:
            thread_group.set("inkstitch:thread", str(tid))
            
        rects = merge_runs(threads[tid], horizontal_only=True)
        total_runs += len(rects)

        for r in rects:
            x_start, y = grid_to_svg(r.row, r.col, cell_size)
            width = r.width * cell_size
            height = cell_size
            
            # Build a single cross path per run, combining adjacent cells in the same row.
            margins = cell_size * 0.15
            segments = []
            for col in range(r.col, r.col + r.width):
                x, y_cell = grid_to_svg(r.row, col, cell_size)
                x1 = x + margins
                y1 = y_cell + margins
                x2 = x + cell_size - margins
                y2 = y_cell + cell_size - margins
                segments.append(f"M{x1},{y1} L{x2},{y2}")
                segments.append(f"M{x1},{y2} L{x2},{y1}")

            cross_path = " ".join(segments)
            cross_elem = inkex.PathElement(attrib={
                "d": cross_path,
                "style": f"fill:none;stroke:{tid};stroke-width:1.5;stroke-linecap:round;stroke-opacity:0.9"
            })
            thread_group.append(cross_elem)
            
        root_group.append(thread_group)
        
    if total_runs > MAX_EXPORT_RECTS:
        logger.warning(
            "DOM SCALING WARNING: Extracted %d SVG runs. Render performance will degrade.", 
            total_runs
        )
        
    # Embed compressed grid state into the group metadata
    ser_state = _serialize_state(grid_state)
    root_group.set("inkstitch:grid-state", ser_state)
    
    if len(ser_state) > 50000:
        logger.warning(
            "SERIALIZATION BUDGET WARNING: Artifact payload reached %d bytes", 
            len(ser_state)
        )
        
    return root_group


def export_to_svg(svg_doc, layer, grid_state: GridStateManager, cell_size: float, correction_transform=None):
    """
    Perform atomic replacement of our tagged group onto the active SVG layer.
    """
    new_group = build_export_group(grid_state, cell_size, correction_transform)
    
    # Locate existing EXPORT_GROUP_ID using standard lxml xpath
    old_groups = svg_doc.xpath(f"//*[@id='{EXPORT_GROUP_ID}']")
    old_group = old_groups[0] if old_groups else None
    
    # On an empty canvas export
    if not grid_state.cells:
        if old_group is not None:
            # Option A UX rule: Clear the output when canvas is naturally emptied
            old_group.getparent().remove(old_group)
        return
        
    # Normal replacement path
    if old_group is not None:
        old_group.getparent().remove(old_group)
        
    layer.append(new_group)
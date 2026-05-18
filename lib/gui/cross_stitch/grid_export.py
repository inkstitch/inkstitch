# Authors: see git history
#
# Copyright (c) 2026 Authors
# Licensed under the GNU GPL version 3.0 or later.
# See the file LICENSE for details.
import logging
import re
from typing import Optional
from lxml import etree
import inkex

from .grid_state import GridStateManager, Cell, DEFAULT_THREAD_COLOR

logger = logging.getLogger(__name__)

EXPORT_GROUP_ID = "inkstitch-cross-stitch-canvas"


def build_export_group(
    grid_state: GridStateManager,
    cell_size: float,
    correction_transform: Optional[inkex.Transform] = None
) -> etree.Element:
    """Build the root SVG group containing the cross-stitch elements.

    Generates native cross-stitch fill paths for each cell,
    organized by thread color.

    Args:
        grid_state: Current grid manager holding sparse cell coordinates.
        cell_size: Visual width/height of a single cell in SVG user units.
        correction_transform: Transform matrix to correct document scaling.

    Returns:
        The generated lxml etree.Element representing the root export group.
    """
    root_group = inkex.Group()
    root_group.set("id", EXPORT_GROUP_ID)

    # Save the original grid rows and columns as attributes on the group
    root_group.set(inkex.addNS("rows", "inkstitch"), str(grid_state.rows))
    root_group.set(inkex.addNS("cols", "inkstitch"), str(grid_state.cols))

    if correction_transform:
        root_group.transform = correction_transform

    if not grid_state.cells:
        return root_group

    from ...svg import PIXELS_PER_MM
    cell_size_mm = cell_size / PIXELS_PER_MM
    pat_sz = f"{cell_size_mm:.6f} {cell_size_mm:.6f}"

    ns_fill_method = inkex.addNS("fill_method", "inkstitch")
    ns_pattern_sz = inkex.addNS("pattern_size_mm", "inkstitch")
    ns_grid_origin = inkex.addNS("canvas_grid_origin", "inkstitch")
    ns_method = inkex.addNS("cross_stitch_method", "inkstitch")
    ns_thread_count = inkex.addNS("cross_thread_count", "inkstitch")

    for pos, cell in sorted(grid_state.cells.items()):
        row, col = pos
        tid = cell.thread_id or DEFAULT_THREAD_COLOR

        x = col * cell_size
        y = row * cell_size
        d_path = (
            f"M {x:.2f},{y:.2f} h {cell_size:.2f} v {cell_size:.2f} "
            f"h {-cell_size:.2f} Z"
        )

        path_elem = inkex.PathElement(attrib={
            "d": d_path,
            "fill": tid,
            "stroke": "none",
            ns_fill_method: "cross_stitch",
            ns_pattern_sz: pat_sz,
            ns_grid_origin: "true",
            ns_method: "simple_cross",
            ns_thread_count: "4"
        })
        root_group.append(path_elem)

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
    a freshly built one.

    Args:
        svg_doc: Root SVG document tree, used for xpath lookup of old groups.
        layer: The inkex Layer where the group should be appended.
        grid_state: Current canvas state to serialize and render.
        cell_size: Size of each grid cell in SVG user units.
        correction_transform: Optional transform applied to the root group.
    """
    new_group = build_export_group(
        grid_state, cell_size, correction_transform
    )

    # Automatically ensure the document has the correct Ink/Stitch SVG version
    try:
        from ...metadata import InkStitchMetadata
        from ...update import INKSTITCH_SVG_VERSION
        metadata = InkStitchMetadata(svg_doc.getroot())
        metadata['inkstitch_svg_version'] = INKSTITCH_SVG_VERSION
    except Exception:
        pass

    # Locate existing EXPORT_GROUP_ID using standard lxml xpath
    old_groups = svg_doc.xpath(f"//*[@id='{EXPORT_GROUP_ID}']")
    old_group = old_groups[0] if old_groups else None

    if old_group is not None:
        old_group.getparent().remove(old_group)

    layer.append(new_group)


def import_from_svg(
    svg_doc: etree._ElementTree,
    cell_size: float
) -> Optional[GridStateManager]:
    """Parse native cross-stitch fill paths to restore GridStateManager.

    Args:
        svg_doc: The lxml root SVG document tree.
        cell_size: Visual cell size in SVG user units.

    Returns:
        Restored GridStateManager, or None if no group exists.
    """
    old_groups = svg_doc.xpath(f"//*[@id='{EXPORT_GROUP_ID}']")
    if not old_groups:
        return None
    root_group = old_groups[0]

    rows = int(root_group.get(inkex.addNS("rows", "inkstitch"), "80"))
    cols = int(root_group.get(inkex.addNS("cols", "inkstitch"), "80"))

    grid_state = GridStateManager(rows=rows, cols=cols)

    paths = root_group.xpath(".//*[local-name()='path']")
    pattern = re.compile(r"M\s*([\d.-]+)\s*,\s*([\d.-]+)", re.IGNORECASE)

    for path in paths:
        fill_method = path.get(inkex.addNS("fill_method", "inkstitch"))
        if fill_method != "cross_stitch":
            continue

        color = path.get("fill") or DEFAULT_THREAD_COLOR
        d = path.get("d", "")

        # Parse M commands to reconstruct row and col indices
        for match in pattern.finditer(d):
            x = float(match.group(1))
            y = float(match.group(2))
            col = round(x / cell_size)
            row = round(y / cell_size)
            if grid_state.in_bounds(row, col):
                cell_obj = Cell(thread_id=color, stitch_type="full")
                grid_state.set_cell(row, col, cell_obj)

    return grid_state
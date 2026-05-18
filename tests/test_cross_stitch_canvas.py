# Authors: see git history
#
# Copyright (c) 2026 Authors
# Licensed under the GNU GPL version 3.0 or later.
# See the file LICENSE for details.
from lib.gui.cross_stitch.grid_state import GridStateManager, Cell
from lib.gui.cross_stitch.grid_export import export_to_svg, import_from_svg


def test_cross_stitch_canvas_export_import():
    # 1. Create and populate a GridStateManager
    state = GridStateManager(rows=10, cols=10)
    state.set_cell(2, 3, Cell(thread_id="#ff0000"))
    state.set_cell(5, 5, Cell(thread_id="#00ff00"))
    state.set_cell(2, 4, Cell(thread_id="#ff0000"))

    # 2. Set up a dummy Inkscape SVG document structure
    from inkex import SvgDocumentElement, Layer
    svg_doc = SvgDocumentElement()
    layer = svg_doc.add(Layer(id="layer1"))

    # 3. Export to SVG
    cell_size = 12.0
    export_to_svg(svg_doc, layer, state, cell_size)

    # 4. Import from SVG and verify the state is perfectly reconstructed
    restored_state = import_from_svg(svg_doc, cell_size)

    assert restored_state is not None
    assert restored_state.rows == 10
    assert restored_state.cols == 10
    assert len(restored_state.cells) == 3

    # Check cell at (2, 3)
    c1 = restored_state.get_cell(2, 3)
    assert c1 is not None
    assert c1.thread_id == "#ff0000"

    # Check cell at (2, 4)
    c2 = restored_state.get_cell(2, 4)
    assert c2 is not None
    assert c2.thread_id == "#ff0000"

    # Check cell at (5, 5)
    c3 = restored_state.get_cell(5, 5)
    assert c3 is not None
    assert c3.thread_id == "#00ff00"


def test_cross_stitch_snapped_translation():
    import inkex
    from inkex import SvgDocumentElement, Layer
    from lib.gui.cross_stitch.grid_export import EXPORT_GROUP_ID
    from lib.svg.path import get_node_transform
    from lib.svg import get_correction_transform

    # 1. Create document and export a basic grid
    state = GridStateManager(rows=10, cols=10)
    state.set_cell(2, 3, Cell(thread_id="#ff0000"))

    svg_doc = SvgDocumentElement()
    layer = svg_doc.add(Layer(id="layer1"))
    cell_size = 12.0

    export_to_svg(svg_doc, layer, state, cell_size)

    # 2. Simulate manual user move in Inkscape (e.g. translate(15.2, 23.9))
    old_groups = svg_doc.xpath(f"//*[@id='{EXPORT_GROUP_ID}']")
    assert len(old_groups) == 1
    old_groups[0].set("transform", "translate(15.2, 23.9)")

    # 3. Perform snap calculations
    tx, ty = 0.0, 0.0
    global_trans = get_node_transform(old_groups[0])
    tx = global_trans.e
    ty = global_trans.f

    # Snap to nearest multiples of cell_size (12.0)
    tx_snapped = round(tx / cell_size) * cell_size
    ty_snapped = round(ty / cell_size) * cell_size

    assert tx_snapped == 12.0
    assert ty_snapped == 24.0

    corr_str = get_correction_transform(layer, child=True)
    corr_transform = (
        inkex.Transform(corr_str) if corr_str else inkex.Transform()
    )

    snap_t = inkex.Transform().add_translate(tx_snapped, ty_snapped)
    final_transform = corr_transform @ snap_t

    # 4. Re-export and verify new group has the snapped transform
    export_to_svg(svg_doc, layer, state, cell_size, final_transform)

    new_groups = svg_doc.xpath(f"//*[@id='{EXPORT_GROUP_ID}']")
    assert len(new_groups) == 1
    transform_attr = new_groups[0].get("transform")
    assert transform_attr is not None

    t = inkex.Transform(transform_attr)
    assert t.e == 12.0
    assert t.f == 24.0

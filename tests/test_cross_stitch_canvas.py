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
    from inkex import SvgDocumentElement, Group
    svg_doc = SvgDocumentElement()
    layer = svg_doc.add(Group(id="layer1"))

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
    from inkex import SvgDocumentElement, Group
    from lib.gui.cross_stitch.grid_export import EXPORT_GROUP_ID
    from lib.svg.path import get_node_transform
    from lib.svg import get_correction_transform

    # 1. Create document and export a basic grid
    state = GridStateManager(rows=10, cols=10)
    state.set_cell(2, 3, Cell(thread_id="#ff0000"))

    svg_doc = SvgDocumentElement()
    layer = svg_doc.add(Group(id="layer1"))
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


def test_cross_stitch_fill_and_fill_eraser():
    from lib.gui.cross_stitch.grid_interaction import GridInteractionEngine
    from lib.gui.cross_stitch.undo_manager import UndoManager

    class MockVisualizer:
        def __init__(self):
            self.dpi_scale = 1.0
            self.offset_x = 0.0
            self.offset_y = 0.0
            self.scale = 1.0
            self.cell_size = 12.0

        def request_render(self, state):
            pass

        def mark_dirty(self, r, c):
            pass

    # Initialize state
    state = GridStateManager(rows=10, cols=10)
    undo_mgr = UndoManager(state)
    visualizer = MockVisualizer()
    engine = GridInteractionEngine(visualizer, state, undo_mgr)

    # 1. Fill empty background
    engine.current_tool = "fill"
    engine.active_thread = "#ff0000"
    
    # Perform fill at (0, 0)
    engine.on_mouse_down(6.0, 6.0)
    engine.on_mouse_up(6.0, 6.0)

    assert len(state.cells) == 100
    for r in range(10):
        for c in range(10):
            cell = state.get_cell(r, c)
            assert cell is not None
            assert cell.thread_id == "#ff0000"

    # 2. Test Undo
    restored = undo_mgr.undo(state)
    assert len(restored.cells) == 0

    # Restore the state for the next tests
    state = GridStateManager(rows=10, cols=10)
    undo_mgr = UndoManager(state)
    engine = GridInteractionEngine(visualizer, state, undo_mgr)

    # 3. Create a box boundary at row=2 and col=2
    state.set_cell(0, 2, Cell(thread_id="#0000ff"))
    state.set_cell(1, 2, Cell(thread_id="#0000ff"))
    state.set_cell(2, 2, Cell(thread_id="#0000ff"))
    state.set_cell(2, 1, Cell(thread_id="#0000ff"))
    state.set_cell(2, 0, Cell(thread_id="#0000ff"))

    # Flood fill at (0, 0) with #ff0000. It should only fill the 2x2 area
    engine.current_tool = "fill"
    engine.active_thread = "#ff0000"
    engine.on_mouse_down(6.0, 6.0)
    engine.on_mouse_up(6.0, 6.0)

    # Verify filled cells
    for r in range(2):
        for c in range(2):
            cell = state.get_cell(r, c)
            assert cell is not None
            assert cell.thread_id == "#ff0000"

    # Verify boundary cells are unchanged
    assert state.get_cell(0, 2).thread_id == "#0000ff"
    assert state.get_cell(2, 2).thread_id == "#0000ff"

    # Verify cells outside boundary are unchanged (still empty)
    assert state.get_cell(3, 3) is None

    # 4. Test Flood Fill Eraser
    engine.current_tool = "fill_eraser"
    engine.on_mouse_down(6.0, 6.0)
    engine.on_mouse_up(6.0, 6.0)

    # Verify the 2x2 area is now None (erased)
    for r in range(2):
        for c in range(2):
            assert state.get_cell(r, c) is None

    # Verify boundary is still intact
    assert state.get_cell(0, 2).thread_id == "#0000ff"

    # 5. Drag behavior prevention
    engine.current_tool = "fill"
    engine.active_thread = "#ff0000"
    # Mouse down at (0, 2) - should fill the boundary
    engine.on_mouse_down(2 * 12.0 + 6.0, 6.0)
    # Drag to (0, 3) - should not perform flood fill there
    engine.on_mouse_move(3 * 12.0 + 6.0, 6.0)
    engine.on_mouse_up(3 * 12.0 + 6.0, 6.0)

    # The original boundary at col=2 and row=2 should be filled with #ff0000
    assert state.get_cell(0, 2).thread_id == "#ff0000"
    assert state.get_cell(1, 2).thread_id == "#ff0000"
    assert state.get_cell(2, 2).thread_id == "#ff0000"
    assert state.get_cell(2, 1).thread_id == "#ff0000"
    assert state.get_cell(2, 0).thread_id == "#ff0000"

    # But (0, 3) must remain None (unfilled)
    assert state.get_cell(0, 3) is None

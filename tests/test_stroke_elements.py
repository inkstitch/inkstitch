import pytest
from inkex.tester.svg import svg
from inkex import PathElement

from lib.elements import node_to_elements


def test_single_point_stroke_path():
    """Test that a stroke path with only one point doesn't crash Ink/Stitch."""
    root = svg()
    # Create a path with only one point (invalid for LineString)
    path = PathElement(attrib={
        "d": "M 100 100",  # Single moveto, no lineto
        "style": "stroke:black;stroke-width:1;fill:none;"
    })
    root.add(path)

    # This should not raise an exception
    elements = node_to_elements(path, None)
    assert len(elements) >= 0  # At least no crash, possibly no elements if skipped


def test_valid_stroke_path():
    """Test that a valid multi-point stroke path works normally."""
    root = svg()
    path = PathElement(attrib={
        "d": "M 100 100 L 200 200",  # Two points
        "style": "stroke:black;stroke-width:1;fill:none;"
    })
    root.add(path)

    elements = node_to_elements(path, None)
    assert len(elements) > 0  # Should generate elements
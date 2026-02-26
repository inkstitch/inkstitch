from inkex import LinearGradient, Rectangle, Stop, SvgDocumentElement
from inkex.tester.svg import svg

from lib.elements import EmbroideryElement
from lib.elements import node_to_elements
from lib.threads.color import ThreadColor


def test_init_color_from_string_rgb():
    color = ThreadColor("rgb(170, 187, 204)")
    assert color.rgb == (170, 187, 204)


def test_init_color_from_string_hex():
    color = ThreadColor("#AABBCC")
    assert color.rgb == (170, 187, 204)


def test_init_color_from_string_hex_icc():
    color = ThreadColor("#AABBCC icc-color(Some-Profile, 0.1, 0.2, 0.3, 0.4)")
    assert color.rgb == (170, 187, 204)


def test_invalid_color():
    # defaults to black
    color = ThreadColor("bad_color")
    assert color.rgb == (0, 0, 0)


def test_fill_color():
    root: SvgDocumentElement = svg()
    rect = Rectangle(attrib={
        "width": "10",
        "height": "10",
        "style": "fill:red;"
    })
    root.add(rect)

    # test with red color
    element = EmbroideryElement(rect)
    assert element.fill_color == [255, 0, 0]

    # test with invalid color (defaults to black)
    rect.style = "fill:bad_color;"
    element = EmbroideryElement(rect)
    assert element.fill_color == "black"


def test_stroke_color():
    root: SvgDocumentElement = svg()
    rect = Rectangle(attrib={
        "width": "10",
        "height": "10",
        "style": "fill:none;stroke:red;"
    })
    root.add(rect)

    # test with red color
    element = EmbroideryElement(rect)
    assert element.stroke_color == [255, 0, 0]

    # test with invalid color
    rect.style = "fill:none;stroke:bad_color;"
    element = EmbroideryElement(rect)
    assert element.stroke_color is None


def test_gradient_colors():
    root: SvgDocumentElement = svg()

    defs = root.defs
    linear_gradient = LinearGradient(
        attrib={
            "id": "good_gradient"
        }
    )
    stop1 = Stop(
        attrib={
            "style": "stop-color: #ff0000;"
        }
    )
    stop2 = Stop(
        attrib={
            "style": "stop-color: bad_color;"
        }
    )
    linear_gradient.add(stop1)
    linear_gradient.add(stop2)
    defs.add(linear_gradient)

    rect = Rectangle(attrib={
        "width": "10",
        "height": "10",
        "style": "fill:url(#good_gradient)"
    })
    rect.set("inkstitch:fill_method", "linear_gradient_fill")
    root.add(rect)

    [element] = node_to_elements(root[1])
    stitch_groups = element.embroider(None)

    assert stitch_groups[0].color == [255, 0, 0]
    assert stitch_groups[1].color == [0, 0, 0]


def test_tartan_colors():
    root: SvgDocumentElement = svg()
    rect = Rectangle(attrib={
        "width": "20",
        "height": "20",
    })
    root.add(rect)

    rect.set('inkstitch:fill_method', 'tartan_fill')
    rect.set('inkstitch:fill_underlay', False)
    rect.set(
        'inkstitch:tartan',
        '{"symmetry": true, "equal_warp_weft": true, "rotate": 0.0, "scale": 100, "offset_x": 0.0, "offset_y": 0.0,'
        '"palette": "(#ffff00)/5.0 (#00ffff)/5.0", "output": "embroidery", "stitch_type": "legacy_fill",'
        '"row_spacing": 1.0, "angle_warp": 0.0, "angle_weft": 90.0, "min_stripe_width": 1.0, "bean_stitch_repeats": 0}'
    )

    [element] = node_to_elements(root[0])
    stitch_groups = element.embroider(None)

    assert stitch_groups[0].color == [255, 255, 0]
    assert stitch_groups[1].color == [0, 255, 255]

    # Set second color to an invalid value. Tartan will disable the color stripe for rendering.
    rect.set(
        'inkstitch:tartan',
        '{"symmetry": true, "equal_warp_weft": true, "rotate": 0.0, "scale": 100, "offset_x": 0.0, "offset_y": 0.0,'
        '"palette": "(#ffff00)/5.0 (bad_color)/5.0", "output": "embroidery", "stitch_type": "legacy_fill",'
        '"row_spacing": 1.0, "angle_warp": 0.0, "angle_weft": 90.0, "min_stripe_width": 1.0, "bean_stitch_repeats": 0}'
    )

    [element] = node_to_elements(root[0])
    stitch_groups = element.embroider(None)

    assert stitch_groups[0].color == [255, 255, 0]
    assert len(stitch_groups) == 1

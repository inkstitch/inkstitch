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

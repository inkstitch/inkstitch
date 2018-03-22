import simplestyle
import re
import colorsys

class ThreadColor(object):
    hex_str_re = re.compile('#([0-9a-z]{3}|[0-9a-z]{6})', re.I)

    def __init__(self, color, name=None, description=None):
        if color is None:
            self.rgb = (0, 0, 0)
        elif self.hex_str_re.match(color):
            self.rgb = simplestyle.parseColor(color)
        else:
            self.rgb = tuple(color)

        self.name = name
        self.description = description

    def __eq__(self, other):
        if isinstance(other, ThreadColor):
            return self.rgb == other.rgb
        else:
            return self == ThreadColor(other)

    def __hash__(self):
        return hash(self.rgb)

    def __ne__(self, other):
        return not(self == other)

    def __repr__(self):
        return "ThreadColor" + repr(self.rgb)

    def to_hex_str(self):
        return "#%02X%02X%02X" % self.rgb

    @property
    def rgb_normalized(self):
        return tuple(channel / 255.0 for channel in self.rgb)

    @property
    def font_color(self):
        """Pick a color that will allow text to show up on a swatch in the printout."""
        hls = colorsys.rgb_to_hls(*self.rgb_normalized)

        # We'll use white text unless the swatch color is too light.
        if hls[1] > 0.7:
            return (1, 1, 1)
        else:
            return (254, 254, 254)

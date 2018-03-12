import simplestyle
import re

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

    def __ne__(self, other):
        return not(self == other)

    def __repr__(self):
        return "ThreadColor" + repr(self.rgb)

    def to_hex_str(self):
        return "#%02X%02X%02X" % self.rgb

    @property
    def rgb_normalized(self):
        return tuple(channel / 255.0 for channel in self.rgb)

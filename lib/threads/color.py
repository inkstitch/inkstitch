import colorsys
from pyembroidery.EmbThread import EmbThread
import re

import simplestyle


class ThreadColor(object):
    hex_str_re = re.compile('#([0-9a-z]{3}|[0-9a-z]{6})', re.I)

    def __init__(self, color, name=None, number=None, manufacturer=None):
        if color is None:
            self.rgb = (0, 0, 0)
        elif isinstance(color, EmbThread):
            self.name = color.description
            self.number = color.catalog_number
            self.manufacturer = color.brand
            self.rgb = (color.get_red(), color.get_green(), color.get_blue())
            return
        elif isinstance(color, (list, tuple)):
            self.rgb = tuple(color)
        elif self.hex_str_re.match(color):
            self.rgb = simplestyle.parseColor(color)
        else:
            raise ValueError("Invalid color: " + repr(color))

        self.name = name
        self.number = number
        self.manufacturer = manufacturer

    def __json__(self):
        jsonified = self._as_dict()
        jsonified["visible_on_white"] = self.visible_on_white._as_dict()

        return jsonified

    def _as_dict(self):
        return dict(name=self.name,
                    number=self.number,
                    manufacturer=self.manufacturer,
                    rgb=self.rgb,
                    hex=self.to_hex_str(),
                    )

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
        return "#%s" % self.hex_digits

    @property
    def pyembroidery_thread(self):
        return {
            "name": self.name,
            "id": self.number,
            "manufacturer": self.manufacturer,
            "rgb": int(self.hex_digits, 16),
        }

    @property
    def hex_digits(self):
        return "%02X%02X%02X" % self.rgb

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

    @property
    def visible_on_white(self):
        """A ThreadColor similar to this one but visible on white.

        If the thread color is white, we don't want to try to draw white in the
        simulation view or print white in the print-out.  Choose a color that's
        as close as possible to the actual thread color but is still at least
        somewhat visible on a white background.
        """

        hls = list(colorsys.rgb_to_hls(*self.rgb_normalized))

        # Capping lightness should make the color visible without changing it
        # too much.
        if hls[1] > 0.85:
            hls[1] = 0.85

        color = colorsys.hls_to_rgb(*hls)

        # convert back to values in the range of 0-255
        color = tuple(value * 255 for value in color)

        return ThreadColor(color, name=self.name, number=self.number, manufacturer=self.manufacturer)

    @property
    def darker(self):
        hls = list(colorsys.rgb_to_hls(*self.rgb_normalized))

        # Capping lightness should make the color visible without changing it
        # too much.
        hls[1] *= 0.75

        color = colorsys.hls_to_rgb(*hls)

        # convert back to values in the range of 0-255
        color = tuple(value * 255 for value in color)

        return ThreadColor(color, name=self.name, number=self.number, manufacturer=self.manufacturer)

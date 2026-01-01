# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import colorsys

from inkex import Color, ColorError

from pystitch.EmbThread import EmbThread


class ThreadColor(object):
    def __init__(self, color, name=None, number=None, manufacturer=None, description=None, chart=None):  # noqa: C901
        self.rgb = None

        if isinstance(color, str) and color.lower().startswith(('url', 'currentcolor', 'context')):
            '''
            Avoid error messages for currentcolor, context-fill, context-stroke and every string starting with an url.
            they should not just be black, but we want to avoid error messages
            '''
            color = None
        elif isinstance(color, str) and color.startswith('rgb'):
            color = tuple(int(value) for value in color[4:-1].split(','))
            # remove alpha channel
            if len(color) == 4:
                color = color[:3]

        if color is None:
            self.rgb = (0, 0, 0)
        elif isinstance(color, Color):
            self.rgb = color.to('rgb')
        elif isinstance(color, EmbThread):
            self.name = color.description
            self.number = color.catalog_number
            self.manufacturer = color.brand
            self.description = color.description
            self.chart = color.chart
            self.rgb = (color.get_red(), color.get_green(), color.get_blue())
            return
        elif isinstance(color, str):
            try:
                self.rgb = tuple(Color(color).to('rgb'))
            except ColorError:
                self.rgb = None
        elif isinstance(color, (list, tuple)):
            self.rgb = tuple(color)

        if self.rgb is None:
            '''
            Instead of erroring out, we want to set everything to black at this point.
            This includes for example patterns and gradients
            '''
            self.rgb = (0, 0, 0)

        self.name = name
        self.number = number
        self.manufacturer = manufacturer
        self.description = description
        self.chart = chart

    def __json__(self):
        jsonified = self._as_dict()
        jsonified["visible_on_white"] = self.visible_on_white._as_dict()

        return jsonified

    def _as_dict(self):
        return dict(name=self.name,
                    number=self.number,
                    manufacturer=self.manufacturer,
                    description=self.description,
                    chart=self.chart,
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
        return not (self == other)

    def __repr__(self):
        return "ThreadColor" + repr(self.rgb)

    def to_hex_str(self):
        return "#%s" % self.hex_digits

    @property
    def pystitch_thread(self):
        return {
            "name": self.name,
            "id": self.number,
            "manufacturer": self.manufacturer,
            "description": self.description,
            "chart": self.chart,
            "rgb": int(self.hex_digits, 16),
        }

    @property
    def hex_digits(self):
        return "%02X%02X%02X" % tuple([int(x) for x in self.rgb])

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

        return ThreadColor(color, name=self.name, number=self.number, manufacturer=self.manufacturer, description=self.description, chart=self.chart)

    def visible_on_background(self, background_color):
        """A ThreadColor similar to this one but visible on given background color.

        Choose a color that's as close as possible to the actual thread color but is still at least
        somewhat visible on given background.
        """
        hls = list(colorsys.rgb_to_hls(*self.rgb_normalized))
        background = ThreadColor(background_color)
        background_hls = list(colorsys.rgb_to_hls(*background.rgb_normalized))

        difference = hls[1] - background_hls[1]

        if abs(difference) < 0.1:
            if hls[1] > 0.5:
                hls[1] -= 0.1
            else:
                hls[1] += 0.1

            color = colorsys.hls_to_rgb(*hls)

            # convert back to values in the range of 0-255
            color = tuple(value * 255 for value in color)

            return ThreadColor(color, name=self.name, number=self.number, manufacturer=self.manufacturer,
                               description=self.description, chart=self.chart)

        return self

    @property
    def darker(self):
        hls = list(colorsys.rgb_to_hls(*self.rgb_normalized))

        # Capping lightness should make the color visible without changing it
        # too much.
        hls[1] *= 0.75

        color = colorsys.hls_to_rgb(*hls)

        # convert back to values in the range of 0-255
        color = tuple(value * 255 for value in color)

        return ThreadColor(color, name=self.name, number=self.number, manufacturer=self.manufacturer, description=self.description, chart=self.chart)

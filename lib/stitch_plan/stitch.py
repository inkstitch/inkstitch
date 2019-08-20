from lib.i18n import _
from ..utils.geometry import Point

# L10N command label at bottom of simulator window
COMMAND_NAMES = [_("STITCH"), _("JUMP"), _("TRIM"), _("STOP"), _("COLOR CHANGE"), _("END")]
STITCH = 0
JUMP = 1
TRIM = 2
STOP = 3
COLOR_CHANGE = 4
END = 5

NO_COMMAND = -1

# It's not possible to specify a line thickness less than 1 pixel, even
# though we're drawing anti-aliased lines.  To get around this we scale
# the stitch positions up by this factor and then scale down by a
# corresponding amount during rendering.
PIXEL_DENSITY = 10


class Stitch(Point):
    def __init__(self, x, y=None, color=None, jump=False, stop=False, trim=False, color_change=False,
                 no_ties=False, end=False):
        Point.__init__(self, x, y)
        self.color = color
        self.jump = jump
        self.trim = trim
        self.end = end
        self.stop = stop
        self.color_change = color_change
        self.no_ties = no_ties

        # Allow creating a Stitch from a Point
        if isinstance(x, Point):
            point = x
            self.x = point.x
            self.y = point.y

    def __repr__(self):
        return "Stitch(%s, %s, %s, %s, %s, %s, %s, %s, %s)" % (self.x,
                                                               self.y,
                                                               self.color,
                                                               "JUMP" if self.jump else " ",
                                                               "TRIM" if self.trim else " ",
                                                               "STOP" if self.stop else " ",
                                                               "NO TIES" if self.no_ties else " ",
                                                               "COLOR CHANGE" if self.color_change else " ",
                                                               "END" if self.end else " "
                                                               )

    def copy(self):
        return Stitch(self.x, self.y, self.color, self.jump, self.stop, self.trim, self.color_change, self.no_ties,
                      self.end)

    @property
    def command_at_point(self):
        this_command = STITCH
        if self.trim is True:
            this_command = TRIM
        elif self.jump is True:
            this_command = JUMP
        elif self.color_change is True:
            this_command = COLOR_CHANGE
        elif self.stop is True:
            this_command = STOP
        elif self.end is True:
            this_command = END
        return this_command


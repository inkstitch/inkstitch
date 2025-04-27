import re
from math import degrees
from typing import List, Optional

from inkex import DirectedLineSegment, Path
from shapely.geometry import LineString

from ..debug.debug import debug
from ..i18n import _
from ..svg import PIXELS_PER_MM
from ..utils import string_to_floats
from .stitch import Stitch


class LockStitchDefinition:
    def __init__(self, lock_id=None, name=None, path=None, preview_image=None) -> None:
        self.id: str = lock_id
        self.name: str = name
        self._path: str = path
        self.preview_image: Optional[str] = None

    def __repr__(self) -> str:
        return "LockStitchDefinition(%s, %s, %s, %s)" % (self.id, self.name, self._path, self.preview_image)

    def stitches(self, stitches, pos, scale) -> List[Stitch]:
        raise NotImplementedError(f"{self.__class__.__name__} must implement stitches()")


class LockStitch:
    def __init__(self, lock_type, lock_id, scale_percent, scale_absolute):
        self.lock_stitch_definition = get_lock_stitch_definition_by_id(lock_type, lock_id)
        self.scale = LockStitchScale(scale_percent, scale_absolute)

    def set_path(self, path):
        self.lock_stitch_definition = CustomLock("custom", _("Custom"), path)

    def stitches(self, stitches, pos):
        return self.lock_stitch_definition.stitches(stitches, pos, self.scale)


class LockStitchScale:
    def __init__(self, scale_percent, scale_absolute):
        self.percent = scale_percent / 100
        self.absolute = scale_absolute


class CustomLock(LockStitchDefinition):
    def stitches(self, stitches, pos, scale):
        path_type = self._get_path_type()
        debug.log(f"CustomLock path={self._path} path_type={path_type}")
        if path_type == "svg":
            return SVGLock(self.id,
                           self.name,
                           self._path).stitches(stitches, pos, scale)
        elif path_type == "absolute":
            return AbsoluteLock(self.id,
                                self.name,
                                self._path).stitches(stitches, pos, scale)
        else:
            return half_stitch.stitches(stitches, pos, scale)

    def _get_path_type(self):
        if not self._path:
            return "invalid"
        if not re.match("^ *[0-9 .,-]*$", self._path):
            path = Path(self._path)
            if not path or len(list(path.end_points)) < 3:
                return None
            else:
                return "svg"
        else:
            path = string_to_floats(self._path, " ")
            if not path:
                return "invalid"
            else:
                return "absolute"


class RelativeLock(LockStitchDefinition):
    def stitches(self, stitches, pos, scale):
        if pos == "end":
            stitches = list(reversed(stitches))

        path = string_to_floats(self._path, " ")
        # ommit first path point from end lock stitches
        # to avoid duplicated stitches in the end result
        if len(path) > 1 and pos == "end":
            path = path[1:]

        # Travel back one stitch, stopping halfway there.
        # Then go forward one stitch, stopping halfway between
        # again.
        direction, length = self.get_direction_and_length(stitches)
        lock_stitches = []
        for delta in path:
            lock_stitches.append(Stitch(stitches[0] + delta * length * direction, tags=('lock_stitch',)))

        return lock_stitches

    def get_direction_and_length(self, stitches, i=1):
        if len(stitches) < i+1 or i > 15:
            # we exceeded the stitch length of the path or tried 15 times already
            # we don't want to try any longer and return a default value
            return Stitch(1, 0), 0.5

        to_previous = stitches[i] - stitches[0]
        length = to_previous.length()

        if length <= 0.5 * PIXELS_PER_MM:
            return self.get_direction_and_length(stitches, i+1)
        else:
            direction = to_previous.unit()

        # travel at least 0.5 and at most 1.5
        length = max(length, 0.5 * PIXELS_PER_MM)
        length = min(length, 1.5 * PIXELS_PER_MM)

        return direction, length


class AbsoluteLock(LockStitchDefinition):
    def stitches(self, stitches, pos, scale):
        if pos == "end":
            stitches = list(reversed(stitches))

        # make sure the path consists of only floats
        path = string_to_floats(self._path, " ")

        # get the length of our lock stitch path
        if pos == 'start':
            lock_pos = []
            lock = 0
            # reverse the list to make sure we end with the first stitch of the target path
            for tie_path in reversed(path):
                lock = lock - tie_path * scale.absolute
                lock_pos.insert(0, lock)
        elif pos == 'end':
            lock_pos = []
            lock = 0
            for tie_path in path:
                lock = lock + tie_path * scale.absolute
                lock_pos.append(lock)
        max_lock_length = max(lock_pos)

        # calculate the amount stitches we need from the target path
        # and generate a line
        upcoming = [stitches[0]]
        for stitch in stitches[1:]:
            to_start = stitch - upcoming[-1]
            upcoming.append(stitch)
            if to_start.length() >= max_lock_length:
                break
        line = LineString(upcoming)

        # add tie stitches
        lock_stitches = []
        for i, tie_path in enumerate(lock_pos):
            if tie_path < 0:
                stitch = Stitch(stitches[0] + tie_path * (stitches[1] - stitches[0]).unit())
            else:
                point = line.interpolate(tie_path)
                stitch = Stitch(point.x, point.y, tags=('lock_stitch',))
            lock_stitches.append(stitch)
        return lock_stitches


class SVGLock(LockStitchDefinition):
    def stitches(self, stitches, pos, scale):
        if pos == "end":
            stitches = list(reversed(stitches))

        path = Path(self._path)
        path.scale(PIXELS_PER_MM, PIXELS_PER_MM, True)
        path.scale(scale.percent, scale.percent, True)

        end_points = list(path.end_points)

        lock = DirectedLineSegment(end_points[-2], end_points[-1])
        lock_stitch_angle = lock.angle

        stitch = DirectedLineSegment((stitches[0].x, stitches[0].y),
                                     (stitches[1].x, stitches[1].y))
        stitch_angle = stitch.angle

        # rotate and translate the lock stitch
        path.rotate(degrees(stitch_angle - lock_stitch_angle), lock.start, True)
        translate = stitch.start - lock.start
        path.translate(translate.x, translate.y, True)

        # Remove direction indicator from path and also
        # remove start:last/end:first stitch (it is the position of the first/last stitch of the target path)
        path = list(path.end_points)[:-2]

        if pos == 'end':
            path = reversed(path)

        lock_stitches = []
        for i, stitch in enumerate(path):
            stitch = Stitch(stitch[0], stitch[1], tags=('lock_stitch',))
            lock_stitches.append(stitch)
        return lock_stitches


def get_lock_stitch_definition_by_id(pos, lock_type, default="half_stitch"):
    id_list = [lock.id for lock in LOCK_DEFAULTS[pos]]

    try:
        lock = LOCK_DEFAULTS[pos][id_list.index(lock_type)]
    except ValueError:
        lock = LOCK_DEFAULTS[pos][id_list.index(default)]
    return lock


half_stitch = RelativeLock("half_stitch", _("Half Stitch"), "0 0.5 1 0.5 0")
arrow = SVGLock("arrow", _("Arrow"), "M 0.5,0.3 0.3,1.31 -0.11,0.68 H 0.9 L 0.5,1.31 0.4,0.31 V 0.31 1.3")
back_forth = AbsoluteLock("back_forth", _("Back and forth"), "1 1 -1 -1")
bowtie = SVGLock("bowtie", _("Bowtie"), "M 0,0 -0.39,0.97 0.3,0.03 0.14,1.02 0,0 V 0.15")
cross = SVGLock("cross", _("Cross"), "M 0,0 -0.7,-0.7 0.7,0.7 0,0 -0.7,0.7 0.7,-0.7 0,0 -0,-0.7")
star = SVGLock("star", _("Star"), "M 0.67,-0.2 C 0.27,-0.06 -0.22,0.11 -0.67,0.27 L 0.57,0.33 -0.5,-0.27 0,0.67 V 0 -0.5")
simple = SVGLock("simple", _("Simple"), "M -0.03,0 0.09,0.81 0,1.49 V 0 0.48")
triangle = SVGLock("triangle", _("Triangle"), "M -0.26,0.33 H 0.55 L 0,0.84 V 0 L 0.34,0.82")
zigzag = SVGLock("zigzag", _("Zig-zag"), "M -0.25,0.2 0.17,0.77 -0.22,1.45 0.21,2.05 -0.03,3 0,0")
custom = CustomLock("custom", _("Custom"))

LOCK_DEFAULTS = {'start': [half_stitch, arrow, back_forth, bowtie, cross, star, simple, triangle, zigzag, custom],
                 'end': [half_stitch, arrow, back_forth, cross, bowtie, star, simple, triangle, zigzag, custom]}

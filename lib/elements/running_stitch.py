# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import shapely.geometry

from .element import EmbroideryElement, param
from ..i18n import _
from ..stitch_plan import StitchGroup
from ..stitches import bean_stitch, running_stitch
from ..utils import Point, cache

warned_about_legacy_running_stitch = False


class RunningStitch(EmbroideryElement):
    element_name = _("Running Stitch")

    @property
    def color(self):
        return self.get_style("stroke")

    @property
    @param('running_stitch_length_mm',
           _('Running stitch length'),
           tooltip=_('Length of stitches in running stitch mode.'),
           unit='mm',
           type='float',
           default=1.5,
           sort_index=3)
    def running_stitch_length(self):
        return max(self.get_float_param("running_stitch_length_mm", 1.5), 0.01)

    @property
    @param(
        'bean_stitch_repeats',
        _('Bean stitch number of repeats'),
        tooltip=_('Backtrack each stitch this many times.  '
                  'A value of 1 would triple each stitch (forward, back, forward).  '
                  'A value of 2 would quintuple each stitch, etc.'),
        type='int',
        default=0,
        sort_index=2)
    def bean_stitch_repeats(self):
        return self.get_int_param("bean_stitch_repeats", 0)

    @property
    @param('repeats',
           _('Repeats'),
           tooltip=_('Defines how many times to run down and back along the path.'),
           type='int',
           default="1",
           sort_index=1)
    def repeats(self):
        return self.get_int_param("repeats", 1)

    @property
    @cache
    def shape(self):
        line_strings = [shapely.geometry.LineString(path) for path in self.paths]

        # Using convex_hull here is an important optimization.  Otherwise
        # complex paths cause operations on the shape to take a long time.
        # This especially happens when importing machine embroidery files.
        return shapely.geometry.MultiLineString(line_strings).convex_hull

    def handle_repeats(self, path):
        repeated_path = []

        # go back and forth along the path as specified by self.repeats
        for i in range(self.repeats):
            if i % 2 == 1:
                # reverse every other pass
                this_path = path[::-1]
            else:
                this_path = path[:]

            repeated_path.extend(this_path)

        return repeated_path

    def to_stitch_groups(self, last_patch):
        patches = []

        for path in self.paths:
            path = self.handle_repeats(path)
            path = [Point(x, y) for x, y in path]

            stitches = running_stitch(path, self.running_stitch_length)

            if self.bean_stitch_repeats > 0:
                stitches = bean_stitch(stitches, self.bean_stitch_repeats)

            patches.append(StitchGroup(self.color, stitches))

        return patches

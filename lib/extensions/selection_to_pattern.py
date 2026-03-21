# Authors: see git history
#
# Copyright (c) 2021 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import errormsg

from ..gui.selection_to_pattern import SelectionToPatternApp
from ..i18n import _
from ..marker import set_marker
from ..svg.tags import EMBROIDERABLE_TAGS
from .base import InkstitchExtension


class SelectionToPattern(InkstitchExtension):
    '''
    Applies a patten marker to selected elements

    Stroke patterns have additional options:
        - interval (str): a list with integers to define a skip pattern
        - start offset (int): an initial offset before the interval starts
    '''
    def effect(self):
        if not self.svg.selection:
            errormsg(_("Please select at least one element."))
            return

        settings = {'interval': [], 'start_offset': [], 'remove': False, 'apply': False}

        for pattern in self.svg.selection:
            if pattern.tag in EMBROIDERABLE_TAGS and pattern.style('stroke') is not None:
                interval = pattern.get('inkstitch:pattern_interval', None)
                if interval is not None:
                    settings['interval'].append(interval)
                start_offset = pattern.get('inkstitch:pattern_offset', None)
                if start_offset is not None:
                    settings['start_offset'].append(start_offset)

        app = SelectionToPatternApp(settings=settings)
        app.MainLoop()

        if not settings['apply']:
            return

        self.settings = settings

        # Remove marker
        if settings['remove']:
            if not self.svg.selection:
                errormsg(_("Please select at least one object to remove the pattern marker."))
                return
            self._remove_marker_and_settings()
        else:
            if not self.svg.selection:
                errormsg(_("Please select at least one object to be marked as a pattern."))
                return
            self._add_marker()

    def _remove_marker_and_settings(self):
        for element in self.svg.selection:
            try:
                marker = element.style['marker-start']
                if 'inkstitch' in marker and 'pattern' in marker:
                    element.style['marker-start'] = None
            except KeyError:
                pass
            element.pop("inkstitch:pattern_offset")
            element.pop("inkstitch:pattern_interval")

    def _add_marker(self):
        # ensure all interval values are integers
        # then convert back to string as this is the format we need in the end
        try:
            interval = self.settings["interval"].split(" ")
            interval = [str(int(i)) for i in interval if i]
        except (TypeError, ValueError):
            interval = [1]

        # ensure start_offset is an integer value
        try:
            start_offset = int(self.settings["start_offset"])
        except ValueError:
            start_offset = 0

        for pattern in self.svg.selection:
            if pattern.tag in EMBROIDERABLE_TAGS:
                set_marker(pattern, 'start', 'pattern')
                if pattern.style('stroke') is not None:
                    pattern.set('inkstitch:pattern_interval', " ".join(interval))
                    pattern.set('inkstitch:pattern_offset', str(start_offset))

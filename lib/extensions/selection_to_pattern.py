# Authors: see git history
#
# Copyright (c) 2021 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import Boolean, errormsg

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

    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--notebook")
        self.arg_parser.add_argument("--interval", type=str, default="1", dest="interval")
        self.arg_parser.add_argument("--start_offset", type=int, default=0, dest="start_offset")
        self.arg_parser.add_argument("--remove_pattern_marker", type=Boolean, default=False, dest="remove")

    def effect(self):
        self.patterns = self.get_nodes()

        # Remove marker
        if self.options.remove:
            if not self.svg.selection:
                errormsg(_("Please select at least one object to remove the pattern marker."))
                return
            self._remove_marker()
        else:
            if not self.svg.selection:
                errormsg(_("Please select at least one object to be marked as a pattern."))
                return
            self._add_marker()

    def _remove_marker(self):
        for element in self.svg.selection:
            try:
                marker = element.style['marker-start']
                if 'inkstitch' in marker and 'pattern' in marker:
                    element.style['marker-start'] = None
            except KeyError:
                pass

    def _add_marker(self):
        # ensure all interval values are integers
        # then convert back to string as this is the format we need in the end
        try:
            interval = self.options.interval.split(" ")
            interval = [str(int(i)) for i in interval if i]
        except (TypeError, ValueError):
            interval = [1]

        for pattern in self.svg.selection:
            if pattern.tag in EMBROIDERABLE_TAGS:
                set_marker(pattern, 'start', 'pattern')
                if pattern.style('stroke') is not None:
                    pattern.set('inkstitch:pattern_interval', " ".join(interval))
                    pattern.set('inkstitch:pattern_offset', str(self.options.start_offset))

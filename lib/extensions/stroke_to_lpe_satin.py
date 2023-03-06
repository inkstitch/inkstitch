# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import inkex

from ..elements import Stroke
from ..i18n import _
from ..svg.tags import ORIGINAL_D, PATH_EFFECT, SODIPODI_NODETYPES
from .base import InkstitchExtension


class StrokeToLpeSatin(InkstitchExtension):
    """Convert a satin column into a running stitch."""

    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("-p", "--pattern", type=str, default="normal", dest="pattern")
        self.arg_parser.add_argument("-i", "--min-width", type=float, default=1.5, dest="min_width")
        self.arg_parser.add_argument("-a", "--max-width", type=float, default=7, dest="max_width")
        self.arg_parser.add_argument("-l", "--length", type=float, default=15, dest="length")
        self.arg_parser.add_argument("-t", "--stretched", type=inkex.Boolean, default=False, dest="stretched")

    def effect(self):
        if not self.svg.selection or not self.get_elements():
            inkex.errormsg(_("Please select at least one stroke."))
            return

        if not any(isinstance(item, Stroke) for item in self.elements):
            # L10N: Convert To Satin extension, user selected one or more objects that were not lines.
            inkex.errormsg(_("Please select at least one stroke to convert to a satin column."))
            return

        pattern = self.options.pattern
        if pattern not in satin_patterns:
            inkex.errormsg(_("Could not find the specified pattern."))
            return

        min_width = max(self.options.min_width, 0.5)
        max_width = max(self.options.max_width, 0.5)
        length = self.options.length
        pattern = satin_patterns[pattern]
        pattern_path = pattern.get_path(min_width, max_width, length)
        pattern_node_type = pattern.node_types

        copy_type = 'repeated' if self.options.stretched is False else 'repeated_stretched'

        # add the path effect element to the defs section
        lpe = inkex.PathEffect(attrib={'effect': "skeletal",
                                       'is_visible': "true",
                                       'lpeversion': "1",
                                       'pattern': pattern_path,
                                       'copytype': copy_type,
                                       'prop_scale': "1",
                                       'scale_y_rel': "false",
                                       'spacing': "0",
                                       'normal_offset': "0",
                                       'tang_offset': "0",
                                       'prop_units': "false",
                                       'vertical_pattern': "false",
                                       'hide_knot': "false",
                                       'fuse_tolerance': "0.02",
                                       'pattern-nodetypes': pattern_node_type})
        self.svg.defs.add(lpe)

        for element in self.elements:
            if not isinstance(element, Stroke):
                continue

            element.set_param('satin_column', 'true')
            element.node.set(PATH_EFFECT, lpe.get_id(as_url=1))
            element.node.set(ORIGINAL_D, element.node.get('d', ''))
            element.node.pop('d')

        # It can happen that the d-less path will disappear and cannot be restored.
        # Poosibly related: https://gitlab.com/inkscape/inkscape/-/merge_requests/4520
        # It seems as if it behaves better with some sort of output - but that would be a bit annoying.
        # inkex.errormsg(_("You can edit the pattern through Path > Path Effects ..."))

class SatinPattern:
    def __init__(self, path=None, node_types=None, flip=True):
        self.path: str = path
        self.node_types: str = node_types
        self.flip: bool = flip

    def get_path(self, min_width, max_width, length):
        el1 = inkex.PathElement(attrib={'d': self.path,
                                        SODIPODI_NODETYPES: self.node_types})
        bbox = el1.bounding_box()
        scale_x = length / max(bbox.width, 0.1)
        if bbox.height == 0:
            scale_y = 1
        else:
            scale_y = (max_width - min_width) / (bbox.height * 2)
        el1.transform = inkex.Transform(f'scale({scale_x}, {scale_y})')
        el1.apply_transform()
        path1 = el1.get_path()

        el2 = el1.copy()
        if self.flip:
            el2.transform = inkex.Transform(f'scale(1, -1) translate(0, {min_width})')
        else:
            el2.transform = inkex.Transform(f'translate(0, {-min_width})')
        el2.apply_transform()
        path2 = el2.get_path()

        return str(path1) + str(path2)


satin_patterns = {'normal': SatinPattern('M 0,0.4 H 4 H 8', 'cc'),
                  'pearl': SatinPattern('M 0,0 C 0,0.22 0.18,0.4 0.4,0.4 0.62,0.4 0.8,0.22 0.8,0', 'csc'),
                  'diamond': SatinPattern('M 0,0 0.4,0.2 0.8,0', 'ccc'),
                  'triangle': SatinPattern('M 0.0,0 0.4,0.1 0.8,0.2 V 0', 'cccc'),
                  'square': SatinPattern('M 0,0 H 0.2 0.4 V 0.2 H 0.8 V 0', 'ccccc'),
                  'wave': SatinPattern('M 0,0 C 0.2,0.01 0.29,0.2 0.4,0.2 0.51,0.2 0.58,0.01 0.8,0', 'cac'),
                  'arch': SatinPattern('M 0,0.25 C 0,0.25 0.07,0.05 0.4,0.05 0.7,0.05 0.8,0.25 0.8,0.25', 'czcczc', False)}

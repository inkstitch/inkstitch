# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import inkex

from ..elements import SatinColumn, Stroke
from ..i18n import _
from ..svg.tags import ORIGINAL_D, PATH_EFFECT, SODIPODI_NODETYPES
from .base import InkstitchExtension


class StrokeToLpeSatin(InkstitchExtension):
    """Convert a satin column into a running stitch."""

    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--lpe_satin", type=str, default=None)
        self.arg_parser.add_argument("--options", type=str, default=None)
        self.arg_parser.add_argument("--info", type=str, default=None)

        self.arg_parser.add_argument("-p", "--pattern", type=str, default="normal", dest="pattern")
        self.arg_parser.add_argument("-i", "--min-width", type=float, default=1.5, dest="min_width")
        self.arg_parser.add_argument("-a", "--max-width", type=float, default=7, dest="max_width")
        self.arg_parser.add_argument("-l", "--length", type=float, default=15, dest="length")
        self.arg_parser.add_argument("-t", "--stretched", type=inkex.Boolean, default=False, dest="stretched")
        self.arg_parser.add_argument("-r", "--rungs", type=inkex.Boolean, default=False, dest="add_rungs")

    def effect(self):
        if not self.svg.selection or not self.get_elements():
            inkex.errormsg(_("Please select at least one stroke."))
            return

        if not any((isinstance(item, Stroke) or isinstance(item, SatinColumn)) for item in self.elements):
            # L10N: Convert To Satin extension, user selected one or more objects that were not lines.
            inkex.errormsg(_("Please select at least one stroke to convert to a satin column."))
            return

        pattern = self.options.pattern
        if pattern not in satin_patterns:
            inkex.errormsg(_("Could not find the specified pattern."))
            return

        # convert user input values to the units of the current svg
        min_width = inkex.units.convert_unit(str(max(self.options.min_width, 0.5)) + 'mm', self.svg.unit)
        max_width = inkex.units.convert_unit(str(max(self.options.max_width, 0.5)) + 'mm', self.svg.unit)
        length = inkex.units.convert_unit(str(self.options.length) + 'mm', self.svg.unit)

        # get pattern path and nodetypes
        pattern_obj = satin_patterns[pattern]
        pattern_path = pattern_obj.get_path(self.options.add_rungs, min_width, max_width, length, self.svg.unit)
        pattern_node_type = pattern_obj.node_types

        # the lpe 'pattern along path' has two options to repeat the pattern, get user input
        copy_type = 'repeated' if self.options.stretched is False else 'repeated_stretched'

        # add the path effect element to the defs section
        self.lpe = inkex.PathEffect(attrib={'id': f'inkstitch-effect-{pattern}',
                                            'effect': "skeletal",
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
        self.svg.defs.add(self.lpe)

        for element in self.elements:
            if isinstance(element, SatinColumn):
                self._process_satin_column(element)
            elif isinstance(element, Stroke):
                self._process_stroke(element)

    def _process_stroke(self, element):
        previous_effects = element.node.get(PATH_EFFECT, None)
        if not previous_effects:
            element.node.set(PATH_EFFECT, self.lpe.get_id(as_url=1))
            element.node.set(ORIGINAL_D, element.node.get('d', ''))
        else:
            url = previous_effects + ';' + self.lpe.get_id(as_url=1)
            element.node.set(PATH_EFFECT, url)
        element.node.pop('d')
        element.set_param('satin_column', 'true')

        element.node.style['stroke-width'] = self.svg.viewport_to_unit('0.756')
        # remove running_stitch dashes if they are there
        element.update_dash(False)

    def _process_satin_column(self, element):
        current_effects = element.node.get(PATH_EFFECT, None)
        # there are possibly multiple path effects, let's check if inkstitch-effect is among them
        if not current_effects or 'inkstitch-effect' not in current_effects:
            # it wouldn't make sense to apply it to a normal satin column without the inkstitch-effect
            inkex.errormsg(_('Cannot convert a satin column into a live path effect satin. Please select a stroke.'))
            return
        # isolate get the inkstitch effect
        current_effects = current_effects.split(';')
        inkstitch_effect_position = [i for i, effect in enumerate(current_effects) if 'inkstitch-effect' in effect][0]
        inkstitch_effect = current_effects[inkstitch_effect_position][1:]
        # get the path effect element
        old_effect_element = self.svg.getElementById(inkstitch_effect)
        # remove the old inkstitch-effect
        old_effect_element.getparent().remove(old_effect_element)
        # update the path effect link
        current_effects[inkstitch_effect_position] = self.lpe.get_id(as_url=1)
        element.node.set(PATH_EFFECT, ';'.join(current_effects))
        element.node.pop('d')


class SatinPattern:
    def __init__(self, path=None, node_types=None, flip=True, rung_node=1):
        self.path: str = path
        self.node_types: str = node_types
        self.flip: bool = flip
        self.rung_node: int = rung_node

    def get_path(self, add_rungs, min_width, max_width, length, to_unit):
        # scale the pattern path to fit the unit of the current svg
        scale_factor = scale_factor = 1 / inkex.units.convert_unit('1mm', f'{to_unit}')
        pattern_path = inkex.Path(self.path).transform(inkex.Transform(f'scale({scale_factor})'), True)

        # create a path element
        el1 = inkex.PathElement(attrib={'d': str(pattern_path),
                                        SODIPODI_NODETYPES: self.node_types})

        # transform to fit user input size values
        bbox = el1.bounding_box()
        scale_x = length / max(bbox.width, 0.1)
        if bbox.height == 0:
            scale_y = 1
        else:
            scale_y = (max_width - min_width) / (bbox.height * 2)
        el1.transform = inkex.Transform(f'scale({scale_x}, {scale_y})')
        el1.apply_transform()
        path1 = el1.get_path()

        # copy first path and (optionally) flip it to generate the second satin rail
        el2 = el1.copy()
        if self.flip:
            el2.transform = inkex.Transform(f'scale(1, -1) translate(0, {min_width})')
        else:
            el2.transform = inkex.Transform(f'translate(0, {-min_width})')
        el2.apply_transform()
        path2 = el2.get_path()

        # setup a rung
        point1 = list(path1.end_points)[self.rung_node]
        point2 = list(path2.end_points)[self.rung_node]

        rungs = ''
        if add_rungs:
            rungs = f' M {point1[0]} {point1[1] + 0.1} L {point2[0]} {point2[1] - 0.2}'

        return str(path1) + str(path2) + rungs


satin_patterns = {'normal': SatinPattern('M 0,0.4 H 4 H 8', 'cc'),
                  'pearl': SatinPattern('M 0,0 C 0,0.22 0.18,0.4 0.4,0.4 0.62,0.4 0.8,0.22 0.8,0', 'csc'),
                  'diamond': SatinPattern('M 0,0 0.4,0.2 0.8,0', 'ccc'),
                  'triangle': SatinPattern('M 0.0,0 0.4,0.1 0.8,0.2 V 0', 'cccc'),
                  'square': SatinPattern('M 0,0 H 0.2 0.4 V 0.2 H 0.8 V 0', 'ccccc'),
                  'wave': SatinPattern('M 0,0 C 0.2,0.01 0.29,0.2 0.4,0.2 0.51,0.2 0.58,0.01 0.8,0', 'cac'),
                  'arch': SatinPattern('M 0,0.25 C 0,0.25 0.07,0.05 0.4,0.05 0.7,0.05 0.8,0.25 0.8,0.25', 'czcczc', False)}

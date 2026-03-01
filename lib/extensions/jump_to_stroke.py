# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import Boolean, DirectedLineSegment, Path, PathElement, Transform

from ..elements import Stroke
from ..i18n import _
from ..svg import PIXELS_PER_MM, generate_unique_id, get_correction_transform
from ..svg.tags import INKSTITCH_ATTRIBS, SVG_GROUP_TAG
from .base import InkstitchExtension


class JumpToStroke(InkstitchExtension):
    """Adds a running stitch as a connection between two (or more) selected elements.
       The elements must have the same color and a minimum distance (collapse_len)."""

    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--tab")

        self.arg_parser.add_argument("-i", "--minimum-jump-length", type=float, default=3.0, dest="min_jump")
        self.arg_parser.add_argument("-a", "--maximum-jump-length", type=float, default=0, dest="max_jump")
        self.arg_parser.add_argument("--connect", type=str, default="all", dest="connect")
        self.arg_parser.add_argument("--exclude-trim", type=Boolean, default=True, dest="exclude_trim")
        self.arg_parser.add_argument("--exclude-stop", type=Boolean, default=True, dest="exclude_stop")
        self.arg_parser.add_argument("--exclude-force-lock-stitch", type=Boolean, default=True, dest="exclude_forced_lock")

        self.arg_parser.add_argument("-m", "--merge", type=Boolean, default=False, dest="merge")
        self.arg_parser.add_argument("--merge_subpaths", type=Boolean, default=False, dest="merge_subpaths")
        self.arg_parser.add_argument("-l", "--stitch-length", type=float, default=2.5, dest="running_stitch_length_mm")
        self.arg_parser.add_argument("-t", "--tolerance", type=float, default=2.0, dest="running_stitch_tolerance_mm")

    def effect(self):
        self._set_selection()
        self.get_elements()
        self.metadata = self.get_inkstitch_metadata()

        if self.options.merge_subpaths:
            # when we merge stroke elements we are going to replace original path elements
            # which would be bad in the case that the element has more subpaths
            self._split_stroke_elements_with_subpaths()

        last_group = None
        last_layer = None
        last_element = None
        last_stitch_group = None
        next_elements = [None]
        if len(self.elements) > 1:
            next_elements = self.elements[1:] + next_elements
        for element, next_element in zip(self.elements, next_elements):
            layer, group = self._get_element_layer_and_group(element)
            stitch_groups = element.embroider(last_stitch_group, next_element)
            multiple = not self.options.merge_subpaths and stitch_groups

            if multiple:
                ending_point = stitch_groups[0].stitches[0]
                stitch_groups = [stitch_groups[-1]]

            if (not stitch_groups or
                    last_element is None or
                    (self.options.connect == "layer" and last_layer != layer) or
                    (self.options.connect == "group" and last_group != group) or
                    (self.options.exclude_trim and (last_element.has_command("trim") or last_element.trim_after)) or
                    (self.options.exclude_stop and (last_element.has_command("stop") or last_element.stop_after)) or
                    (self.options.exclude_forced_lock and last_element.force_lock_stitches)):
                last_layer = layer
                last_group = group
                last_element = element
                if stitch_groups:
                    last_stitch_group = stitch_groups[-1]
                continue

            for stitch_group in stitch_groups:
                if last_stitch_group is None or stitch_group.color != last_stitch_group.color:
                    last_layer = layer
                    last_group = group
                    last_stitch_group = stitch_group
                    continue
                start = last_stitch_group.stitches[-1]
                if multiple:
                    end = ending_point
                else:
                    end = stitch_group.stitches[0]
                self.generate_stroke(last_element, element, start, end)
                last_stitch_group = stitch_group

            last_group = group
            last_layer = layer
            last_element = element

    def _set_selection(self):
        if not self.svg.selection:
            self.svg.selection.clear()

    def _get_element_layer_and_group(self, element):
        layer = None
        group = None
        for ancestor in element.node.iterancestors(SVG_GROUP_TAG):
            if group is None:
                group = ancestor
            if ancestor.groupmode == "layer":
                layer = ancestor
                break
        return layer, group

    def _split_stroke_elements_with_subpaths(self):
        elements = []
        for element in self.elements:
            if isinstance(element, Stroke) and len(element.paths) > 1:
                if element.get_param('stroke_method', None) in ['ripple_stitch']:
                    elements.append(element)
                    continue
                node = element.node
                parent = node.getparent()
                index = parent.index(node)
                paths = node.get_path().break_apart()

                block_ids = []
                for path in paths:
                    subpath_element = node.copy()
                    subpath_id = generate_unique_id(node, f'{node.get_id()}_', block_ids)
                    subpath_element.set('id', subpath_id)
                    subpath_element.set('d', str(path))
                    block_ids.append(subpath_id)
                    parent.insert(index, subpath_element)
                    elements.append(Stroke(subpath_element))
                node.delete()
            else:
                elements.append(element)
        self.elements = elements

    def _is_mergable(self, element1, element2):
        if not (isinstance(element1, Stroke)):
            return False
        if (self.options.merge_subpaths and
                element1.node.get_id() not in self.svg.selection.ids and
                element2.node.get_id() not in self.svg.selection.ids):
            return True
        if (self.options.merge and
                element1.node.TAG == "path" and
                element1.get_param('stroke_method', None) == element2.get_param('stroke_method', None) and
                not element1.get_param('stroke_method', '') == 'ripple_stitch'):
            return True
        return False

    def generate_stroke(self, last_element, element, start, end):
        node = element.node
        parent = node.getparent()
        index = parent.index(node)

        # do not add a running stitch if the distance is smaller than min_jump setting
        # when the extension didn't define a value, use the actual min. jump stitch length
        min_jump = self.options.min_jump
        if not min_jump:
            min_jump = last_element.min_jump_stitch_length
        if min_jump is None:
            min_jump = self.metadata['collapse_len_mm'] * PIXELS_PER_MM
        line = DirectedLineSegment((start.x, start.y), (end.x, end.y))
        if line.length <= min_jump:
            return

        # do not add a running stitch if the distance is longer than max_jump setting
        if self.options.max_jump > 0 and line.length >= self.options.max_jump * PIXELS_PER_MM:
            return

        path = Path([(start.x, start.y), (end.x, end.y)])
        # option: merge line with paths
        merged = False
        if self._is_mergable(last_element, element):
            path.transform(Transform(get_correction_transform(last_element.node, True)), True)
            path = last_element.node.get_path() + path[1:]
            last_element.node.set('d', str(path))
            path.transform(-Transform(get_correction_transform(last_element.node)), True)
            merged = True
        if self._is_mergable(element, last_element):
            path.transform(Transform(get_correction_transform(node)), True)
            path = path + node.get_path()[1:]
            node.set('d', str(path))
            if merged:
                # remove last element (since it is merged)
                last_parent = last_element.node.getparent()
                last_element.node.delete()
                # remove parent group if empty
                if len(last_parent) == 0:
                    last_parent.delete()
            return

        if merged:
            return

        # add simple stroke to connect elements
        path.transform(Transform(get_correction_transform(node)), True)
        color = element.color
        style = f'stroke:{color};stroke-width:{self.svg.viewport_to_unit("1px")};fill:none;'

        line = PathElement(d=str(path), style=style)
        line.label = _('Running Stitch')
        line.set(INKSTITCH_ATTRIBS['running_stitch_length_mm'], self.options.running_stitch_length_mm)
        line.set(INKSTITCH_ATTRIBS['running_stitch_tolerance_mm'], self.options.running_stitch_tolerance_mm)
        parent.insert(index, line)


if __name__ == '__main__':
    JumpToStroke().run()

# Authors: see git history
#
# Copyright (c) 2025 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import json
from typing import Optional

from inkex import (Boolean, PathElement, ShapeElement, Transform, Vector2d,
                   errormsg)

from ..i18n import _
from ..tartan.utils import get_tartan_settings
from .base import InkstitchExtension


class TransformElements(InkstitchExtension):
    '''
    This will apply transformations while also transforming fill angles.
    '''
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--notebook")
        self.arg_parser.add_argument("-r", "--rotate", type=float, default=0, dest="rotate")
        self.arg_parser.add_argument("-f", "--flip-horizontally", type=Boolean, default=False, dest="horizontal_flip")
        self.arg_parser.add_argument("-v", "--flip-vertically", type=Boolean, default=False, dest="vertical_flip")

    def effect(self) -> None:
        if not self.svg.selection:
            errormsg(_("Please select one or more elements."))
            return
        selection_center = self.svg.selection.bounding_box().center

        nodes = self.get_nodes()
        for node in nodes:
            parent_transform = node.composed_transform() @ -node.transform
            if self.options.rotate != 0:
                self.rotate_node(node, parent_transform, selection_center)
            if self.options.horizontal_flip:
                self.flip_node_horizontally(node, parent_transform, selection_center)
            if self.options.vertical_flip:
                self.flip_node_vertically(node, parent_transform, selection_center)

            # Apply transform to path elements, simply because it's possible and nicer
            if isinstance(node, PathElement):
                node.apply_transform()

    def flip_node_vertically(self, node: ShapeElement, parent_transform: Transform, center: Vector2d) -> None:
        node.transform = (
            -parent_transform @
            Transform(f'translate({center[0], center[1]}) scale(1, -1) translate({-center[0], -center[1]})') @
            node.composed_transform()
        )
        self.adapt_fill_angle(node, -1)

    def flip_node_horizontally(self, node: ShapeElement, parent_transform: Transform, center: Vector2d) -> None:
        node.transform = (
            -parent_transform @
            Transform(f'translate({center[0], center[1]}) scale(-1, 1) translate({-center[0], -center[1]})') @
            node.composed_transform()
        )
        self.adapt_fill_angle(node, -1)

    def rotate_node(self, node: ShapeElement, parent_transform: Transform, center: Vector2d) -> None:
        node.transform = (
            -parent_transform @
            Transform(f'rotate({self.options.rotate}, {center[0]}, {center[1]})') @
            node.composed_transform()
        )
        self.adapt_fill_angle(node, None, self.options.rotate)

    def adapt_fill_angle(self, node: ShapeElement, multiplier: Optional[int] = None, rotation: Optional[float] = None) -> None:
        if not node.style("fill", "black"):
            return

        self._apply_angle(node, "inkstitch:fill_underlay_angle", None, multiplier, rotation)
        if node.get('inkstitch:fill_method', None) == "tartan_fill":
            # Also rotate tartan pattern rotation setting
            self._rotate_tartan_pattern(node, multiplier, rotation)
        elif node.get('inkstitch:fill_method', None) == "meander_fill":
            self._apply_angle(node, "inkstitch:meander_angle", "0", multiplier, rotation)
        else:
            self._apply_angle(node, "inkstitch:angle", "0", multiplier, rotation)

    def _apply_angle(self, node: ShapeElement, attrib: str, default: Optional[str], multiplier: Optional[int], rotation: Optional[float]) -> None:
        angle_string = node.get(attrib, default)
        if angle_string is None:
            return

        try:
            angle = float(angle_string)
        except ValueError:
            return

        if multiplier is not None:
            angle *= multiplier
        elif rotation is not None:
            angle -= rotation
        node.set(attrib, str(angle))

    def _rotate_tartan_pattern(self, node: ShapeElement, multiplier: Optional[int], rotation: Optional[float]) -> None:
        settings = get_tartan_settings(node)
        tartan_rotation = settings['rotate']

        if multiplier is not None:
            tartan_rotation *= multiplier
        elif rotation is not None:
            tartan_rotation += rotation
        settings['rotate'] = tartan_rotation
        node.set("inkstitch:tartan", json.dumps(settings))

# Authors: see git history
#
# Copyright (c) 2025 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from typing import Optional

from inkex import (Boolean, PathElement, ShapeElement, Transform, Vector2d,
                   errormsg)

from ..i18n import _
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
        fill_angle = float(node.get("inkstitch:angle", 0))
        underlay_angle = node.get("inkstitch:fill_underlay_angle", None)
        if underlay_angle is not None:
            underlay_angle = float(underlay_angle)
        if multiplier is not None:
            fill_angle *= multiplier
            if underlay_angle is not None:
                underlay_angle *= multiplier
        elif rotation is not None:
            fill_angle -= rotation
            if underlay_angle is not None:
                underlay_angle -= self.options.rotate

        node.set('inkstitch:angle', str(fill_angle))
        if underlay_angle is not None:
            node.set('inkstitch:fill_underlay_angle', str(underlay_angle))

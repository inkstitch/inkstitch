# Authors: see git history
#
# Copyright (c) 2024 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from collections import deque

from inkex import Path, Transform, errormsg
from shapely import MultiPoint, Point

from ..elements import EmbroideryElement
from ..i18n import _
from ..svg import get_correction_transform
from .base import InkstitchExtension


class RemoveDuplicatedPoints(InkstitchExtension):
    '''
    This extension will remove duplicated points within the given range
    '''
    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("--notebook")
        self.arg_parser.add_argument("-n", "--num_points", type=int, default=10, dest="num_points")
        self.arg_parser.add_argument("-d", "--distance", type=float, default=0.01, dest="distance")

    def effect(self):
        if not self.get_elements():
            return

        if not self.svg.selection:
            errormsg(_("Please select one or more strokes."))
            return

        visited_nodes = []
        for element in self.elements:
            if element.node.get_id() in visited_nodes:
                continue
            visited_nodes.append(element.node.get_id())
            if element.node.TAG != 'path':
                # convert objects into paths
                node = element.node.to_path_element()
                element.node.getparent().replace(element.node, node)
                element = EmbroideryElement(node)
            new_paths = []
            for path in element.paths:
                new_path = []
                for point in path:
                    # do compare with more than 10 points
                    points = deque(new_path, maxlen=self.options.num_points)
                    if not points or Point(point).distance(MultiPoint(points)) > self.options.distance:
                        new_path.append(point)
                new_paths.append(new_path)
            transform = -element.node.transform @ Transform(get_correction_transform(element.node))
            element.node.set('d', str(Path(new_paths[0]).transform(transform)))

# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import inkex

from ..elements import Stroke
from ..i18n import _
from .base import InkstitchExtension


class MeanderStrokeToSatin(InkstitchExtension):
    """Convert a satin column into a running stitch."""

    def effect(self):
        if not self.svg.selection or not self.get_elements():
            inkex.errormsg(_("Please select at least one stroke."))
            return

        if not any(isinstance(item, Stroke) for item in self.elements):
            # L10N: Convert To Satin extension, user selected one or more objects that were not lines.
            inkex.errormsg(_("Please select at least one stroke to convert to a satin column."))
            return

        for element in self.elements:
            #                                    _   _
            # the path should look like this: |_| |_| | it always starts and ends with a rung
            # to build the satin column path we need to create the two rails and all the rungs.
            #   First rail  - every first and fourth node
            #   Second rail - every second and third node
            #   Rungs       - every odd node builds a rung together with the following even node
            #

            rungs = []
            rails = [[], []]

            # group the nodes in lists of four
            nodes = list(element.node.get_path().end_points)
            nodes = [nodes[i*4:i*4+4] for i in range(len(nodes)-4)]

            for i, points in enumerate(nodes):
                if len(points) <= 1:
                    break

                elif len(points) < 4 and len(points) > 1:
                    rails[0].append(str(points[0]))
                    rails[1].append(str(points[1]))
                    rungs.append([str(points[0]), str(points[1])])
                    break

                rails[0].extend([str(points[0]), str(points[3])])
                rails[1].extend([str(points[1]), str(points[2])])
                rungs.extend([[points[0], points[1]], [points[2], points[3]]])

            path = ""
            # make the rungs slightly bigger and remove the first and last rung
            for rung in rungs[1:-1]:
                line = inkex.DirectedLineSegment(rung[0], rung[1])
                point0 = line.point_at_ratio(-0.1)
                point1 = line.point_at_ratio(1.1)
                path += f'M {point0[0]}, {point0[1]} {point1[0]}, {point1[1]} '

            # set path
            for rail in rails:
                path += 'M '
                path += ' '.join(rail)
            element.node.set('d', path)
            element.set_param('satin_column', True)

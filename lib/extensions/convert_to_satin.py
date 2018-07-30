import inkex
from shapely import geometry as shgeo
from itertools import chain

from .base import InkstitchExtension
from ..svg.tags import SVG_PATH_TAG
from ..svg import get_correction_transform, PIXELS_PER_MM
from ..elements import Stroke
from ..utils import Point


class ConvertToSatin(InkstitchExtension):
    """Convert a line to a satin column of the same width."""

    def effect(self):
        if not self.get_elements():
            return

        if not self.selected:
            inkex.errormsg(_("Please select at least one line to convert to a satin column."))
            return

        if not all(isinstance(item, Stroke) for item in self.elements):
            # L10N: Convert To Satin extension, user selected one or more objects that were not lines.
            inkex.errormsg(_("Only simple lines may be converted to satin columns."))
            return

        for element in self.elements:
            parent = element.node.getparent()
            index = parent.index(element.node)
            correction_transform = get_correction_transform(element.node)

            for path in element.paths:
                try:
                    rails, rungs = self.path_to_satin(path, element.stroke_width)
                except ValueError:
                    inkex.errormsg(_("Cannot convert %s to a satin column because it intersects itself.  Try breaking it up into multiple paths.") % element.node.get('id'))

                parent.insert(index, self.satin_to_svg_node(rails, rungs, correction_transform))

            parent.remove(element.node)

    def path_to_satin(self, path, stroke_width):
        path = shgeo.LineString(path)

        left_rail = path.parallel_offset(stroke_width / 2.0, 'left')
        right_rail = path.parallel_offset(stroke_width / 2.0, 'right')

        if not isinstance(left_rail, shgeo.LineString) or \
           not isinstance(right_rail, shgeo.LineString):
                # If the parallel offsets come out as anything but a LineString, that means the
                # path intersects itself, when taking its stroke width into consideration.  See
                # the last example for parallel_offset() in the Shapely documentation:
                #   https://shapely.readthedocs.io/en/latest/manual.html#object.parallel_offset
                raise ValueError()

        # for whatever reason, shapely returns a right-side offset's coordinates in reverse
        left_rail = list(left_rail.coords)
        right_rail = list(reversed(right_rail.coords))

        rungs = self.generate_rungs(path, stroke_width)

        return (left_rail, right_rail), rungs

    def generate_rungs(self, path, stroke_width):
        rungs = []

        # approximately 1cm between rungs, and we don't want them at the very start or end
        num_rungs = int(path.length / PIXELS_PER_MM / 10) - 1

        if num_rungs < 1 or num_rungs == 2:
            # avoid 2 rungs because it can be ambiguous (which are the rails and which are the
            # rungs?)
            num_rungs += 1

        distance_between_rungs = path.length / (num_rungs + 1)

        for i in xrange(num_rungs):
            rung_center = path.interpolate((i + 1) * distance_between_rungs)
            rung_center = Point(rung_center.x, rung_center.y)

            # TODO: use bezierslopeatt or whatever
            # we need to calculate the normal at this point so grab another point just a little
            # further down the path, effectively grabbing a small segment of the path
            segment_end = path.interpolate((i + 1) * distance_between_rungs + 0.1)
            segment_end = Point(segment_end.x, segment_end.y)

            tangent = segment_end - rung_center
            normal = tangent.unit().rotate_left()
            offset = normal * stroke_width * 0.75

            rung_start = rung_center + offset
            rung_end = rung_center - offset

            rungs.append((rung_start.as_tuple(), rung_end.as_tuple()))

        return rungs
        import sys
        print >> sys.stderr, rails, rungs



    def satin_to_svg_node(self, rails, rungs, correction_transform):
        d = ""
        for path in chain(rails, rungs):
            d += "M"
            for x, y in path:
                d += "%s,%s " % (x, y)
            d += " "

        return inkex.etree.Element(SVG_PATH_TAG,
            {
                "id": self.uniqueId("path"),
                "style": "stroke:#000000;stroke-width:1px;fill:none",
                "transform": correction_transform,
                "d": d,
                "embroider_satin_column": "true",
            }
        )

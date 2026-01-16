# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from shapely import make_valid
from shapely.errors import GEOSException
from shapely.geometry import MultiPolygon, Polygon

from ..i18n import _
from ..svg.path import get_node_transform
from ..utils.geometry import ensure_multi_polygon
from .element import EmbroideryElement
from .validation import ObjectTypeWarning


class ImageTypeWarning(ObjectTypeWarning):
    name = _("Image")
    description = _("Ink/Stitch can't work with objects like images.")
    steps_to_solve = [
        _('* Redraw the image with the pen (P) or bezier (B) tool'),
        _('* Alternatively convert your image into a path: Path > Trace Bitmap... (Shift+Alt+B) '
          '(further steps might be required)'),
        _('* To convert the image for cross stitching, use Tools: Fill > Cross Stitch Helper')
    ]


class ImageObject(EmbroideryElement):
    name = "Image"

    @property
    def shape(self):
        shape = self._get_clipped_path()

        if shape.is_valid:
            # set_precision to avoid FloatingPointErrors
            return ensure_multi_polygon(shape, 3)

        shape = make_valid(shape)

        return ensure_multi_polygon(shape, 3)

    def _get_clipped_path(self):
        if self.clip_shape is None:
            return self.original_shape

        # make sure clip path and shape are valid
        clip_path = make_valid(self.clip_shape)
        shape = make_valid(self.original_shape)

        try:
            intersection = clip_path.intersection(shape)
        except GEOSException:
            return self.original_shape

        return intersection

    @property
    def original_shape(self):
        # shapely's idea of "holes" are to subtract everything in the second set
        # from the first. So let's at least make sure the "first" thing is the
        # biggest path.
        paths = self.paths
        paths.sort(key=lambda point_list: Polygon(point_list).area, reverse=True)
        shape = MultiPolygon([(paths[0], paths[1:])])
        return shape

    def center(self):
        parent = self.node.getparent()
        assert parent is not None, "This should be part of a tree and therefore have a parent"
        transform = get_node_transform(parent)
        center = self.node.bounding_box(transform).center
        return center

    def validation_warnings(self):
        yield ImageTypeWarning(self.center())

    def to_stitch_groups(self, last_stitch_group, next_element):
        return []

    def first_stitch(self):
        return None

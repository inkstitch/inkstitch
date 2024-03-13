# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from math import atan2, degrees, radians

from inkex import CubicSuperPath, Path, Transform, ShapeElement
from shapely import MultiLineString

from ..stitch_plan.stitch_group import StitchGroup

from ..commands import is_command_symbol
from ..i18n import _
from ..svg.path import get_node_transform
from ..svg.tags import (EMBROIDERABLE_TAGS, INKSTITCH_ATTRIBS, SVG_USE_TAG,
                        XLINK_HREF, SVG_GROUP_TAG)
from ..utils import cache
from .element import EmbroideryElement, param
from .validation import ValidationWarning


class CloneWarning(ValidationWarning):
    name = _("Clone Object")
    description = _("There are one or more clone objects in this document.  "
                    "Ink/Stitch can work with single clones, but you are limited to set a very few parameters. ")
    steps_to_solve = [
        _("If you want to convert the clone into a real element, follow these steps:"),
        _("* Select the clone"),
        _("* Run: Edit > Clone > Unlink Clone (Alt+Shift+D)")
    ]


class Clone(EmbroideryElement):
    # A clone embroidery element is linked to an embroiderable element.
    # It will be ignored if the source element is not a direct child of the xlink attribute.

    element_name = "Clone"

    def __init__(self, *args, **kwargs):
        super(Clone, self).__init__(*args, **kwargs)

    @property
    @param('clone', _("Clone"), type='toggle', inverse=False, default=True)
    def clone(self):
        return self.get_boolean_param("clone")

    @property
    @param('angle',
           _('Custom fill angle'),
           tooltip=_("This setting will apply a custom fill angle for the clone."),
           unit='deg',
           type='float')
    @cache
    def clone_fill_angle(self):
        return self.get_float_param('angle') or None

    @property
    @param('flip_angle',
           _('Flip angle'),
           tooltip=_("Flip automatically calucalted angle if it appears to be wrong."),
           type='boolean')
    @cache
    def flip_angle(self):
        return self.get_boolean_param('flip_angle')

    def get_cache_key_data(self, previous_stitch):
        source_node = get_clone_source(self.node)
        source_elements = self.clone_to_elements(source_node)
        return [element.get_cache_key(previous_stitch) for element in source_elements]

    def clone_to_elements(self, node):
        from .utils import node_to_elements
        elements = []
        if node.tag in EMBROIDERABLE_TAGS:
            elements = node_to_elements(node, True)
        elif node.tag == SVG_GROUP_TAG:
            for child in node.iterdescendants():
                elements.extend(node_to_elements(child, True))
        return elements

    def to_stitch_groups(self, last_patch=None) -> list[StitchGroup]:
        patches = []

        source_node = get_clone_source(self.node)
        # Instead of copying the cloned nodes, we operate on them in-place.
        # The consequence of this is that any changes we make to the node tree must also be undone.
        if source_node.tag not in EMBROIDERABLE_TAGS and source_node.tag != SVG_GROUP_TAG:
            return []

        old_transform = source_node.get('transform', '')
        source_transform = source_node.composed_transform()
        source_path = Path(source_node.get_path()).transform(source_node.composed_transform())
        transform = Transform(source_node.get('transform', '')) @ -source_transform
        transform @= self.node.composed_transform() @ Transform(source_node.get('transform', ''))
        source_node.set('transform', transform)

        # Calculate the rotation angle to apply to cloned elements
        if self.clone_fill_angle is None:
            angle = self._get_rotation(transform, source_node, source_path)

        elements = self.clone_to_elements(source_node)
        for element in elements:
            old_angle = float(element.node.get(INKSTITCH_ATTRIBS['angle'], 0))

            if self.clone_fill_angle is None:  # Normally, rotate the cloned element's angle by the clone's rotation.
                element.node.set(INKSTITCH_ATTRIBS['angle'], old_angle + angle)
            else:  # If clone_fill_angle is specified, override the angle instead.
                element.node.set(INKSTITCH_ATTRIBS['angle'], self.clone_fill_angle)

            stitch_groups = element.to_stitch_groups(last_patch)
            patches.extend(stitch_groups)
            # Reset the angle on the underlying node
            element.node.set(INKSTITCH_ATTRIBS['angle'], old_angle)

        # Reset source node attribs
        source_node.set('transform', old_transform)
        return patches

    def _get_rotation(self, transform: Transform, source_node: ShapeElement, source_path: Path) -> float:
        """
        Get a rotation value (used for rotating the fill angle)
        :param transform: The transform to get a rotation from
        :param source_node: As a fallback, extract a rotation angle from the node's shape.
        :return: returns a rotation angle.
        """
        try:
            rotation = transform.rotation_degrees()
        except ValueError:
            source_path = CubicSuperPath(source_path)[0]
            clone_path = Path(source_node.get_path()).transform(source_node.composed_transform())
            clone_path = CubicSuperPath(clone_path)[0]

            angle_source = atan2(source_path[1][1][1] - source_path[0][1][1], source_path[1][1][0] - source_path[0][1][0])
            angle_clone = atan2(clone_path[1][1][1] - clone_path[0][1][1], clone_path[1][1][0] - clone_path[0][1][0])
            angle_embroidery = radians(-float(source_node.get(INKSTITCH_ATTRIBS['angle'], 0)))

            diff = angle_source - angle_embroidery
            rotation = degrees(diff + angle_clone)

            if self.flip_angle:
                rotation = -degrees(diff - angle_clone)

        return -rotation

    def center(self, source_node):
        transform = get_node_transform(self.node.getparent())
        center = self.node.bounding_box(transform).center
        return center

    @property
    def shape(self):
        path = self.node.get_path()
        transform = Transform(self.node.composed_transform())
        path = path.transform(transform)
        path = path.to_superpath()
        return MultiLineString(path)

    def validation_warnings(self):
        source_node = get_clone_source(self.node)
        point = self.center(source_node)
        yield CloneWarning(point)


def is_clone(node):
    if node.tag == SVG_USE_TAG and node.get(XLINK_HREF) and not is_command_symbol(node):
        return True
    return False


def get_clone_source(node):
    return node.href

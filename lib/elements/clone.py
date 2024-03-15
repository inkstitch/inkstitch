# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from math import degrees
from copy import deepcopy

from inkex import Transform, IBaseElement

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
           tooltip=_("Flip automatically calculated angle if it appears to be wrong."),
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

        source_node: IBaseElement = get_clone_source(self.node)
        if source_node.tag not in EMBROIDERABLE_TAGS and source_node.tag != SVG_GROUP_TAG:
            return []

        # Effectively, manually clone the href'd element: Place it into the tree at the same location
        # as the use element this Clone represents, with the same transform
        parent: IBaseElement = self.node.getparent()
        cloned_node = deepcopy(source_node)
        parent.add(cloned_node)
        cloned_node.set('transform', Transform(self.node.get('transform')) @ Transform(cloned_node.get('transform')))

        # Calculate the rotation angle to apply to the fill of cloned elements, if applicable
        if self.clone_fill_angle is None:
            source_transform = source_node.composed_transform()
            cloned_transform = cloned_node.composed_transform()

            def angle_for_transform(t: Transform) -> float:
                # Calculate a rotational angle, in degrees, for a transformation matrix

                # Strip out the translation component from the matrix
                t = Transform((t.a, t.b, t.c, t.d, 0, 0))
                try:
                    return t.rotation_degrees()
                except ValueError:
                    # Something is weird about the matrix such that it apparently isn't a rotation with a uniform scale.
                    # So, next best thing is to apply it to a unit vector and pull the angle from that.
                    return degrees(t.apply_to_point((1, 0).angle))

            source_angle = angle_for_transform(source_transform)
            cloned_angle = angle_for_transform(cloned_transform)
            angle = cloned_angle - source_angle

        elements = self.clone_to_elements(cloned_node)
        for element in elements:
            # We manipulate the element's node directly here instead of using get/set param methods, because otherwise
            # we run into issues due to those methods' use of caching not updating if the underlying param value is changed.

            if self.clone_fill_angle is None:  # Normally, rotate the cloned element's angle by the clone's rotation.
                element_angle = float(element.node.get(INKSTITCH_ATTRIBS['angle'], 0)) - angle
            else:  # If clone_fill_angle is specified, override the angle instead.
                element_angle = self.clone_fill_angle

            if self.flip_angle:
                element_angle = -element_angle

            element.node.set(INKSTITCH_ATTRIBS['angle'], element_angle)

            stitch_groups = element.to_stitch_groups(last_patch)
            patches.extend(stitch_groups)

        # Remove the "manually cloned" tree.
        parent.remove(cloned_node)

        return patches

    def center(self, source_node):
        transform = get_node_transform(self.node.getparent())
        center = self.node.bounding_box(transform).center
        return center

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

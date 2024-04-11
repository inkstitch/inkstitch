# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from math import degrees
from copy import deepcopy
from contextlib import contextmanager
from typing import Generator, List

from inkex import Transform, BaseElement, Style
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
                    "Ink/Stitch can work with clones, but you are limited to set a very few parameters. ")
    steps_to_solve = [
        _("If you want to convert the clone into a real element, follow these steps:"),
        _("* Select the clone"),
        _("* Run: Extensions > Ink/Stitch > Edit > Unlink Clone")
    ]


class Clone(EmbroideryElement):
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
        return self.get_float_param('angle')

    @property
    @param('flip_angle',
           _('Flip angle'),
           tooltip=_(
               "Flip automatically calculated angle if it appears to be wrong."),
           type='boolean')
    @cache
    def flip_angle(self):
        return self.get_boolean_param('flip_angle', False)

    def get_cache_key_data(self, previous_stitch):
        source_node = self.node.href
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

    def to_stitch_groups(self, last_stitch_group=None) -> List[StitchGroup]:
        with self.clone_elements() as elements:
            stitch_groups = []

            for element in elements:
                element_stitch_groups = element.to_stitch_groups(last_stitch_group)
                if len(element_stitch_groups):
                    last_stitch_group = element_stitch_groups[-1]
                    stitch_groups.extend(element_stitch_groups)

            return stitch_groups

    @contextmanager
    def clone_elements(self) -> Generator[List[EmbroideryElement], None, None]:
        """
        A context manager method which yields a set of elements representing the cloned element(s) href'd by this clone's element.
        Cleans up after itself afterwards.
        This is broken out from to_stitch_groups for testing convenience, primarily.
        Could possibly be refactored into just a generator - being a context manager is mainly to control the lifecycle of the elements
        that are cloned (again, for testing convenience primarily)
        """
        parent: BaseElement = self.node.getparent()
        cloned_node = self.resolve_clone()
        try:
            # In a try block so we can ensure that the cloned_node is removed from the tree in the event of an exception.
            # Otherwise, it might be left around on the document if we throw for some reason.
            yield self.clone_to_elements(cloned_node)
        finally:
            # Remove the "manually cloned" tree.
            parent.remove(cloned_node)

    def resolve_clone(self, recursive=True) -> BaseElement:
        """
        "Resolve" this clone element by copying the node it hrefs as if unlinking the clone in Inkscape.
        The node will be added as a sibling of this element's node, with its transform and style applied.
        The fill angles for resolved elements will be rotated per the transform and clone_fill_angle properties of the clone.

        :param recursive: Recursively "resolve" all child clones in the same manner
        :returns: The "resolved" node
        """
        parent: BaseElement = self.node.getparent()
        source_node: BaseElement = self.node.href
        source_parent: BaseElement = source_node.getparent()
        cloned_node = deepcopy(source_node)

        if recursive:
            # Recursively resolve all clones as if the clone was in the same place as its source
            source_parent.add(cloned_node)

            if is_clone(cloned_node):
                resolved_cloned_node = Clone(cloned_node).resolve_clone()
                cloned_node.getparent().remove(cloned_node)
                # Replace the cloned_node with its resolved version
                cloned_node = resolved_cloned_node
            else:
                clones: List[BaseElement] = [n for n in cloned_node.iterdescendants() if is_clone(n)]
                for clone in clones:
                    Clone(clone).resolve_clone()
                    clone.getparent().remove(clone)

            source_parent.remove(cloned_node)

        # Add the cloned node to be a sibling of this node
        parent.add(cloned_node)
        # The transform of a resolved clone is based on the clone's transform as well as the source element's transform.
        # This makes intuitive sense: The clone of a scaled item is also scaled, the clone of a rotated item is also rotated, etc.
        cloned_node.set('transform', Transform(self.node.get('transform')) @ Transform(cloned_node.get('transform')))

        # Merge the style, if any: Note that the source node's style applies on top of the use's, not the other way around.
        clone_style = self.node.get('style')
        if clone_style:
            merged_style = Style(clone_style)
            merged_style.update(cloned_node.get('style'))
            cloned_node.set('style', merged_style)

        # Compute angle transform:
        # Effectively, this is (local clone transform) * (to parent space) * (from clone's parent space)
        # There is a translation component here that will be ignored.
        source_transform = source_parent.composed_transform()
        clone_transform = self.node.composed_transform()
        angle_transform = clone_transform @ -source_transform
        self.apply_angles(cloned_node, angle_transform)

        return cloned_node

    def apply_angles(self, cloned_node: BaseElement, transform: Transform) -> None:
        """
        Adjust angles on a cloned tree based on their transform.
        """
        if self.clone_fill_angle is None:
            # Strip out the translation component to simplify the fill vector rotation angle calculation:
            # Otherwise we'd have to calculate the transform of (0,0) and subtract it from the transform of (1,0)
            angle_transform = Transform((transform.a, transform.b, transform.c, transform.d, 0.0, 0.0))

        elements = self.clone_to_elements(cloned_node)
        for node in cloned_node.iter():
            # Only need to adjust angles on embroiderable nodes
            if node.tag not in EMBROIDERABLE_TAGS:
                continue

            # Normally, rotate the cloned element's angle by the clone's rotation.
            if self.clone_fill_angle is None:
                element_angle = float(node.get(INKSTITCH_ATTRIBS['angle'], 0))
                # We have to negate the angle because SVG/Inkscape's definition of rotation is clockwise, while Inkstitch uses counter-clockwise
                fill_vector = (angle_transform @ Transform(f"rotate(${-element_angle})")).apply_to_point((1, 0))
                # Same reason for negation here.
                element_angle = -degrees(fill_vector.angle)
            else:  # If clone_fill_angle is specified, override the angle instead.
                element_angle = self.clone_fill_angle

            if self.flip_angle:
                element_angle = -element_angle

            node.set(INKSTITCH_ATTRIBS['angle'], round(element_angle, 6))

        return elements

    @property
    def shape(self):
        path = self.node.get_path()
        transform = Transform(self.node.composed_transform())
        path = path.transform(transform)
        path = path.to_superpath()
        return MultiLineString(path)

    def center(self, source_node):
        transform = get_node_transform(self.node.getparent())
        center = self.node.bounding_box(transform).center
        return center

    def validation_warnings(self):
        source_node = self.node.href
        point = self.center(source_node)
        yield CloneWarning(point)


def is_clone(node):
    if node.tag == SVG_USE_TAG and node.get(XLINK_HREF) and not is_command_symbol(node):
        return True
    return False

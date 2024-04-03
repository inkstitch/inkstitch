# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from math import degrees
from copy import deepcopy
from contextlib import contextmanager
from typing import Generator, List, Tuple

from inkex import Transform, BaseElement
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
        source_node, local_transform = get_concrete_source(self.node)

        if source_node.tag not in EMBROIDERABLE_TAGS and source_node.tag != SVG_GROUP_TAG:
            yield []
            return

        # Effectively, manually clone the href'd element: Place it into the tree at the same location
        # as the use element this Clone represents, with the same transform
        parent: BaseElement = self.node.getparent()
        cloned_node = deepcopy(source_node)
        cloned_node.set('transform', local_transform)
        parent.add(cloned_node)
        try:
            # In a try block so we can ensure that the cloned_node is removed from the tree in the event of an exception.
            # Otherwise, it might be left around on the document if we throw for some reason.
            self.resolve_all_clones(cloned_node)

            source_parent_transform = source_node.getparent().composed_transform()
            clone_transform = cloned_node.composed_transform()
            global_transform = clone_transform @ -source_parent_transform
            self.apply_angles(cloned_node, global_transform)

            yield self.clone_to_elements(cloned_node)
        finally:
            # Remove the "manually cloned" tree.
            parent.remove(cloned_node)

    def resolve_all_clones(self, node: BaseElement) -> None:
        """
        For a subtree, recursively replace all `use` tags with the elements they href.
        """
        clones: List[BaseElement] = [n for n in node.iterdescendants() if n.tag == SVG_USE_TAG]
        for clone in clones:
            parent: BaseElement = clone.getparent()
            source_node, local_transform = get_concrete_source(clone)
            cloned_node = deepcopy(source_node)
            parent.add(cloned_node)
            cloned_node.set('transform', local_transform)
            parent.remove(clone)
            self.resolve_all_clones(cloned_node)
            self.apply_angles(cloned_node, local_transform)

    def apply_angles(self, cloned_node: BaseElement, transform: Transform) -> None:
        """
        Adjust angles on a cloned tree based on their transform.
        """
        if self.clone_fill_angle is None:
            # Strip out the translation component to simplify the fill vector rotation angle calculation.
            angle_transform = Transform((transform.a, transform.b, transform.c, transform.d, 0.0, 0.0))

        elements = self.clone_to_elements(cloned_node)
        for element in elements:
            # We manipulate the element's node directly here instead of using get/set param methods, because otherwise
            # we may run into issues due to those methods' use of caching not updating if the underlying param value is changed.

            # Normally, rotate the cloned element's angle by the clone's rotation.
            if self.clone_fill_angle is None:
                element_angle = float(element.node.get(INKSTITCH_ATTRIBS['angle'], 0))
                # We have to negate the angle because SVG/Inkscape's definition of rotation is clockwise, while Inkstitch uses counter-clockwise
                fill_vector = (angle_transform @ Transform(f"rotate(${-element_angle})")).apply_to_point((1, 0))
                # Same reason for negation here.
                element_angle = -degrees(fill_vector.angle)
            else:  # If clone_fill_angle is specified, override the angle instead.
                element_angle = self.clone_fill_angle

            if self.flip_angle:
                element_angle = -element_angle

            element.node.set(INKSTITCH_ATTRIBS['angle'], element_angle)

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


def get_concrete_source(node: BaseElement) -> Tuple[BaseElement, Transform]:
    """
    Given a use element, follow hrefs until finding an element that is not a use.
    Returns that non-use element, and a transform to apply to a copy of that element
    which will place that copy in the same position as the use if added as a sibling of the use.
    """
    # Compute the transform that will be applied to the cloned element, which is based off of the cloned element.
    # This makes intuitive sense: The clone of a scaled element will also be scaled, the clone of a rotated element will also
    # be rotated, etc. Any transforms from the use element will be applied on top of that.
    transform = Transform(node.get('transform'))
    source_node: BaseElement = node.href
    while source_node.tag == SVG_USE_TAG:
        # In case the source_node href's a use (and that href's a use...), iterate up the chain until we get a source node,
        # applying the transforms as we go.
        transform @= Transform(source_node.get('transform'))
        source_node = source_node.href
    transform @= Transform(source_node.get('transform'))
    return (source_node, transform)

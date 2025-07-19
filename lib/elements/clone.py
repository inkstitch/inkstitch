# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from contextlib import contextmanager
from math import degrees
from typing import Dict, Generator, List, Optional, Tuple, Any, cast

from inkex import BaseElement, Title, Transform, Vector2d
from lxml.etree import _Comment
from shapely import Geometry, MultiLineString, Point as ShapelyPoint

from ..commands import (find_commands, is_command_symbol,
                        point_command_symbols_up)
from ..i18n import _
from ..stitch_plan.stitch_group import StitchGroup
from ..svg.path import get_node_transform
from ..svg.svg import copy_no_children
from ..svg.tags import (CONNECTION_END, CONNECTION_START, EMBROIDERABLE_TAGS,
                        INKSTITCH_ATTRIBS, SVG_GROUP_TAG, SVG_SYMBOL_TAG,
                        SVG_USE_TAG)
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
    name = "Clone"
    element_name = _("Clone")

    def __init__(self, node: BaseElement) -> None:
        super(Clone, self).__init__(node)

    @property
    @param('clone', _("Clone"), type='toggle', inverse=False, default=True)
    def clone(self) -> bool:
        return self.get_boolean_param("clone", True)

    @property
    @param('angle',
           _('Custom fill angle'),
           tooltip=_("This setting will apply a custom fill angle for the clone."),
           unit='deg',
           type='float')
    @cache
    def clone_fill_angle(self) -> float:
        return self.get_float_param('angle')

    @property
    @param('flip_angle',
           _('Flip angle'),
           tooltip=_(
               "Flip automatically calculated angle if it appears to be wrong."),
           type='boolean',
           default=False)
    @cache
    def flip_angle(self) -> bool:
        return self.get_boolean_param('flip_angle', False)

    def get_cache_key_data(self, previous_stitch: Any, next_element: EmbroideryElement) -> List[str]:
        source_node = self.node.href
        source_elements = self.clone_to_elements(source_node)
        return [element.get_cache_key(previous_stitch, next_element) for element in source_elements]

    def clone_to_elements(self, node: BaseElement) -> List[EmbroideryElement]:
        # Only used in get_cache_key_data, actual embroidery uses nodes_to_elements+iterate_nodes
        from .utils.nodes import node_to_elements
        elements = []
        if node.tag in EMBROIDERABLE_TAGS:
            elements = node_to_elements(node, True)
        elif node.tag == SVG_GROUP_TAG:
            for child in node.iterdescendants():
                elements.extend(node_to_elements(child, True))
        return elements

    def to_stitch_groups(self, last_stitch_group: Optional[StitchGroup], next_element: Optional[EmbroideryElement] = None) -> List[StitchGroup]:
        if not self.clone:
            return []

        with self.clone_elements() as elements:
            if not elements:
                return []
            stitch_groups = []

            next_elements = [next_element]
            if len(elements) > 1:
                next_elements = cast(List[Optional[EmbroideryElement]], elements[1:]) + next_elements
            for element, next_element in zip(elements, next_elements):
                # Using `embroider` here to get trim/stop after commands, etc.
                element_stitch_groups = element.embroider(last_stitch_group, next_element)
                if len(element_stitch_groups):
                    last_stitch_group = element_stitch_groups[-1]
                    stitch_groups.extend(element_stitch_groups)

            return stitch_groups

    @property
    def first_stitch(self) -> Optional[ShapelyPoint]:
        first, last = self.first_and_last_element()
        if first:
            return first.first_stitch
        return None

    def uses_previous_stitch(self) -> bool:
        first, last = self.first_and_last_element()
        if first:
            return first.uses_previous_stitch()
        return False

    def uses_next_element(self) -> bool:
        first, last = self.first_and_last_element()
        if last:
            return last.uses_next_element()
        return False

    @cache
    def first_and_last_element(self) -> Tuple[Optional[EmbroideryElement], Optional[EmbroideryElement]]:
        with self.clone_elements() as elements:
            if len(elements):
                return elements[0], elements[-1]
        return None, None

    @contextmanager
    def clone_elements(self) -> Generator[List[EmbroideryElement], None, None]:
        """
        A context manager method which yields a set of elements representing the cloned element(s) href'd by this clone's element.
        Cleans up after itself afterwards.
        This is broken out from to_stitch_groups for testing convenience, primarily.
        Could possibly be refactored into just a generator - being a context manager is mainly to control the lifecycle of the elements
        that are cloned (again, for testing convenience primarily)
        """
        from .utils.nodes import iterate_nodes, nodes_to_elements

        cloned_nodes = self.resolve_clone()
        try:
            # In a try block so we can ensure that the cloned_node is removed from the tree in the event of an exception.
            # Otherwise, it might be left around on the document if we throw for some reason.
            yield nodes_to_elements(iterate_nodes(cloned_nodes[0]))
        finally:
            # Remove the "manually cloned" tree.
            for cloned_node in cloned_nodes:
                cloned_node.delete()

    def resolve_clone(self, recursive: bool = True) -> List[BaseElement]:
        """
        "Resolve" this clone element by copying the node it hrefs as if unlinking the clone in Inkscape.
        The node will be added as a sibling of this element's node, with its transform and style applied.
        The fill angles for resolved elements will be rotated per the transform and clone_fill_angle properties of the clone.

        :param recursive: Recursively "resolve" all child clones in the same manner
        :returns: A list where the first element is the "resolved" node, and zero or more commands attached to that node
        """
        parent: Optional[BaseElement] = self.node.getparent()
        assert parent is not None, f"Element {self.node.get_id()} should have a parent"
        source_node: Optional[BaseElement] = self.node.href
        assert source_node is not None, f"Target of {self.node.get_id()} was None!"
        source_parent: Optional[BaseElement] = source_node.getparent()
        assert source_parent is not None, f"Target {source_node.get_id()} of {self.node.get_id()} should have a parent"
        cloned_node = clone_with_fixup(parent, source_node)

        if recursive:
            # Recursively resolve all clones as if the clone was in the same place as its source
            source_parent.add(cloned_node)

            if is_clone(cloned_node):
                cloned_node = cloned_node.replace_with(Clone(cloned_node).resolve_clone()[0])
            else:
                clones: List[BaseElement] = [n for n in cloned_node.iterdescendants() if is_clone(n)]
                for clone in clones:
                    clone.replace_with(Clone(clone).resolve_clone()[0])

            cloned_node.delete()

        # Add the cloned node to be a sibling of this node
        parent.add(cloned_node)
        # The transform of a resolved clone is based on the clone's transform as well as the source element's transform.
        # This makes intuitive sense: The clone of a scaled item is also scaled, the clone of a rotated item is also rotated, etc.
        clone_translate = Transform(f"translate({float(self.node.get('x', '0'))}, {float(self.node.get('y', '0'))})")

        if cloned_node.tag == SVG_SYMBOL_TAG:
            for child in cloned_node:
                child.transform = self.node.transform @ clone_translate @ child.transform
        else:
            cloned_node.transform = self.node.transform @ clone_translate @ cloned_node.transform

        # Merge the style, if any: Note that the source node's style applies on top of the use's, not the other way around.
        cloned_node.style = self.node.style + cloned_node.style

        # Compute angle transform:
        # Effectively, this is (local clone transform) * (to parent space) * (from clone's parent space)
        # There is a translation component here that will be ignored.
        if cloned_node.tag == SVG_SYMBOL_TAG:
            source_transform: Transform = parent.composed_transform()
        else:
            source_transform = source_parent.composed_transform()
        clone_transform: Transform = self.node.composed_transform()
        angle_transform = clone_transform @ -source_transform
        self.apply_angles(cloned_node, angle_transform)

        ret = [cloned_node]

        # For aesthetic purposes, transform all of the cloned command symbols so they're facing upwards
        point_command_symbols_up(cloned_node)

        # We need to copy all commands that were attached directly to the href'd node
        for command in find_commands(source_node):
            ret.append(command.clone(cloned_node))

        return ret

    def apply_angles(self, cloned_node: BaseElement, transform: Transform) -> None:
        """
        Adjust angles on a cloned tree based on their transform.
        """
        if self.clone_fill_angle is None:
            # Strip out the translation component to simplify the fill vector rotation angle calculation:
            # Otherwise we'd have to calculate the transform of (0,0) and subtract it from the transform of (1,0)
            angle_transform = Transform((transform.a, transform.b, transform.c, transform.d, 0.0, 0.0))

        for node in cloned_node.iter():
            # Only need to adjust angles on embroiderable nodes
            if node.tag not in EMBROIDERABLE_TAGS:
                continue

            # Only need to adjust angles on fill elements.
            element = EmbroideryElement(node)
            if not (element.get_style("fill", "black") and not element.get_style('fill-opacity', 1) == "0"):
                continue

            # Normally, rotate the cloned element's angle by the clone's rotation.
            if self.clone_fill_angle is None:
                element_angle = float(node.get(INKSTITCH_ATTRIBS['angle'], 0))
                # We have to negate the angle because SVG/Inkscape's definition of rotation is clockwise, while Inkstitch uses counter-clockwise
                fill_vector = (angle_transform @ Transform(f"rotate(${-element_angle})")).apply_to_point((1, 0))
                # Same reason for negation here.
                element_angle = -degrees(fill_vector.angle or 0)  # Fallback to 0 if an insane transform is used.
            else:  # If clone_fill_angle is specified, override the angle instead.
                element_angle = self.clone_fill_angle

            if self.flip_angle:
                element_angle = -element_angle

            node.set(INKSTITCH_ATTRIBS['angle'], round(element_angle, 6))

    @property
    def shape(self) -> Geometry:
        path = self.node.get_path()
        transform = Transform(self.node.composed_transform())
        path = path.transform(transform)
        path = path.to_superpath()
        return MultiLineString(path[0])

    def center(self, source_node: BaseElement) -> Vector2d:
        translate = Transform(f"translate({float(self.node.get('x', '0'))}, {float(self.node.get('y', '0'))})")
        parent = self.node.getparent()
        assert parent is not None, "This should be part of a tree and therefore have a parent"
        transform = get_node_transform(parent) @ translate
        center = self.node.bounding_box(transform).center
        return center

    def validation_warnings(self) -> Generator[CloneWarning, Any, None]:
        source_node = self.node.href
        point = self.center(source_node)
        yield CloneWarning(point)


def is_clone(node: BaseElement) -> bool:
    if node.tag == SVG_USE_TAG and node.href is not None and not is_command_symbol(node):
        return True
    return False


def clone_with_fixup(parent: BaseElement, node: BaseElement) -> BaseElement:
    """
    Clone the node, placing the clone as a child of parent, and fix up
    references in the cloned subtree to point to elements from the clone subtree.
    """
    # A map of "#id" -> "#corresponding-id-in-the-cloned-subtree"
    id_map: Dict[str, str] = {}

    def clone_children(parent: BaseElement, node: BaseElement) -> BaseElement:
        # Copy the node without copying its children.
        cloned = copy_no_children(node)
        parent.append(cloned)
        id_map[f"#{node.get_id()}"] = f"#{cloned.get_id()}"

        for child in node:
            if not isinstance(child, _Comment) and not isinstance(child, Title):
                clone_children(cloned, child)

        return cloned

    ret = clone_children(parent, node)

    def fixup_id_attr(node: BaseElement, attr: str) -> None:
        # Replace the id value for this attrib with the corresponding one in the clone subtree, if applicable.
        val = node.get(attr)
        if val is not None:
            node.set(attr, id_map.get(val, val))

    for n in ret.iter():
        fixup_id_attr(n, CONNECTION_START)
        fixup_id_attr(n, CONNECTION_END)

    return ret

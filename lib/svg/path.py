# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import inkex

from .tags import SVG_GROUP_TAG, SVG_LINK_TAG
from .units import get_viewbox_transform


def apply_transforms(path: inkex.Path, node: inkex.BaseElement) -> inkex.Path:
    transform = get_node_transform(node)

    # apply the combined transform to this node's path
    path = path.transform(transform)

    return path


def compose_parent_transforms(node: inkex.BaseElement, mat: inkex.Transform) -> inkex.Transform:
    # This is adapted from Inkscape's simpletransform.py's composeParents()
    # function.  That one can't handle nodes that are detached from a DOM.

    trans = node.get('transform')
    if trans:
        mat = inkex.transforms.Transform(trans) @ mat
    parent = node.getparent()
    if parent is not None:
        if parent.tag in [SVG_GROUP_TAG, SVG_LINK_TAG]:
            mat = compose_parent_transforms(parent, mat)
    return mat


def get_node_transform(node: inkex.BaseElement) -> inkex.Transform:
    """
    if getattr(node, "composed_transform", None):
        return node.composed_transform()
    """

    # start with the identity transform
    transform = inkex.transforms.Transform([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])

    # this if is because sometimes inkscape likes to create paths outside of a layer?!
    if node.getparent() is not None:
        # combine this node's transform with all parent groups' transforms
        transform = compose_parent_transforms(node, transform)

    # add in the transform implied by the viewBox
    viewbox_transform = get_viewbox_transform(node.getroottree().getroot())
    transform = viewbox_transform @ transform

    return transform


def get_correction_transform(node: inkex.BaseElement, child=False) -> str:
    """Get a transform to apply to new siblings or children of this SVG node

    Arguments:
        child (boolean) -- whether the new nodes we're going to add will be
                           children of node (child=True) or siblings of node
                           (child=False)

    This allows us to add a new child node that has its path specified in
    absolute coordinates.  The correction transform will undo the effects of
    the parent's and ancestors' transforms so that absolute coordinates
    work properly.
    """

    if child:
        transform = get_node_transform(node)
    else:
        # we can ignore the transform on the node itself since it won't apply
        # to the objects we add
        parent = node.getparent()
        if parent is not None:
            transform = get_node_transform(parent)
        else:
            transform = inkex.Transform()

    # now invert it, so that we can position our objects in absolute
    # coordinates
    transform = -transform

    return str(transform)


def line_strings_to_csp(line_strings):
    try:
        # This lets us accept a MultiLineString or a list.
        line_strings = line_strings.geoms
    except AttributeError:
        pass

    if line_strings is None:
        return None

    return point_lists_to_csp(ls.coords for ls in line_strings)


def point_lists_to_csp(point_lists):
    csp = []

    for point_list in point_lists:
        subpath = []
        for point in point_list:
            # cubicsuperpath is very particular that these must be lists, not tuples
            point = list(point)
            # create a straight line as a degenerate bezier
            subpath.append([point, point, point])
        csp.append(subpath)

    return csp


def line_strings_to_path(line_strings):
    csp = line_strings_to_csp(line_strings)

    return inkex.PathElement(attrib={
        "d": str(inkex.paths.CubicSuperPath(csp))
    })

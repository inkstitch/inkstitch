import inkex
from lxml import etree

from .tags import SVG_GROUP_TAG, SVG_LINK_TAG
from .units import get_viewbox_transform


def apply_transforms(path, node):
    transform = get_node_transform(node)

    # apply the combined transform to this node's path
    path = path.transform(transform)

    return path


def compose_parent_transforms(node, mat):
    # This is adapted from Inkscape's simpletransform.py's composeParents()
    # function.  That one can't handle nodes that are detached from a DOM.

    trans = node.get('transform')
    if trans:
        mat = inkex.transforms.Transform(trans) * mat
    if node.getparent() is not None:
        if node.getparent().tag in [SVG_GROUP_TAG, SVG_LINK_TAG]:
            mat = compose_parent_transforms(node.getparent(), mat)
    return mat


def get_node_transform(node):
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
    transform = viewbox_transform * transform

    return transform


def get_correction_transform(node, child=False):
    """Get a transform to apply to new siblings or children of this SVG node"""

    # if we want to place our new nodes in the same group/layer as this node,
    # then we'll need to factor in the effects of any transforms set on
    # the parents of this node.

    if child:
        transform = get_node_transform(node)
    else:
        # we can ignore the transform on the node itself since it won't apply
        # to the objects we add
        transform = get_node_transform(node.getparent())

    # now invert it, so that we can position our objects in absolute
    # coordinates
    transform = -transform

    return str(transform)


def line_strings_to_csp(line_strings):
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

    return etree.Element("path", {
        "d": str(inkex.paths.CubicSuperPath(csp))
    })

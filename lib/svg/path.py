import simpletransform
import cubicsuperpath

from .units import get_viewbox_transform

def apply_transforms(path, node):
    transform = get_node_transform(node)

    # apply the combined transform to this node's path
    simpletransform.applyTransformToPath(transform, path)

    return path

def get_node_transform(node):
    # start with the identity transform
    transform = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]

    # combine this node's transform with all parent groups' transforms
    transform = simpletransform.composeParents(node, transform)

    # add in the transform implied by the viewBox
    viewbox_transform = get_viewbox_transform(node.getroottree().getroot())
    transform = simpletransform.composeTransform(viewbox_transform, transform)

    return transform

def get_correction_transform(node):
    """Get a transform to apply to new siblings of this SVG node"""

    # if we want to place our new nodes in the same group/layer as this node,
    # then we'll need to factor in the effects of any transforms set on
    # the parents of this node.

    # we can ignore the transform on the node itself since it won't apply
    # to the objects we add
    transform = get_node_transform(node.getparent())

    # now invert it, so that we can position our objects in absolute
    # coordinates
    transform = simpletransform.invertTransform(transform)

    return simpletransform.formatTransform(transform)

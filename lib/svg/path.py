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

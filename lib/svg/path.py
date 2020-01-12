import cubicsuperpath
import inkex
import simpletransform

from .tags import SVG_CIRCLE_TAG, SVG_ELLIPSE_TAG, SVG_RECT_TAG
from .units import get_viewbox_transform


def apply_transforms(path, node):
    transform = get_node_transform(node)

    # apply the combined transform to this node's path
    simpletransform.applyTransformToPath(transform, path)

    return path


def compose_parent_transforms(node, mat):
    # This is adapted from Inkscape's simpletransform.py's composeParents()
    # function.  That one can't handle nodes that are detached from a DOM.

    trans = node.get('transform')

    if trans:
        mat = simpletransform.composeTransform(simpletransform.parseTransform(trans), mat)
    if node.getparent() is not None:
        if node.getparent().tag == inkex.addNS('g', 'svg'):
            mat = compose_parent_transforms(node.getparent(), mat)
    return mat


def get_node_transform(node):
    # start with the identity transform
    transform = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]

    # this if is because sometimes inkscape likes to create paths outside of a layer?!
    if node.getparent() is not None:
        # combine this node's transform with all parent groups' transforms
        transform = compose_parent_transforms(node, transform)

    if node.get('id', '').startswith('clone_'):
        transform = simpletransform.parseTransform(node.get('transform', ''))

    # add in the transform implied by the viewBox
    viewbox_transform = get_viewbox_transform(node.getroottree().getroot())
    transform = simpletransform.composeTransform(viewbox_transform, transform)

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
    transform = simpletransform.invertTransform(transform)

    return simpletransform.formatTransform(transform)


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

    return inkex.etree.Element("path", {
        "d": cubicsuperpath.formatPath(csp)
    })


def get_path(node):
    d = node.get("d", "")

    if not d:
        if node.tag == SVG_RECT_TAG:
            d = rect_to_path(node)
        elif node.tag == SVG_ELLIPSE_TAG:
            d = ellipse_to_path(node)
        elif node.tag == SVG_CIRCLE_TAG:
            d = circle_to_path(node)

    return d


def rect_to_path(node):
    x = float(node.get('x', '0'))
    y = float(node.get('y', '0'))
    width = float(node.get('width', '0'))
    height = float(node.get('height', '0'))
    rx = None
    ry = None

    # rounded corners
    # the following rules apply for radius calculations:
    #   if rx or ry is missing it has to take the value of the other one
    #   the radius cannot be bigger than half of the corresponding side
    #   (otherwise we receive an invalid path)
    if node.get('rx') or node.get('ry'):
        if node.get('rx'):
            rx = float(node.get('rx', '0'))
            ry = rx
        if node.get('ry'):
            ry = float(node.get('ry', '0'))
            if not ry:
                ry = rx

        rx = min(width/2, rx)
        ry = min(height/2, ry)

        path = 'M %(startx)f,%(y)f ' \
               'h %(width)f ' \
               'q %(rx)f,0 %(rx)f,%(ry)f ' \
               'v %(height)f ' \
               'q 0,%(ry)f -%(rx)f,%(ry)f ' \
               'h -%(width)f ' \
               'q -%(rx)f,0 -%(rx)f,-%(ry)f ' \
               'v -%(height)f ' \
               'q 0,-%(ry)f %(rx)f,-%(ry)f ' \
               'Z' \
               % dict(startx=x+rx, x=x, y=y, width=width-(2*rx), height=height-(2*ry), rx=rx, ry=ry)

    else:
        path = "M %f,%f H %f V %f H %f Z" % (x, y, width+x, height+y, x)

    return path


def ellipse_to_path(node):
    rx = float(node.get('rx', "0")) or float(node.get('r', "0"))
    ry = float(node.get('ry', "0")) or float(node.get('r', "0"))
    cx = float(node.get('cx'))
    cy = float(node.get('cy'))

    path = 'M %(cxrx)f,%(cy)f ' \
           'A %(rx)f,%(ry)f 0 0 1 '\
           '%(cx)f,%(cyry)f %(rx)f,%(ry)f 0 0 1 ' \
           '%(cx_rx)f,%(cy)f %(rx)f,%(ry)f 0 0 1 ' \
           '%(cx)f,%(cy_ry)f %(rx)f,%(ry)f 0 0 1 ' \
           '%(cxrx)f,%(cy)f ' \
           'Z' \
           % dict(cxrx=cx+rx, cyry=cy+ry, cx_rx=cx-rx, cy_ry=cy-ry, rx=rx, ry=ry, cx=cx, cy=cy)

    return path


def circle_to_path(node):
    cx = float(node.get('cx'))
    cy = float(node.get('cy'))
    r = float(node.get('r'))

    path = 'M %(xstart)f,%(cy)f ' \
           'a %(r)f,%(r)f 0 0 1 '\
           '-%(r)f,%(r)f %(r)f,%(r)f 0 0 1 ' \
           '-%(r)f,-%(r)f %(r)f,%(r)f 0 0 1 ' \
           '%(r)f,-%(r)f %(r)f,%(r)f 0 0 1 ' \
           '%(r)f,%(r)f ' \
           'Z' \
           % dict(xstart=cx+r, cy=cy, r=r)

    return path

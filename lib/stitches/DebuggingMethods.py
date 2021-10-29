import matplotlib.pyplot as plt
from shapely.geometry import Polygon

from anytree import PreOrderIter

# import LineStringSampling as Sampler
import numpy as np
import matplotlib.collections as mcoll

# def offset_polygons(polys, offset,joinstyle):
#     if polys.geom_type == 'Polygon':
#         inners = polys.interiors
#         outer = polys.exterior
#         polyinners = []
#         for inner in inners:
#             inner = inner.parallel_offset(offset,'left', 5, joinstyle, 1)
#             polyinners.append(Polygon(inner))
#         outer = outer.parallel_offset(offset,'left', 5, joinstyle, 1)
#         return Polygon(outer).difference(MultiPolygon(polyinners))
#     else:
#         polyreturns = []
#         for poly in polys:
#             inners = poly.interiors
#             outer = poly.exterior
#             polyinners = []
#             for inner in inners:
#                 inner = inner.parallel_offset(offset,'left', 5, joinstyle, 1)
#                 polyinners.append(Polygon(inner))
#             outer = outer.parallel_offset(offset,'left', 5, joinstyle, 1)
#             result = Polygon(outer).difference(MultiPolygon(polyinners))
#             polyreturns.append(result)
#         return MultiPolygon(polyreturns)

# For debugging


def plot_MultiPolygon(MultiPoly, plt, colorString):
    if MultiPoly.is_empty:
        return
    if MultiPoly.geom_type == "Polygon":
        x2, y2 = MultiPoly.exterior.xy
        plt.plot(x2, y2, colorString)

        for inners in MultiPoly.interiors:
            x2, y2 = inners.coords.xy
            plt.plot(x2, y2, colorString)
    else:
        for poly in MultiPoly:
            x2, y2 = poly.exterior.xy
            plt.plot(x2, y2, colorString)

            for inners in poly.interiors:
                x2, y2 = inners.coords.xy
                plt.plot(x2, y2, colorString)


# Test whether there are areas which would currently not be stitched but should be stitched


def subtractResult(poly, rootPoly, offsetThresh):
    poly2 = Polygon(poly)
    for node in PreOrderIter(rootPoly):
        poly2 = poly2.difference(node.val.buffer(offsetThresh, 5, 3, 3))
    return poly2


# Used for debugging - plots all polygon exteriors within an AnyTree which is provided by the root node rootPoly.


def drawPoly(rootPoly, colorString):
    fig, axs = plt.subplots(1, 1)
    axs.axis("equal")
    plt.gca().invert_yaxis()
    for node in PreOrderIter(rootPoly):
        # if(node.id == "hole"):
        #    node.val = LinearRing(node.val.coords[::-1])
        print("Bounds:")
        print(node.val.bounds)
        x2, y2 = node.val.coords.xy
        plt.plot(x2, y2, colorString)
    plt.show(block=True)


def drawresult(resultcoords, resultcoords_Origin, colorString):
    fig, axs = plt.subplots(1, 1)
    axs.axis("equal")
    plt.gca().invert_yaxis()
    plt.plot(*zip(*resultcoords), colorString)

    colormap = np.array(["r", "g", "b", "c", "m", "y", "k", "gray", "m"])
    labelmap = np.array(
        [
            "MUST_USE",
            "REGULAR_SPACING",
            "INITIAL_RASTERING",
            "EDGE_NEEDED",
            "NOT_NEEDED",
            "ALREADY_TRANSFERRED",
            "ADDITIONAL_TRACKING_POINT_NOT_NEEDED",
            "EDGE_RASTERING_ALLOWED",
            "EDGE_PREVIOUSLY_SHIFTED",
        ]
    )

    for i in range(0, 8 + 1):
        # if i != Sampler.PointSource.EDGE_NEEDED and i != Sampler.PointSource.INITIAL_RASTERING:
        #    continue
        selection = []
        for j in range(len(resultcoords)):
            if i == resultcoords_Origin[j]:
                selection.append(resultcoords[j])
        if len(selection) > 0:
            plt.scatter(*zip(*selection), c=colormap[i], label=labelmap[i])

    #  plt.scatter(*zip(*resultcoords),
    #              c=colormap[resultcoords_Origin])
    axs.legend()
    plt.show(block=True)


# Just for debugging in order to draw the connected line with color gradient


def colorline(
    x,
    y,
    z=None,
    cmap=plt.get_cmap("copper"),
    norm=plt.Normalize(0.0, 1.0),
    linewidth=3,
    alpha=1.0,
):
    """
    http://nbviewer.ipython.org/github/dpsanders/matplotlib-examples/blob/master/colorline.ipynb
    http://matplotlib.org/examples/pylab_examples/multicolored_line.html
    Plot a colored line with coordinates x and y
    Optionally specify colors in the array z
    Optionally specify a colormap, a norm function and a line width
    """

    # Default colors equally spaced on [0,1]:
    if z is None:
        z = np.linspace(0.0, 1.0, len(x))

    # Special case if a single number:
    if not hasattr(z, "__iter__"):  # to check for numerical input -- this is a hack
        z = np.array([z])

    z = np.asarray(z)

    segments = make_segments(x, y)
    lc = mcoll.LineCollection(
        segments, array=z, cmap=cmap, norm=norm, linewidth=linewidth, alpha=alpha
    )

    ax = plt.gca()
    ax.add_collection(lc)

    return lc


# Used by colorline


def make_segments(x, y):
    """
    Create list of line segments from x and y coordinates, in the correct format
    for LineCollection: an array of the form numlines x (points per line) x 2 (x
    and y) array
    """
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    return segments

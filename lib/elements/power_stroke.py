from inkex import CubicSuperPath, Path

from ..svg import find_elements
from ..svg.tags import INKSCAPE_LPE, INKSCAPE_ORIGINAL_D


def get_power_stroke_path(node):
    # a power stroke is a closed path
    # for a satin column we need to open the path at the beginning and
    # split it at the center and reverse one side of the path

    original_d = Path(node.get(INKSCAPE_ORIGINAL_D)).to_superpath()
    path = node.get_path()

    if original_d[0][0] == original_d[0][-1]:
        # closed path source
        d = _get_closed_path_rails(path)
    else:
        # path with start and end
        # get start and end cap style
        # possible values: zerowidth (default), square, round, peak, butt
        lpe = _get_lpe_source(node)
        start_cap = lpe.get('start_linecap_type')
        end_cap = lpe.get('end_linecap_type')

        # make it an open path
        d = _get_power_stroke_rails(path, start_cap, end_cap)

    # add rungs from original path (if existent)
    rungs = ""
    if len(original_d) > 1:
        rungs = CubicSuperPath(original_d[1:]).to_path()

    d = Path(d + rungs).to_superpath()
    return d


def _get_power_stroke_rails(path, start_cap, end_cap):
    # make it an open path
    path = Path(path[0:-1]).to_superpath()

    # start cap
    # zerowidth and butt start_caps are good without the z which we already removed
    if start_cap == 'square':
        # move last node to the beginning
        path = [path[0][-1:] + path[0][:-1]]
    elif start_cap == 'peak':
        # copy last node to the beginning
        path = [path[0][-1:] + path[0]]
    if start_cap == 'round':
        path = [path[0][-2:] + path[0][1:-1]]

    # end cap
    rail_length = int(len(path[0]) / 2)
    if end_cap in ['zerowidth', 'peak', 'round']:
        rail1 = CubicSuperPath([path[0][:rail_length + 1]]).to_path()
        rail2 = CubicSuperPath([path[0][rail_length:]]).to_path().reverse()
    elif end_cap in ['butt', 'square']:
        rail1 = CubicSuperPath([path[0][:rail_length]]).to_path()
        rail2 = CubicSuperPath([path[0][rail_length:]]).to_path().reverse()

    # combine rails into one path
    return rail1 + rail2


def _get_closed_path_rails(path):
    path = path.to_superpath()
    rail1 = CubicSuperPath(path[0][:-1]).to_path()
    rail2 = CubicSuperPath(path[1][:-1]).to_path().reverse()
    return rail1 + rail2


def is_power_stroke(node):
    lpe_source = _get_lpe_source(node)
    if lpe_source is not None and lpe_source.get('effect') == 'powerstroke':
        return True
    return False


def _get_lpe_source(node):
    lpe = node.get(INKSCAPE_LPE, None)
    if lpe is not None:
        return find_elements(node, ".//*[@id='%s']" % lpe[1:])[0]
    return None

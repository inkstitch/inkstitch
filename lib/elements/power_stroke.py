from inkex import CubicSuperPath, Path

from ..svg import find_elements
from ..svg.tags import INKSCAPE_LPE, INKSCAPE_ORIGINAL_D


def get_power_stroke_path(node):
    # a power stroke is a closed path
    # for a satin column we need to open the path at the beginning and
    # split it at the center

    # get start and end cap style
    # possible values: zerowidth (default), square, round, peak, butt
    lpe = get_lpe_source(node)
    start_cap = lpe.get('start_linecap_type')
    end_cap = lpe.get('end_linecap_type')

    # make it an open path
    d = get_power_stroke_rails(node.get_path(), start_cap, end_cap)

    # add rungs from original path (if existent)
    rungs = ""
    original_d = node.get(INKSCAPE_ORIGINAL_D)
    if original_d.lower().count('m') > 1:
        rungs = original_d[original_d.lower().find("m", 1):].rstrip()

    d = Path(d + rungs).to_superpath()
    return d


def get_power_stroke_rails(path, start_cap, end_cap):
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
    elif end_cap in ['square', 'butt']:
        rail1 = CubicSuperPath([path[0][:rail_length - 1]]).to_path()
        rail2 = CubicSuperPath([path[0][rail_length - 1:]]).to_path().reverse()

    # combine rails into one path
    path = str(rail1) + str(rail2)
    return path


def is_power_stroke(node):
    lpe_source = get_lpe_source(node)
    if lpe_source is not None and lpe_source.get('effect') == 'powerstroke':
        return True
    return False


def get_lpe_source(node):
    lpe = node.get(INKSCAPE_LPE, None)
    if lpe is not None:
        return find_elements(node, ".//*[@id='%s']" % lpe[1:])[0]
    return None

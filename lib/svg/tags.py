import inkex


SVG_PATH_TAG = inkex.addNS('path', 'svg')
SVG_POLYLINE_TAG = inkex.addNS('polyline', 'svg')
SVG_DEFS_TAG = inkex.addNS('defs', 'svg')
SVG_GROUP_TAG = inkex.addNS('g', 'svg')

INKSCAPE_LABEL = inkex.addNS('label', 'inkscape')
INKSCAPE_GROUPMODE = inkex.addNS('groupmode', 'inkscape')

EMBROIDERABLE_TAGS = (SVG_PATH_TAG, SVG_POLYLINE_TAG)

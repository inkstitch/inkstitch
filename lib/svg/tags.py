import inkex


# This is used below and added to the document in ../extensions/base.py.
inkex.NSS['inkstitch'] = 'http://inkstitch.org/namespace'


SVG_PATH_TAG = inkex.addNS('path', 'svg')
SVG_POLYLINE_TAG = inkex.addNS('polyline', 'svg')
SVG_TEXT_TAG = inkex.addNS('text', 'svg')
SVG_TSPAN_TAG = inkex.addNS('tspan', 'svg')
SVG_DEFS_TAG = inkex.addNS('defs', 'svg')
SVG_GROUP_TAG = inkex.addNS('g', 'svg')
SVG_SYMBOL_TAG = inkex.addNS('symbol', 'svg')
SVG_USE_TAG = inkex.addNS('use', 'svg')

EMBROIDERABLE_TAGS = (SVG_PATH_TAG, SVG_POLYLINE_TAG)

INKSCAPE_LABEL = inkex.addNS('label', 'inkscape')
INKSCAPE_GROUPMODE = inkex.addNS('groupmode', 'inkscape')
CONNECTION_START = inkex.addNS('connection-start', 'inkscape')
CONNECTION_END = inkex.addNS('connection-end', 'inkscape')
CONNECTOR_TYPE = inkex.addNS('connector-type', 'inkscape')

XLINK_HREF = inkex.addNS('href', 'xlink')

SODIPODI_NAMEDVIEW = inkex.addNS('namedview', 'sodipodi')
SODIPODI_GUIDE = inkex.addNS('guide', 'sodipodi')
SODIPODI_ROLE = inkex.addNS('role', 'sodipodi')

INKSTITCH_LETTERING = inkex.addNS('lettering', 'inkstitch')

INKSTITCH_ATTRIBS = {}
# Fill
inkstitch_attribs = [
                'ties',
                'trim_after',
                'stop_after',
                # fill
                'angle',
                'auto_fill',
                'expand_mm',
                'fill_underlay',
                'fill_underlay_angle',
                'fill_underlay_inset_mm',
                'fill_underlay_max_stitch_length_mm',
                'fill_underlay_row_spacing_mm',
                'fill_underlay_skip_last',
                'max_stitch_length_mm',
                'row_spacing_mm',
                'end_row_spacing_mm',
                'skip_last',
                'staggers',
                'underlay_underpath',
                'underpath',
                'flip',
                'expand_mm',
                # stroke
                'manual_stitch',
                'bean_stitch_repeats',
                'repeats',
                'running_stitch_length_mm',
                # satin column
                'satin_column',
                'satin_column',
                'running_stitch_length_mm',
                'center_walk_underlay',
                'center_walk_underlay_stitch_length_mm',
                'contour_underlay',
                'contour_underlay_stitch_length_mm',
                'contour_underlay_inset_mm',
                'zigzag_underlay',
                'zigzag_spacing_mm',
                'zigzag_underlay_inset_mm',
                'zigzag_underlay_spacing_mm',
                'e_stitch',
                'pull_compensation_mm',
                'stroke_first',
                # Legacy
                'embroider_trim_after',
                'embroider_stop_after'
                ]
for attrib in inkstitch_attribs:
    INKSTITCH_ATTRIBS[attrib] = inkex.addNS(attrib, 'inkstitch')

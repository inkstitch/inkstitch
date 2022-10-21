# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from lxml import etree

import inkex

etree.register_namespace("inkstitch", "http://inkstitch.org/namespace")
inkex.NSS['inkstitch'] = 'http://inkstitch.org/namespace'

SVG_PATH_TAG = inkex.addNS('path', 'svg')
SVG_POLYLINE_TAG = inkex.addNS('polyline', 'svg')
SVG_POLYGON_TAG = inkex.addNS('polygon', 'svg')
SVG_RECT_TAG = inkex.addNS('rect', 'svg')
SVG_ELLIPSE_TAG = inkex.addNS('ellipse', 'svg')
SVG_CIRCLE_TAG = inkex.addNS('circle', 'svg')
SVG_TEXT_TAG = inkex.addNS('text', 'svg')
SVG_TSPAN_TAG = inkex.addNS('tspan', 'svg')
SVG_DEFS_TAG = inkex.addNS('defs', 'svg')
SVG_GROUP_TAG = inkex.addNS('g', 'svg')
SVG_LINK_TAG = inkex.addNS('a', 'svg')
SVG_SYMBOL_TAG = inkex.addNS('symbol', 'svg')
SVG_USE_TAG = inkex.addNS('use', 'svg')
SVG_IMAGE_TAG = inkex.addNS('image', 'svg')
SVG_CLIPPATH_TAG = inkex.addNS('clipPath', 'svg')
SVG_MASK_TAG = inkex.addNS('mask', 'svg')

INKSCAPE_LABEL = inkex.addNS('label', 'inkscape')
INKSCAPE_GROUPMODE = inkex.addNS('groupmode', 'inkscape')
CONNECTION_START = inkex.addNS('connection-start', 'inkscape')
CONNECTION_END = inkex.addNS('connection-end', 'inkscape')
CONNECTOR_TYPE = inkex.addNS('connector-type', 'inkscape')
INKSCAPE_DOCUMENT_UNITS = inkex.addNS('document-units', 'inkscape')

XLINK_HREF = inkex.addNS('href', 'xlink')

SODIPODI_NAMEDVIEW = inkex.addNS('namedview', 'sodipodi')
SODIPODI_GUIDE = inkex.addNS('guide', 'sodipodi')
SODIPODI_ROLE = inkex.addNS('role', 'sodipodi')

INKSTITCH_LETTERING = inkex.addNS('lettering', 'inkstitch')

EMBROIDERABLE_TAGS = (SVG_PATH_TAG, SVG_POLYLINE_TAG, SVG_POLYGON_TAG,
                      SVG_RECT_TAG, SVG_ELLIPSE_TAG, SVG_CIRCLE_TAG)
NOT_EMBROIDERABLE_TAGS = (SVG_IMAGE_TAG, SVG_TEXT_TAG)
SVG_OBJECT_TAGS = (SVG_ELLIPSE_TAG, SVG_CIRCLE_TAG, SVG_RECT_TAG)

INKSTITCH_ATTRIBS = {}
inkstitch_attribs = [
    'ties',
    'force_lock_stitches',
    # clone
    'clone',
    # polyline
    'polyline',
    # fill
    'angle',
    'auto_fill',
    'fill_method',
    'contour_strategy',
    'guided_fill_strategy',
    'join_style',
    'avoid_self_crossing',
    'clockwise',
    'reverse',
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
    'random_feathering_in',
    'random_feathering_out',
    'random_stitch_length_increase',
    'random_stitch_length_decrease',
    'random_angle',
    'underlay_underpath',
    'random_underlay_feathering_in',
    'random_underlay_feathering_out',
    'random_row_spacing',
    'underpath',
    'flip',
    'expand_mm',
    # stroke
    'stroke_method',
    'bean_stitch_repeats',
    'repeats',
    'running_stitch_length_mm',
    'running_stitch_tolerance_mm',
    # ripples
    'line_count',
    'exponent',
    'flip_exponent',
    'skip_start',
    'skip_end',
    'scale_axis',
    'scale_start',
    'scale_end',
    'rotate_ripples',
    'grid_size',
    # satin column
    'satin_column',
    'short_stitch_distance_mm',
    'short_stitch_inset',
    'running_stitch_length_mm',
    'center_walk_underlay',
    'center_walk_underlay_stitch_length_mm',
    'center_walk_underlay_repeats',
    'contour_underlay',
    'contour_underlay_stitch_length_mm',
    'contour_underlay_inset_mm',
    'zigzag_underlay',
    'zigzag_spacing_mm',
    'zigzag_underlay_inset_mm',
    'zigzag_underlay_spacing_mm',
    'zigzag_underlay_max_stitch_length_mm',
    'e_stitch',
    'pull_compensation_mm',
    'pull_compensation_percent',
    'pull_compensation_rails',
    'stroke_first',
    'random_split_factor',
    'random_first_rail_factor_in',
    'random_first_rail_factor_out',
    'random_second_rail_factor_in',
    'random_second_rail_factor_out',
    'random_zigzag_spacing',
    'use_seed',
    # stitch_plan
    'invisible_layers',
    # Legacy
    'trim_after',
    'stop_after',
    'manual_stitch',
]
for attrib in inkstitch_attribs:
    INKSTITCH_ATTRIBS[attrib] = inkex.addNS(attrib, 'inkstitch')

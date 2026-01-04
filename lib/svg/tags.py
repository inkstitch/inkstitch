# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import inkex
from lxml import etree

etree.register_namespace("inkstitch", "http://inkstitch.org/namespace")
inkex.NSS['inkstitch'] = 'http://inkstitch.org/namespace'

SVG_PATH_TAG = inkex.addNS('path', 'svg')
SVG_LINE_TAG = inkex.addNS('line', 'svg')
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

SVG_METADATA_TAG = inkex.addNS("metadata", "svg")
INKSCAPE_LABEL = inkex.addNS('label', 'inkscape')
INKSCAPE_GROUPMODE = inkex.addNS('groupmode', 'inkscape')
CONNECTION_START = inkex.addNS('connection-start', 'inkscape')
CONNECTION_END = inkex.addNS('connection-end', 'inkscape')
CONNECTOR_TYPE = inkex.addNS('connector-type', 'inkscape')
INKSCAPE_DOCUMENT_UNITS = inkex.addNS('document-units', 'inkscape')
ORIGINAL_D = inkex.addNS('original-d', 'inkscape')
PATH_EFFECT = inkex.addNS('path-effect', 'inkscape')

XLINK_HREF = inkex.addNS('href', 'xlink')

SODIPODI_NAMEDVIEW = inkex.addNS('namedview', 'sodipodi')
SODIPODI_GUIDE = inkex.addNS('guide', 'sodipodi')
SODIPODI_ROLE = inkex.addNS('role', 'sodipodi')
SODIPODI_INSENSITIVE = inkex.addNS('insensitive', 'sodipodi')
SODIPODI_NODETYPES = inkex.addNS('nodetypes', 'sodipodi')

INKSTITCH_LETTERING = inkex.addNS('lettering', 'inkstitch')
INKSTITCH_TARTAN = inkex.addNS('tartan', 'inkstitch')

EMBROIDERABLE_TAGS = (SVG_PATH_TAG, SVG_LINE_TAG, SVG_POLYLINE_TAG, SVG_POLYGON_TAG,
                      SVG_RECT_TAG, SVG_ELLIPSE_TAG, SVG_CIRCLE_TAG)
NOT_EMBROIDERABLE_TAGS = (SVG_IMAGE_TAG, SVG_TEXT_TAG)
SVG_OBJECT_TAGS = (SVG_ELLIPSE_TAG, SVG_CIRCLE_TAG, SVG_RECT_TAG)

INKSTITCH_ATTRIBS = {}
inkstitch_attribs = [
    'min_stitch_length_mm',
    'min_jump_stitch_length_mm',
    'ties',
    'force_lock_stitches',
    'lock_start',
    'lock_start_scale_mm',
    'lock_start_scale_percent',
    'lock_custom_start',
    'lock_end',
    'lock_end_scale_mm',
    'lock_end_scale_percent',
    'lock_custom_end',
    # clone
    'clone',
    'flip_angle',
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
    'smoothness_mm',
    'clockwise',
    'reverse',
    'meander_pattern',
    'meander_scale_percent',
    'meander_angle',
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
    'stop_at_ending_point',
    'flip',
    'clip',
    'rows_per_thread',
    'herringbone_width_mm',
    'tartan_angle',
    'enable_random_stitch_length',
    'random_stitch_length_jitter_percent',
    'gap_fill_rows',
    # cross stitch
    'pattern_size_mm',
    'fill_coverage',
    'cross_stitch_method',
    'max_cross_stitch_length_mm',
    'cross_offset_mm',
    'cross_thread_count',
    'canvas_grid_origin',
    # stroke
    'stroke_method',
    'bean_stitch_repeats',
    'repeats',
    'running_stitch_length_mm',
    'running_stitch_tolerance_mm',
    'cutwork_needle',
    'zigzag_width_mm',
    # ripples
    'manual_pattern_placement',
    'flip_copies',
    'line_count',
    'min_line_dist_mm',
    'satin_guide_pattern_position',
    'exponent',
    'flip_exponent',
    'skip_start',
    'skip_end',
    'scale_axis',
    'scale_start',
    'scale_end',
    'rotate_ripples',
    'grid_size_mm',
    'grid_first',
    # satin column
    'satin_column',
    'satin_method',
    'short_stitch_distance_mm',
    'short_stitch_inset',
    'reverse_rails',
    'swap_satin_rails',
    'center_walk_underlay',
    'center_walk_underlay_stitch_length_mm',
    'center_walk_underlay_stitch_tolerance_mm',
    'center_walk_underlay_repeats',
    'center_walk_underlay_position',
    'contour_underlay',
    'contour_underlay_stitch_length_mm',
    'contour_underlay_stitch_tolerance_mm',
    'contour_underlay_inset_mm',
    'contour_underlay_inset_percent',
    'zigzag_underlay',
    'zigzag_spacing_mm',
    'zigzag_underlay_inset_mm',
    'zigzag_underlay_inset_percent',
    'zigzag_underlay_spacing_mm',
    'zigzag_underlay_max_stitch_length_mm',
    'e_stitch',
    'stroke_pull_compensation_mm',
    'zigzag_angle',
    'pull_compensation_mm',
    'pull_compensation_percent',
    'stroke_first',
    'random_width_decrease_percent',
    'random_width_increase_percent',
    'random_zigzag_spacing_percent',
    'split_method',
    'split_staggers',
    'random_split_phase',
    'random_split_jitter_percent',
    'min_random_split_length_mm',
    'running_stitch_position',
    'start_at_nearest_point',
    'end_at_nearest_point',
    # stitch_plan
    'invisible_layers',
    'layer_visibility',
    # All elements
    'trim_after',
    'stop_after',
    'random_seed',
    'manual_stitch',
    # legacy
    'grid_size',
    # sew stack
    'sew_stack_only',
    'sew_stack'
]
for attrib in inkstitch_attribs:
    INKSTITCH_ATTRIBS[attrib] = inkex.addNS(attrib, 'inkstitch')

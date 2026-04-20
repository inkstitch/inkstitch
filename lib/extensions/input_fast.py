# Fast Input path for embroidery file import.
# Uses only lxml + pystitch (no inkex) to minimize import time.
# Produces SVG compatible with what the full Input path generates.

import math
import os
import sys
from copy import deepcopy
from html import escape
from random import random

from lxml import etree

import pystitch

# Namespace map matching inkex.NSS (None = default namespace for SVG)
_NSS = {
    None: 'http://www.w3.org/2000/svg',
    'svg': 'http://www.w3.org/2000/svg',
    'inkscape': 'http://www.inkscape.org/namespaces/inkscape',
    'sodipodi': 'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd',
    'xlink': 'http://www.w3.org/1999/xlink',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'cc': 'http://creativecommons.org/ns#',
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'xml': 'http://www.w3.org/XML/1998/namespace',
    'inkstitch': 'inkstitch',
}

_SVG_NS = _NSS['svg']
_INKSCAPE_NS = _NSS['inkscape']
_INKSTITCH_NS = _NSS['inkstitch']

_INKSCAPE_LABEL = '{%s}label' % _INKSCAPE_NS
_INKSCAPE_GROUPMODE = '{%s}groupmode' % _INKSCAPE_NS
_INKSTITCH_STROKE_METHOD = '{%s}stroke_method' % _INKSTITCH_NS
_INKSTITCH_TRIM_AFTER = '{%s}trim_after' % _INKSTITCH_NS
_INKSTITCH_STOP_AFTER = '{%s}stop_after' % _INKSTITCH_NS
_INKSTITCH_SVG_VERSION_TAG = '{%s}inkstitch_svg_version' % _INKSTITCH_NS
_XLINK_HREF = '{%s}href' % _NSS['xlink']
_INKSCAPE_CONNECTOR_TYPE = '{%s}connector-type' % _INKSCAPE_NS
_INKSCAPE_CONNECTION_START = '{%s}connection-start' % _INKSCAPE_NS
_INKSCAPE_CONNECTION_END = '{%s}connection-end' % _INKSCAPE_NS

PIXELS_PER_MM = 96 / 25.4
INKSTITCH_SVG_VERSION = 3


def _svg_tag(local):
    return '{%s}%s' % (_SVG_NS, local)


def _load_command_symbols(extension_dir):
    """Load trim and stop symbol definitions from inkstitch.svg."""
    symbols_file = os.path.join(extension_dir, 'symbols', 'inkstitch.svg')
    if not os.path.isfile(symbols_file):
        return {}
    try:
        tree = etree.parse(symbols_file)
        root = tree.getroot()
        symbols = {}
        for cmd in ('trim', 'stop'):
            sym_id = 'inkstitch_%s' % cmd
            found = root.xpath('//*[@id="%s"]' % sym_id)
            if found:
                sym = deepcopy(found[0])
                sym.set('transform', 'scale(0.25)')
                sym.set('style', 'opacity: 0.7')
                symbols[cmd] = sym
        return symbols
    except Exception:
        return {}


def _add_visual_command(parent, path_el, points, command, cmd_counter):
    """Add visual command marker (symbol + connector) after a path element."""
    try:
        prev_x, prev_y, last_x, last_y = points
        dx = last_x - prev_x
        dy = last_y - prev_y
        length = math.sqrt(dx * dx + dy * dy) or 1.0
        distance = 10
        perp_x = -dy / length * distance
        perp_y = dx / length * distance
        jitter = random() * 0.05 * distance
        pos_x = last_x + perp_x + jitter
        pos_y = last_y + perp_y + jitter
        centroid_x = (prev_x + last_x) / 2
        centroid_y = (prev_y + last_y) / 2

        cmd_desc = 'Trim thread' if command == 'trim' else 'Stop (pause machine)'
        gid = 'command_group_%d' % cmd_counter[0]
        uid = 'command_use_%d' % cmd_counter[0]
        cid = 'command_connector_%d' % cmd_counter[0]
        cmd_counter[0] += 1

        idx = list(parent).index(path_el)
        group = etree.Element(_svg_tag('g'), attrib={
            'id': gid,
            _INKSCAPE_LABEL: 'Ink/Stitch Command: %s' % cmd_desc,
        })
        parent.insert(idx + 1, group)

        path_id = path_el.get('id', '')
        etree.SubElement(group, _svg_tag('path'), attrib={
            'id': cid,
            'd': 'M %g,%g %g,%g' % (pos_x, pos_y, centroid_x, centroid_y),
            'style': 'fill:none;stroke:#000000;stroke-width:1;stroke-opacity:0.5;vector-effect:non-scaling-stroke;',
            _INKSCAPE_CONNECTION_START: '#%s' % uid,
            _INKSCAPE_CONNECTION_END: '#%s' % path_id,
            _INKSCAPE_LABEL: 'connector',
            _INKSCAPE_CONNECTOR_TYPE: 'polyline',
        })

        etree.SubElement(group, _svg_tag('use'), attrib={
            'id': uid,
            _XLINK_HREF: '#inkstitch_%s' % command,
            'height': '100%',
            'width': '100%',
            'x': str(pos_x),
            'y': str(pos_y),
            _INKSCAPE_LABEL: 'command marker',
        })
    except Exception:
        pass  # Non-fatal: design still loads without visual markers


def run_fast_input(embroidery_file):
    """Read an embroidery file and print SVG to stdout. No inkex needed."""

    if not os.path.isfile(embroidery_file):
        sys.stderr.write('File does not exist: %s\n' % embroidery_file)
        sys.exit(1)

    if embroidery_file.endswith(('edr', 'col', 'inf')):
        sys.stderr.write('Cannot import color formats directly.\n')
        sys.exit(0)

    pattern = pystitch.read(embroidery_file)
    if pattern is None:
        sys.stderr.write('Failed to read embroidery file: %s\n' % embroidery_file)
        sys.exit(1)
    scale = PIXELS_PER_MM / 10.0

    STITCH_CMD = pystitch.STITCH
    TRIM_CMD = pystitch.TRIM
    STOP_CMD = pystitch.STOP
    JUMP_CMD = pystitch.JUMP
    SEQUIN_EJECT_CMD = pystitch.SEQUIN_EJECT

    # Build color blocks: list of (hex_color, segments, trim_after, stop_after)
    # Each segment: (d_string, prev_sx, prev_sy, last_sx, last_sy, preceding_break)
    # preceding_break: None | TRIM_CMD | STOP_CMD | JUMP_CMD
    color_blocks = []
    max_x = 0.0
    max_y = 0.0

    for raw_stitches, thread in pattern.get_as_colorblocks():
        hex_color = thread.hex_color()
        segments = []
        coords = []
        trim_after = False
        stop_after = False
        last_cmd = None
        pending_break = None
        prev_sx = prev_sy = 0.0
        last_sx = last_sy = 0.0

        for x, y, command in raw_stitches:
            if command == STITCH_CMD or command == SEQUIN_EJECT_CMD:
                sx = x * scale
                sy = y * scale
                if abs(sx) > max_x:
                    max_x = abs(sx)
                if abs(sy) > max_y:
                    max_y = abs(sy)
                prev_sx, prev_sy = last_sx, last_sy
                last_sx, last_sy = sx, sy
                coords.append('%g %g' % (sx, sy))
                last_cmd = None
            elif command == TRIM_CMD:
                if len(coords) > 1:
                    segments.append(('M' + ' '.join(coords), prev_sx, prev_sy, last_sx, last_sy, pending_break))
                coords = []
                pending_break = TRIM_CMD
                last_cmd = TRIM_CMD
            elif command == STOP_CMD:
                if len(coords) > 1:
                    segments.append(('M' + ' '.join(coords), prev_sx, prev_sy, last_sx, last_sy, pending_break))
                coords = []
                pending_break = STOP_CMD
                last_cmd = STOP_CMD
            elif command == JUMP_CMD:
                if len(coords) > 1:
                    segments.append(('M' + ' '.join(coords), prev_sx, prev_sy, last_sx, last_sy, pending_break))
                    pending_break = JUMP_CMD
                elif pending_break not in (TRIM_CMD, STOP_CMD):
                    pending_break = JUMP_CMD
                coords = []

        if len(coords) > 1:
            segments.append(('M' + ' '.join(coords), prev_sx, prev_sy, last_sx, last_sy, pending_break))

        # Check if last stitch was trim/stop
        if last_cmd == TRIM_CMD:
            trim_after = True
        elif last_cmd == STOP_CMD:
            stop_after = True

        if segments:
            color_blocks.append((hex_color, segments, trim_after, stop_after))

    # Remove trailing stop from last block (redundant)
    if color_blocks and color_blocks[-1][3]:
        hc, segs, ta, sa = color_blocks[-1]
        color_blocks[-1] = (hc, segs, ta, False)

    # Load command symbols for visual rendering on canvas
    ext_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    symbols = _load_command_symbols(ext_dir)

    # Build SVG
    extents_x = max_x + 10
    extents_y = max_y + 10
    w = str(extents_x * 2)
    h = str(extents_y * 2)

    svg = etree.Element(_svg_tag('svg'), nsmap=_NSS, attrib={
        'width': w,
        'height': h,
        'viewBox': '0 0 %s %s' % (w, h),
    })

    # Add metadata with inkstitch_svg_version
    metadata = etree.SubElement(svg, _svg_tag('metadata'))
    rdf_rdf = etree.SubElement(metadata, '{%s}RDF' % _NSS['rdf'])
    etree.SubElement(rdf_rdf, '{%s}Work' % _NSS['cc'])
    ver_el = etree.SubElement(metadata, _INKSTITCH_SVG_VERSION_TAG)
    ver_el.text = str(INKSTITCH_SVG_VERSION)

    # Add symbol definitions to defs for visual command markers
    if symbols:
        defs = etree.SubElement(svg, _svg_tag('defs'))
        for sym in symbols.values():
            defs.append(sym)

    # Create stitch plan layer
    layer = etree.SubElement(svg, _svg_tag('g'), attrib={
        _INKSCAPE_LABEL: escape(os.path.basename(embroidery_file)),
        _INKSCAPE_GROUPMODE: 'layer',
        'transform': 'translate(%s,%s)' % (extents_x, extents_y),
    })

    obj_id = 0
    cmd_id = [0]
    line_width = 0.4

    for i, (hex_color, segments, trim_after, stop_after) in enumerate(color_blocks):
        group = etree.SubElement(layer, _svg_tag('g'), attrib={
            'id': '__color_block_%d__' % i,
            _INKSCAPE_LABEL: 'color block %d' % (i + 1),
        })

        style = 'stroke: %s; stroke-width: %s; fill: none;stroke-linejoin: round;stroke-linecap: round;' % (hex_color, line_width)

        prev_path_el = None
        prev_seg_points = None
        for j, (d_string, s_px, s_py, s_lx, s_ly, brk) in enumerate(segments):
            # Add command marker between segments
            if j > 0 and prev_path_el is not None and prev_seg_points:
                if brk == TRIM_CMD:
                    prev_path_el.set(_INKSTITCH_TRIM_AFTER, 'true')
                    if symbols:
                        _add_visual_command(group, prev_path_el, prev_seg_points, 'trim', cmd_id)
                elif brk == STOP_CMD:
                    prev_path_el.set(_INKSTITCH_STOP_AFTER, 'true')
                    if symbols:
                        _add_visual_command(group, prev_path_el, prev_seg_points, 'stop', cmd_id)
                # JUMP_CMD → no marker, just separate paths

            path_el = etree.SubElement(group, _svg_tag('path'), attrib={
                'id': 'object%d' % obj_id,
                'style': style,
                'd': d_string,
                'transform': '',
                _INKSTITCH_STROKE_METHOD: 'manual_stitch',
            })
            obj_id += 1
            prev_path_el = path_el
            prev_seg_points = (s_px, s_py, s_lx, s_ly)

        if segments and prev_path_el is not None:
            if trim_after:
                prev_path_el.set(_INKSTITCH_TRIM_AFTER, 'true')
                if symbols:
                    _add_visual_command(group, prev_path_el, prev_seg_points, 'trim', cmd_id)
            if stop_after:
                prev_path_el.set(_INKSTITCH_STOP_AFTER, 'true')
                if symbols:
                    _add_visual_command(group, prev_path_el, prev_seg_points, 'stop', cmd_id)

    out = etree.tostring(svg).decode('utf-8')
    print(out)

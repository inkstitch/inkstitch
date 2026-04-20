# Fast Output path for embroidery file export.
# Uses only lxml + pystitch (no inkex) to minimize startup time.
# Only works for SVGs where ALL paths use manual_stitch (re-export of imported files).

import os
import sys
import tempfile
import re

from lxml import etree

import pystitch

PIXELS_PER_MM = 96 / 25.4

_SVG_NS = 'http://www.w3.org/2000/svg'
_INKSTITCH_NS = 'inkstitch'
_INKSCAPE_NS = 'http://www.inkscape.org/namespaces/inkscape'

_NSMAP = {
    'svg': _SVG_NS,
    'inkstitch': _INKSTITCH_NS,
    'inkscape': _INKSCAPE_NS,
}

_STROKE_METHOD_ATTR = '{%s}stroke_method' % _INKSTITCH_NS
_TRIM_AFTER_ATTR = '{%s}trim_after' % _INKSTITCH_NS
_STOP_AFTER_ATTR = '{%s}stop_after' % _INKSTITCH_NS

# Pre-compiled regex for extracting stroke color from style attribute
_COLOR_RE = re.compile(r'stroke:\s*(#[0-9a-fA-F]{6})')

# Inverse scale: convert SVG pixels back to raw pystitch coordinates (tenths of mm)
_INV_SCALE = 10.0 / PIXELS_PER_MM


def _parse_color(style):
    """Extract stroke hex color from CSS style string."""
    m = _COLOR_RE.search(style or '')
    return m.group(1) if m else '#000000'


def _parse_d_fast(d_string):
    """Parse SVG path 'd' attribute into list of (x, y) float tuples.

    Handles format: "Mx1 y1 x2 y2 ... Mx3 y3 x4 y4 ..."
    Returns list of segments, each segment is a list of (x, y) tuples.
    """
    segments = []
    for part in d_string.split('M'):
        part = part.strip()
        if not part:
            continue
        nums = part.split()
        n = len(nums)
        if n < 2:
            continue
        seg = []
        i = 0
        while i < n - 1:
            seg.append((float(nums[i]), float(nums[i + 1])))
            i += 2
        if seg:
            segments.append(seg)
    return segments


def run_fast_output(file_extension, settings_dict, svg_data):
    """Fast output for SVGs with only manual_stitch paths.

    Args:
        file_extension: Target format (e.g. 'dst', 'pes', 'jef')
        settings_dict: Additional write settings from command line
        svg_data: Raw SVG bytes (already read from stdin)

    Returns True on success, False to fall back to normal path.
    """
    # Quick byte-level check
    if b'manual_stitch' not in svg_data:
        return False

    try:
        root = etree.fromstring(svg_data)
    except Exception:
        return False

    # Verify ALL stitch paths are manual_stitch (skip command connector paths and defs)
    all_paths = root.xpath(
        './/svg:g[@inkscape:groupmode="layer"]//svg:path', namespaces=_NSMAP)
    if not all_paths:
        return False
    _connector_label = '{%s}label' % _INKSCAPE_NS
    has_manual_stitch = False
    for p in all_paths:
        if p.get(_STROKE_METHOD_ATTR) == 'manual_stitch':
            has_manual_stitch = True
        elif p.get(_connector_label) == 'connector':
            continue  # Skip command connector paths
        else:
            return False
    if not has_manual_stitch:
        return False

    # Find layer groups
    layers = root.xpath(
        './/svg:g[@inkscape:groupmode="layer"]', namespaces=_NSMAP)
    if not layers:
        return False

    NEEDLE_AT = pystitch.NEEDLE_AT
    TRIM = pystitch.TRIM
    STOP = pystitch.STOP
    COLOR_CHANGE = pystitch.COLOR_CHANGE

    pattern = pystitch.EmbPattern()
    _stitches = pattern.stitches
    _append = _stitches.append
    inv = _INV_SCALE

    last_x = 0.0
    last_y = 0.0
    num_color_blocks = 0

    for layer in layers:
        color_groups = layer.xpath('svg:g', namespaces=_NSMAP)
        if not color_groups:
            continue

        total_groups = len(color_groups)

        for gi, group in enumerate(color_groups):
            paths = group.xpath('svg:path', namespaces=_NSMAP)
            if not paths:
                continue

            # Get color from first path
            hex_color = _parse_color(paths[0].get('style', ''))
            thread = pystitch.EmbThread()
            thread.set(hex_color)
            pattern.add_thread(thread)
            num_color_blocks += 1

            for path in paths:
                d = path.get('d', '')
                if not d:
                    continue

                trim_after = path.get(_TRIM_AFTER_ATTR) == 'true'
                stop_after = path.get(_STOP_AFTER_ATTR) == 'true'

                segments = _parse_d_fast(d)
                for seg in segments:
                    for px, py in seg:
                        raw_x = px * inv
                        raw_y = py * inv
                        _append([raw_x, raw_y, NEEDLE_AT])
                        last_x, last_y = raw_x, raw_y

                if trim_after:
                    _append([last_x, last_y, TRIM])
                if stop_after:
                    _append([last_x, last_y, STOP])

            # Color change between groups (except last)
            if gi < total_groups - 1:
                _append([last_x, last_y, COLOR_CHANGE])

    if not _stitches:
        return False

    _append([last_x, last_y, pystitch.END])

    # Write to temp file
    temp_file = tempfile.NamedTemporaryFile(
        suffix='.%s' % file_extension, delete=False)
    temp_file.close()

    write_settings = {
        'full_jump': True,
        'trims': True,
    }

    if file_extension not in ('col', 'edr', 'inf'):
        write_settings['encode'] = True

    # Merge user settings but don't allow scale/translate
    # (our coordinates are already in raw format)
    for k, v in settings_dict.items():
        if k not in ('scale', 'translate', 'format'):
            write_settings[k] = v

    try:
        pystitch.write(pattern, temp_file.name, write_settings)

        if sys.platform == 'win32':
            import msvcrt
            msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

        with open(temp_file.name, 'rb') as f:
            sys.stdout.buffer.write(f.read())
            sys.stdout.flush()
    finally:
        try:
            os.unlink(temp_file.name)
        except OSError:
            pass

    return True

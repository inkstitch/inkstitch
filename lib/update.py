from inkex import errormsg

from .elements import EmbroideryElement
from .i18n import _
from .metadata import InkStitchMetadata
from .svg import PIXELS_PER_MM
from .svg.tags import EMBROIDERABLE_TAGS, INKSTITCH_ATTRIBS

INKSTITCH_SVG_VERSION = 2


def update_inkstitch_document(svg, selection=None):
    document = svg.getroot()
    # get the inkstitch svg version from the document
    search_string = "//*[local-name()='inkstitch_svg_version']//text()"
    file_version = document.findone(search_string)
    try:
        file_version = int(file_version)
    except (TypeError, ValueError):
        file_version = 0

    if file_version == INKSTITCH_SVG_VERSION:
        return

    if file_version > INKSTITCH_SVG_VERSION:
        errormsg(_("This document was created with a newer Version of Ink/Stitch. "
                   "It is possible that not everything works as expected.\n\n"
                   "Please update your Ink/Stitch version: https://inkstitch.org/docs/install/"))
        # they may not want to be bothered with this info everytime they call an inkstitch extension
        # let's udowngrade the file version number
        _update_inkstitch_svg_version(svg)
    else:
        # this document is either a new document or it is outdated
        # if we cannot find any inkstitch attribute in the document, we assume that this is a new document which doesn't need to be updated
        search_string = "//*[namespace-uri()='http://inkstitch.org/namespace' or " \
                        "@*[namespace-uri()='http://inkstitch.org/namespace'] or " \
                        "@*[starts-with(name(), 'embroider_')]]"
        inkstitch_element = document.findone(search_string)
        if inkstitch_element is None:
            _update_inkstitch_svg_version(svg)
            return

        # update elements
        if selection:
            # this comes from the updater extension where we only update selected elements
            for element in selection:
                update_legacy_params(EmbroideryElement(element), file_version, INKSTITCH_SVG_VERSION)
        else:
            # this is the automatic update when a legacy inkstitch svg version was recognized
            for element in document.iterdescendants():
                if element.tag in EMBROIDERABLE_TAGS:
                    update_legacy_params(EmbroideryElement(element), file_version, INKSTITCH_SVG_VERSION)
        _update_inkstitch_svg_version(svg)


def _update_inkstitch_svg_version(svg):
    # set inkstitch svg version
    metadata = InkStitchMetadata(svg.getroot())
    metadata['inkstitch_svg_version'] = INKSTITCH_SVG_VERSION


def update_legacy_params(element, file_version, inkstitch_svg_version):
    for version in range(file_version + 1, inkstitch_svg_version + 1):
        _update_to(version, element)


def _update_to(version, element):
    if version == 1:
        _update_to_one(element)
    elif version == 2:
        _update_to_two(element)


def _update_to_two(element):
    if element.node.TAG == "polyline" and element.node.style("stroke") is not None:
        element.set_param('stroke_method', 'manual_stitch')


def _update_to_one(element):  # noqa: C901
    # update legacy embroider_ attributes to namespaced attributes
    legacy_attribs = False
    for attrib in element.node.attrib:
        if attrib.startswith('embroider_'):
            _replace_legacy_embroider_param(element, attrib)
            legacy_attribs = True

    # convert legacy tie setting
    legacy_tie = element.get_param('ties', None)
    if legacy_tie == "True":
        element.set_param('ties', 0)
    elif legacy_tie == "False":
        element.set_param('ties', 3)

    # convert legacy fill_method
    legacy_fill_method = element.get_int_param('fill_method', None)
    if legacy_fill_method == 0:
        element.set_param('fill_method', 'auto_fill')
    elif legacy_fill_method == 1:
        element.set_param('fill_method', 'contour_fill')
    elif legacy_fill_method == 2:
        element.set_param('fill_method', 'guided_fill')
    elif legacy_fill_method == 3:
        element.set_param('fill_method', 'legacy_fill')

    underlay_angle = element.get_param('fill_underlay_angle', None)
    if underlay_angle and ',' in underlay_angle:
        element.set_param('fill_underlay_angle', underlay_angle.replace(',', ' '))

    # legacy satin method
    if element.get_boolean_param('e_stitch', False) is True:
        element.remove_param('e_stitch')
        element.set_param('satin_method', 'e_stitch')

    if element.get_boolean_param('satin_column', False) or element.get_int_param('stroke_method', 0) == 1:
        # reverse_rails defaults to Automatic, but we should never reverse an
        # old satin automatically, only new ones
        element.set_param('reverse_rails', 'none')

    # default setting for fill_underlay has changed
    if legacy_attribs and not element.get_param('fill_underlay', ""):
        element.set_param('fill_underlay', False)
    # default setting for running stitch length has changed (fills and strokes, not satins)
    if not element.get_boolean_param('satin_column', False) and element.get_float_param('running_stitch_length_mm', None) is None:
        element.set_param('running_stitch_length_mm', 1.5)

    # convert legacy stroke_method
    if element.get_style("stroke") and not element.node.get('inkscape:connection-start', None):
        # manual stitch
        legacy_manual_stitch = element.get_boolean_param('manual_stitch', False)
        if legacy_manual_stitch is True:
            element.remove_param('manual_stitch')
            element.set_param('stroke_method', 'manual_stitch')
        # stroke_method
        legacy_stroke_method = element.get_int_param('stroke_method', None)
        if legacy_stroke_method == 0:
            element.set_param('stroke_method', 'running_stitch')
        elif legacy_stroke_method == 1:
            element.set_param('stroke_method', 'ripple_stitch')
        if (not element.get_param('stroke_method', None) and
                element.get_param('satin_column', False) is False and
                not element.node.style('stroke-dasharray')):
            element.set_param('stroke_method', 'zigzag_stitch')
        # grid_size was supposed to be mm, but it was in pixels
        grid_size = element.get_float_param('grid_size', None)
        if grid_size:
            size = grid_size / PIXELS_PER_MM
            size = "{:.2f}".format(size)
            element.set_param('grid_size_mm', size)
            element.remove_param('grid_size')


def _replace_legacy_embroider_param(element, param):
    # remove "embroider_" prefix
    new_param = param[10:]
    if new_param in INKSTITCH_ATTRIBS:
        value = element.node.get(param, "").strip()
        element.set_param(param[10:], value)
    del element.node.attrib[param]

def update_legacy_params(element, file_version, inkstitch_svg_version):
    for version in range(file_version + 1, inkstitch_svg_version + 1):
        _update_to(version, element)


def _update_to(version, element):
    if version == 1:
        _update_to_one(element)


def _update_to_one(element):  # noqa: C901
    # update legacy embroider_ attributes to namespaced attributes
    legacy_attribs = False
    for attrib in element.node.attrib:
        if attrib.startswith('embroider_'):
            element.replace_legacy_param(attrib)
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

    # legacy satin method
    if element.get_boolean_param('e_stitch', False) is True:
        element.remove_param('e_stitch')
        element.set_param('satin_method', 'e_stitch')

    # default setting for fill_underlay has changed
    if legacy_attribs and not element.get_param('fill_underlay', ""):
        element.set_param('fill_underlay', False)

    # convert legacy stroke_method
    if element.get_style("stroke"):
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

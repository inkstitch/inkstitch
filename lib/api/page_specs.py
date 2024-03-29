# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from flask import Blueprint, g, jsonify

page_specs = Blueprint('page_specs', __name__)


@page_specs.route('')
def get_page_specs():
    svg = g.extension.document.getroot()
    width = svg.get('width', 0)
    height = svg.get('height', 0)
    pagecolor = "white"
    deskcolor = "white"
    bordercolor = "black"
    showpageshadow = True

    namedview = svg.namedview
    if namedview is not None:
        pagecolor = namedview.get('pagecolor', pagecolor)
        deskcolor = namedview.get('inkscape:deskcolor', deskcolor)
        bordercolor = namedview.get('bordercolor', bordercolor)
        showpageshadow = namedview.get('inkscape:showpageshadow', showpageshadow)

    page_specs = {
        "width": width,
        "height": height,
        "pagecolor": pagecolor,
        "deskcolor": deskcolor,
        "bordercolor": bordercolor,
        "showpageshadow": showpageshadow
    }
    return jsonify(page_specs)

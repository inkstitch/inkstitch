# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from flask import Blueprint, g, jsonify

page_specs = Blueprint('page_specs', __name__)

@page_specs.route('')
def get_page_specs():

    metadata = g.extension.get_inkstitch_metadata()

    page_specs = {
        "width": metadata.document.get('width'),
        "height": metadata.document.get('height'),
        "pagecolor": metadata.document[1].get('pagecolor'),
        "deskcolor": metadata.document[1].get('inkscape:deskcolor')
    }
    
    return jsonify(page_specs)
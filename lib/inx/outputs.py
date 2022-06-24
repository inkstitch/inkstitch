# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import pyembroidery

from .utils import build_environment, write_inx_file


def pyembroidery_output_formats():
    for format in pyembroidery.supported_formats():
        if 'writer' in format:
            description = format['description']
            if format['category'] == "color":
                description = "%s [COLOR]" % description
            elif format['category'] == "image":
                description = "%s [IMAGE]" % description
            elif format['category'] == "stitch":
                description = "%s [STITCH]" % description
            elif format['category'] != "embroidery":
                description = "%s [DEBUG]" % description
            yield format['extension'], description, format['mimetype'], format['category']


def generate_output_inx_files():
    env = build_environment()
    template = env.get_template('output.xml')

    for format, description, mimetype, category in pyembroidery_output_formats():
        name = "output_%s" % format.upper()
        write_inx_file(name, template.render(format=format, mimetype=mimetype, description=description))

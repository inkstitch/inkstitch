# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import pystitch

from .utils import build_environment, write_inx_file


def pystitch_output_formats():
    for format in pystitch.supported_formats():
        if 'writer' in format:
            description = format['description']
            if format['category'] == "color":
                description = f"{description} [COLOR]"
            elif format['category'] == "image":
                description = f"{description} [IMAGE]"
            elif format['category'] == "stitch":
                description = f"{description} [STITCH]"
            elif format['category'] == "quilting":
                description = f"{description} [QUILTING]"
            elif format['category'] != "embroidery":
                description = f"{description} [DEBUG]"
            if not format['extension'] == 'png':
                yield format['extension'], description, format['mimetype'], format['category']


def generate_output_inx_files(alter_data):
    env = build_environment()
    template = env.get_template('output.xml')

    for format, description, mimetype, category in pystitch_output_formats():
        name = f"output_{format.upper()}"
        write_inx_file(name, template.render(alter_data, format=format, mimetype=mimetype, description=description))

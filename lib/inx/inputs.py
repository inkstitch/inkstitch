# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import pyembroidery

from .utils import build_environment, write_inx_file


def pyembroidery_input_formats():
    for format in pyembroidery.supported_formats():
        if 'reader' in format and format['category'] in ['embroidery', 'color', 'stitch', 'debug']:
            yield format['extension'], format['description']


def generate_input_inx_files(alter_data):
    env = build_environment()
    template = env.get_template('input.xml')

    for format, description in pyembroidery_input_formats():
        name = f"input_{format.upper()}"
        write_inx_file(name, template.render(alter_data, format=format, description=description))

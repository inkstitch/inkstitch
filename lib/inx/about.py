# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from .utils import build_environment, write_inx_file


def generate_about_inx_file():
    env = build_environment()
    template = env.get_template('about.xml')
    write_inx_file("about", template.render())

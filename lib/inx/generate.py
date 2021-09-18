# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from .info import generate_info_inx_files
from .extensions import generate_extension_inx_files
from .inputs import generate_input_inx_files
from .outputs import generate_output_inx_files


def generate_inx_files():
    generate_input_inx_files()
    generate_output_inx_files()
    generate_extension_inx_files()
    generate_info_inx_files()

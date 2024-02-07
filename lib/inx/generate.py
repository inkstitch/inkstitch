# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from .info import generate_info_inx_files
from .extensions import generate_extension_inx_files
from .inputs import generate_input_inx_files
from .outputs import generate_output_inx_files


def generate_inx_files(alter=None):
    if alter is not None:
        # Ensure the alter is lowercase and string a-z and one letter long
        if len(alter) != 1 or not alter[0].isalpha() or not alter[0].islower():  # error
            raise ValueError(f"Invalid alter '{alter}' for inx files, must be a single letter a-z.")

    if alter is None:
        id_inkstitch = "inkstitch"
        menu_inkstitch = "Ink/Stitch"
    else:
        id_inkstitch = f"{alter}-inkstitch"
        menu_inkstitch = f"Ink/Stitch-{alter}"

    # print(f"generate_inx_files: id_inkstitch={id_inkstitch}, menu_inkstitch={menu_inkstitch}")

    alter_data = {
        'id_inkstitch': id_inkstitch,
        'menu_inkstitch': menu_inkstitch,
    }

    generate_input_inx_files(alter_data)
    generate_output_inx_files(alter_data)
    generate_extension_inx_files(alter_data)
    generate_info_inx_files(alter_data)

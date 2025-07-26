# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import os

import pystitch

from ..commands import (COMMANDS, GLOBAL_COMMANDS, LAYER_COMMANDS,
                        OBJECT_COMMANDS)
from ..extensions import Input, Output, extensions
from ..lettering.categories import FONT_CATEGORIES
from ..threads import ThreadCatalog
from .outputs import pystitch_output_formats
from .utils import build_environment, write_inx_file


def layer_commands():
    # We purposefully avoid using commands.get_command_description() here.  We
    # want to call _() on the description inside the actual template so that
    # we use the translation language selected in build_environment().
    return [(command, COMMANDS[command]) for command in LAYER_COMMANDS]


def global_commands():
    return [(command, COMMANDS[command]) for command in GLOBAL_COMMANDS]


def object_commands():
    return [(command, COMMANDS[command]) for command in OBJECT_COMMANDS]


def pystitch_debug_formats():
    for format in pystitch.supported_formats():
        if 'writer' in format and format['category'] not in ['embroidery', 'image', 'color', 'stitch']:
            yield format['extension'], format['description']


def threadcatalog():
    threadcatalog = ThreadCatalog().palette_names()
    return threadcatalog


def generate_extension_inx_files(alter_data):
    env = build_environment()

    for extension in extensions:
        if extension is Input or extension is Output:
            continue

        if extension.DEVELOPMENT_ONLY and 'BUILD' in os.environ:
            continue

        name = extension.name()
        template = env.get_template(f'{name}.xml')
        write_inx_file(name, template.render(alter_data,
                                             formats=pystitch_output_formats(),
                                             debug_formats=pystitch_debug_formats(),
                                             threadcatalog=threadcatalog(),
                                             font_categories=FONT_CATEGORIES,
                                             layer_commands=layer_commands(),
                                             object_commands=object_commands(),
                                             global_commands=global_commands()))

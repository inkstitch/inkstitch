#!/usr/bin/env python

# ink/stitch: an extension for machine embroidery design using Inkscape
# Copyright (C) 2010 Jon Howell
# Copyright (C) 2015 Bas Wijnen - these additions also released under AGPLv3
# Copyright (C) 2015 Steven Siegl
# Copyright (C) 2016-2018 Lex Neva
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import logging
import os
import sys
import traceback
from argparse import ArgumentParser
from cStringIO import StringIO

import lib.debug as debug
from lib import extensions
from lib.i18n import _
from lib.utils import restore_stderr, save_stderr

logger = logging.getLogger('shapely.geos')
logger.setLevel(logging.DEBUG)
shapely_errors = StringIO()
ch = logging.StreamHandler(shapely_errors)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


parser = ArgumentParser()
parser.add_argument("--extension")
my_args, remaining_args = parser.parse_known_args()

if os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), "DEBUG")):
    debug.enable()

extension_name = my_args.extension

# example: foo_bar_baz -> FooBarBaz
extension_class_name = extension_name.title().replace("_", "")

extension_class = getattr(extensions, extension_class_name)
extension = extension_class()

if hasattr(sys, 'gettrace') and sys.gettrace():
    extension.affect(args=remaining_args)
else:
    save_stderr()
    exception = None
    try:
        extension.affect(args=remaining_args)
    except (SystemExit, KeyboardInterrupt):
        raise
    except Exception:
        exception = traceback.format_exc()
    finally:
        restore_stderr()

        if shapely_errors.tell():
            print >> sys.stderr, shapely_errors.getvalue()

    if exception:
        print >> sys.stderr, _("Ink/Stitch experienced an unexpected error.").encode("UTF-8")
        print >> sys.stderr, _("If you'd like to help, please file an issue at "
                               "https://github.com/inkstitch/inkstitch/issues "
                               "and include the entire error description below:").encode("UTF-8"), "\n"
        print >> sys.stderr, exception
        sys.exit(1)
    else:
        sys.exit(0)

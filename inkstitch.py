# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import logging
import os
import sys
import traceback
from argparse import ArgumentParser
from io import StringIO

if getattr(sys, 'frozen', None) is None:
    # When running in development mode, we want to use the inkex installed by
    # pip install, not the one bundled with Inkscape which is not new enough.
    if sys.platform == "darwin":
        sys.path.remove("/Applications/Inkscape.app/Contents/Resources/share/inkscape/extensions")
        sys.path.append("/Applications/Inkscape.app/Contents/Resources/share/inkscape/extensions")
    else:
        sys.path.remove('/usr/share/inkscape/extensions')
        sys.path.append('/usr/share/inkscape/extensions')

from inkex import errormsg
from lxml.etree import XMLSyntaxError

import lib.debug as debug
from lib import extensions
from lib.i18n import _
from lib.utils import restore_stderr, save_stderr, version

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
    extension.run(args=remaining_args)
else:
    save_stderr()
    exception = None
    try:
        extension.run(args=remaining_args)
    except (SystemExit, KeyboardInterrupt):
        raise
    except XMLSyntaxError:
        msg = _("Ink/Stitch cannot read your SVG file. "
                "This is often the case when you use a file which has been created with Adobe Illustrator.")
        msg += "\n\n"
        msg += _("Try to import the file into Inkscape through 'File > Import...' (Ctrl+I)")
        errormsg(msg)
    except Exception:
        exception = traceback.format_exc()
    finally:
        restore_stderr()

        if shapely_errors.tell():
            errormsg(shapely_errors.getvalue())

    if exception:
        errormsg(_("Ink/Stitch experienced an unexpected error.") + "\n")
        errormsg(_("If you'd like to help, please file an issue at "
                   "https://github.com/inkstitch/inkstitch/issues "
                   "and include the entire error description below:") + "\n")
        errormsg(version.get_inkstitch_version() + "\n")
        errormsg(exception)
        sys.exit(1)
    else:
        sys.exit(0)

import logging
import os
import sys
import traceback
from argparse import ArgumentParser
from io import StringIO

from lxml.etree import XMLSyntaxError

import lib.debug as debug
from lib import extensions
from lib.i18n import _
from lib.utils import restore_stderr, save_stderr
from lib.utils import version

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
        print(_("Ink/Stitch cannot read your SVG file. "
              "This is often the case when you use a file which has been created with Adobe Illustrator."),
              "\n\n",
              _("Try to import the file into Inkscape through 'File > Import...' (Ctrl+I)"), file=sys.stderr)
    except Exception:
        exception = traceback.format_exc()
    finally:
        restore_stderr()

        if shapely_errors.tell():
            print(shapely_errors.getvalue(), file=sys.stderr)

    if exception:
        print(_("Ink/Stitch experienced an unexpected error."), file=sys.stderr)
        print(_("If you'd like to help, please file an issue at "
                "https://github.com/inkstitch/inkstitch/issues "
                "and include the entire error description below:"), "\n", file=sys.stderr)
        print(version.get_inkstitch_version(), file=sys.stderr)
        print(exception, file=sys.stderr)
        sys.exit(1)
    else:
        sys.exit(0)

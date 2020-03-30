import os
import sys
import logging
import traceback
from cStringIO import StringIO
from argparse import ArgumentParser

from lib import extensions
from lib.utils import save_stderr, restore_stderr
import lib.debug as debug


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
        script_name = os.path.basename(__file__)

        if script_name.endswith('.py'):
            binary_name = script_name[:-3]
        else:
            # Probably not right, but we can at least try.
            binary_name = script_name

        binary_path = os.path.join("inkstitch", "bin", binary_name)

        args = sys.argv[:]
        args[0] = binary_path

        print >> sys.stderr, "Unexpected error launching Ink/Stitch."
        print >> sys.stderr, "If you're having trouble, please file an issue here, "\
                             "including the text below: https://github.com/inkstitch/inkstitch/issues\n"
        print >> sys.stderr, "Tried to launch:", binary_path
        print >> sys.stderr, "Arguments:", args
        print >> sys.stderr, "Debugging information:\n"
        print >> sys.stderr, exception
        sys.exit(1)
    else:
        sys.exit(0)

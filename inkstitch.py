import os
import sys
import traceback
from argparse import ArgumentParser

from lib import extensions
from lib.utils import save_stderr, restore_stderr


parser = ArgumentParser()
parser.add_argument("--extension")
my_args, remaining_args = parser.parse_known_args()

if os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), "DEBUG")):
    # How to debug Ink/Stitch:
    #
    # 1. Install LiClipse (liclipse.com) -- no need to install Eclipse first
    # 2. Start debug server as described here: http://www.pydev.org/manual_adv_remote_debugger.html
    #    * follow the "Note:" to enable the debug server menu item
    # 3. Create a file named "DEBUG" next to inkstitch.py in your git clone.
    # 4. Run any extension and PyDev will start debugging.

    import pydevd
    pydevd.settrace()

extension_name = my_args.extension

# example: foo_bar_baz -> FooBarBaz
extension_class_name = extension_name.title().replace("_", "")

extension_class = getattr(extensions, extension_class_name)
extension = extension_class()

exception = None

# save_stderr()
# try:
#     extension.affect(args=remaining_args)
# except (SystemExit, KeyboardInterrupt):
#     raise
# except Exception:
#     exception = traceback.format_exc()
# finally:
#     restore_stderr()
#
# if exception:
#     print >> sys.stderr, exception
#     sys.exit(1)
# else:
#     sys.exit(0)
extension.affect(args=remaining_args)

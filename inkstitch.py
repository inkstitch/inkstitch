import sys
import traceback
from argparse import ArgumentParser
from lib.utils import save_stderr, restore_stderr
from lib import extensions


parser = ArgumentParser()
parser.add_argument("--extension")
my_args, remaining_args = parser.parse_known_args()

extension_name = my_args.extension

# example: foo_bar_baz -> FooBarBaz
extension_class_name = extension_name.title().replace("_", "")

extension_class = getattr(extensions, extension_class_name)
extension = extension_class()

exception = None

save_stderr()
try:
    extension.affect(args=remaining_args)
except (SystemExit, KeyboardInterrupt):
    raise
except Exception:
    exception = traceback.format_exc()
finally:
    restore_stderr()

if exception:
    print >> sys.stderr, exception
    sys.exit(1)
else:
    sys.exit(0)

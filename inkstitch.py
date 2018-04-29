import sys
import traceback
from argparse import ArgumentParser
from inkstitch.utils import save_stderr, restore_stderr
from inkstitch import extensions


def get_extension():
    parser = ArgumentParser()
    parser.add_argument("--extension")
    args, extras = parser.parse_known_args()

    return args.extension


extension_name = get_extension()
extension_class = getattr(extensions, extension_name.capitalize())
extension = extension_class()

exception = None

save_stderr()
try:
    extension.affect()
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

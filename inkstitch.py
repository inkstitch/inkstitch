# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

# only Python 3.11+ is officially supported
import sys
if sys.version_info < (3, 11):  # noqa: UP036
    print("ERROR: Python 3.11 or later is required.", file=sys.stderr)
    sys.exit(1)

import logging
import os
import tomllib
from argparse import ArgumentParser
from pathlib import Path


import lib.debug.logging as debug_logging
import lib.debug.utils as debug_utils
from lib.debug.utils import safe_get    # mimic get method of dict with default value

# --------------------------------------------------------------------------------------------

if len(sys.argv) < 2:
    from textwrap import dedent
    # No CLI arguments provided - script was likely executed directly by double-clicking
    msg = dedent("""
        No arguments given, exiting!
        Ink/Stitch is an Inkscape extension.
        Please enter arguments or run Ink/Stitch through the Inkscape extensions menu.
    """).strip()

    try:
        import wx
        app = wx.App()
        wx.MessageBox(msg, "Ink/Stitch", wx.OK | wx.ICON_ERROR)
    except ImportError:
        print(msg, file=sys.stderr)

    sys.exit(1)


# --------------------------------------------------------------------------------------------

SCRIPTDIR = Path(__file__).parent.absolute()

# running_from_readonly_filesystem = not debug_utils.can_write_to_directory(SCRIPTDIR)

# pyinstaller bundle
# running_as_frozen = getattr(sys, 'frozen', None) is not None

# Create main 'inkstitch' logger
logger = logging.getLogger("inkstitch")

# Load DEBUG.toml if present; fallback to defaults
debug_toml = SCRIPTDIR / "DEBUG.toml"
if debug_toml.exists():
    with debug_toml.open("rb") as f:
        ini = tomllib.load(f)
else:
    ini = {}
# --------------------------------------------------------------------------------------------
development_mode = safe_get(ini, "DEBUG", "development_mode", default=False)
log_location = ""
if development_mode:
    log_location = safe_get(ini, "LOGGING", "log_location", default="")


# Initialize logging before any log calls
LOGDIR = debug_logging.activate_logging(
    development_mode,
    log_location,
    ini,
    SCRIPTDIR
)
# --------------------------------------------------------------------------------------------

# Prevent recursive script creation in CLI/BASH mode
YES_VALUES = {"true", "1", "yes", "y"}
running_from_inkscape = os.environ.get("INKSTITCH_OFFLINE_SCRIPT", "").lower() not in YES_VALUES

# -------------------------------------------------------------------------------------------
# Initialize debug and profiling modes
debug_active = sys.gettrace() is not None     # check if debugger is active on startup
debug_type = 'none'
profiler_type = 'none'

if development_mode:
    # Fallback to INI settings if no debugger is attached
    if not debug_active:
        debug_type = debug_utils.resolve_debug_type(ini)

    # Resolve profiler type from INI file or CLI arguments
    profiler_type = debug_utils.resolve_profiler_type(ini)

    if running_from_inkscape:
        # Generate offline script before sys.path modifications (see inkex below)
        if safe_get(ini, "DEBUG", "create_bash_script", default=False):
            debug_utils.write_offline_debug_script(SCRIPTDIR, ini)

        # Optionally disable debugger when running inside Inkscape
        if safe_get(ini, "DEBUG", "disable_from_inkscape", default=False):
            debug_type = "none"


# -------------------------------------------------------------------------------------------
#  INKEX:

#  WARNING: Must be executed before importing inkex
# Prioritize pip-installed inkex over Inkscape's bundled version
prefer_pip_inkex = safe_get(ini, "LIBRARY", "prefer_pip_inkex", default=True)
debug_imports = os.environ.get("INKSTITCH_DEBUG_IMPORTS", "").lower() in YES_VALUES
debug_imports_file = os.environ.get("INKSTITCH_DEBUG_IMPORTS_FILE")


def debug_import(message: str) -> None:
    if sys.stderr is not None:
        print(message, file=sys.stderr)
    if debug_imports_file:
        with open(debug_imports_file, "a", encoding="utf-8") as report:
            print(message, file=report)

if debug_imports:
    import importlib.util

    inkex_spec = importlib.util.find_spec("inkex")
    debug_import("INKEX IMPORT DEBUG: before reorder")
    debug_import(f"  sys.frozen={getattr(sys, 'frozen', False)}")
    debug_import(f"  spec.origin={inkex_spec.origin if inkex_spec else None}")
    debug_import(f"  sys.modules.loaded={'inkex' in sys.modules}")
    debug_import("  sys.path:")
    for path in sys.path:
        debug_import(f"    {path}")

if prefer_pip_inkex and "PYTHONPATH" in os.environ:
    debug_utils.assert_inkex_not_imported_before_path_setup()
    debug_utils.reorder_sys_path()

if debug_imports:
    import inkex

    debug_import("INKEX IMPORT DEBUG: after reorder")
    debug_import(f"  sys.frozen={getattr(sys, 'frozen', False)}")
    debug_import(f"  inkex.__file__={inkex.__file__}")
    debug_import(f"  sys.modules.loaded={'inkex' in sys.modules}")
    debug_import("  sys.path:")
    for path in sys.path:
        debug_import(f"    {path}")

# -------------------------------------------------------------------------------------------

if debug_type != "none":
    from lib.debug.debugger import init_debugger

    init_debugger(debug_type, ini)
    debug_active = sys.gettrace() is not None


# Enable debug logging (must be imported after sys.path setup)
from lib.debug.debug import debug as debug_logger  # noqa: E402

debug_logger.enable()

debug_logging.startup_info(
    logger,
    SCRIPTDIR,
    LOGDIR,
    development_mode,
    log_location,
    running_from_inkscape,
    debug_active,
    debug_type,
    profiler_type,
)

# --------------------------------------------------------------------------------------------

# Extract '--extension' argument and dynamically load the corresponding extension class
# NOTE: Must be imported after sys.path setup
from lib import extensions  # noqa: E402


# WARN: Do not move up; running earlier breaks release warning suppression.
logging_active = development_mode or LOGDIR is not None
if not logging_active:
    debug_logging.disable_warnings()

# --------------------------------------------------------------------------------------------

parser = ArgumentParser()
parser.add_argument("--extension")
my_args, remaining_args = parser.parse_known_args()

extension_name = my_args.extension

# example: foo_bar_baz -> FooBarBaz
extension_class_name = extension_name.title().replace("_", "")

extension = getattr(extensions, extension_class_name)()

# Execute extension in debug/profile mode vs. normal mode
if profiler_type != "none":
    debug_utils.profile(profiler_type, SCRIPTDIR, ini, extension,
                        remaining_args)
elif debug_active:
    extension.run(args=remaining_args)
else:
    # Normal execution: catch exceptions and suppress GTK output

    from inkex import errormsg  # Display UI error popups in Inkscape
    from lxml.etree import XMLSyntaxError  # Catch malformed or non-standard SVG input
    from lib.exceptions import InkstitchException, format_uncaught_exception
    from lib.i18n import _  # Gettext translation function
    from lib.utils import restore_stderr, save_stderr  # Suppress GTK/C-level warning noise

    save_stderr()  # Suppress GTK warning noise
    try:
        extension.run(args=remaining_args)
    except (SystemExit, KeyboardInterrupt):
        raise
    except XMLSyntaxError:
        errormsg(
            _("Ink/Stitch cannot read your SVG file. "
              "This is often the case when you use a file which has been created with Adobe Illustrator.\n\n"
              "Try to import the file into Inkscape through 'File > Import...' (Ctrl+I)"
              ))
    except InkstitchException as exc:
        errormsg(str(exc))
    except Exception:
        errormsg(format_uncaught_exception())
        sys.exit(1)
    finally:
        restore_stderr()

    sys.exit(0)

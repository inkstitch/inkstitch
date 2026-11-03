# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import logging
import os
import sys
if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib
from argparse import ArgumentParser
from pathlib import Path
from typing import TYPE_CHECKING

import lib.debug.logging as debug_logging
import lib.debug.utils as debug_utils
from lib.debug.config import resolve_development_config
from lib.debug.utils import safe_get    # mimic get method of dict with default value

if TYPE_CHECKING:
    from lib.extensions.base import InkstitchExtension

# --------------------------------------------------------------------------------------------

# Directory of this script.  It is a constant derived from __file__, so the helper
# functions below share it instead of passing it around as an argument.
SCRIPTDIR = Path(__file__).parent.absolute()

# running_from_readonly_filesystem = not debug_utils.can_write_to_directory(SCRIPTDIR)

# pyinstaller bundle
# running_as_frozen = getattr(sys, 'frozen', None) is not None

# Application logger.  Loggers are singletons and the logging HOWTO recommends creating
# the module logger once at module level, so every helper below can log directly.
# The name must stay "inkstitch" - the logging configuration attaches its handlers to
# that exact name (see LOGGING_template.toml).
logger = logging.getLogger("inkstitch")

# Environment values that count as "true" for the INKSTITCH_* boolean variables.
YES_VALUES = {"true", "1", "yes", "y"}


def abort_on_legacy_debug_ini() -> None:
    """Stop the user from running with an obsolete DEBUG.ini file.

    TODO --- temporary --- since 2024-03-20
    """
    if (SCRIPTDIR / "DEBUG.ini").exists():
        print(
            "ERROR: legacy DEBUG.ini exists. "
            "Please reformat its contents to DEBUG.toml and remove DEBUG.ini.",
            file=sys.stderr,
        )
        sys.exit(1)


def abort_without_arguments() -> None:
    """Abort with a friendly message when the script is run without arguments.

    This happens when a user double-clicks the script, for example.
    """
    if len(sys.argv) >= 2:
        return

    from textwrap import dedent

    msg = dedent("""
        No arguments given, exiting!
        Ink/Stitch is an Inkscape extension.
        Please enter arguments or run Ink/Stitch through the Inkscape extensions menu.
    """).strip()

    try:
        import wx
        app = wx.App()  # noqa: F841 this reference must be kept alive for wx.MessageBox
        wx.MessageBox(msg, "Ink/Stitch", wx.OK | wx.ICON_ERROR)
    except ImportError:
        print(msg, file=sys.stderr)

    sys.exit(1)


def load_debug_config() -> dict:
    """Load DEBUG.toml if present; fall back to defaults."""
    debug_toml = SCRIPTDIR / "DEBUG.toml"
    if debug_toml.exists():
        with debug_toml.open("rb") as f:
            return tomllib.load(f)
    return {}


def init_logging() -> tuple[dict, bool, str, Path | None]:
    """Load the configuration and activate logging before any log calls.

    Returns the effective configuration, the development-mode flag, the configured
    log location and the resolved log directory.
    """
    ini = load_debug_config()
    development_mode, ini = resolve_development_config(ini)

    log_location = ""
    if development_mode:
        log_location = safe_get(ini, "LOGGING", "log_location", default="")

    logdir = debug_logging.activate_logging(
        development_mode,
        log_location,
        ini,
        SCRIPTDIR
    )
    return ini, development_mode, log_location, logdir


def detect_running_from_inkscape() -> bool:
    """Prevent recursive script creation in CLI/BASH mode."""
    return os.environ.get("INKSTITCH_OFFLINE_SCRIPT", "").lower() not in YES_VALUES


def resolve_debug_settings(ini: dict, development_mode: bool,
                           from_inkscape: bool) -> tuple[bool, str, str]:
    """Initialize the debug and profiling modes.

    Returns whether a debugger is attached, the debugger type and the profiler type.
    Debugging and profiling are only available in development mode.
    """
    debug_active = sys.gettrace() is not None  # check if debugger is active on startup
    debug_type = "none"
    profiler_type = "none"

    if not development_mode:
        return debug_active, debug_type, profiler_type

    # Fallback to INI settings if no debugger is attached
    if not debug_active:
        debug_type = debug_utils.resolve_debug_type(ini)

    # Resolve profiler type from INI file or CLI arguments
    profiler_type = debug_utils.resolve_profiler_type(ini)

    if from_inkscape:
        # Generate offline script before sys.path modifications (see prioritize_inkex)
        if safe_get(ini, "DEBUG", "create_bash_script", default=False):
            debug_utils.write_offline_debug_script(SCRIPTDIR, ini)

        # Optionally disable debugger when running inside Inkscape
        if safe_get(ini, "DEBUG", "disable_from_inkscape", default=False):
            debug_type = "none"

    return debug_active, debug_type, profiler_type


def prioritize_inkex(ini: dict) -> None:
    """Prioritize the pip-installed inkex over Inkscape's bundled version.

    WARNING: Must be executed before importing inkex.
    """
    prefer_pip_inkex = safe_get(ini, "LIBRARY", "prefer_pip_inkex", default=True)

    if prefer_pip_inkex and "PYTHONPATH" in os.environ:
        debug_utils.assert_inkex_not_imported_before_path_setup()
        debug_utils.reorder_sys_path()


def start_debugger(debug_type: str, ini: dict, debug_active: bool) -> bool:
    """Start the requested debugger and report whether one is really active."""
    if debug_type == "none":
        return debug_active

    from lib.debug.debugger import init_debugger

    init_debugger(debug_type, ini)
    # check if the debugger is really activated
    return sys.gettrace() is not None


def enable_debug_logging() -> None:
    """Enable svg debug logging.

    NOTE: The import must happen after the sys.path setup done by prioritize_inkex.
    """
    from lib.debug.debug import debug as debug_logger  # noqa: E402

    debug_logger.enable()


def log_startup_info(development_mode: bool, log_location: str,
                     logdir: Path | None, from_inkscape: bool,
                     debug_active: bool, debug_type: str,
                     profiler_type: str) -> None:
    """Log the startup information for troubleshooting."""
    debug_logging.startup_info(
        logger,
        SCRIPTDIR,
        logdir,
        development_mode,
        log_location,
        from_inkscape,
        debug_active,
        debug_type,
        profiler_type,
    )


def load_extension(development_mode: bool,
                   logdir: Path | None) -> tuple['InkstitchExtension', list[str]]:
    """Load the extension requested by the --extension argument.

    Returns the extension instance and the remaining command line arguments.
    """
    # Import the extensions only after the sys.path setup done by prioritize_inkex
    from lib import extensions  # noqa: E402

    # WARN: Do not move up; running earlier breaks release warning suppression.
    if not (development_mode or logdir is not None):
        debug_logging.disable_warnings()

    parser = ArgumentParser()
    parser.add_argument("--extension")
    my_args, remaining_args = parser.parse_known_args()

    extension_name = my_args.extension

    # example: foo_bar_baz -> FooBarBaz
    extension_class_name = extension_name.title().replace("_", "")

    return getattr(extensions, extension_class_name)(), remaining_args


def run_extension_safely(extension: 'InkstitchExtension',
                         remaining_args: list[str]) -> None:
    """Run the extension, turning failures into user-facing Inkscape error popups.

    Also suppresses GTK/C-level warning noise while the extension runs.
    """
    from inkex import errormsg  # Display UI error popups in Inkscape
    from lxml.etree import XMLSyntaxError  # Catch malformed or non-standard SVG input
    from lib.exceptions import InkstitchException, format_uncaught_exception
    from lib.i18n import _  # Gettext translation function
    from lib.utils import restore_stderr, save_stderr  # Suppress GTK warning noise

    save_stderr()
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


def run_extension(extension: 'InkstitchExtension', remaining_args: list[str],
                  ini: dict, debug_active: bool, profiler_type: str) -> None:
    """Execute the extension in profile, debug or normal mode."""
    if profiler_type != "none":
        debug_utils.profile(profiler_type, SCRIPTDIR, ini, extension, remaining_args)
    elif debug_active:
        extension.run(args=remaining_args)
    else:
        run_extension_safely(extension, remaining_args)

    sys.exit(0)


def main() -> None:
    abort_without_arguments()
    abort_on_legacy_debug_ini()

    ini, development_mode, log_location, logdir = init_logging()
    from_inkscape = detect_running_from_inkscape()

    debug_active, debug_type, profiler_type = resolve_debug_settings(
        ini, development_mode, from_inkscape)

    # Must run before inkex is imported, which happens in load_extension
    prioritize_inkex(ini)

    debug_active = start_debugger(debug_type, ini, debug_active)

    enable_debug_logging()
    log_startup_info(development_mode, log_location, logdir, from_inkscape,
                     debug_active, debug_type, profiler_type)

    extension, remaining_args = load_extension(development_mode, logdir)

    run_extension(extension, remaining_args, ini, debug_active, profiler_type)


if __name__ == '__main__':
    main()

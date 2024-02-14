# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import os
import sys
from pathlib import Path  # to work with paths as objects
from argparse import ArgumentParser  # to parse arguments and remove --extension

import configparser   # to read DEBUG.ini
import toml           # to read logging configuration from toml file
import warnings
import logging
import logging.config

import lib.debug_utils as debug_utils
import lib.debug_logging as debug_logging

SCRIPTDIR = Path(__file__).parent.absolute()

logger = logging.getLogger("inkstitch")   # create module logger with name 'inkstitch'

ini = configparser.ConfigParser()
ini.read(SCRIPTDIR / "DEBUG.ini")  # read DEBUG.ini file if exists, otherwise use default values in ini object
running_as_frozen = getattr(sys, 'frozen', None) is not None  # check if running from pyinstaller bundle

if not running_as_frozen:  # override running_as_frozen from DEBUG.ini - for testing
    if ini.getboolean("DEBUG", "force_frozen", fallback=False):
        running_as_frozen = True


if len(sys.argv) < 2:
    # no arguments - prevent accidentally running this script
    msg = "No arguments given, exiting!"  # without gettext localization see _()
    if running_as_frozen:  # we show dialog only when running from pyinstaller bundle - using wx
        try:
            import wx
            app = wx.App()
            dlg = wx.MessageDialog(None, msg, "Inkstitch", wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
        except ImportError:
            print(msg)
    else:
        print(msg)
    exit(1)

# Configure logging:
# in release mode normally we want to ignore all warnings and logging, but we can enable it by setting environment variables
#  - INKSTITCH_LOGLEVEL - logging level:
#       'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
#  - PYTHONWARNINGS, -W - warnings action controlled by python
#       actions: 'error', 'ignore', 'always', 'default', 'module', 'once'
if running_as_frozen:  # in release mode
    loglevel = os.environ.get('INKSTITCH_LOGLEVEL')  # read log level from environment variable or None
    docpath = os.environ.get('DOCUMENT_PATH')  # read document path from environment variable (set by inkscape) or None

    if docpath is not None and loglevel is not None and loglevel.upper() in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        # enable logging-warning and redirect output to input_svg.inkstitch.log
        logfilename = Path(docpath).with_suffix('.inkstitch.log')  # log file is created in document path
        loglevel = loglevel.upper()

        logging.config.dictConfig(debug_logging.frozen_config)  # configure root logger from dict - using loglevel, logfilename
        logging.captureWarnings(True)                           # capture all warnings to log file with level WARNING
    else:
        logging.disable()                # globally disable all logging of all loggers
        warnings.simplefilter('ignore')  # ignore all warnings

else:
    # in development mode we want to use configuration from some LOGGING.toml file
    logging_config_file = ini.get("LOGGING", "log_config_file", fallback=None)
    if logging_config_file is not None:
        logging_config_file = Path(logging_config_file)
        if logging_config_file.exists():
            with open(logging_config_file, "r") as f:
                development_config = toml.load(f)
        else:
            raise FileNotFoundError(f"{logging_config_file} file not found")
    else:                         # if LOGGING.toml file does not exist, use default logging configuration
        loglevel = 'DEBUG'        # set log level to DEBUG
        logfilename = SCRIPTDIR / "inkstitch.log"  # log file is created in current directory
        development_config = debug_logging.development_config

    debug_logging.configure_logging(development_config, ini, SCRIPTDIR)  # initialize logging configuration
    logger.info("Running in development mode")
    logger.info(f"Using logging configuration from file: {logging_config_file}")

# check if running from inkscape, given by environment variable
if os.environ.get('INKSTITCH_OFFLINE_SCRIPT', '').lower() in ['true', '1', 'yes', 'y']:
    running_from_inkscape = False
else:
    running_from_inkscape = True

# initialize debug and profiler type
debug_active = bool((gettrace := getattr(sys, 'gettrace')) and gettrace())  # check if debugger is active on startup
debug_type = 'none'
profiler_type = 'none'

if not running_as_frozen:  # debugging/profiling only in development mode
    # specify debugger type
    #   but if script was already started from debugger then don't read debug type from ini file or cmd line
    if not debug_active:
        debug_type = debug_utils.resolve_debug_type(ini)  # read debug type from ini file or cmd line

    profile_type = debug_utils.resolve_profile_type(ini)  # read profile type from ini file or cmd line

    if running_from_inkscape:
        # process creation of the Bash script - should be done before sys.path is modified, see below in prefere_pip_inkex
        if ini.getboolean("DEBUG", "create_bash_script", fallback=False):  # create script only if enabled in DEBUG.ini
            debug_utils.write_offline_debug_script(SCRIPTDIR, ini)

        # disable debugger when running from inkscape
        disable_from_inkscape = ini.getboolean("DEBUG", "disable_from_inkscape", fallback=False)
        if disable_from_inkscape:
            debug_type = 'none'  # do not start debugger when running from inkscape

    # prefer pip installed inkex over inkscape bundled inkex, pip version is bundled with Inkstitch
    # - must be be done before importing inkex
    prefere_pip_inkex = ini.getboolean("LIBRARY", "prefer_pip_inkex", fallback=True)
    if prefere_pip_inkex and 'PYTHONPATH' in os.environ:
        debug_utils.reorder_sys_path()

# enabling of debug depends on value of debug_type in DEBUG.ini file
if debug_type != 'none':
    from lib.debug import debug  # import global variable debug - don't import whole module
    debug.enable(debug_type, SCRIPTDIR, ini)
    # check if debugger is really activated
    debug_active = bool((gettrace := getattr(sys, 'gettrace')) and gettrace())

# log startup info
debug_logging.startup_info(logger, SCRIPTDIR, running_as_frozen, running_from_inkscape, debug_active, debug_type, profiler_type)

# pop '--extension' from arguments and generate extension class name from extension name
#   example:  --extension=params will instantiate Params() class from lib.extensions.

# we need to import only after possible modification of sys.path, we disable here flake8 E402
from lib import extensions  # noqa: E402  # import all supported extensions of institch

parser = ArgumentParser()
parser.add_argument("--extension")
my_args, remaining_args = parser.parse_known_args()

extension_name = my_args.extension

# example: foo_bar_baz -> FooBarBaz
extension_class_name = extension_name.title().replace("_", "")

extension_class = getattr(extensions, extension_class_name)
extension = extension_class()  # create instance of extension class - call __init__ method

# extension run(), we differentiate between debug and normal mode
# - in debug or profile mode we debug or profile extension.run() method
# - in normal mode we run extension.run() in try/except block to catch all exceptions and hide GTK spam
if debug_active or profiler_type != "none":  # if debug or profile mode
    if profiler_type == 'none':             # only debugging
        extension.run(args=remaining_args)
    else:                                  # do profiling
        debug_utils.profile(profiler_type, SCRIPTDIR, ini, extension, remaining_args)

else:   # if not debug nor profile mode
    from lib.exceptions import InkstitchException, format_uncaught_exception
    from inkex import errormsg  # to show error message in inkscape
    from lxml.etree import XMLSyntaxError  # to catch XMLSyntaxError from inkex
    from lib.i18n import _      # see gettext translation function _()
    from lib.utils import restore_stderr, save_stderr  # to hide GTK spam

    save_stderr()  # hide GTK spam
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
    except InkstitchException as exc:
        errormsg(str(exc))
    except Exception:
        errormsg(format_uncaught_exception())
        sys.exit(1)
    finally:
        restore_stderr()

    sys.exit(0)

# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import os
import sys
from pathlib import Path  # to work with paths as objects
import configparser   # to read DEBUG.ini

import lib.debug_utils as debug_utils  

SCRIPTDIR = Path(__file__).parent.absolute()

running_as_frozen = getattr(sys, 'frozen', None) is not None  # check if running from pyinstaller bundle

if len(sys.argv) < 2:
    # no arguments - prevent accidentally running this script
    msg = "No arguments given, exiting!" # without gettext localization see _()
    if running_as_frozen: # we show dialog only when running from pyinstaller bundle - using wx
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

ini = configparser.ConfigParser()
ini.read(SCRIPTDIR / "DEBUG.ini")  # read DEBUG.ini file if exists

# check if running from inkscape, given by environment variable
if os.environ.get('INKSTITCH_OFFLINE_SCRIPT', '').lower() in ['true', '1', 'yes', 'y']:
    running_from_inkscape = False
else:
    running_from_inkscape = True

debug_active = bool((gettrace := getattr(sys, 'gettrace')) and gettrace())  # check if debugger is active on startup
debug_type = 'none'
profiler_type = 'none'

if not running_as_frozen: # debugging/profiling only in development mode
    # specify debugger type
    # - if script was already started from debugger then don't read debug type from ini file or cmd line
    if not debug_active:
        # enable/disable debugger
        if os.environ.get('INKSTITCH_DEBUG_ENABLE', '').lower() in ['true', '1', 'yes', 'y']:
            debug_enable = True
        else:
            debug_enable = ini.getboolean("DEBUG","debug_enable", fallback=False)  # enable debugger on startup from ini

        debug_type = ini.get("DEBUG","debug_type", fallback="none")  # debugger type vscode, pycharm, pydevd
        if not debug_enable:
            debug_type = 'none'

        debug_to_file = ini.getboolean("DEBUG","debug_to_file", fallback=False)  # write debug output to file
        if debug_to_file and debug_type == 'none':
            debug_type = 'file'

    # enbale/disable profiling
    if os.environ.get('INKSTITCH_PROFILE_ENABLE', '').lower() in ['true', '1', 'yes', 'y']: 
        profile_enable = True
    else:
        profile_enable = ini.getboolean("PROFILE","profile_enable", fallback=False) # read from ini

    # specify profiler type
    profiler_type = ini.get("PROFILE","profiler_type", fallback="none")  # profiler type cprofile, profile, pyinstrument
    if not profile_enable:
        profiler_type = 'none'

    if running_from_inkscape:
        # process creation of the Bash script - should be done before sys.path is modified, see below in prefere_pip_inkex
        if ini.getboolean("DEBUG","create_bash_script", fallback=False):  # create script only if enabled in DEBUG.ini
            debug_utils.write_offline_debug_script(SCRIPTDIR, ini)
        
        # disable debugger when running from inkscape
        disable_from_inkscape = ini.getboolean("DEBUG","disable_from_inkscape", fallback=False)
        if disable_from_inkscape:
            debug_type = 'none'  # do not start debugger when running from inkscape

    # prefer pip installed inkex over inkscape bundled inkex, pip version is bundled with Inkstitch
    # - must be be done before importing inkex
    prefere_pip_inkex = ini.getboolean("LIBRARY","prefer_pip_inkex", fallback=True)
    if prefere_pip_inkex and 'PYTHONPATH' in os.environ:
        debug_utils.reorder_sys_path()

from argparse import ArgumentParser  # to parse arguments and remove --extension
import logging # to set logger for shapely
from io import StringIO  # to store shapely errors

from lib.exceptions import InkstitchException, format_uncaught_exception

from inkex import errormsg  # to show error message in inkscape
from lxml.etree import XMLSyntaxError  # to catch XMLSyntaxError from inkex

from lib.debug import debug  # import global variable debug - don't import whole module

from lib import extensions  # import all supported extensions of institch
from lib.i18n import _      # see gettext translation function _()
from lib.utils import restore_stderr, save_stderr  # to hide GTK spam

# enabling of debug depends on value of debug_type in DEBUG.ini file
if debug_type != 'none':
    debug.enable(debug_type, SCRIPTDIR, ini)
    # check if debugger is really activated
    debug_active = bool((gettrace := getattr(sys, 'gettrace')) and gettrace())

# warnings are used by some modules, we want to ignore them all in release
#   - see warnings.warn()
if running_as_frozen or not debug_active:
    import warnings
    warnings.filterwarnings('ignore')

# TODO - check if this is still for shapely needed, apparently, shapely uses only exceptions instead of io.
#        all logs were removed from version 2.0.0, ensure that shapely is always >= 2.0.0

#  ---- plan to remove this in future ----
# set logger for shapely - for old versions of shapely
# logger = logging.getLogger('shapely.geos')  # attach logger of shapely
# logger.setLevel(logging.DEBUG)
# shapely_errors = StringIO()                # in memory file to store shapely errors
# ch = logging.StreamHandler(shapely_errors)
# ch.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
# ch.setFormatter(formatter)
# logger.addHandler(ch)
#  ---- plan to remove this in future ----

# pop '--extension' from arguments and generate extension class name from extension name
#   example:  --extension=params will instantiate Params() class from lib.extensions.
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
    save_stderr() # hide GTK spam
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

        # if shapely_errors.tell():
        #     errormsg(shapely_errors.getvalue())

    sys.exit(0)

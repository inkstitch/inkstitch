# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
import traceback
import sys
import platform
import subprocess
from glob import glob


class InkstitchException(Exception):
    pass


def get_os_version():
    if sys.platform == "win32":
        # To get the windows version, python functions are used
        # Using python subprocess with cmd.exe in windows is currently a security risk
        os_ver = "Windows " + platform.release() + " version: " + platform.version()
    if sys.platform == "darwin":
        # macOS command line progam provides accurate info than python functions
        mac_v = subprocess.run(["sw_vers"], capture_output=True, text=True)
        os_ver = str(mac_v.stdout.strip())
    if sys.platform == "linux":
        # Getting linux version method used here is for systemd and nonsystemd linux.
        try:
            ltmp = subprocess.run(["cat"] + glob("/etc/*-release"), capture_output=True, text=True)
            lnx_ver = ltmp.stdout.splitlines()
            lnx_ver = str(list(filter(lambda x: "PRETTY_NAME" in x, lnx_ver)))
            os_ver = lnx_ver[15:][:-3]
        except FileNotFoundError:
            os_ver = "Cannot get Linux distro version"

    return os_ver


def format_uncaught_exception():
    """Format the current exception as a request for a bug report.

    Call this inside an except block so that there is an exception that we can
    call traceback.format_exc() on.
    """

    # importing locally to avoid any possibility of circular import
    from lib.utils import version
    from .i18n import _

    message = ""
    message += _("Ink/Stitch experienced an unexpected error. This means it is a bug in Ink/Stitch.")
    message += "\n\n"
    # L10N this message is followed by a URL: https://github.com/inkstitch/inkstitch/issues/new
    message += _("If you'd like to help please\n"
                 "- copy the entire error message below\n"
                 "- save your SVG file and\n"
                 "- create a new issue at")
    message += " https://github.com/inkstitch/inkstitch/issues/new\n\n"
    message += _("Include the error description and also (if possible) the svg file.")
    message += '\n\n'
    message += get_os_version()
    message += '\n\n'
    message += version.get_inkstitch_version() + '\n'
    message += traceback.format_exc()

    return message

# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
import traceback


class InkstitchException(Exception):
    pass


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
    message += '\n\n\n'
    message += version.get_inkstitch_version() + '\n'
    message += traceback.format_exc()

    return message

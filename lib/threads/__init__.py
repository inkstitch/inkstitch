# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from .color import ThreadColor as ThreadColor


def __getattr__(name):
    if name == "ThreadCatalog":
        from .catalog import ThreadCatalog
        return ThreadCatalog
    if name == "ThreadPalette":
        from .palette import ThreadPalette
        return ThreadPalette
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

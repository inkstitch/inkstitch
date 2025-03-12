# Authors: see git history
#
# Copyright (c) 2023 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from ..gui.about import AboutInkstitchApp
from .base import InkstitchExtension


class About(InkstitchExtension):

    def effect(self) -> None:
        app = AboutInkstitchApp()
        app.MainLoop()

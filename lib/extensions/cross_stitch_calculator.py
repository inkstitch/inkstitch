# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from ..gui.cross_stitch_calculator import CrossStitchCalculatorApp
from .base import InkstitchExtension


class CrossStitchCalculator(InkstitchExtension):
    def effect(self):
        app = CrossStitchCalculatorApp()
        app.MainLoop()

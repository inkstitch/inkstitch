# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import Layer

from ..gui.lettering_font_sample import LetteringFontSampleApp
from .base import InkstitchExtension


class LetteringFontSample(InkstitchExtension):
    '''
    This extension helps font creators to generate an output of every glyph from a selected font
    '''
    def effect(self):
        layer = self.svg.add(Layer())
        app = LetteringFontSampleApp(layer=layer)
        app.MainLoop()
        if len(layer) == 0:
            self.svg.remove(layer)

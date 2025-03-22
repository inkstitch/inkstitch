# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from inkex import Layer

from ..gui.lettering_font_sample import LetteringFontSampleApp
from ..i18n import _
from .base import InkstitchExtension
from ..svg import get_correction_transform


class LetteringFontSample(InkstitchExtension):
    '''
    This extension helps font creators to generate an output of every glyph from a selected font
    '''
    def effect(self):
        layer = Layer()
        self.svg.add(layer)
        layer.label = _("Font Sample")
        transform = get_correction_transform(layer, child=True)
        layer.transform = transform
        app = LetteringFontSampleApp(layer=layer)
        app.MainLoop()
        if len(layer) == 0:
            layer.delete()

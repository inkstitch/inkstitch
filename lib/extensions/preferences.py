# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from .base import InkstitchExtension
from ..gui.preferences import PreferencesApp


class Preferences(InkstitchExtension):
    '''
    This saves embroider settings into the metadata of the file
    '''

    def effect(self):
        app = PreferencesApp(self)
        app.MainLoop()

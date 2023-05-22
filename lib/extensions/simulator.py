# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from ..api import APIServer
from ..gui import open_url

from .base import InkstitchExtension


class Simulator(InkstitchExtension):
    def __init__(self):
        InkstitchExtension.__init__(self)

    def effect(self):
        if not self.get_elements():
            return
        api_server = APIServer(self)
        port = api_server.start_server()
        electron = open_url("/simulator", port)
        electron.wait()
        api_server.stop()
        api_server.join()

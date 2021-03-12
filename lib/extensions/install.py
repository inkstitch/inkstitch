# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from .base import InkstitchExtension
from ..api import APIServer
from ..gui import open_url


class Install(InkstitchExtension):
    def __init__(self):
        InkstitchExtension.__init__(self)

    def effect(self):
        api_server = APIServer(self)
        port = api_server.start_server()
        electron = open_url("/install?port=%d" % port)
        electron.wait()
        api_server.stop()
        api_server.join()

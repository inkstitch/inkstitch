# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import json
import sys
import os

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
        os.environ['FLASKPORT'] = str(port)
        # this creates the .json for dev mode to get translations
        if getattr(sys, 'frozen', None) is None:
            dynamic_port = {
                  "_comment1": "port should not be declared when commiting",
                  "port": port,
              }
            port_object = json.dumps(dynamic_port, indent=1)
            with open(os.path.join("electron/src/lib/flaskserverport.json"), "w") as outfile:
                outfile.write(port_object)

        electron = open_url("/simulator?port=%d" % port)
        electron.wait()
        api_server.stop()
        api_server.join()

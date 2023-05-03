# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

import json
import sys
import os

from .base import InkstitchExtension
from ..api import APIServer
from ..gui import open_url


class Preferences(InkstitchExtension):
    '''
    This saves embroider settings into the metadata of the file
    '''

    def __init__(self, *args, **kwargs):
        InkstitchExtension.__init__(self, *args, **kwargs)
        self.arg_parser.add_argument("-c", "--collapse_len_mm",
                                     action="store", type=float,
                                     dest="collapse_length_mm", default=3.0,
                                     help="max collapse length (mm)")
        self.arg_parser.add_argument("-l", "--min_stitch_len_mm",
                                     action="store", type=float,
                                     dest="min_stitch_len_mm", default=0,
                                     help="minimum stitch length (mm)")

    def effect(self):
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

        electron = open_url("/preferences?port=%d" % port)
        electron.wait()
        api_server.stop()
        api_server.join()

        # self.metadata = self.get_inkstitch_metadata()
        # self.metadata['collapse_len_mm'] = self.options.collapse_length_mm
        # self.metadata['min_stitch_len_mm'] = self.options.min_stitch_len_mm

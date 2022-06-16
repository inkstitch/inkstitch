# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from .base import InkstitchExtension


class EmbroiderSettings(InkstitchExtension):
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
        self.metadata = self.get_inkstitch_metadata()
        self.metadata['collapse_len_mm'] = self.options.collapse_length_mm
        self.metadata['min_stitch_len_mm'] = self.options.min_stitch_len_mm

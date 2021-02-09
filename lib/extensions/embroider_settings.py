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

    def effect(self):
        self.metadata = self.get_inkstitch_metadata()
        self.metadata['collapse_len_mm'] = self.options.collapse_length_mm

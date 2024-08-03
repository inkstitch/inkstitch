from .elements import EmbroideryElement


stitch_layers = None


class SewStack(EmbroideryElement):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = self.get_json_param('sew_stack_config')
        self.load_layers()
        self.init_stitch_layers()

    @staticmethod
    def init_stitch_layers():
        global stitch_layers
        if stitch_layers is None:
            # We're waiting until now to import this so that it doesn't slow down
            # the initial startup.
            from . import stitch_layers as _stitch_layers
            stitch_layers = _stitch_layers

    def sew_stack_only(self):
        """Should we only process the SewStack for this object and skip legacy Params-based EmbroideryElements?"""
        return self.get_boolean_param('sew_stack_only', False)

    def load_layers(self):

        return []

    def save(self):
        """Gather configuration from all layers and save sew_stack_config attribute"""
        pass

    def to_stitch_groups(self, last_stitch_group):
        return []

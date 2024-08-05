from .elements import EmbroideryElement
from .utils.dotdict import DefaultDotDict

stitch_layers = None


class SewStack(EmbroideryElement):
    DEFAULT_CONFIG = {
        "layers": []
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = DefaultDotDict(self.get_json_param('sew_stack'), defaults=self.DEFAULT_CONFIG)

        self.load_layers()

    @staticmethod
    def init_stitch_layers():
        global stitch_layers
        if stitch_layers is None:
            # We're waiting until now to import this so that it doesn't slow down
            # the initial startup.
            from . import stitch_layers as _stitch_layers
            stitch_layers = _stitch_layers

    @property
    def sew_stack_only(self):
        """Should we only process the SewStack for this object and skip legacy Params-based EmbroideryElements?"""
        return self.get_boolean_param('sew_stack_only', False)

    def load_layers(self):
        self.init_stitch_layers()

        self.layers = []
        for layer_config in self.config.layers:
            layer_class = stitch_layers.by_id[layer_config.layer_id]
            self.layers.append(layer_class(self, layer_config))

    def save(self):
        """Gather configuration from all layers and save sew_stack_config attribute"""
        pass

    def uses_previous_stitch(self):
        if self.config.layers:
            return self.config.layers[0].uses_previous_stitch_group
        else:
            return False

    def get_cache_key_data(self, previous_stitch):
        return self.config.layers

    def get_default_random_seed(self):
        return self.node.get_id()

    @property
    def stroke_color(self):
        return self.get_style("stroke")

    def to_stitch_groups(self, previous_stitch_group):
        stitch_groups = []

        for layer in self.layers:
            stitch_groups.extend(layer.embroider(previous_stitch_group))

            if stitch_groups:
                previous_stitch_group = stitch_groups[-1]

        return stitch_groups

import wx

from . import stitch_layers
from ..debug.debug import debug
from ..elements import EmbroideryElement
from ..utils import DotDict


class SewStack(EmbroideryElement):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config = DotDict(self.get_json_param('sew_stack', default=dict(layers=list())))

        self.layers = []
        for layer_config in self.config.layers:
            layer_class = stitch_layers.by_id[layer_config.layer_id]
            self.layers.append(layer_class(sew_stack=self, config=layer_config))
            debug.log(f"layer name: {self.layers[-1].name}")

    @property
    def sew_stack_only(self):
        """Should we only process the SewStack for this object and skip legacy Params-based EmbroideryElements?"""
        return self.get_boolean_param('sew_stack_only', False)

    def move_layer(self, from_index, to_index):
        layer = self.config.layers.pop(from_index)
        self.config.layers.insert(to_index, layer)

    def append_layer(self, layer_class):
        new_layer = self.layers.append(layer_class(sew_stack=self, config={}))
        return new_layer

    def delete_layer(self, index):
        del self.layers[index]

    def save(self):
        """Save current configuration of layers to sew_stack SVG attribute"""
        self.config.layers = [layer.config for layer in self.layers]
        self.set_json_param("sew_stack", self.config)

    def uses_previous_stitch(self):
        if self.config.layers:
            return self.config.layers[0].uses_previous_stitch_group
        else:
            return False

    def get_cache_key_data(self, previous_stitch):
        return self.config.layers

    def get_default_random_seed(self):
        return self.node.get_id() or ""

    def to_stitch_groups(self, previous_stitch_group):
        stitch_groups = []
        for layer in self.layers:
            if layer.enabled:
                stitch_groups.extend(layer.embroider(stitch_groups[-1] if stitch_groups else None))

        return stitch_groups

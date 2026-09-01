from . import stitch_layers
from ..debug.debug import debug
from ..elements import EmbroideryElement
from ..utils import DotDict


class SewStack(EmbroideryElement):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.config = DotDict(self.get_json_param('sew_stack', default=dict(layers=list())))
        self.sew_stack_only = self.get_boolean_param('sew_stack_only', False)

        self.layers = []
        for layer_config in self.config.layers:
            layer_class = stitch_layers.by_id[layer_config.layer_id]
            self.layers.append(layer_class(sew_stack=self, config=layer_config))
            debug.log(f"layer name: {self.layers[-1].name}")

    def move_layer(self, from_index, to_index):
        layer = self.layers.pop(from_index)
        self.layers.insert(to_index, layer)

    def append_layer(self, layer_class):
        new_layer = layer_class(sew_stack=self, config={})
        self.layers.append(new_layer)
        return new_layer

    def delete_layer(self, index):
        del self.layers[index]

    def save(self):
        """Save current configuration of layers to sew_stack SVG attribute"""
        self.config.layers = [layer.config for layer in self.layers]
        self.set_json_param("sew_stack", self.config)
        self.set_param("sew_stack_only", self.sew_stack_only)

    def uses_previous_stitch(self):
        if self.config.layers:
            return self.config.layers[0].uses_previous_stitch_group
        else:
            return False

    @property
    def first_stitch(self):
        # For now, we'll return None, but later on we might let the first
        # StitchLayer set the first_stitch.
        return None

    def uses_next_element(self):
        return True

    def get_cache_key_data(self, previous_stitch, next_element):
        return self.config.layers

    def get_default_random_seed(self):
        return self.node.get_id() or ""

    def to_stitch_groups(self, previous_stitch_group=None, next_element=None):
        stitch_groups = []
        for layer in self.layers:
            if layer.enabled:
                this_layer_previous_stitch_group = this_layer_next_element = None

                if layer is self.layers[0]:
                    this_layer_previous_stitch_group = previous_stitch_group
                else:
                    this_layer_previous_stitch_group = stitch_groups[-1]

                if layer is self.layers[-1]:
                    this_layer_next_element = next_element

                stitch_groups.extend(layer.embroider(this_layer_previous_stitch_group, this_layer_next_element))

        return stitch_groups

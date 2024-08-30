from ...utils import coordinate_list_to_point_list
from ...utils.dotdict import DotDict


class StitchLayer:
    # can be overridden in child class
    uses_last_stitch_group = False

    def __init__(self, *args, config=None, sew_stack=None, change_callback=None, **kwargs):
        self.config = DotDict(config)
        self.element = sew_stack
        self.change_callback = change_callback

        super().__init__(*args, **kwargs)

    @classmethod
    @property
    def layer_id(my_class):
        """Get the internal layer ID

        Internal layer name is not shown to users and is used to identify the
        layer class when loading a SewStack.

        Example:
            class RunningStitchLayer(StitchLayer): ...
            layer_id = RunningStitch
        """

        if my_class.__name__.endswith('Layer'):
            return my_class.__name__[:-5]
        else:
            return my_class.__name__

    @property
    def name(self):
        return self.config.get('name', self.default_layer_name)

    @name.setter
    def name(self, value):
        self.config.name = value

    @property
    def default_layer_name(self):
        # defaults to the same as the layer type name but can be overridden in a child class
        return self.layer_type_name

    @property
    def layer_type_name(self):
        raise NotImplementedError(f"{self.__class__.__name__} must implement type_name property!")

    @property
    def enabled(self):
        return self.config.get('enabled', True)

    def enable(self, enabled=True):
        self.config.enabled = enabled

    @property
    def paths(self):
        return [coordinate_list_to_point_list(path) for path in self.element.paths]

    @property
    def stroke_color(self):
        return self.element.get_style("stroke")

    @property
    def fill_color(self):
        return self.element.get_style("stroke")

    def to_stitch_groups(self, *args):
        raise NotImplementedError(f"{self.__class__.__name__} must implement to_stitch_groups()!")

    def embroider(self, last_stitch_group):
        if self.uses_last_stitch_group:
            return self.to_stitch_groups(last_stitch_group)
        else:
            return self.to_stitch_groups()

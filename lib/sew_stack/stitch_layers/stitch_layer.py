from .utils import PathUtilsMixin
from ...utils.dotdict import DotDict


class StitchLayer(PathUtilsMixin):
    # can be overridden in child class
    uses_last_stitch_group = False

    def __init__(self, *args, config=None, **kwargs):
        super().__init__(*args, **kwargs)

        if config is None:
            config = {"enabled": True}
        self.config = DotDict(config)

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
        return self.config.enabled

    def enable(self, enabled=True):
        self.config.enabled = enabled

    def to_stitch_groups(self, *args):
        raise NotImplementedError(f"{self.__class__.__name__} must implement to_stitch_groups()!")

    def embroider(self, last_stitch_group):
        if self.uses_last_stitch_group:
            return self.to_stitch_groups(last_stitch_group)
        else:
            return self.to_stitch_groups()

from .utils import ConfigMixin, PathUtilsMixin


class StitchLayer(PathUtilsMixin, ConfigMixin):
    DEFAULT_CONFIG = {
        "enabled": True,

        # override in child class to set default layer name
        "name": "",
    }

    # can be overridden in child class
    uses_last_stitch_group = False

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
        return self.config.name

    @property
    def type_name(self):
        raise NotImplementedError(f"{self.__class__.__name__} must implement type_name property!")

    @name.setter
    def name(self, value):
        self.config.name = value

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

from .utils import ConfigMixin, PathUtilsMixin


class StitchLayer(PathUtilsMixin, ConfigMixin):
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

    def get_default_layer_name(self):
        """Get the default name for this type of layer, translated to the user's language

        Override this in every subclass.
        """

        # Example implementation:
        # return _("Running Stitch")

        raise NotImplementedError(f"{self.__class__.__name__} must implement get_default_layer_name()!")

    @property
    def name(self):
        return self.config.name

    @name.setter
    def name(self, value):
        self.config.name = value

    @property
    def uses_previous_stitch_group(self):
        # Can be overridden in child class
        return False

    def to_stitch_groups(self, *args):
        raise NotImplementedError(f"{self.__class__.__name__} must implement to_stitch_groups()!")

    def embroider(self, last_stitch_group):
        if self.uses_last_stitch_group:
            return self.to_stitch_groups(last_stitch_group)
        else:
            return self.to_stitch_groups()

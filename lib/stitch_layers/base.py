class StitchLayer:
    def __init__(self, config):
        self.config = config

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
        return self.config.get('name', self.get_default_layer_name())

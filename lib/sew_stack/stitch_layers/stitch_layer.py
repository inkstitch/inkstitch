from typing import Type

from ...utils import coordinate_list_to_point_list
from ...utils.classproperty import classproperty
from ...utils.dotdict import DotDict
from .stitch_layer_editor import StitchLayerEditor


class StitchLayer:
    # must be overridden in child classes and set to a subclass of StitchLayerEditor
    editor_class: Type[StitchLayerEditor] = None  # type:ignore[assignment]

    # not to be overridden in child classes
    _defaults = None

    def __init__(self, *args, config, sew_stack=None, change_callback=None, **kwargs):
        self.config = DotDict(self.defaults)
        self.config.layer_id = self.layer_id
        self.config.update(config)
        self.element = sew_stack

        super().__init__(*args, **kwargs)

    @classproperty
    def defaults(cls):
        # Implement this in each child class.  Return a dict with default
        # values for all properties used in this layer.
        raise NotImplementedError(f"{cls.__name__} must implement class property: defaults")

    @classproperty
    def layer_id(my_class):
        """Get the internal layer ID

        Internal layer ID is not shown to users and is used to identify the
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
        return self.element.stroke_color

    @property
    def fill_color(self):
        return self.element.fill_color

    def to_stitch_groups(self, *args):
        raise NotImplementedError(f"{self.__class__.__name__} must implement to_stitch_groups()!")

    def embroider(self, last_stitch_group, next_element=None):
        return self.to_stitch_groups(last_stitch_group, next_element)

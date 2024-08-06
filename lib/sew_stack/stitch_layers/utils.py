from ...utils import coordinate_list_to_point_list
from ...utils.dotdict import DefaultDotDict


class PathUtilsMixin:
    def __init__(self, *args, **kwargs):
        self.element = kwargs.pop('sew_stack')
        super().__init__(*args, **kwargs)

    @property
    def paths(self):
        return [coordinate_list_to_point_list(path) for path in self.element.paths]

    @property
    def stroke_color(self):
        return self.element.get_style("stroke")

    @property
    def fill_color(self):
        return self.element.get_style("stroke")


class ConfigMixin:
    def __init__(self, *args, **kwargs):
        self.config = DefaultDotDict(kwargs.pop('config', {}))
        super().__init__(*args, **kwargs)

        # merge in default configs from all parent classes
        for ancestor_class in reversed(self.__class__.__mro__):
            try:
                self.config.update_defaults(ancestor_class.DEFAULT_CONFIG)
            except AttributeError:
                # ignore ancestor classes that don't have DEFAULT_CONFIG
                pass


class RandomizationMixin(PathUtilsMixin, ConfigMixin):
    DEFAULT_CONFIG = dict(
        random_seed=None
    )

    def get_random_seed(self):
        if self.config.random_seed is None:
            self.config.random_seed = self.element.get_default_random_seed() or ""

        return self.config.random_seed

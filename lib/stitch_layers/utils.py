from lib.utils import coordinate_list_to_point_list


class NodeUtilsMixin:
    @property
    def paths(self):
        return [coordinate_list_to_point_list(path) for path in self.node.paths]


class RandomizationMixin:
    DEFAULT_CONFIG = dict(
        random_seed=None
    )

    def get_random_seed(self):
        if self.config.random_seed is None:
            self.config.random_seed = self.node.get_default_random_seed() or ""

        return self.config.random_seed

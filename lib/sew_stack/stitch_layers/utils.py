from ...utils import coordinate_list_to_point_list


# Functionality for StitchLayers is broken down into separate "mix-in" classes.
# This allows us to divide up the implementation so that we don't end up with
# one gigantic StitchLayer class.  Individual StitchLayer subclasses can include
# just the functionality they need.
#
# Python multiple inheritance is cool, and as long as we include a super().__init__()
# call in every __init__() method we implement, we'll ensure that all mix-in
# classes' constructors get called.  Skipping implementing the __init__() method in a
# mix-in class is also allowed.

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


class RandomizationMixin:
    def get_random_seed(self):
        if self.config.random_seed is None:
            self.config.random_seed = self.element.get_default_random_seed() or ""

        return self.config.random_seed

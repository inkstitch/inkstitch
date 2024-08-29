import wx.propgrid

from .property_grid import Category, Property
from ....i18n import _


class RandomSeedProperty(wx.propgrid.IntProperty):
    pass


class RandomizationMixin:
    def get_random_seed(self):
        if 'random_seed' not in self.config:
            self.config.random_seed = self.element.get_default_random_seed() or ""

        return self.config.random_seed

    @classmethod
    @property
    def randomization_properties(cls):
        return Category(_("Randomization")).children(
            Property("random_seed", _("Random seed"), type=RandomSeedProperty)
        )

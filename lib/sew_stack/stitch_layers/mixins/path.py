from ..stitch_layer_editor import Category, Property
from ....i18n import _
from ....utils import DotDict, Point


class PathPropertiesMixin:
    @classmethod
    def path_properties(cls):
        return Category(_("Path")).children(
            Property("reverse_path", _("Reverse path"), type=bool,
                     help=_("Reverse the path when stitching this layer."))
        )


class PathMixin:
    config: DotDict
    paths: 'list[list[Point]]'

    def get_paths(self):
        paths = self.paths

        if self.config.reverse_path:
            paths.reverse()
            for path in paths:
                path.reverse()

        return paths

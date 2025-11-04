from .protocol import LayerProtocol
from ..stitch_layer_editor import Category, Property
from ....i18n import _


class PathPropertiesMixin:
    @classmethod
    def path_properties(cls):
        return Category(_("Path")).children(
            Property("reverse_path", _("Reverse path"), type=bool,
                     help=_("Reverse the path when stitching this layer."))
        )


class PathMixin:
    @classmethod
    def path_defaults(cls):
        return dict(
            reverse_path=False,
        )

    def get_paths(self: LayerProtocol):
        paths = self.paths

        if self.config.reverse_path:
            paths.reverse()
            for path in paths:
                path.reverse()

        return paths

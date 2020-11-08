from ..i18n import _
from ..svg.path import get_node_transform
from .element import EmbroideryElement
from .validation import ObjectTypeWarning


class ImageTypeWarning(ObjectTypeWarning):
    name = _("Image")
    description = _("Ink/Stitch can't work with objects like images.")
    steps_to_solve = [
        _('* Convert your image into a path: Path > Trace Bitmap... (Shift+Alt+B) '
          '(further steps might be required)'),
        _('* Alternatively redraw the image with the pen (P) or bezier (B) tool')
    ]


class ImageObject(EmbroideryElement):

    def center(self):
        transform = get_node_transform(self.node.getparent())
        center = self.node.bounding_box(transform).center
        return center

    def validation_warnings(self):
        yield ImageTypeWarning(self.center())

    def to_patches(self, last_patch):
        return []

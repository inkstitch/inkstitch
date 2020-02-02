from simpletransform import applyTransformToPoint

from ..i18n import _
from ..svg import get_node_transform
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
        point = [float(self.node.get('x', 0)), float(self.node.get('y', 0))]
        point = [(point[0]+(float(self.node.get('width', 0))/2)), (point[1]+(float(self.node.get('height', 0))/2))]

        transform = get_node_transform(self.node)
        applyTransformToPoint(transform, point)

        return point

    def validation_warnings(self):
        yield ImageTypeWarning(self.center())

    def to_patches(self, last_patch):
        return []

from simpletransform import applyTransformToPoint

from ..i18n import _
from ..svg import get_node_transform
from .element import EmbroideryElement
from .validation import ObjectTypeWarning


class TextTypeWarning(ObjectTypeWarning):
    name = _("Text")
    description = _("Ink/Stitch cannot work with objects like text.")
    steps_to_solve = [
        _('* Text: Create your own letters or try the lettering tool:'),
        _('- Extensions > Ink/Stitch > Lettering')
    ]


class TextObject(EmbroideryElement):

    def center(self):
        point = [float(self.node.get('x', 0)), float(self.node.get('y', 0))]

        transform = get_node_transform(self.node)
        applyTransformToPoint(transform, point)

        return point

    def validation_warnings(self):
        yield TextTypeWarning(self.center())

    def to_patches(self, last_patch):
        return []

from ..i18n import _
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

    def pointer(self):
        transform = self.node.composed_transform()*-self.node.transform
        point = self.node.bounding_box(transform).center

        return point

    def validation_warnings(self):
        yield TextTypeWarning(self.pointer())

    def to_patches(self, last_patch):
        return []

from ..stitch_plan import patches_to_stitch_plan
from ..svg import render_stitch_plan
from .base import InkstitchExtension


class StitchPlanPreview(InkstitchExtension):
    def effect(self):
        # delete old stitch plan
        svg = self.document.getroot()
        layer = svg.find(".//*[@id='__inkstitch_stitch_plan__']")
        if layer is not None:
            del layer[:]

        # create new stitch plan
        if not self.get_elements():
            return

        realistic = False
        patches = self.elements_to_patches(self.elements)
        stitch_plan = patches_to_stitch_plan(patches)
        render_stitch_plan(svg, stitch_plan, realistic)

        # translate stitch plan to the right side of the canvas
        layer = svg.find(".//*[@id='__inkstitch_stitch_plan__']")
        layer.set('transform', 'translate(%s)' % svg.get('viewBox', '0 0 800 0').split(' ')[2])

from inkex.tester import TestCase
from inkex import SvgDocumentElement, Rectangle
from inkex.tester.svg import svg

from lib.svg.tags import INKSTITCH_ATTRIBS
from lib import output
from lib.stitch_plan.stitch_plan import StitchPlan, stitch_groups_to_stitch_plan
from lib.elements.utils import node_to_elements


class OutputTest(TestCase):
    def _get_output(self, svg: SvgDocumentElement, format: str) -> bytes:
        # TODO: support SVGs with more than one element
        # (turn InkstitchExtension.elements_to_stitch_groups into a function so we can use it here?)
        assert len(svg) == 1
        [element] = node_to_elements(svg[0])
        stitch_groups = element.embroider(None)
        stitch_plan = stitch_groups_to_stitch_plan(stitch_groups)
        path = self.temp_file(suffix=f".{format}")
        output.write_embroidery_file(path, stitch_plan, svg)
        with open(path, "rb") as f:
            return f.read()

    def test_jef_output_does_not_change(self):
        root: SvgDocumentElement = svg()
        rect = root.add(
            Rectangle(
                attrib={
                    "width": "10",
                    "height": "10",
                }
            )
        )
        output1 = self._get_output(root, "jef")
        output2 = self._get_output(root, "jef")
        assert output1 == output2

    def test_jef_output_includes_trims(self):
        root: SvgDocumentElement = svg()
        rect = root.add(
            Rectangle(
                attrib={
                    "width": "10",
                    "height": "10",
                }
            )
        )
        output1 = self._get_output(root, "jef")

        rect.attrib[INKSTITCH_ATTRIBS["trim_after"]] = "true"

        output2 = self._get_output(root, "jef")
        assert output1 != output2

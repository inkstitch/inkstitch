from inkex import Group, Rectangle, Style
from inkex.tester import TestCase
from inkex.tester.svg import svg

from lib.elements import FillStitch, nodes_to_elements, iterate_nodes

from .utils import element_count


class ElementsUtilsTest(TestCase):
    # These tests test two functions at once, but they're sort of complimentary.
    # Might suggest that they could be combined in a later refactor?
    def test_iterate_nodes_to_elements(self) -> None:
        root = svg()
        g = root.add(Group())
        rect = g.add(Rectangle(attrib={
            "width": "10",
            "height": "10"
        }))
        hidden_rect = g.add(Rectangle(attrib={  # noqa: F841
            "width": "10",
            "height": "10",
            "style": "display:none"
        }))
        hidden_group = g.add(Group(attrib={
            "style": "display:none"
        }))
        child_of_hidden = hidden_group.add(Rectangle(attrib={  # noqa: F841
            "width": "10",
            "height": "10",
        }))

        elements = nodes_to_elements(iterate_nodes(g))
        self.assertEqual(len(elements), element_count())
        self.assertEqual(type(elements[0]), FillStitch)
        self.assertEqual(elements[0].node, rect)

    def test_iterate_nodes_to_elements_root_embroiderable(self) -> None:
        """ Case where the root node is directly embroiderable """
        root = svg()
        rect = root.add(Rectangle(attrib={
            "width": "10",
            "height": "10"
        }))

        elements = nodes_to_elements(iterate_nodes(rect))
        self.assertEqual(len(elements), element_count())
        self.assertEqual(type(elements[0]), FillStitch)
        self.assertEqual(elements[0].node, rect)

        # Now make the element hidden: It shouldn't return an element
        rect.style = rect.style + Style({"display": "none"})

        elements = nodes_to_elements(iterate_nodes(rect))
        self.assertEqual(len(elements), 0)

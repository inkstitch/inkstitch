from lib.elements import utils, FillStitch
from inkex import Rectangle, Group, Style
from inkex.tester import TestCase
from inkex.tester.svg import svg


class ElementsUtilsTest(TestCase):
    def test_node_and_children_to_elements(self):
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

        elements = utils.node_and_children_to_elements(g)
        self.assertEqual(len(elements), 1)
        self.assertEqual(type(elements[0]), FillStitch)
        self.assertEqual(elements[0].node, rect)

    def test_node_and_children_to_elements_root_embroiderable(self):
        """ Test node_and_children_to_elements where the the node passed is directly embroiderable """
        root = svg()
        rect = root.add(Rectangle(attrib={
            "width": "10",
            "height": "10"
        }))

        elements = utils.node_and_children_to_elements(rect)
        self.assertEqual(len(elements), 1)
        self.assertEqual(type(elements[0]), FillStitch)
        self.assertEqual(elements[0].node, rect)

        # Now make the element hidden: It shouldn't return an element
        rect.style = rect.style + Style({"display": "none"})

        elements = utils.node_and_children_to_elements(rect)
        self.assertEqual(len(elements), 0)

from lib.elements import Clone, EmbroideryElement
from lib.svg.tags import INKSTITCH_ATTRIBS
from inkex import SvgDocumentElement, Rectangle, Circle, Group, Use, Transform, TextElement
from inkex.tester import TestCase
from inkex.tester.svg import svg

from typing import Optional

from math import sqrt


def element_fill_angle(element: EmbroideryElement) -> Optional[float]:
    angle = element.node.get(INKSTITCH_ATTRIBS['angle'])
    if angle is not None:
        angle = float(angle) % 180
    return angle


class CloneElementTest(TestCase):
    def assertAngleAlmostEqual(self, a, b):
        self.assertAlmostEqual(a % 180, b % 180, 4)

    def test_not_embroiderable(self):
        root: SvgDocumentElement = svg()
        text = root.add(TextElement())
        text.text = "Can't embroider this!"
        use = root.add(Use())
        use.href = text

        clone = Clone(use)
        stitch_groups = clone.to_stitch_groups(None)
        self.assertEqual(len(stitch_groups), 0)

    # These tests make sure the element cloning works as expected, using the `clone_elements` method.

    def test_basic(self):
        root: SvgDocumentElement = svg()
        rect = root.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
            INKSTITCH_ATTRIBS["angle"]: "30"
        }))
        use = root.add(Use())
        use.href = rect

        clone = Clone(use)
        with clone.clone_elements() as elements:
            self.assertEqual(len(elements), 1)
            self.assertAlmostEqual(element_fill_angle(elements[0]), 30)

    def test_angle_rotated(self):
        root: SvgDocumentElement = svg()
        rect = root.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
            INKSTITCH_ATTRIBS["angle"]: "30"
        }))
        use = root.add(Use())
        use.href = rect
        use.set('transform', Transform().add_rotate(20))

        clone = Clone(use)
        with clone.clone_elements() as elements:
            self.assertEqual(len(elements), 1)
            self.assertAngleAlmostEqual(element_fill_angle(elements[0]), 10)

    def test_angle_flipped(self):
        root: SvgDocumentElement = svg()
        rect = root.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
            INKSTITCH_ATTRIBS["angle"]: "30"
        }))
        use = root.add(Use())
        use.href = rect
        use.set('transform', Transform().add_scale(-1, 1))

        clone = Clone(use)
        with clone.clone_elements() as elements:
            self.assertEqual(len(elements), 1)
            self.assertAngleAlmostEqual(element_fill_angle(elements[0]), -30)

    def test_angle_flipped_rotated(self):
        root: SvgDocumentElement = svg()
        rect = root.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
            INKSTITCH_ATTRIBS["angle"]: "30"
        }))
        use = root.add(Use())
        use.href = rect
        use.set('transform', Transform().add_rotate(20).add_scale(-1, 1))

        clone = Clone(use)
        with clone.clone_elements() as elements:
            self.assertEqual(len(elements), 1)
            # Fill angle goes from 30 -> -30 after flip -> -50 after rotate
            self.assertAngleAlmostEqual(element_fill_angle(elements[0]), -50)

    def test_angle_non_uniform_scale(self):
        """
        The angle isn't *as* well-defined for non-rotational scales, but we try to follow how the slope will be altered.
        """
        root: SvgDocumentElement = svg()
        rect = root.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
            INKSTITCH_ATTRIBS["angle"]: "30"
        }))
        use = root.add(Use())
        use.href = rect
        use.set('transform', Transform().add_rotate(10).add_scale(1, -sqrt(3)))

        clone = Clone(use)
        with clone.clone_elements() as elements:
            self.assertEqual(len(elements), 1)
            # Slope of the stitching goes from tan(30deg) = 1/sqrt(3) to -sqrt(3)/sqrt(3) = tan(-45deg),
            # then rotated another -10 degrees to -55
            self.assertAngleAlmostEqual(element_fill_angle(elements[0]), -55)

    def test_transform_inherits_from_cloned_element(self):
        """
        Elements cloned by cloned_elements need to inherit their transform from their href'd element and their use to match what's shown.
        """
        root: SvgDocumentElement = svg()
        rect = root.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
            INKSTITCH_ATTRIBS["angle"]: "30",
        }))
        rect.set('transform', Transform().add_scale(2, 2))
        use = root.add(Use())
        use.href = rect
        use.set('transform', Transform().add_translate((5, 10)))

        clone = Clone(use)
        with clone.clone_elements() as elements:
            self.assertEqual(len(elements), 1)
            self.assertTransformEqual(
                elements[0].node.composed_transform(),
                Transform().add_translate((5, 10)).add_scale(2, 2))

    def test_transform_inherits_from_tree(self):
        root: SvgDocumentElement = svg()
        g1 = root.add(Group())
        g1.set('transform', Transform().add_translate((0, 5)).add_rotate(5))
        rect = g1.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
            INKSTITCH_ATTRIBS["angle"]: "30",
        }))
        rect.set('transform', Transform().add_scale(2, 2))
        use = root.add(Use())
        use.href = g1
        use.set('transform', Transform().add_translate((5, 10)))

        clone = Clone(use)
        with clone.clone_elements() as elements:
            self.assertEqual(len(elements), 1)
            self.assertTransformEqual(
                elements[0].node.composed_transform(),
                Transform().add_translate((5, 10))  # use
                .add_translate((0, 5)).add_rotate(5)  # g1
                .add_scale(2, 2),  # rect
                5)

    def test_transform_inherits_from_tree_up_tree(self):
        root: SvgDocumentElement = svg()
        g1 = root.add(Group())
        g1.set('transform', Transform().add_translate((0, 5)).add_rotate(5))
        rect = g1.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
            INKSTITCH_ATTRIBS["angle"]: "30",
        }))
        rect.set('transform', Transform().add_scale(2, 2))
        circ = g1.add(Circle())
        circ.radius = 5
        g2 = root.add(Group())
        g2.set('transform', Transform().add_translate((1, 2)).add_scale(0.5, 1))
        use = g2.add(Use())
        use.href = g1
        use.set('transform', Transform().add_translate((5, 10)))

        clone = Clone(use)
        with clone.clone_elements() as elements:
            self.assertEqual(len(elements), 2)
            self.assertTransformEqual(
                elements[0].node.composed_transform(),
                Transform().add_translate((1, 2)).add_scale(0.5, 1)  # g2
                .add_translate((5, 10))  # use
                .add_translate((0, 5)).add_rotate(5)  # g1
                .add_scale(2, 2),  # rect
                5)
            self.assertTransformEqual(
                elements[1].node.composed_transform(),
                Transform().add_translate((1, 2)).add_scale(0.5, 1)  # g2
                .add_translate((5, 10))  # use
                .add_translate((0, 5)).add_rotate(5),  # g1
                5)

    def test_clone_fill_angle_not_specified(self):
        root: SvgDocumentElement = svg()
        rect = root.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
            INKSTITCH_ATTRIBS["angle"]: "30"
        }))
        use = root.add(Use())
        use.href = rect
        use.set('transform', Transform().add_rotate(20))

        clone = Clone(use)
        self.assertEqual(clone.clone_fill_angle, None)

    def test_clone_fill_angle(self):
        root: SvgDocumentElement = svg()
        rect = root.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
            INKSTITCH_ATTRIBS["angle"]: "30"
        }))
        use = root.add(Use())
        use.href = rect
        use.set(INKSTITCH_ATTRIBS["angle"], 42)
        use.set('transform', Transform().add_rotate(20))

        clone = Clone(use)
        self.assertEqual(clone.clone_fill_angle, 42)

        with clone.clone_elements() as elements:
            self.assertEqual(len(elements), 1)
            self.assertAngleAlmostEqual(element_fill_angle(elements[0]), 42)

    def test_angle_manually_flipped(self):
        root: SvgDocumentElement = svg()
        rect = root.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
            INKSTITCH_ATTRIBS["angle"]: "30"
        }))
        use = root.add(Use())
        use.href = rect
        use.set('transform', Transform().add_rotate(20))
        use.set(INKSTITCH_ATTRIBS["flip_angle"], True)

        clone = Clone(use)
        self.assertTrue(clone.flip_angle)
        with clone.clone_elements() as elements:
            self.assertEqual(len(elements), 1)
            self.assertAngleAlmostEqual(element_fill_angle(elements[0]), -10)

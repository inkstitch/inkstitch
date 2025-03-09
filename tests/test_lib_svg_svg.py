from lib.svg.svg import point_upwards

from inkex import Rectangle, Transform, PathElement
from inkex.tester import TestCase
from inkex.tester.svg import svg


class LibSvgSvgTest(TestCase):
    def test_point_upwards(self) -> None:
        root = svg()
        rect = root.add(Rectangle(attrib={
            "width": "10",
            "height": "10",
            "x": "10",
            "y": "20"
        }))
        rect.transform = Transform().add_rotate(-45)

        point_upwards(rect)

        self.assertTransformEqual(
            rect.transform,
            Transform().add_translate(Transform().add_rotate(-45).apply_to_point((10, 20))),
            4
        )

    def test_point_upwards_mirrored(self) -> None:
        root = svg()
        rect = root.add(PathElement(attrib={
            "d": "M 0,0 L 10,0 0,5 Z",
        }))
        rect.transform = Transform().add_rotate(-45).add_scale(-1, 1)

        point_upwards(rect)

        self.assertTransformEqual(
            rect.transform,
            Transform(),
            4
        )

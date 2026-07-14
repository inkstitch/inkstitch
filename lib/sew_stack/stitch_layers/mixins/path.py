from copy import copy
from typing import Callable

from ....i18n import _
from ....stitch_plan.stitch import Stitch
from ....stitch_plan.stitch_group import StitchGroup
from ....utils.geometry import Point
from ..stitch_layer_editor import Category, Property
from .protocol import LayerProtocol


class PathPropertiesMixin:
    @classmethod
    def path_properties(cls):
        return Category(_("Path")).children(
            Property(
                "reverse_path", _("Reverse path"), type=bool,
                help=_("Reverse the path when stitching this layer.")
            ),
            Category(_("Repeats")).children(
                Property(
                    "repeats", _("Repeats"),
                    help=_('Defines how many times to run down and back along the path.'),
                    type=int,
                    min=1,
                ),
                Property(
                    "repeat_stitches", _("Repeat exact stitches"),
                    type=bool,
                    help=_(
                        'Should the exact same stitches be repeated in each pass?  ' +
                        'If unchecked, different randomization settings are applied on each pass.'
                    ),
                ),
            )
        )


class PathMixin:
    @classmethod
    def path_defaults(cls):
        return dict(
            reverse_path=False,
            repeats=1,
            repeat_stitches=True,
        )

    def get_num_copies(self):
        if self.config.repeat_stitches:
            # When repeating stitches, we use multiple copies of one pass of running stitch
            return 1
        else:
            # Otherwise, we re-run running stitch every time, so that
            # post-processing such as randomization is different every pass
            return self.config.repeats

    def get_paths(self: LayerProtocol):
        paths = self.paths

        if self.config.reverse_path:
            paths.reverse()
            for path in paths:
                path.reverse()

        return paths

    def stitch_path(
            self: LayerProtocol,
            stitcher: Callable[[list[Point]], list[Stitch]],
            processor: Callable[[list[Stitch]], None],
            path: list[Point]) -> StitchGroup:
        stitches: list[Stitch] = []

        for i in range(self.get_num_copies()):
            if i % 2 == 0:
                this_path = path
            else:
                this_path = list(reversed(path))

            stitches.extend(stitcher(this_path))

        processor(stitches)

        if self.config.repeats > 0 and self.config.repeat_stitches:
            repeated_stitches = []
            for i in range(self.config.repeats):
                if i % 2 == 0:
                    repeated_stitches.extend(copy(stitches))
                else:
                    # reverse every other pass
                    repeated_stitches.extend(reversed(copy(stitches)))
            stitches = repeated_stitches

        return StitchGroup(stitches=stitches, color=self.stroke_color)

    def stitch_paths(
            self: LayerProtocol,
            stitcher: Callable[[list[Point]], list[Stitch]],
            processor: Callable[[list[Stitch]], None]) -> list[StitchGroup]:
        return [self.stitch_path(stitcher, processor, path) for path in self.get_paths()]

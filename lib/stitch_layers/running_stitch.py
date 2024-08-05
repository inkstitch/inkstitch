from .base import StitchLayer
from .utils import RandomizationMixin
from ..stitch_plan import StitchGroup
from ..stitches.running_stitch import running_stitch
from ..svg import PIXELS_PER_MM


class RunningStitchLayer(StitchLayer, RandomizationMixin):
    DEFAULT_CONFIG = dict(
        stitch_length=2,
        stitch_length_jitter_percent=0,
        tolerance=0.2,
        repeats=1,
        repeat_stitches=True
    )

    uses_previous_stitch_group = False

    def num_copies(self):
        if self.config.repeat_stitches:
            # When repeating stitches, we use multiple copies of one pass of running stitch
            return 1
        else:
            # Otherwise, we re-run running stitch every time, so that
            # randomization is different every pass
            return self.config.repeats

    def running_stitch(self, path):
        stitches = []

        for i in range(self.num_copies()):
            if i % 2 == 0:
                this_path = path
            else:
                this_path = reversed(path)

            stitches.extend(running_stitch(
                this_path,
                self.config.stitch_length * PIXELS_PER_MM,
                self.config.tolerance * PIXELS_PER_MM,
                (self.config.stitch_length_jitter_percent > 0),
                self.config.stitch_length_jitter_percent,
                self.get_random_seed()
            ))

        if self.config.repeats > 0 and self.config.repeat_stitches:
            repeated_stitches = []
            for i in range(self.config.repeats):
                if i % 2 == 0:
                    repeated_stitches.extend(stitches)
                else:
                    # reverse every other pass
                    repeated_stitches.extend(reversed(stitches))
            stitches = repeated_stitches

        return StitchGroup(stitches=stitches, color=self.node.stroke_color)

    def to_stitch_groups(self):
        return [self.running_stitch(path) for path in self.paths]

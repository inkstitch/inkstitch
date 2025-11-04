from copy import copy

from ....i18n import _
from ....stitch_plan import StitchGroup
from ....stitches.running_stitch import running_stitch
from ....svg import PIXELS_PER_MM
from ....utils.classproperty import classproperty
from ..mixins.path import PathMixin, PathPropertiesMixin
from ..mixins.randomization import (RandomizationMixin,
                                    RandomizationPropertiesMixin)
from ..stitch_layer import StitchLayer
from ..stitch_layer_editor import (Category, Properties, Property,
                                   StitchLayerEditor)


class RunningStitchLayerEditor(StitchLayerEditor, RandomizationPropertiesMixin, PathPropertiesMixin):
    @classproperty
    def properties(cls):
        return Properties(
            Category(_("Running Stitch"), help=_("Stitch along a path using evenly-spaced stitches.")).children(
                Property("stitch_length", _("Stitch length"),
                         help=_('Length of stitches. Stitches can be shorter according to the stitch tolerance setting.'),
                         min=0.1,
                         unit="mm",
                         ),
                Property("tolerance", _("Tolerance"),
                         help=_('Determines how closely the stitch path matches the SVG path.  ' +
                                'A lower tolerance means stitches will be closer together and ' +
                                'fit the SVG path more precisely.  A higher tolerance means ' +
                                'some corners may be rounded and fewer stitches are needed.'),
                         min=0.01,
                         unit="mm",
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
                        help=_('Should the exact same stitches be repeated in each pass?  ' +
                               'If unchecked, different randomization settings are applied on each pass.'),
                    ),
                ),
                cls.path_properties(),
            ),
            cls.randomization_properties().children(
                Property(
                    "stitch_length_jitter_percent", _('Stitch length variance'),
                    help=_('Enter a percentage.  Stitch length will vary randomly by up to this percentage.'),
                    prefix="±",
                    unit="%",
                ),
            ),
        )


class RunningStitchLayer(StitchLayer, RandomizationMixin, PathMixin):
    editor_class = RunningStitchLayerEditor

    @classproperty
    def defaults(cls):
        defaults = dict(
            name=_("Running Stitch"),
            type_name=_("Running Stitch"),
            stitch_length=2,
            tolerance=0.2,
            stitch_length_jitter_percent=0,
            repeats=1,
            repeat_stitches=True,
        )
        defaults.update(cls.randomization_defaults())
        defaults.update(cls.path_defaults())

        return defaults

    @property
    def layer_type_name(self):
        return _("Running Stitch")

    def get_num_copies(self):
        if self.config.repeat_stitches:
            # When repeating stitches, we use multiple copies of one pass of running stitch
            return 1
        else:
            # Otherwise, we re-run running stitch every time, so that
            # randomization is different every pass
            return self.config.repeats

    def running_stitch(self, path):
        stitches = []

        for i in range(self.get_num_copies()):
            if i % 2 == 0:
                this_path = path
            else:
                this_path = list(reversed(path))

            stitches.extend(running_stitch(
                this_path,
                self.config.stitch_length * PIXELS_PER_MM,
                self.config.tolerance * PIXELS_PER_MM,
                (self.config.stitch_length_jitter_percent > 0),
                self.config.stitch_length_jitter_percent,
                self.get_random_seed()
            ))

        self.offset_stitches(stitches)

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

    def to_stitch_groups(self, previous_stitch_group, next_element):
        return [self.running_stitch(path) for path in self.get_paths()]

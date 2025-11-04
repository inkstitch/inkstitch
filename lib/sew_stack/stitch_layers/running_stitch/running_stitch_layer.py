from ....i18n import _
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
                Property("bean_stitch_repeats", _("Bean Stitch Repeats"),
                         help=_('Backtrack each stitch this many times.  '
                                'A value of 1 would triple each stitch (forward, back, forward).  '
                                'A value of 2 would quintuple each stitch, etc.\n\n'
                                'A pattern with various repeats can be created with a list of values separated by a space.  '
                                'For example, a pattern of 1 2 would triple the first stitch, quintuple the second stitch, '
                                'triple the third, etc.'),
                         min=0,
                         type=int,
                         multi=True,
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
            bean_stitch_repeats=[0],
            tolerance=0.2,
            stitch_length_jitter_percent=0,
        )
        defaults.update(cls.randomization_defaults())
        defaults.update(cls.path_defaults())

        return defaults

    @property
    def layer_type_name(self):
        return _("Running Stitch")

    def running_stitch(self, path):
        return running_stitch(
                path,
                self.config.stitch_length * PIXELS_PER_MM,
                self.config.tolerance * PIXELS_PER_MM,
                (self.config.stitch_length_jitter_percent > 0),
                self.config.stitch_length_jitter_percent,
                self.get_random_seed()
            )

    def to_stitch_groups(self, previous_stitch_group, next_element):
        return self.stitch_paths(self.running_stitch, self.apply_random_stitch_offset)

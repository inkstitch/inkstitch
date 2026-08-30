from ...i18n import _
from ..validation import ValidationError, ValidationWarning

rung_message = _("Each rung should intersect both rails once.")


class NotStitchableError(ValidationError):
    name = _("Not stitchable satin column")
    description = _("A satin column can be build from a single stroke or consists of two rails and optional rungs. "
                    "This satin column has a different setup.")
    steps_to_solve = [
        _('Make sure your satin column is not a combination of multiple satin columns.'),
        _('Go to our website and read how a satin column should look like https://inkstitch.org/docs/stitches/satin-column/'),
    ]


class ClosedPathWarning(ValidationWarning):
    name = _("Rail is a closed path")
    description = _("Rail is a closed path without a definite starting and ending point.")
    steps_to_solve = [
        _('* Select the node where you want the satin to start.'),
        _('* Click on: Break path at selected nodes.')
    ]


class DanglingRungWarning(ValidationWarning):
    name = _("Rung doesn't intersect rails")
    description = _("Satin column: A rung doesn't intersect both rails.") + " " + rung_message


class NoRungWarning(ValidationWarning):
    name = _("Satin has no rungs")
    description = _("Rungs control the stitch direction in satin columns. It is best practice to use them.")
    steps_to_solve = [
        _('* With the selected object press "P" to activate the pencil tool.'),
        _('* Hold "Shift" while drawing a rung.')
    ]


class TooManyIntersectionsWarning(ValidationWarning):
    name = _("Rung intersects too many times")
    description = _("Satin column: A rung intersects a rail more than once.") + " " + rung_message


class StrokeSatinWarning(ValidationWarning):
    name = _("Simple Satin")
    description = _("If you need more control over the stitch directions within this satin column, convert it to a real satin path")
    steps_to_solve = [
        _('* Select the satin path'),
        _('* Run Extensions > Ink/Stitch > Tools: Satin > Stroke to Satin')
    ]


class NarrowSatinWarning(ValidationWarning):
    name = _("Narrow Satin")
    description = _("This element renders as a satin, but it is too narrow.")
    steps_to_solve = [
        _("* Increase stroke width."),
        _("Ink/Stitch will not register elements with a stroke width underneath 0.3 mm as satin, but it is recommended to stay above 1mm."),
    ]


class TwoRungsWarning(ValidationWarning):
    name = _("Satin has exactly two rungs")
    description = _("There are exactly two rungs. This may lead to false rail/rung detection.")
    steps_to_solve = [
        _('* With the selected object press "P" to activate the pencil tool.'),
        _('* Hold "Shift" while drawing a rung.')
    ]


class UnequalPointsWarning(ValidationWarning):
    name = _("Unequal number of points")
    description = _("Satin column: There are no rungs and rails have an unequal number of points.")
    steps_to_solve = [
        _('The easiest way to solve this issue is to add one or more rungs. '),
        _('Rungs control the stitch direction in satin columns.'),
        _('* With the selected object press "P" to activate the pencil tool.'),
        _('* Hold "Shift" while drawing the rung.')
    ]

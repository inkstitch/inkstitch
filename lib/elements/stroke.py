"""Module for Stroke element."""

# Authors: see git history
#
# Copyright (c) 2010 Authors
# Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

from math import ceil

import shapely.geometry as shgeo
from shapely.errors import GEOSException

from ..i18n import _
from ..marker import get_marker_elements
from ..stitch_plan import StitchGroup
from ..stitches.ripple_stitch import ripple_stitch
from ..stitches.running_stitch import bean_stitch, running_stitch, zigzag_stitch
from ..svg import PIXELS_PER_MM
from ..threads import ThreadColor
from ..utils import Point, cache
from ..utils.param import ParamOption
from .element import EmbroideryElement, param
from .validation import ValidationWarning


class MultipleGuideLineWarning(ValidationWarning):
    """Warning for multiple guide lines."""

    name = _("Multiple Guide Lines")
    description = _("This object has multiple guide lines, but only the first one will be used.")
    steps_to_solve = [_("* Remove all guide lines, except for one.")]


class TooNarrowSatinWarning(ValidationWarning):
    """Stroke is too narrow to render as satin."""

    name = _("Too narrow satin")
    description = _("This element renders as running stitch while it has a satin column parameter.")
    steps_to_solve = [
        _("* Increase stroke width."),
        _("Ink/Stitch will not register elements with a stroke width underneath 0.3 mm as satin, but it is recommended to stay above 1mm."),
    ]


class Stroke(EmbroideryElement):
    """Stroke element."""

    name = "Stroke"
    element_name = _("Stroke")

    @property
    @param("satin_column", _("Running stitch along paths"), type="toggle", inverse=True)
    def satin_column(self):
        """Return True if satin column is enabled."""
        return self.get_boolean_param("satin_column")

    @property
    def color(self):
        """Return the color of the stroke."""
        color = self.stroke_color
        if self.cutwork_needle is not None:
            color = ThreadColor(color, description=self.cutwork_needle, chart=self.cutwork_needle)
        return color

    @property
    def cutwork_needle(self):
        """Return cutwork needle number."""
        needle = self.get_int_param("cutwork_needle") or None
        if needle is not None:
            needle = f"Cut {needle}"
        return needle

    _stroke_methods = [
        ParamOption("running_stitch", _("Running Stitch / Bean Stitch")),
        ParamOption("ripple_stitch", _("Ripple Stitch")),
        ParamOption("zigzag_stitch", _("ZigZag Stitch")),
        ParamOption("manual_stitch", _("Manual Stitch")),
    ]

    @property
    @param(
        "stroke_method",
        _("Method"),
        type="combo",
        default=0,
        options=_stroke_methods,
        sort_index=0,
    )
    def stroke_method(self):
        """Return the stroke method."""
        return self.get_param("stroke_method", "running_stitch")

    @property
    @param(
        "repeats",
        _("Repeats"),
        tooltip=_("Defines how many times to run down and back along the path."),
        type="int",
        select_items=[
            ("stroke_method", "running_stitch"),
            ("stroke_method", "ripple_stitch"),
            ("stroke_method", "zigzag_stitch"),
        ],
        default="1",
        sort_index=2,
    )
    def repeats(self):
        """Return the number of repeats."""
        return max(1, self.get_int_param("repeats", 1))

    @property
    @param(
        "bean_stitch_repeats",
        _("Bean stitch number of repeats"),
        tooltip=_(
            "Backtrack each stitch this many times.  "
            "A value of 1 would triple each stitch (forward, back, forward).  "
            "A value of 2 would quintuple each stitch, etc.\n\n"
            "A pattern with various repeats can be created with a list of values separated "
            "by a space."
        ),
        type="str",
        select_items=[
            ("stroke_method", "running_stitch"),
            ("stroke_method", "ripple_stitch"),
            ("stroke_method", "manual_stitch"),
            ("stroke_method", "zigzag_stitch"),
        ],
        default=0,
        sort_index=3,
    )
    def bean_stitch_repeats(self):
        """Return the number of bean stitch repeats."""
        return self.get_multiple_int_param("bean_stitch_repeats", "0")

    @property
    @param(
        "manual_pattern_placement",
        _("Manual stitch placement"),
        tooltip=_("No extra stitches will be added to the original ripple pattern and the running stitch length value will be ignored."),
        type="boolean",
        select_items=[("stroke_method", "ripple_stitch")],
        default=False,
        sort_index=3,
    )
    def manual_pattern_placement(self):
        """Return True if manual pattern placement is enabled."""
        return self.get_boolean_param("manual_pattern_placement", False)

    @property
    @param(
        "running_stitch_length_mm",
        _("Running stitch length"),
        tooltip=_(
            "Length of stitches. Stitches can be shorter according to the stitch tolerance "
            "setting.\n"
            "It is possible to create stitch length patterns by adding multiple values separately."
        ),
        unit="mm",
        type="string",
        select_items=[
            ("stroke_method", "running_stitch"),
            ("stroke_method", "ripple_stitch"),
        ],
        default="2.5",
        sort_index=4,
    )
    def running_stitch_length(self):
        """Return the running stitch length."""
        return [max(value, 0.01) for value in self.get_multiple_float_param("running_stitch_length_mm", "2.5")]

    @property
    @param(
        "running_stitch_tolerance_mm",
        _("Stitch tolerance"),
        tooltip=_(
            "All stitches must be within this distance from the path.  "
            + "A lower tolerance means stitches will be closer together.  "
            + "A higher tolerance means sharp corners may be rounded."
        ),
        unit="mm",
        type="float",
        select_items=[
            ("stroke_method", "running_stitch"),
            ("stroke_method", "ripple_stitch"),
        ],
        default=0.2,
        sort_index=4,
    )
    def running_stitch_tolerance(self):
        """Return the running stitch tolerance."""
        return max(self.get_float_param("running_stitch_tolerance_mm", 0.2), 0.01)

    @property
    @param(
        "enable_random_stitch_length",
        _("Randomize stitch length"),
        tooltip=_(
            "Randomize stitch length and phase instead of dividing evenly or staggering. "
            "This is recommended for closely-spaced curved fills to avoid Moiré artefacts."
        ),
        type="boolean",
        select_items=[
            ("stroke_method", "running_stitch"),
            ("stroke_method", "ripple_stitch"),
        ],
        enables=["random_stitch_length_jitter_percent"],
        default=False,
        sort_index=5,
    )
    def enable_random_stitch_length(self):
        """Return True if random stitch length is enabled."""
        return self.get_boolean_param("enable_random_stitch_length", False)

    @property
    @param(
        "random_stitch_length_jitter_percent",
        _("Random stitch length jitter"),
        tooltip=_("Amount to vary the length of each stitch by when randomizing."),
        unit="± %",
        type="float",
        select_items=[
            ("stroke_method", "running_stitch"),
            ("stroke_method", "ripple_stitch"),
        ],
        default=10,
        sort_index=6,
    )
    def random_stitch_length_jitter(self):
        """Return the random stitch length jitter."""
        return max(self.get_float_param("random_stitch_length_jitter_percent", 10), 0.0) / 100

    @property
    @param(
        "max_stitch_length_mm",
        _("Max stitch length"),
        tooltip=_("Split stitches longer than this."),
        unit="mm",
        type="float",
        select_items=[("stroke_method", "manual_stitch")],
        sort_index=5,
    )
    def max_stitch_length(self):
        """Return the maximum stitch length."""
        max_length = self.get_float_param("max_stitch_length_mm", None)
        if not max_length or max_length <= 0:
            return
        return max_length

    @property
    @param(
        "zigzag_spacing_mm",
        _("Zig-zag spacing (peak-to-peak)"),
        tooltip=_("Length of stitches in zig-zag mode."),
        unit="mm",
        type="string",
        default="0.4",
        select_items=[("stroke_method", "zigzag_stitch")],
        sort_index=6,
    )
    @cache
    def zigzag_spacing(self):
        """Return the zig-zag spacing."""
        return [max(value, 0.01) for value in self.get_multiple_float_param("zigzag_spacing_mm", "0.4")]

    @property
    @param(
        "stroke_pull_compensation_mm",
        _("Pull compensation"),
        tooltip=_(
            "Zigzag stitches pull the fabric together, resulting in a column narrower than you "
            "draw in Inkscape. "
            "This widens the zigzag line width."
        ),
        unit=_("mm (each side)"),
        type="float",
        default=0,
        select_items=[("stroke_method", "zigzag_stitch")],
        sort_index=6,
    )
    @cache
    def pull_compensation(self):
        """Return the pull compensation."""
        return self.get_split_mm_param_as_px("stroke_pull_compensation_mm", (0, 0))

    @property
    @param(
        "zigzag_peak_offset_mm",
        _("Peak offset"),
        tooltip=_(
            "Shift zigzag peaks forward along the path. "
            "Positive values create a forward-leaning zigzag, "
            "negative values create a backward-leaning zigzag. "
            "Use this for decorative slanted effects."
        ),
        unit="mm",
        type="float",
        default=0,
        select_items=[("stroke_method", "zigzag_stitch")],
        sort_index=7,
    )
    @cache
    def zigzag_peak_offset(self):
        """Return the zigzag peak offset in pixels."""
        return self.get_float_param("zigzag_peak_offset_mm", 0) * PIXELS_PER_MM

    @property
    @param(
        "line_count",
        _("Number of lines"),
        tooltip=_("Number of lines from start to finish"),
        type="int",
        default=10,
        select_items=[("stroke_method", "ripple_stitch")],
        sort_index=7,
    )
    @cache
    def line_count(self):
        """Return the number of lines."""
        return max(self.get_int_param("line_count", 10), 1)

    @property
    @param(
        "min_line_dist_mm",
        _("Minimum line distance"),
        tooltip=_("Overrides the number of lines setting."),
        unit="mm",
        type="float",
        select_items=[("stroke_method", "ripple_stitch")],
        sort_index=8,
    )
    @cache
    def min_line_dist(self):
        """Return the minimum line distance."""
        min_dist = self.get_float_param("min_line_dist_mm")
        if min_dist is None:
            return
        return min_dist

    _satin_guided_pattern_options = [
        ParamOption("default", _("Line count / Minimum line distance")),
        ParamOption("render_at_rungs", _("Render at rungs")),
        ParamOption("adaptive", _("Adaptive + minimum line distance")),
    ]

    @property
    @param(
        "satin_guide_pattern_position",
        _("Pattern position"),
        tooltip=_("Pattern position for satin guided ripples."),
        type="combo",
        options=_satin_guided_pattern_options,
        default="default",
        select_items=[("stroke_method", "ripple_stitch")],
        sort_index=9,
    )
    def satin_guide_pattern_position(self):
        """Return the satin guide pattern position."""
        return self.get_param("satin_guide_pattern_position", "line_count")

    @property
    @param(
        "staggers",
        _("Stagger lines this many times before repeating"),
        tooltip=_(
            "Length of the cycle by which successive stitch lines are staggered. "
            "Fractional values are allowed and can have less visible diagonals than integer "
            "values. "
            "A value of 0 (default) disables staggering and instead stitches evenly."
            "For linear ripples only."
        ),
        type="int",
        select_items=[("stroke_method", "ripple_stitch")],
        default=0,
        sort_index=15,
    )
    def staggers(self):
        """Return the staggers value."""
        return self.get_float_param("staggers", 1)

    @property
    @param(
        "skip_start",
        _("Skip first lines"),
        tooltip=_("Skip this number of lines at the beginning."),
        type="int",
        default=0,
        select_items=[("stroke_method", "ripple_stitch")],
        sort_index=16,
    )
    @cache
    def skip_start(self):
        """Return the number of lines to skip at the start."""
        return abs(self.get_int_param("skip_start", 0))

    @property
    @param(
        "skip_end",
        _("Skip last lines"),
        tooltip=_("Skip this number of lines at the end"),
        type="int",
        default=0,
        select_items=[("stroke_method", "ripple_stitch")],
        sort_index=17,
    )
    @cache
    def skip_end(self):
        """Return the number of lines to skip at the end."""
        return abs(self.get_int_param("skip_end", 0))

    @property
    @param(
        "flip_copies",
        _("Flip every second line"),
        tooltip=_("Linear ripple: wether to flip the pattern every second line or not."),
        type="boolean",
        select_items=[("stroke_method", "ripple_stitch")],
        default=True,
        sort_index=18,
    )
    def flip_copies(self):
        """Return True if flip copies is enabled."""
        return self.get_boolean_param("flip_copies", True)

    @property
    @param(
        "exponent",
        _("Line distance exponent"),
        tooltip=_("Increase density towards one side."),
        type="float",
        default=1,
        select_items=[("stroke_method", "ripple_stitch")],
        sort_index=19,
    )
    @cache
    def exponent(self):
        """Return the exponent value."""
        return max(self.get_float_param("exponent", 1), 0.1)

    @property
    @param(
        "flip_exponent",
        _("Flip exponent"),
        tooltip=_("Reverse exponent effect."),
        type="boolean",
        default=False,
        select_items=[("stroke_method", "ripple_stitch")],
        sort_index=20,
    )
    @cache
    def flip_exponent(self):
        """Return True if flip exponent is enabled."""
        return self.get_boolean_param("flip_exponent", False)

    @property
    @param(
        "reverse",
        _("Reverse"),
        tooltip=_("Flip start and end point"),
        type="boolean",
        default=False,
        select_items=[("stroke_method", "ripple_stitch")],
        sort_index=21,
    )
    @cache
    def reverse(self):
        """Return True if reverse is enabled."""
        return self.get_boolean_param("reverse", False)

    _reverse_rails_options = [
        ParamOption("automatic", _("Automatic")),
        ParamOption("none", _("Don't reverse")),
        ParamOption("first", _("Reverse first rail")),
        ParamOption("second", _("Reverse second rail")),
        ParamOption("both", _("Reverse both rails")),
    ]

    @property
    @param(
        "reverse_rails",
        _("Reverse rails"),
        tooltip=_("Reverse satin ripple rails. Default: automatically detect and fix a reversed rail."),
        type="combo",
        options=_reverse_rails_options,
        default="automatic",
        select_items=[("stroke_method", "ripple_stitch")],
        sort_index=22,
    )
    def reverse_rails(self):
        """Return the reverse rails setting."""
        return self.get_param("reverse_rails", "automatic")

    @property
    @param(
        "swap_satin_rails",
        _("Swap rails"),
        tooltip=_("Swaps the first and second rails of a satin ripple, affecting which side the thread finished on as well as any sided properties"),
        type="boolean",
        default="false",
        select_items=[("stroke_method", "ripple_stitch")],
        sort_index=23,
    )
    def swap_rails(self):
        """Return True if rails should be swapped."""
        return self.get_boolean_param("swap_satin_rails", False)

    @property
    @param(
        "grid_size_mm",
        _("Grid size"),
        tooltip=_("Render as grid. Use with care and watch your stitch density."),
        type="float",
        default=0,
        unit="mm",
        select_items=[("stroke_method", "ripple_stitch")],
        sort_index=24,
    )
    @cache
    def grid_size(self):
        """Return the grid size."""
        return abs(self.get_float_param("grid_size_mm", 0))

    @property
    @param(
        "grid_first",
        _("Stitch grid first"),
        tooltip=_("Reverse the stitch paths, so that the grid will be stitched first"),
        type="boolean",
        default=False,
        select_items=[("stroke_method", "ripple_stitch")],
        sort_index=25,
    )
    @cache
    def grid_first(self):
        """Return True if grid should be stitched first."""
        return self.get_boolean_param("grid_first", False)

    @property
    @param(
        "scale_axis",
        _("Scale axis"),
        tooltip=_("Scale axis for satin guided ripple stitches."),
        type="dropdown",
        default=0,
        # 0: xy, 1: x, 2: y, 3: none
        options=["X Y", "X", "Y", _("None")],
        select_items=[("stroke_method", "ripple_stitch")],
        sort_index=25,
    )
    def scale_axis(self):
        """Return the scale axis."""
        return self.get_int_param("scale_axis", 0)

    @property
    @param(
        "scale_start",
        _("Starting scale"),
        tooltip=_("How big the first copy of the line should be, in percent.") + " " + _("Used only for ripple stitch with a guide line."),
        type="float",
        unit="%",
        default=100,
        select_items=[("stroke_method", "ripple_stitch")],
        sort_index=26,
    )
    def scale_start(self):
        """Return the starting scale."""
        return self.get_float_param("scale_start", 100.0)

    @property
    @param(
        "scale_end",
        _("Ending scale"),
        tooltip=_("How big the last copy of the line should be, in percent.") + " " + _("Used only for ripple stitch with a guide line."),
        type="float",
        unit="%",
        default=0.0,
        select_items=[("stroke_method", "ripple_stitch")],
        sort_index=27,
    )
    def scale_end(self):
        """Return the ending scale."""
        return self.get_float_param("scale_end", 0.0)

    @property
    @param(
        "rotate_ripples",
        _("Rotate"),
        tooltip=_("Rotate satin guided ripple stitches"),
        type="boolean",
        default=True,
        select_items=[("stroke_method", "ripple_stitch")],
        sort_index=30,
    )
    @cache
    def rotate_ripples(self):
        """Return True if ripples should be rotated."""
        return self.get_boolean_param("rotate_ripples", True)

    @property
    @param(
        "join_style",
        _("Join style"),
        tooltip=_("Join style for non circular ripples."),
        type="dropdown",
        default=0,
        options=(_("flat"), _("point")),
        select_items=[("stroke_method", "ripple_stitch")],
        sort_index=31,
    )
    @cache
    def join_style(self):
        """Return the join style."""
        return self.get_int_param("join_style", 0)

    @property
    @param(
        "random_seed",
        _("Random seed"),
        tooltip=_("Use a specific seed for randomized attributes. Uses the element ID if empty."),
        select_items=[
            ("stroke_method", "running_stitch"),
            ("stroke_method", "ripple_stitch"),
        ],
        type="random_seed",
        default="",
        sort_index=100,
    )
    @cache
    def random_seed(self) -> str:
        """Return the random seed."""
        seed = self.get_param("random_seed", "")
        if not seed:
            seed = self.node.get_id() or ""
            # TODO(#1696): When inplementing grouped clones, join this with the IDs of any shadow
            # roots, letting each instance without a specified seed get a different default.
        return seed

    def _is_closed(self, clipped=True):
        # returns true if the outline of a single line stroke is a closed shape
        # (with a small tolerance)
        if clipped:
            lines = self.as_multi_line_string().geoms
        else:
            lines = self.as_multi_line_string(False).geoms
        if len(lines) == 1:
            coords = lines[0].coords
            return Point(*coords[0]).distance(Point(*coords[-1])) < 0.05
        return False

    @property
    @cache
    def is_closed_unclipped(self):
        """Return True if unclipped path is closed."""
        return self._is_closed(False)

    @property
    @cache
    def is_closed_clipped(self):
        """Return True if clipped path is closed."""
        return self._is_closed()

    @property
    def paths(self):
        return self._get_paths()

    @property
    def unclipped_paths(self):
        """Return unclipped paths."""
        return self._get_paths(False)

    def _get_paths(self, clipped=True):
        path = self.parse_path()
        flattened = self.flatten(path)
        if clipped:
            flattened = self._get_clipped_path(flattened)
        if flattened is None:
            return []

        # manipulate invalid path
        if len(flattened[0]) == 1:
            return [
                [
                    [flattened[0][0][0], flattened[0][0][1]],
                    [flattened[0][0][0] + 1.0, flattened[0][0][1]],
                ]
            ]

        if self.stroke_method == "manual_stitch":
            coords = [shgeo.LineString(self.strip_control_points(subpath)).coords for subpath in path]
            coords = self._get_clipped_path(coords)
            return coords
        else:
            return flattened

    @property
    @cache
    def shape(self):
        return self.as_multi_line_string().convex_hull

    @property
    @cache
    def unclipped_shape(self):
        """Return the unclipped shape's convex hull."""
        return self.as_multi_line_string(False).convex_hull

    @cache
    def as_multi_line_string(self, clipped=True):
        """Return paths as a MultiLineString."""
        if clipped:
            paths = self.paths
        else:
            paths = self.unclipped_paths
        line_strings = [shgeo.LineString(path) for path in paths if len(path) > 1]
        return shgeo.MultiLineString(line_strings)

    @property
    def first_stitch(self):
        return shgeo.Point(self.as_multi_line_string().geoms[0].coords[0])

    def _get_clipped_path(self, paths):
        if self.clip_shape is None:
            return paths

        # path to linestrings
        line_strings = [shgeo.LineString(path) for path in paths if len(path) > 1]
        try:
            intersection = self.clip_shape.intersection(shgeo.MultiLineString(line_strings))
        except GEOSException:
            return paths

        coords = []
        if intersection.is_empty:
            return None
        elif isinstance(intersection, shgeo.MultiLineString):
            for c in [intersection for intersection in intersection.geoms if isinstance(intersection, shgeo.LineString)]:
                coords.append(c.coords)
        elif isinstance(intersection, shgeo.LineString):
            coords.append(intersection.coords)
        else:
            return paths
        return coords

    def get_ripple_target(self):
        """Return the ripple target point."""
        command = self.get_command("target_point")
        if command:
            return shgeo.Point(*command.target_point)
        else:
            return self.unclipped_shape.centroid

    def simple_satin(self, path, zigzag_spacing, stroke_width, pull_compensation, peak_offset):
        """Generate zig-zag along the path at the specified spacing and width.

        Applies zigzag to a single pass first, then handles repeats manually.
        This ensures stitch points align perfectly across all passes.
        """
        # `self.zigzag_spacing` is the length for a zig and a zag
        # together (a V shape).  Start with running stitch at half
        # that length:
        spacing = [value / 2 for value in zigzag_spacing]

        # Generate running stitches for a SINGLE pass (no repeats)
        single_pass_stitches = running_stitch(
            path,
            spacing,
            self.running_stitch_tolerance,
            False,  # enable_random_stitch_length
            0,  # random_sigma
            "",  # random_seed
        )

        # Apply zigzag transformation to the single pass
        zigzag_stitches = zigzag_stitch(
            single_pass_stitches,
            zigzag_spacing,
            stroke_width,
            pull_compensation,
            peak_offset,
        )

        # For closed paths (circles), ensure the last stitch connects to the first
        is_closed = self.is_closed_unclipped
        if is_closed and len(zigzag_stitches) >= 2:
            # Make the last stitch position exactly match the first
            first_stitch = zigzag_stitches[0]
            last_stitch = zigzag_stitches[-1]
            last_stitch.x = first_stitch.x
            last_stitch.y = first_stitch.y

        # Now handle repeats by reversing the already-zigzagged stitches
        # This ensures each physical point keeps its offset across all passes
        repeated_stitches = []
        for i in range(self.repeats):
            if i % 2 == 1:
                # Reverse every other pass
                this_pass = zigzag_stitches[::-1]
            else:
                this_pass = list(zigzag_stitches)

            if i > 0 and this_pass:
                # Skip the first stitch of subsequent passes to avoid duplicate
                # at the junction (prevents thread stacking)
                repeated_stitches.extend(this_pass[1:])
            else:
                repeated_stitches.extend(this_pass)

        return StitchGroup(
            self.color,
            stitches=repeated_stitches,
            lock_stitches=self.lock_stitches,
            force_lock_stitches=self.force_lock_stitches,
        )

    def running_stitch(
        self,
        path,
        stitch_length,
        tolerance,
        enable_random_stitch_length,
        random_sigma,
        random_seed,
    ):
        """Generate running stitch with repeats."""
        # running stitch with repeats
        stitches = running_stitch(
            path,
            stitch_length,
            tolerance,
            enable_random_stitch_length,
            random_sigma,
            random_seed,
        )

        repeated_stitches = []
        # go back and forth along the path as specified by self.repeats
        for i in range(self.repeats):
            if i % 2 == 1:
                # reverse every other pass
                this_path = stitches[::-1]
            else:
                this_path = stitches[:]

            repeated_stitches.extend(this_path)

        return StitchGroup(
            self.color,
            stitches=repeated_stitches,
            lock_stitches=self.lock_stitches,
            force_lock_stitches=self.force_lock_stitches,
        )

    def apply_max_stitch_length(self, path):
        """Split segments longer than max stitch length."""
        # apply max distances
        max_len_path = [path[0]]
        for points in zip(path[:-1], path[1:]):
            line = shgeo.LineString(points)
            dist = line.length
            if dist > self.max_stitch_length:
                num_subsections = ceil(dist / self.max_stitch_length)
                additional_points = [
                    Point(coord.x, coord.y)
                    for coord in [line.interpolate((i / num_subsections), normalized=True) for i in range(1, num_subsections + 1)]
                ]
                max_len_path.extend(additional_points)
            max_len_path.append(points[1])
        return max_len_path

    def ripple_stitch(self):
        """Generate ripple stitches."""
        ripple_stitches = ripple_stitch(self)
        stitch_groups = []
        for stitches in ripple_stitches:
            stitch_group = StitchGroup(
                color=self.color,
                tags=["ripple_stitch"],
                stitches=stitches,
                lock_stitches=self.lock_stitches,
                force_lock_stitches=self.force_lock_stitches,
            )
            stitch_group.stitches = self.do_bean_repeats(stitch_group.stitches)
            stitch_groups.append(stitch_group)
        return stitch_groups

    def do_bean_repeats(self, stitches):
        """Apply bean repeats if any are specified."""
        if any(self.bean_stitch_repeats):
            return bean_stitch(stitches, self.bean_stitch_repeats)
        return stitches

    def to_stitch_groups(self, last_stitch_group, next_element=None):  # noqa: C901
        """Convert stroke to stitch groups."""
        stitch_groups = []

        # ripple stitch
        if self.stroke_method == "ripple_stitch":
            stitch_groups.extend(self.ripple_stitch())
        else:
            for path in self.paths:
                path = [Point(x, y) for x, y in path]
                # manual stitch
                if self.stroke_method == "manual_stitch":
                    if self.max_stitch_length:
                        path = self.apply_max_stitch_length(path)

                    if self.force_lock_stitches:
                        lock_stitches = self.lock_stitches
                    else:
                        # manual stitch disables lock stitches unless they force them
                        lock_stitches = (None, None)
                    stitch_group = StitchGroup(
                        color=self.color,
                        stitches=path,
                        lock_stitches=lock_stitches,
                        force_lock_stitches=self.force_lock_stitches,
                    )
                    # apply bean stitch settings
                    stitch_group.stitches = self.do_bean_repeats(stitch_group.stitches)
                # simple satin
                elif self.stroke_method == "zigzag_stitch":
                    stitch_group = self.simple_satin(
                        path,
                        self.zigzag_spacing,
                        self.stroke_width,
                        self.pull_compensation,
                        self.zigzag_peak_offset,
                    )
                    # bean stitch
                    if any(self.bean_stitch_repeats):
                        stitch_group.stitches = self.do_bean_repeats(stitch_group.stitches)
                # running stitch
                else:
                    stitch_group = self.running_stitch(
                        path,
                        self.running_stitch_length,
                        self.running_stitch_tolerance,
                        self.enable_random_stitch_length,
                        self.random_stitch_length_jitter,
                        self.random_seed,
                    )
                    # bean stitch
                    if any(self.bean_stitch_repeats):
                        stitch_group.stitches = self.do_bean_repeats(stitch_group.stitches)

                if stitch_group:
                    stitch_groups.append(stitch_group)

        return stitch_groups

    @cache
    def get_guide_line(self):
        """Return the guide line element."""
        guide_lines = get_marker_elements(self.node, "guide-line", False, True, True)
        # No or empty guide line
        if not guide_lines or (not guide_lines["stroke"] and not guide_lines["satin"]):
            return None

        # use the satin guide line if there is one, else use stroke
        # ignore multiple guide lines
        if len(guide_lines["satin"]) >= 1:
            return guide_lines["satin"][0]
        return guide_lines["stroke"][0]

    @cache
    def get_anchor_line(self):
        """Return the anchor line element."""
        anchor_lines = get_marker_elements(self.node, "anchor-line", False, True, False)
        # No or empty guide line
        if not anchor_lines or not anchor_lines["stroke"]:
            return None

        # ignore multiple anchor lines
        return anchor_lines["stroke"][0].geoms[0]

    def _representative_point(self):
        """Return a representative point on the stroke."""
        # if we just take the center of a line string we could end up on some point far away from
        # the actual line
        try:
            coords = list(self.shape.coords)
        except NotImplementedError:
            # linear rings to not have a coordinate sequence
            coords = list(self.shape.exterior.coords)
        return coords[int(len(coords) / 2)]

    def validation_warnings(self):
        # satin column warning
        if self.get_boolean_param("satin_column", False) and self.stroke_width <= 0.3 * PIXELS_PER_MM:
            yield TooNarrowSatinWarning(self._representative_point())
        # ripple stitch warnings
        if self.stroke_method == 1:
            guide_lines = get_marker_elements(self.node, "guide-line", False, True, True)
            if sum(len(x) for x in guide_lines.values()) > 1:
                yield MultipleGuideLineWarning(self._representative_point())

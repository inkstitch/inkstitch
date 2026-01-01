# Project TODOs

## [ ] 1. E-Stitch (Blanket Stitch)

**Description**: A comb-like stitch often used for applique borders. It consists of a line of running stitching along the edge with perpendicular stitches extending inward.

**Implementation Details**:

- Add `ParamOption("e_stitch", _("E-Stitch"))` to `_stroke_methods`.
- Add parameters:
  - `e_stitch_width`: Length of the "teeth".
  - `e_stitch_spacing`: Distance between "teeth".
  - `e_stitch_length`: Stitch length for the running stitch spine.
- Logic: Iterate through path points, creating a running stitch, but at fixed intervals, branch out perpendicularly and return.

## [ ] 2. Stem Stitch

**Description**: A rope-like twisted line used for stems and outlines. It is thicker than a run stitch but narrower than a satin column.

**Implementation Details**:

- Add `ParamOption("stem_stitch", _("Stem Stitch"))`.
- Add parameters:
  - `stem_thickness`: How wide the stitch should appear.
  - `stem_angle`: (Optional) precise control over the overlap angle.
- Logic: Generate a running stitch where each forward movement overlaps the previous stitch by a certain percentage, slightly offset to one side.

## [ ] 3. Back Stitch

**Description**: A strong, unbroken line stitch. Unlike Bean Stitch (in-place triple), Back Stitch moves forward two steps and back one step (or similar pattern).

**Implementation Details**:

- Add `ParamOption("back_stitch", _("Back Stitch"))`.
- Logic: Generate points in a sequence: `p[i] -> p[i+2] -> p[i+1] -> p[i+3]`.

## [ ] 4. Motif Runs (Patterned Lines)

**Description**: Instead of a line, stitch a repeating shape (star, heart, circle) along the path.

**Implementation Details**:

- Add `ParamOption("motif_stitch", _("Motif Stitch"))`.
- Add parameters:
  - `motif_shape`: Dropdown of available shapes.
  - `motif_scale`: Size of the shape.
  - `motif_spacing`: Distance between shapes.
  - `motif_rotation`: Rotate shapes relative to path tangent.

## [ ] 5. Satin Border Caps

**Description**: Enhancement for the existing ZigZag (Satin) stitch to allow controlled endings (pointed, rounded) instead of abrupt cutoffs.

**Implementation Details**:

- Add parameters to the existing `zigzag_stitch` method:
  - `cap_start`: [Flat, Pointed, Rounded]
  - `cap_end`: [Flat, Pointed, Rounded]
- Logic: Modify the `to_stitch_groups` logic or `zigzag_stitch` function to taper the width at the start and end of the line.

## [ ] 6. SVG Dashed Line Support

**Description**: Respect the standard SVG `stroke-dasharray` property.

**Implementation Details**:

- Feature: Check `self.get_style("stroke-dasharray")`.
- Logic: If dashes are present, break the single path into multiple sub-paths corresponding to the dash segments. Insert Jump/Trim commands between these segments so the machine stops stitching in the gaps.

## [ ] 7. Circular ZigZag Alignment

**Description**: In circular zigzag stitches with large spacing, the starting and ending points do not match exactly, causing a visible discontinuity.

**Implementation Details**:

- Issue: fixed spacing not dividing evenly into the circumference.
- Fix: Detect closed paths (`self.is_closed_unclipped`) and adjust `zigzag_spacing` slightly to fit an integer number of cycles (`total_length % new_spacing == 0`).

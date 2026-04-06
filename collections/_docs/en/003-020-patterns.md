---
title: "Stitch patterns"
permalink: /docs/stitches/patterns/
last_modified_at: 2026-04-06
toc: true
---
Patterns are created by special stitch positioning.

![Pattern](/assets/images/docs/stitch-type-pattern.png)

[Download sample file](/assets/images/docs/pattern.svg)

## Generate Patterns

In Ink/Stitch you can generate patterns by either adding stitches or removing stitches from any existing embroidery element.

1. **Create embroidery element(s).** This can be either a satin column or fill area. Patterns will also work on strokes, but they may not be the best target for patterns.

2. **Create pattern path(s).** A pattern consists of strokes or fill areas (or both at the same time). Strokes will be used to add stitches, while patterns with a fill will remove stitches from the embroidery element.

3. Select both, the embroidery element and the pattern and hit `Ctrl+G` to **group them together**.

4. **Convert to pattern.**

  Select only the pattern and run `Extensions > Ink/Stitch > Edit > Selection to pattern`.
  This will add a start marker to the pattern element to indicate, that it will not be embroidered but will be used as a pattern for all elements in the same group.
  Elements in subgroups of the very same group will not be affected.

  ![Pattern groups](/assets/images/docs/en/pattern.png)

  {% include upcoming_release.html %}

  Interval: An interval can be set for patterns with a stroke color. 
  This value determines at which pattern the addition of nodes at path intersections should be skipped.
  Multiple values are separated by spaces.

  Offset: Patterns with a stroke color only begin after this number of path intersections.

## Remove Pattern Marker

Remove the pattern marker by running `Extensions > Ink/Stitch > Edit > Selection to Pattern`, select the `Remove pattern marker` option.

### Manual pattern marker removal

The pattern marker can be removed in the fill and stroke panel (`Ctrl+Shift+F`). Open the Stroke style tab and set the first dropdown list in "Markers" to  the very first (empty) option.

![Remove pattern](/assets/images/docs/en/stitch-type-remove-pattern.png)

### Samples Files Including Pattern Stitches

{% include tutorials/tutorial_list key="stitch-type" value="Pattern Stitch" %}


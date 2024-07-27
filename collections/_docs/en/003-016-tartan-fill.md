---
title: "Tartan Fill"
permalink: /docs/stitches/tartan-fill/
last_modified_at: 2024-03-11
toc: true
---
## What it is

[![Tartan Fill Sample](/assets/images/docs/tartan-fill.jpg){: width="200x"}](/assets/images/docs/tartan-fill.svg){: title="Download SVG File" .align-left download="tartan-fill.svg" }
Tartan is a patterned fabric with colored horizontal and vertical stripes. It is typically known from scottish kilts. The embroidery stitch type tries to mimic the typical pattern.

## How to Create

* Create a **closed path with a fill color**. The shape may have holes.
* Open the tartan extension under `Extensions > Ink/Stitch > Tools: Fill > Tartan` and create your own tartan pattern
* You can update and change more stitch params in the params dialog (`Extensions > Ink/Stitch > Params`)

## Edit Tartan Patterns

The Tartan Pattern Editor can be found in `Extensions > Ink/Stitch > Tools: Fill > Tartan`

[Read more about the Tartan Stripe Editor](/docs/fill-tools#tartan)

## Params

Run `Extensions > Ink/Stitch  > Params` to tweak the settings to your needs.

Settings||Description
---|---|---
Automatically routed fill stitching| ☑ |Must be enabled for these settings to take effect.
Fill method          |Tartan Fill|Tartan Fill must be selected.
Expand               |![Expand example](/assets/images/docs/params-fill-expand.png)  |Expand the shape before stitching, to compensate for gaps between shapes.
Angle of lines of stitches|| Relative to the tartan stripe direction.
Maximum fill stitch length         |![Stitch length example](/assets/images/docs/params-fill-stitch_length.png) |The length of each stitch in a row. "Max" is because a shorter stitch may be used at the start or end of a row.
Spacing between rows               |![Spacing example](/assets/images/docs/params-fill-spacing_between_rows.png) |Distance between rows of stitches
Stagger rows this many times before repeating|![Stagger example](/assets/images/docs/params-fill-stagger.png) |Stitches are staggered so that neighboring rows of stitches don't all fall in the same column (which would create a distracting valley effect). Setting this dictates the length of the cycle by which successive stitch rows are staggered. Fractional values are allowed and can have less visible diagonals than integer values.
Running stitch length||Length of stitches around the outline of the fill region used when moving from section to section. 
Running stitch tolerance||All stitches must be within this distance from a path. A lower tolerance means stitches will be closer together. A higher tolerance means sharp corner may be rounded.
Bean stitch number of repeats ||◦ Enable [Bean Stitch Mode](/docs/stitches/bean-stitch/)<br />◦ Backtrack each stitch this many times.<br />◦ A value of 1 would triple each stitch (forward, back, forward).<br />◦ A value of 2 would quintuple each stitch, etc.
Rows per tartan thread || Consecutive rows of the same color
Herringbone width    ||Defines the width of a herringbone pattern. Use 0 for regular rows. It is recommended to use a multiple or a fraction of the defined stripe width (or to use only one color on warp and an other color on weft).
Minimum stitch length         ||Overwrite global minimum stitch length setting. Shorter stitches than that will be removed.
Minimum  jump stitch  length             ||Overwrite global minimum jump stitch length setting. Shorter distances to the next object will have no lock stitches
Allow lock stitches                ||Enables lock stitches in only desired positions
Force lock stitches                |☑ |Sew lock stitches after sewing this element, even if the distance to the next object is shorter than defined by the collapse length value in the Ink/Stitch preferences.
Tack stitch                        ||Chose your [favorite style](/docs/stitches/lock-stitches/)
Scale Tack stitch    ||
Lock stitch                        ||Chose your [favorite style](/docs/stitches/lock-stitches/)
Scale Lock stitch    ||
Trim After                         |☑ |Trim the thread after sewing this object.
Stop After                         |☑ |Stop the machine after sewing this object. Before stopping it will jump to the stop position (frame out) if defined.
{: .params-table }

## Underlay

Underlay in Tartan Fill is a normal Auto FillUnderlay and uses the fill angle which can be defined in the underlay [params](/docs/stitches/fill-stitch#underlay).

## Sample Files Including Tartan Fill Stitches

{% include tutorials/tutorial_list key="stitch-type" value="Tartan Fill" %}

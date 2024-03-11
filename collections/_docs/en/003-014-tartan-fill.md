---
title: "Tartan Fill"
permalink: /docs/stitches/tartan-fill/
last_modified_at: 2024-03-11
toc: true
---
{% include upcoming_release.html %}

## What it is

Tartan is a patterned fabric with colored horizontal and vertical stripes. It is typically known from scottish kilts. The embroidery stitch type tries to mimic the typical pattern.

## How to Create

* Create a **closed path with a fill color**. The shape may have holes.
* Open the tartan pattern editor (`Extensions > Ink/Stitch > Tools: Fill > Tartan`)
* More stitch params are available in the params dialog (`Extensions > Ink/Stitch > Params`)

## Edit Tartan Patterns

The Stripe Editor can be found in `Extensions > Ink/Stitch > Tools: Fill > Tartan`

[Read more about the Tartan Stripe Editor](/docs/fill-tools#tartan)

## Params

Run `Extensions > Ink/Stitch  > Params` to tweak the settings to your needs.

Settings||Description
---|---|---
Automatically routed fill stitching| ☑ |Must be enabled for these settings to take effect.
Fill method          |Tartan Fill|Tartan Fill must be selected.
Expand               |![Expand example](/assets/images/docs/params-fill-expand.png)  |Expand the shape before stitching, to compensate for gaps between shapes.
Running stitch length||For circular fill this is the overall stitch length.
Running stitch tolerance||All stitches must be within this distance from a path. A lower tolerance means stitches will be closer together. A higher tolerance means sharp corner may be rounded.
Bean stitch number of repeats ||◦ Enable [Bean Stitch Mode](/docs/stitches/bean-stitch/)<br />◦ Backtrack each stitch this many times.<br />◦ A value of 1 would triple each stitch (forward, back, forward).<br />◦ A value of 2 would quintuple each stitch, etc.
Rows per tartan thread || Consecutive rows of the same color
Herringbone width    ||Defines the width of a herringbone pattern. Use 0 for regular rows. It is recommended to use a multiple or a fraction of the defined stripe width (or to use only one color on warp and an other color on weft).
Allow lock stitches  ||Enables lock stitches in only desired positions
Force lock stitches  ||Sew lock stitches after sewing this element, even if the distance to the next object is smaller than defined in the collapse length value value in the Ink/Stitch prefreneces.
Tack stitch          ||Select [tack stitch](/docs/stitches/lock-stitches) type (start).
Lock stitch          ||Select [lock stitch](/docs/stitches/lock-stitches) type (end).
Trim After           ||Trim the thread after sewing this object.
Stop After           ||Stop the machine after sewing this object. Before stopping it will jump to the stop position (frame out) if defined.

## Underlay

Underlay in Tartan Fill is a normal Auto FillUnderlay and uses the fill angle which can be defined in the underlay [params](/docs/stitches/fill-stitch#underlay).

## Samples Files Including Tartan Fill Stitches

{% include tutorials/tutorial_list key="stitch-type" value="Tartan Fill" %}

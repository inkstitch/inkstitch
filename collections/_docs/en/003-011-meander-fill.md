---
title: "Meander Fill"
permalink: /docs/stitches/meander-fill/
excerpt: ""
last_modified_at: 2023-02-26
toc: true
---
{% include upcoming_release.html %}

## What it is

Meander fill has its origins in quilting techniques. A beautiful patterned effect results for machine embroidery. Large areas can be filled with relatively few stitches.

![Meander stitch detail](/assets/images/docs/meander-fill.png)

## How to Create

* Create a **closed path with a fill color**. This shape may have holes.
* Open the params dialog (`Extensions > Ink/Stitch > Params`) and select `Meander Fill` as the fill method.
  There are many meander fill patterns you can choose from. Influence the look by adapting scale, smoothness, stitch length and tolerance values.

## Set Start and End Point

Set start and end points for autofill objects with [Visual commands](/docs/commands/).

## Params

Run `Extensions > Ink/Stitch  > Params` to tweak the settings to your needs.

Settings||Description
---|---|---
Automatically routed fill stitching| ☑ |Must be enabled for these settings to take effect.
Fill method          |Meander Fill|Meander Fill must be selected.
Meander Pattern      ||Various patterns to choose from
Meander pattern scale||Scale the pattern (%)
Expand               |![Expand example](/assets/images/docs/params-fill-expand.png)  |Expand the shape before stitching, to compensate for gaps between shapes.
Smoothness           ||Smooth the stitch path. Smoothness linits how far the smoothed stitch path is allowed to deviate from the original path. Try low numbers like 0.2. Hint: a lower running stitch tolerance may be needed too.
Running stitch length||For meander fill this is the overall stitch length.
Running stitch tolerance||All stitches must be within this distance from a path. A lower tolerance means stitches will be closer together. A higher tolerance means sharp corner may be rounded.
Allow lock stitches  ||Enables lock stitches in only desired positions
Force lock stitches  ||Sew lock stitches after sewing this element, even if the distance to the next object is smaller than defined in the collapse length value value in the Ink/Stitch preferences.
Tack stitch                  ||Chose your [favorite style](/docs/stitches/lock-stitches/)
Lock stitch                   ||Chose your [favorite style](/docs/stitches/lock-stitches/)
Trim After           ||Trim the thread after sewing this object.
Stop After           ||Stop the machine after sewing this object. Before stopping it will jump to the stop position (frame out) if defined.

## Underlay

Underlay in Guided Fill doesn't follow the guide line, but uses the fill angle which can be defined in the underlay [params](/docs/stitches/fill-stitch#underlay).

## Samples Files Including Meander Fill Stitches
{% include tutorials/tutorial_list key="stitch-type" value="Meander Fill" %}

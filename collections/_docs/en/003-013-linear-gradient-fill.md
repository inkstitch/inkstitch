---
title: "Linear Gradient Fill"
permalink: /docs/stitches/linear-gradient-fill/
last_modified_at: 2024-03-11
toc: true
---
 {% include upcoming_release.html %}

## What it is

[![Linear Gradient Fill Sample](/assets/images/docs/linear-gradient.jpg){: width="200x"}](/assets/images/docs/linear-gradient.svg){: title="Download SVG File" .align-left download="linear-gradient.svg" }
Fill stitch is used to fill big areas with a color.

Linear gradient fill uses Inkscapes linear gradient color to create seamless gradients with a consistent stitch positioning.

## How to Create

* Create a closed path. The shape may have holes.
* In the `Fill and Stroke` dialog, select a linear gradient as a fill and adjust colors. On canvas adjust the gradient angle. The stitch angle will have a 90 degree angle to gradient direction.
  ![linear gradient](/assets/images/docs/en/linear-gradient.png)
* Open the params dialog (`Extensions > Ink/Stitch > Params`) and select `Linear Gradient Fill` as the fill method
  Set the params as you wish and Apply

## Set Start and End Point

Set start and end points for autofill objects with [Visual commands](/docs/commands/).

## Params

Run `Extensions > Ink/Stitch  > Params` to tweak the settings to your needs.

Settings||Description
---|---|---
Automatically routed fill stitching| ☑ |Must be enabled for these settings to take effect.
Fill method          |Linear Gradient Fill|Linear Gradient Fill must be selected.
Expand               |![Expand example](/assets/images/docs/params-fill-expand.png)  |Expand the shape before stitching, to compensate for gaps between shapes.
Maximum fill stitch length    ||The length of each stitch in a row. "Max" is because a shorter stitch may be used at the start or end of a row.
Spacing between rows          ||Distance between rows of stitches.
Stagger row this many times before repeating||Stitches are staggered so that neighboring rows of stitches don't all fall in the same column (which would create a distracting valley effect). Setting this dictates how many rows apart the stitches will be before they fall in the same column position.
Skip last stitch in each row  ||The last stitch in each row is quite close to the first stitch in the next row.
Stop at ending point  | ☑ |If this option is disabled, the ending point will only be used to define a general direction for stitch routing. When enabled the last section will end at the defined spot.
Running stitch length||For circular fill this is the overall stitch length.
Running stitch tolerance||All stitches must be within this distance from a path. A lower tolerance means stitches will be closer together. A higher tolerance means sharp corner may be rounded.
Allow lock stitches  ||Enables lock stitches in only desired positions
Force lock stitches  ||Sew lock stitches after sewing this element, even if the distance to the next object is smaller than defined in the collapse length value value in the Ink/Stitch prefreneces.
Tack stitch          ||Select [tack stitch](/docs/stitches/lock-stitches) type (start).
Lock stitch          ||Select [lock stitch](/docs/stitches/lock-stitches) type (end).
Stop After           ||Stop the machine after sewing this object. Before stopping it will jump to the stop position (frame out) if defined.
Trim After           ||Trim the thread after sewing this object.

## Underlay

Underlay in Linear Gradient Fill is the same as for Auto Fill and uses the fill angle which can be defined in the underlay [params](/docs/stitches/fill-stitch#underlay).

## Samples Files Including Linear Gradient Fill Stitches

{% include tutorials/tutorial_list key="stitch-type" value="Linear Gradient Fill" %}

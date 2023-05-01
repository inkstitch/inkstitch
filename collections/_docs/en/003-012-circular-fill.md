---
title: "Circular Fill"
permalink: /docs/stitches/circular-fill/
excerpt: ""
last_modified_at: 2023-04-30
toc: true
---
{% include upcoming_release.html %}

## What it is

Circular fill fills a shape with an embroidered spiral. The center of the spiral is positioned at the center of the shape. A target point can be used to define a custom spiral center.

![Meander stitch detail](/assets/images/docs/circular-fill-detail.png)

## How to Create

* Create a **closed path with a fill color**. The shape may have holes.
* Open the params dialog (`Extensions > Ink/Stitch > Params`) and select `Circular Fill` as the fill method.
  Set the params as you wish and Apply.

## Set spiral center

* Select the circular fill shape and attach the Target point command to the shape. Read [how to attach commands to objects](/docs/commands/).

## Set Start and End Point

Set start and end points for autofill objects with [Visual commands](/docs/commands/).

## Params

Run `Extensions > Ink/Stitch  > Params` to tweak the settings to your needs.

Settings||Description
---|---|---
Automatically routed fill stitching| ☑ |Must be enabled for these settings to take effect.
Fill method          |Circular Fill|Circular Fill must be selected.
Expand               |![Expand example](/assets/images/docs/params-fill-expand.png)  |Expand the shape before stitching, to compensate for gaps between shapes.
Running stitch length||For circular fill this is the overall stitch length.
Running stitch tolerance||All stitches must be within this distance from a path. A lower tolerance means stitches will be closer together. A higher tolerance means sharp corner may be rounded.
Underpath            |![Unterpath example](/assets/images/docs/params-fill-underpathing.png)|Must be enabled to let running stitches travel inside shape instead of around the border when moving from section to section
Allow lock stitches  ||Enables lock stitches in only desired positions
Force lock stitches  ||Sew lock stitches after sewing this element, even if the distance to the next object is smaller than defined in the collapse length value value in the Ink/Stitch prefreneces.
Tack stitch          ||Select [tack stitch](/docs/stitches/lock-stitches) type (start).
Lock stitch          ||Select [lock stitch](/docs/stitches/lock-stitches) type (end).
Trim After           ||Trim the thread after sewing this object.
Stop After           ||Stop the machine after sewing this object. Before stopping it will jump to the stop position (frame out) if defined.

## Underlay

Underlay in Circular Fill is the same as for Auto Fill and uses the fill angle which can be defined in the underlay [params](/docs/stitches/fill-stitch#underlay).

## Samples Files Including Circular Fill Stitches
{% include tutorials/tutorial_list key="stitch-type" value="Circular Fill" %}

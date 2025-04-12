---
title: "Contour Fill"
permalink: /docs/stitches/contour-fill/
last_modified_at: 2025-04-12
toc: true
---
## What it is

![Contour fill detail](/assets/images/docs/contour-fill-detail.jpg)

Contour fill covers areas with stitches following the contour of an object.

## How to Create

Create a **closed path with a fill color**.

## Set Start and End Point

Set start and end points for autofill objects with [Visual commands](/docs/commands/).

## Params

Run `Extensions > Ink/Stitch  > Params`. Set fill method to `Contour Fill` and tweak the settings to your needs.

Settings||Description
---|---|---
Automatically routed fill stitching| ☑ |Must be enabled for these settings to take effect.
Fill method                        |Contour Fill|Contour Fill must be selected to sew spiral lines of the contour
Contour Fill Strategy              |![Inner to Outer](/assets/images/docs/contour-fill-innertoouter-bottlenecks.jpg)<br>![Contour spirals](/assets/images/docs/contour-fill-spirals.jpg)|**Inner to outer** (default) is able to fill shapes with bottlenecks<br>**Single spiral** fills a shape with a single spiral from the outside to the inside<br>**Double spiral** fills a shape with a double spiral, starts and ends at the outside border of the shape.
Join Style                         |Round, Mitered, Beveled |Method to handle the edges when the size the contour is reduced for the inner spirals
Avoid self-crossing                |![Avoid self crossing effect](/assets/images/docs/contour-fill-self-crossing.jpg)|Wheter inner to outer is allowed to cross itself or not
Clockwise                          |☑ |Direction to move around the contour
Smoothness                         ||Smooth the stitch path.  Smoothness limits how far the smoothed stitch path is allowed to deviate from the original path.  Try low numbers like 0.2.  Hint: a lower running stitch tolerance may be needed too.
Expand                             ||Expand the shape before fill stitching, to compensate for gaps between the shapes. Negative values contract instead.
Maximum fill stitch length         ||The length of each stitch in a row. "Max" is because a shorter stitch may be used at the start or end of a row.
Spacing between rows               ||Distance between rows of stitches
Running Stitch tolerance           |![Tolerance Sample](/assets/images/docs/contourfilltolerance.svg) |All stitches must be within this distance of the path.  A lower tolerance means stitches will be closer together.  A higher tolerance means sharp corners may be rounded.
Randomize stitches  |☑  |Randomize stitch length and phase instead of dividing evenly or staggering. This is recommended for closely-spaced curved fills to avoid Moiré artefacts.
Random stitch length jitter | |Amount to vary the length of each stitch by when randomizing.
Random Seed| |Rolling the dice or setting a new value will change the random stitches
Minimum stitch length         ||Overwrite global minimum stitch length setting. Shorter stitches than that will be removed.
Minimum  jump stitch  length             ||Overwrite global minimum jump stitch length setting. Shorter distances to the next object will have no lock stitches.
Allow lock stitches                ||Enables lock stitches in only desired positions
Force lock stitches                |☑ |Sew lock stitches after sewing this element, even if the distance to the next object is shorter than defined by the collapse length value in the Ink/Stitch preferences.
Tack stitch                        ||Chose your [favorite style](/docs/stitches/lock-stitches/)
Lock stitch                        ||Chose your [favorite style](/docs/stitches/lock-stitches/
Trim After                         |☑ |Trim the thread after sewing this object.
Stop After                         |☑ |Stop the machine after sewing this object. Before stopping it will jump to the stop position (frame out) if defined.

## Underlay

Underlay in Countour Fill doesn't follow the contour, but uses the fill angle which can be defined in the [fill underlay params](/docs/stitches/fill-stitch#underlay).

## Sample Files Including Contour Fill Stitches

{% include tutorials/tutorial_list key="stitch-type" value="Contour Fill" %}

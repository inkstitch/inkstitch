---
title: "Circular Fill"
permalink: /docs/stitches/circular-fill/
last_modified_at: 2024-06-07
toc: true
---
## What it is

Circular fill fills a shape with an embroidered spiral. The center of the spiral is positioned at the center of the shape. A target point can be used to define a custom spiral center.

![Circular fill stitch detail](/assets/images/docs/circular-fill-detail.png)

## How to Create

* Create a **closed path with a fill color**. The shape may have holes.
* Open the params dialog (`Extensions > Ink/Stitch > Params`) and select `Circular Fill` as the fill method.
  Set the params as you wish and Apply.

## Set spiral center

By default the center of the spiral is the geometrical center of the shape.
Note that this is not equal to the center of the bounding box.

To change default behavior select the circular fill shape and attach the `Target position` command to the shape.
The center of the command symbol will be the new spiral center.

Read [how to attach commands to objects](/docs/commands/).

## Set Start and End Point

Set start and end points for autofill objects with [Visual commands](/docs/commands/).

## Params

Run `Extensions > Ink/Stitch  > Params` to tweak the settings to your needs.

Settings||Description
---|---|---
Automatically routed fill stitching| ☑ |Must be enabled for these settings to take effect.
Fill method                 |Circular Fill|Circular Fill must be selected.
Expand                      |![Expand example](/assets/images/docs/params-fill-expand.png)  |Expand the shape before stitching, to compensate for gaps between shapes.
Spacing between rows        |![Spacing example](/assets/images/docs/params-fill-spacing_between_rows.png) |Distance between rows of stitches
End row spacing             |![End row spacing example](/assets/images/docs/params-fill-end_row_spacing.png) |If set, increases or decreases the row spacing towards the end
Underpath                   |![Unterpath example](/assets/images/docs/params-fill-underpathing.png)|Must be enabled to let running stitches travel inside shape instead of around the border when moving from section to section
Running stitch length       ||For circular fill this is the overall stitch length.
Running stitch tolerance    ||All stitches must be within this distance from a path. A lower tolerance means stitches will be closer together. A higher tolerance means sharp corners may be rounded. Stitches below the value for minimum stitch length (global or object based setting, see below) will be removed.
Randomize stitches          |☑|Randomize stitch length and phase instead of dividing evenly or staggering. This is recommended for closely-spaced curved fills to avoid Moiré artefacts.
Random stitch length jitter | |Amount to vary the length of each stitch by when randomizing.
Random Seed                 | |Rolling the dice or setting a new value will change the random stitches
Minimum stitch length       ||Overwrite [global minimum stitch length](/docs/preferences/#minimum-stitch-length-mm) setting. Shorter stitches than that will be removed.
Minimum  jump stitch  length||Overwrite [global minimum jump stitch length](/docs/preferences/#minimum-jump-stitch-length-mm) setting. Shorter distances to the next object will have no lock stitches.
Repeats                     ||◦ Defines how many times to run down and back along the path<br />◦ Default: 1 (traveling once from the start to the end of the path)<br />◦ Odd number: stitches will end at the end of the path<br />◦ Even number: stitching will return to the start of the path
Bean stitch number of repeats||◦ Enable [Bean Stitch Mode](/docs/stitches/bean-stitch/)<br />◦ Backtrack each stitch this many times.<br />◦ A value of 1 would triple each stitch (forward, back, forward).<br />◦ A value of 2 would quintuple each stitch, etc. <br />◦ It is possible to define a repeat pattern by entering multiple values separated by a space.
Allow lock stitches         ||Enables lock stitches in only desired positions
Force lock stitches         |☑|Sew lock stitches after sewing this element, even if the distance to the next object is shorter than defined by the collapse length value in the Ink/Stitch preferences.
Tack stitch                 ||Chose your [favorite style](/docs/stitches/lock-stitches/)
Scale Tack stitch           ||
Lock stitch                 ||Chose your [favorite style](/docs/stitches/lock-stitches/)
Scale Lock stitch           ||
Trim After                  |☑|Trim the thread after sewing this object.
Stop After                  |☑|Stop the machine after sewing this object. Before stopping it will jump to the stop position (frame out) if defined.
{: .params-table }

## Underlay

Underlay in Circular Fill is the same as for Auto Fill and uses the fill angle which can be defined in the underlay [params](/docs/stitches/fill-stitch#underlay).

## Sample Files Including Circular Fill Stitches

{% include tutorials/tutorial_list key="stitch-type" value="Circular Fill" %}

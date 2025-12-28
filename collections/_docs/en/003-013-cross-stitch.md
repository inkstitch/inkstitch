---
title: "Cross Stitch"
permalink: /docs/stitches/cross-stitch/
last_modified_at: 2025-12-2
toc: true

feature_row:
  - image_path: /assets/images/docs/cross_stitch_coverage.jpg
    alt: "Cross stitch grid with a fill. Fields covered by the fill for more than 50% show a cross on top"
  - image_path: /assets/images/docs/cross_stitch_coverage02.jpg
    alt: "Same image as before, but the fill element has moved. More crosses are build"
---

{% include upcoming_release.html %}

## What it is

Cross stitch mimics traditional hand embroidery techniques.
Cross-stitch is characterized by small, even crosses, which give the embroidered image a flat, blockish look.

![Cross stitched froq in double cross style](/assets/images/upcoming/3.3.0/cross_stitch.jpg)

# How to Create

* Draw a shape with a fill color
* Open the params dialog
* Select `Cross stitch` as the fill method

### Grids And The Coverage Parameter

It is important to understand the cross stitch `coverage` parameter.

The coverage parameter defines the percentage of overlap for each cross with the fill area. This means, it influences wether a cross is build at a specific spot or not.

Cross stitches are alignde to a grid in pattern size. The grid itself is (by default) aligned to the top left corner of the page canvas.

Ink/Stitch will check how much percent of each grid field is covered by the fill element.
If coverage exceeds the value given by the coverage option (by default 50%), a cross stitch is build.

In the following example only the green fields are covered more than 50% by the fill and receive a cross.
When the fill element is moved on canvas, we receive more stitches.

{% include feature_row %}

When the option `Align grid with canvas` is disabled, the element can be moved on canvas without changing the cross stitch result.
But adjacent cross stitch areas may be misaligned.
{: .notice--info }

### Cross Stitch Method

In Ink/Stitch you can choose from various cross stitch methods.

* **Cross stitch and cross stitch flipped**

  This is the most common method. Two diagonals are building a cross.
  When two crosses are only diagonally conntected, add a small expand value to ensure combined stitching.

  ![Cross stitch method: cross stitch](/assets/images/docs/cross_stitch_method_cross_stitch.jpg)
* **Half stitch and half stitch flipped**

  Half stitches build only a half cross stitch (one diagonal), traveling along the outline of the shape.

  ![Cross stitch method: half cross](/assets/images/docs/cross_stitch_method_half_cross.jpg)
* **Upright cross and upright cross flipped**

  A cross stitch turned, building an uprigt cross.
  Please note, that this cross stitch method may produce jumps, when areas are connected only diagonally.

  ![Cross stitch method: upright cross](/assets/images/docs/cross_stitch_method_upright.jpg)
* **Double cross**

  A combination of cross stitch and upright stitch. As they include upright stitches, note possible jump stitches when areas touch diagonally only.

  ![Cross stitch method: double cross](/assets/images/docs/cross_stitch_method_double_cross.jpg)

### Cross Stitch Helper

Ink/Stitch comes with an extension which helps you to perform cross stitch specific tasks all at once.

* Setup a grid for cross stitch alignment (and visual support while working on cross stitches)
* Apply cross stitch params to selected elements
* Pixelize the outline of selected elements, to easily see and adapt cross stitch positions

## Set Start and End Point

By default, an automatic fill starts as close as possible to the previous embroidery element and ends as close as possible to the next embroidery element.

To change this behavior, set start and end points for autofill objects with [Visual commands](/docs/commands/).

## Paramameters

Run `Extensions > Ink/Stitch  > Params` to tweak the settings to your needs.

Settings||Description
---|---|---
Automatically routed fill stitching| ☑      |Must be enabled for these settings to take effect.
Fill method                        |Cross Stitch|Must be set to cross stitch.
Cross stitch method                ||Choose method (for detailed information see above)
Pattern size                       ||Defines the size of the cross stitch (grid)
Align grid with canvas             ||This ensures good alignment for adjacent cross stitch areas, but it also means that the outcome may change when the element is moved off the grid.<br>Disable this option to ensure, that this element stitches the same, independently on its position on the canvas.
Grid Offset                        ||Shifts the cross stitch grid by given values. X and Y values are separated by a space. Only one input value offsets the pattern evenly for x and y.
Fill coverage                      ||Percentage of overlap for each cross with the fill area.
Expand                             |![Expand example](/assets/images/docs/params-fill-expand.png) |Expand the shape before fill stitching, to compensate for gaps between shapes.<br>It is recommended to use at least a small expand value (e.g. 0.2) on cross stitch elements.
Maximum fill stitch length         |![Stitch length example](/assets/images/docs/params-fill-stitch_length.png) |The length of each stitch in a row. "Max" is because a shorter stitch may be used at the start or end of a row.
Bean stitch number of repeats      ||Determines the number of times to repeat each stitch.<br />◦ A value of `0` does not repeat the stitch (normal stitch)<br/>◦ A value of `1` repeats each stitch three times (forward, back, forward).<br />◦ A value of `2` repeats the stitch five times.
Minimum stitch length              ||Overwrite global minimum stitch length setting. Shorter stitches than that will be removed.
Minimum  jump stitch  length       ||Overwrite global minimum jump stitch length setting. Shorter distances to the next object will have no lock stitches
Allow lock stitches                ||Enables lock stitches in only desired positions
Force lock stitches                |☑ |Sew lock stitches after sewing this element, even if the distance to the next object is shorter than defined by the collapse length value in the Ink/Stitch preferences.
Tack stitch                        ||Chose your [favorite style](/docs/stitches/lock-stitches/)
Scale Tack stitch                  ||
Lock stitch                        ||Chose your [favorite style](/docs/stitches/lock-stitches/)
Scale Lock stitch                  ||
Trim After                         |☑ |Trim the thread after sewing this object.
Stop After                         |☑ |Stop the machine after sewing this object. Before stopping it will jump to the stop position (frame out) if defined.
{: .params-table }

### Sample Files Including Fill Stitches

{% include tutorials/tutorial_list key="stitch-type" value="Cross Stitch" %}

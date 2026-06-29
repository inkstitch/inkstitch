---
title: "Cross Stitch"
permalink: /docs/stitches/cross-stitch/
last_modified_at: 2026-03-27
toc: true

feature_row:
  - image_path: /assets/images/docs/cross_stitch_coverage.jpg
    alt: "Cross stitch grid with a fill. Fields covered by the fill for more than 50% show a cross on top"
  - image_path: /assets/images/docs/cross_stitch_coverage02.jpg
    alt: "Same image as before, but the fill element has moved. More crosses are build"
---

{% include upcoming_release.html %}

## Description

Cross stitch mimics traditional hand embroidery techniques.
Cross-stitch is characterized by small, even crosses, which give the embroidered image a flat, blockish look.

{% include folder-galleries path="butterfly-fill-project/cross/" captions="1:Cross stitch with a black bean stitch outline" %}

## Creation

* Draw a closed shape with a fill color
* Open the params dialog
* Select `Cross stitch` as the fill method

### Grids And The Coverage Parameter

It is important to understand the cross stitch `coverage` parameter.

The coverage parameter defines the percentage of overlap for each cross with the fill area. This means, it influences wether a cross is build at a specific spot or not.

Cross stitches are alignde to a grid in pattern size. The grid itself is (by default) aligned to the top left corner of the page canvas.

Ink/Stitch will check how much percent of each grid field is covered by the fill element.
If coverage exceeds the value given by the coverage option (by default 50%), a cross stitch is build.

In the following example only the green fields are covered more than 50% by the black fill and receive a cross.
When the black fill element is moved on canvas, more crosses are created.

{% include feature_row %}

When the option `Align grid with canvas` is disabled, the element can be moved on canvas without changing the cross stitch result.
But adjacent cross stitch areas may be misaligned.
{: .notice--info }

### Cross Stitch Method

In Ink/Stitch you can choose from various cross stitch methods.

* **Cross stitch and cross stitch flipped**

  This is the most common method. Two diagonals are building a cross.
  When two crosses are only diagonally connected, add a small expand value to the underlying fill to ensure combined stitching.

  ![Cross stitch method: cross stitch](/assets/images/docs/cross_stitch_method_cross_stitch.jpg)
* **Half stitch and half stitch flipped**

  Half stitches build only a half cross stitch (one diagonal), traveling along the outline of the shape.

  ![Cross stitch method: half cross](/assets/images/docs/cross_stitch_method_half_cross.jpg)
* **Upright cross and upright cross flipped**

  A cross stitch turned, building an uprigt cross.
  Please note, that this cross stitch method may produce jumps, when areas are connected only diagonally.

  ![Cross stitch method: upright cross](/assets/images/docs/cross_stitch_method_upright.jpg)

* **Dense upright cross and  dense upright cross flipped**

  More upright crosses are used to fill the shape.

  Coverage is set to 50% in this sample.


  ![Cross stitch method:  dense upright cross](/assets/images/docs/cross_stitch_method_dense_upright.jpg)
* **Double cross and upright double cross**

  A combination of cross stitch and upright stitch, with upright cross on bottom.
  
  ![Cross stitch method: double cross](/assets/images/docs/cross_stitch_method_double_cross.jpg)

* **Smyrna cross and upright Smyrna cross**

  A combination of cross stitch and upright stitch, with upright cross on top.
  
  ![Cross stitch method:Smyrna cross](/assets/images/docs/cross_stitch_method_smyrna.jpg)

### Cross Stitch Assistant

Ink/Stitch comes with an extension which helps you to perform cross stitch specific tasks all at once.

* Setup a grid for cross stitch alignment (and visual support while working on cross stitches)
* Apply cross stitch params to selected elements
* Pixelize and combine the outline of selected elements, to avoid jump stitches and receive a better representation of the cross stitch positioning
* Convert bitmap images into cross stitch fill elements

It also computes and displays the stitch length given the grid dimensions. Maximum stitch length in the cross stitches parameters should be larger than this value.

[Read more](/docs/fill-tools/#cross-stitch-assistant)

### Set Start and End Point

By default, an automatic fill starts as close as possible to the previous embroidery element and ends as close as possible to the next embroidery element.

To change this behavior, set start and end points for autofill objects with [Visual commands](/docs/commands/).

## Parameters

Run `Extensions > Ink/Stitch  > Params` to tweak the settings to your needs.

{% include params.html stitch_type='cross_stitch'%}

## Sample Files Including Cross Stitches

{% include tutorials/tutorial_list key="stitch-type" value="Cross Stitch" %}

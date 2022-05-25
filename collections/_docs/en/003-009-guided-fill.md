---
title: "Guided Fill"
permalink: /docs/stitches/guided-fill/
excerpt: ""
last_modified_at: 2022-05-19
toc: true
---
{% include upcoming_release.html %}

## What it is
Generate curved fill with guide lines.

![Fill stitch detail](/assets/images/docs/guided-fill-detail.jpg)






## How to Create

* Create a **closed path with a fill color**. This shape may have holes.
* Create a guide line to define stitch directions:
    * draw a line with a stroke color and without a fill color
    * select that line
    * run `Extensions > Ink/Stitch > Edit > Selection to guide line`
* Select both and group them together (`Ctrl + G`).  
* Open the params dialog (`Extensions > Ink/Stitch > Params`) and select `Guided fill` as the fill method.

Each group is allowed to contain more than one fill object, but only one guide line is effective and will be used to guide all the shapes of the group, guiding each shape with the intersection of the shape and the guide line. In that case, a shape that does not intersect the guide line will not be filled. The group is also allowed to contain regular stroke objects. On the canvas, a   marker allows to distinguish a guide line from a regular stroke.

Additional guide lines will be ignored.
  

### Several fill shapes in a group 
![Guided Fill Group](/assets/images/docs/guided-fill-group.png)

### A single fill shape  in a group
![Guided Fill One in a Group](/assets/images/docs/en/guided-fill-single-en.png)

## Set Start and End Point

Set start and end points for autofill objects with [Visual commands](/docs/commands/).

## Params

Run `Extensions > Ink/Stitch  > Params` to tweak the settings to your needs.

Read detailed information in the [Guided Fill Params](/docs/params/#guided-fill-params) section.

## Underlay

Underlay in Guided Fill doesn't follow the guide line, but uses the fill angle which can be defined in the underlay [params](/docs/params/#fill-underlay).

## Samples Files Including Guided Fill Stitches
{% include tutorials/tutorial_list key="stitch-type" value="Guided Fill" %}

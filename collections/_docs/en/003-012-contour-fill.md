---
title: "Contour Fill"
permalink: /docs/stitches/contour-fill/
last_modified_at: 2025-04-12
toc: true
---
## Description

Contour fill covers areas with stitches following the contour of an object.

{% include folder-galleries path="butterfly-fill-project/contour/" captions="1:Contour fill applied to the entire shape;2:Contour fill applied to shape sections" %}

[<i class="fa fa-download"></i> Download sample files](/assets/images/stitch-type-butterflies/contour_fill.zip)

## Creation

Create a **closed path with a fill color**.

## Set Start and End Point

Only start point can be set with [Visual commands](/docs/commands/). End point command is not effective with contour fill.

## Parameters

Run `Extensions > Ink/Stitch  > Params`. Set fill method to `Contour Fill` and tweak the settings to your needs.

{% include params.html stitch_type='contour_fill'%}

## Underlay

Underlay in Countour Fill doesn't follow the contour, but uses the fill angle which can be defined in the [fill underlay params](/docs/stitches/fill-stitch#underlay).

## Sample Files Including Contour Fill Stitches

{% include tutorials/tutorial_list key="stitch-type" value="Contour Fill" %}

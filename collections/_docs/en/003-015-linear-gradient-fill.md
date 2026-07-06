---
title: "Linear Gradient Fill"
permalink: /docs/stitches/linear-gradient-fill/
last_modified_at: 2024-05-06
toc: true
---
## Description

Linear gradient fill uses Inkscapes linear gradient color to create seamless gradients with a consistent stitch positioning.

{% include folder-galleries path="butterfly-fill-project/linear_gradient/" captions="1:Blue-purple-gradient;2:Red-yellow-gradient" %}

[<i class="fa fa-download"></i> Download sample files](/assets/images/stitch-type-butterflies/linear_gradient_fill.zip)

## Creation

* Create a closed path. The shape may have holes.
* In the `Fill and Stroke` dialog, select a linear gradient as a fill and adjust colors. On canvas adjust the gradient angle. The stitch angle will have a 90 degree angle to gradient direction.
  ![linear gradient](/assets/images/docs/en/linear-gradient.png)
* Open the params dialog (`Extensions > Ink/Stitch > Params`) and select `Linear Gradient Fill` as the fill method
  Set the params as you wish and Apply

<!--

Tutorial?!?

[![Linear Gradient Fill Sample](/assets/images/docs/linear-gradient.jpg){: width="200x"}](/assets/images/docs/linear-gradient.svg){: title="Download SVG File" download="linear-gradient.svg" } -->

## Set Start and End Point

Set start and end points for autofill objects with [Visual commands](/docs/commands/).

## Parameters

Run `Extensions > Ink/Stitch  > Params` to tweak the settings to your needs.

{% include params.html stitch_type='linear_gradient_fill'%}

## Underlay

Underlay in Linear Gradient Fill is the same as for Auto Fill and uses the fill angle which can be defined in the underlay [params](/docs/stitches/fill-stitch#underlay).

## Sample Files Including Linear Gradient Fill Stitches

{% include tutorials/tutorial_list key="stitch-type" value="Linear Gradient Fill" %}

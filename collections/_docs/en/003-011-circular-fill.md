---
title: "Circular Fill"
permalink: /docs/stitches/circular-fill/
last_modified_at: 2024-06-07
toc: true
---
## Description

Circular fill fills a shape with an embroidered spiral. The center of the spiral is positioned at the center of the shape. A target point can be used to define a custom spiral center.

{% include folder-galleries path="butterfly-fill-project/circular/" captions="1:Circular fill using multiple layers;2:Circular fill with subtle color gradient" %}

[<i class="fa fa-download"></i> Download sample files](/assets/images/stitch-type-butterflies/circular_fill.zip)

## Creation

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

## Parameters

Run `Extensions > Ink/Stitch  > Params` to tweak the settings to your needs.

{% include params.html stitch_type='circular_fill'%}

## Underlay

Underlay in Circular Fill is the same as for Auto Fill and uses the fill angle which can be defined in the underlay [params](/docs/stitches/fill-stitch#underlay).

## Sample Files Including Circular Fill Stitches

{% include tutorials/tutorial_list key="stitch-type" value="Circular Fill" %}

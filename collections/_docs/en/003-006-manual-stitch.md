---
title: "Manual Stitch"
permalink: /docs/stitches/manual-stitch/
last_modified_at: 2026-01-03
toc: true
---
## Description

Manual stitches are create by using each node of a path as a needle penetration point.

{% include folder-galleries path="butterfly-fill-project/manual/" captions="1:Manual path - each node represents one stitch" %}

[<i class="fa fa-download"></i> Download sample files](/assets/images/stitch-type-butterflies/manual_stitch.zip)

## Creation

1. Create a path. The line style or width are not used in the creation of a manual stitch. 
2. Open `Extensions > Ink/Stitch  > Params`.
3. Chose `Manual stitch placement` 

Each node of a path represents a needle penetration point. It doesn't care about bezier curves.

![Manual Stitch Placement](/assets/images/docs/manual-stitch-placement.png)

A clean representation of your manual stitch path can be achieved as follows:
1. Select all nodes (`F2` then `Ctrl`+`A`)
2. Click on ![Make selected nodes corner](/assets/images/docs/tool-controls-corner.jpg){: title="Make selected nodes corner" } in the `Tool Controls Bar`.

## Parameters

Open `Extensions > Ink/Stitch  > Params` to change parameters to your needs.

{% include params.html stitch_type='manual-stitch'%}

## Sample Files Including Manual Stitch

{% include tutorials/tutorial_list key="stitch-type" value="Manual Stitch" %}

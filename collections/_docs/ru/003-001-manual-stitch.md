---
title: "Manual Stitch"
permalink: /ru/docs/stitches/manual-stitch/
excerpt: ""
last_modified_at: 2023-01-15
toc: true
---
## What it is
[![Manual Stitch Flowers](/assets/images/docs/manual-stitch.jpg){: width="200x"}](/assets/images/docs/manual-stitch.svg){: title="Download SVG File" .align-left download="manual-stitch.svg" }
In manual stitch mode Ink/Stitch will use each node of a path as a needle penetration point, exactly as you placed them.

![Manual Stitch Detail](/assets/images/docs/manual-stitch-detail.png)

## How to Create

1. Create a path. Line style or width are irrelevant.
2. Open `Extensions > Ink/Stitch  > Params`.
3. Enable `Manual stitch placement`. The other settings will not have any effect in manual stitch mode.

   ![Params Stroke](/assets/images/docs/en/params-manual-stitch.jpg)

Each node of a path represents a needle penetration point. It doesn't care about bezier curves.

![Manual Stitch Placement](/assets/images/docs/manual-stitch-placement.png)

A clean representation of your manual stitch path can be achieved as follows:
1. Select all nodes (`F2` then `Ctrl`+`A`)
2. Click on ![Make selected nodes corner](/assets/images/docs/tool-controls-corner.jpg){: title="Make selected nodes corner" } in the `Tool Controls Bar`.

## Params

Open `Extensions > Ink/Stitch  > Params` to change parameters to your needs.

Settings||Description
---|--|---
Running stitch along paths    ||Must be enabled for these settings to take effect.
Method                        ||Choose running stitch for the running stitch type
Manual stitch placement       ||**Enable manual stitches**
Repeats                       ||This setting has no effect on manual stitches
Running stitch length         ||This setting has no effect on manual stitches
Running stitch tolerance      ||This setting has no effect on manual stitches
Zig-Zag spacing (peak-to-peak)||This setting has no effect on manual stitches
Allow lock stitches           ||Manual stitches to not add lock stitches automatically. Include them directly into your path.
Force lock stitches           ||This setting has no effect on manual stitches
Trim After                    ||Trim the thread after sewing this object.
Stop After                    ||Stop the machine after sewing this object. Before stopping it will jump to the stop position (frame out) if defined.
{: .params-table }

## Sample Files Including Manual Stitch
{: style="clear: both;" }
{% include tutorials/tutorial_list key="stitch-type" value="Manual Stitch" %}

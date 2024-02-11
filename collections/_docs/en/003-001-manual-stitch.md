---
title: "Manual Stitch"
permalink: /docs/stitches/manual-stitch/
last_modified_at: 2023-04-22
toc: true
---
## What it is
[![Manual Stitch Flowers](/assets/images/docs/manual-stitch.jpg){: width="200x"}](/assets/images/docs/manual-stitch.svg){: title="Download SVG File" .align-left download="manual-stitch.svg" }
In manual stitch mode Ink/Stitch will use each node of a path as a needle penetration point, exactly as you placed them.

![Manual Stitch Detail](/assets/images/docs/manual-stitch-detail.png)

## How to Create

1. Create a path. Line style or width are irrelevant.
2. Open `Extensions > Ink/Stitch  > Params`.
3. Chose `Manual stitch placement` as the method.

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
Method                        ||Choose manual stitch
Max stitch length             ||Stitches longer than this will be subdivided. Leave empty for no subdivision. Short stitches will be removed according settings in the [preferences](/docs/preferences/).
Allow lock stitches           ||Usually manual stitches to not add lock stitches automatically and you have to include them directly into your path. But you can enable them through the setting `force lock stitches`.
Force lock stitches           ||Enables lock stitches for manual stitches.
Trim After                    ||Trim the thread after sewing this object.
Stop After                    ||Stop the machine after sewing this object. Before stopping it will jump to the stop position (frame out) if defined.
{: .params-table }

## Sample Files Including Manual Stitch

{% include tutorials/tutorial_list key="stitch-type" value="Manual Stitch" %}

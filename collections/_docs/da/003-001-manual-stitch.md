---
title: "Manual Stitch"
permalink: /da/docs/stitches/manual-stitch/
excerpt: ""
last_modified_at: 2018-10-09
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

## Tips

### Tie-In and Tie-Off

It will not add tie-in or tie-off stitches automatically, so be aware of creating them within the path.

### Make Nodes Corner

Each node of a path represents a needle penetration point. It will not go along curves.

![Manual Stitch Placement](/assets/images/docs/manual-stitch-placement.png)

A clean representation of your manual stitch path can be achieved as follows:
1. Select all nodes (`F2` then `Ctrl`+`A`)
2. Click on ![Make selected nodes corner](/assets/images/docs/tool-controls-corner.jpg){: title="Make selected nodes corner" } in the `Tool Controls Bar`.

## Sample Files Including Manual Stitch
{: style="clear: both;" }
{% include tutorials/tutorial_list key="stitch-type" value="Manual Stitch" %}


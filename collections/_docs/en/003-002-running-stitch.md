---
title: "Running Stitch"
permalink: /docs/stitches/running-stitch/
excerpt: ""
last_modified_at: 2023-04-22
toc: true
---
## What it is

[![Running Stitch Butterfly](/assets/images/docs/running-stitch.jpg){: width="200x"}](/assets/images/docs/running-stitch.svg){: title="Download SVG File" .align-left download="running-stitch.svg" }

Running stitch produces a series of small stitches following a line or curve.

![Running Stitch Detail](/assets/images/docs/running-stitch-detail.jpg)

## How to Create

Running stitch can be created by setting a **dashed stroke** on a path. Any type of dashes will do the job, and the stroke width is irrelevant.

![Running Stitch Dashes](/assets/images/docs/running-stitch-dashes.jpg){: .align-left style="padding: 5px"}
Select the stroke and go to `Object > Fill and Stroke...` and choose one of the dashed lines in the `Stroke style` tab.

The stitch direction can be influenced by the path direction. If you want to swap the starting and ending point of your running stitch run `Path > Reverse`.

If an object consists of multiple paths, they will be stitched in order with a jump between each.

**Info:** In order to avoid rounding corners, an extra stitch will be added at the point of any sharp corners.
{: .notice--info style="clear: both;" }

## Params

Open `Extensions > Ink/Stitch  > Params` to change parameters to your needs.

Settings|Description
---|---
Running stitch along paths    |Must be enabled for these settings to take effect.
Method                        |Choose `Running stitch / Bean stitch` for the running stitch type
Repeats                       |◦ Defines how many times to run down and back along the path<br />◦ Default: 1 (traveling once from the start to the end of the path)<br />◦ Odd number: stitches will end at the end of the path<br />◦ Even number: stitching will return to the start of the path
Bean stitch number of repeats |◦ Enable [Bean Stitch Mode](/docs/stitches/bean-stitch/)<br />◦ Backtrack each stitch this many times.<br />◦ A value of 1 would triple each stitch (forward, back, forward).<br />◦ A value of 2 would quintuple each stitch, etc.
Running stitch length         |Length of stitches
Running stitch tolerance      |All stitches must be within this distance from a path. A lower tolerance means stitches will be closer together. A higher tolerance means sharp corner may be rounded.
Allow lock stitches           |Enables lock stitches in only desired positions
Force lock stitches           |Sew lock stitches after sewing this element, even if the distance to the next object is smaller than defined in the collapse length value value in the Ink/Stitch preferences.
Tack stitch                   |Chose your [favorite style](/docs/stitches/lock-stitches/)
Lock stitch                   |Chose your [favorite style](/docs/stitches/lock-stitches/)
Trim After                    |Trim the thread after sewing this object.
Stop After                    |Stop the machine after sewing this object. Before stopping it will jump to the stop position (frame out) if defined.

## Routing

For a better stitch routing try the extension `Autoroute Running Stitch` in the [stroke tools](/docs/stroke-tools/).

## Patterned Running Stitch

Read the [tutorial](/tutorials/patterned-unning-stitch/) how to easily create a patterned running stitch.

![patterned running stitch](/assets/images/tutorials/pattern-along-path/copy-paste.png)

## Sample Files Including Running Stitch

{% include tutorials/tutorial_list key="stitch-type" value="Running Stitch" %}

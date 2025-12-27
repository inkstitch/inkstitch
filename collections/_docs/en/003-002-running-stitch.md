---
title: "Running Stitch"
permalink: /docs/stitches/running-stitch/
last_modified_at: 2025-12-27
toc: true
---
## What is it?

[![Running Stitch Butterfly](/assets/images/docs/running-stitch.jpg){: width="200x"}](/assets/images/docs/running-stitch.svg){: title="Download SVG File" .align-left download="running-stitch.svg" }

Running stitch produces a series of small stitches following a line or curve.

![Running Stitch Detail](/assets/images/docs/running-stitch-detail.jpg)

## How to Create It

Running stitch is created from a path with a stroke color.

The stitch direction is impacted by the [path direction](/docs/customize/#enabling-path-outlines--direction). If you want to change the starting and ending point of your running stitch, use  `Path > Reverse`.

If an object consists of multiple paths, they will be stitched in order with a jump between each.

## Parameters

Open `Extensions > Ink/Stitch  > Params` to change parameters to your needs.

Setting|Description
---|---
Running stitch along paths    |Must be selected to use these settings.
Method                        |Determines which stitch to use. Select `Running stitch / Bean stitch` 
Repeats                       |◦ Defines how many times to stitch  along the path<br />◦ Default: 1 (traveling once from the start to the end of the path)<br />◦ Odd number: stitches will end at the end of the path<br />◦ Even number: stitching will return to the start of the path
Bean stitch number of repeats |◦ Determines the number of times to repeat each stitch.<br />◦ A value of '0' does not repeat the stitch (normal stitch)<br/>◦ A value of '1' repeats each stitch three times (forward, back, forward).<br />◦ A value of '2' repeats the stitch six times. <br />◦ See [Bean Stitch Mode](/docs/stitches/bean-stitch/) for more information<br />
Running stitch length         |Determines the length of stitches
Running stitch tolerance      |Determines the acceptable distance from the path. A lower tolerance will bring the stitches closer together. A higher tolerance allows for stitches to be farther away from the path.  A higher tolerance may mean sharp corners may be rounded.
Randomize stitch length       |Allows for randomize stitch length. This is recommended for closely-spaced curved fills to avoid Moiré artefacts. 
Random stitch length jitter   |Only available if `Randomize stitch length` is selected. Determines the variation in the length of each stitch.
Random Seed| Rolling the dice or setting a new value will change the random stitches
Minimum stitch length         |Overwrites the global minimum stitch length setting. Stitches small than this value will be removed.
Minimum  jump stitch  length  |Overwrites the global minimum jump stitch length setting. Shorter distances to the next object will have no lock stitches.
Allow lock stitches           |Enables lock stitches in only desired positions
Force lock stitches           |Determines if lock stitches are sewn after this element, even if the distance to the next object is smaller than defined in the Collapse Length value in the Ink/Stitch preferences.
Tack stitch                   |Determines the type of tack stitch.  Tack stitches are small stitches at the beginning of a stitch. They help to secure the beginning of the thread. [favorite style](/docs/stitches/lock-stitches/)
Lock stitch                   |Determines the type of lock stitch. Lock stitches are small stitches at the end of stitch.  They help to secure the end of the thread.  [favorite style](/docs/stitches/lock-stitches/)
Trim After                    |Determines if the thread is trimmed after sewing this object.
Stop After                    |Determines if the machine is stopped after sewing this object. Before stopping it will jump to the stop position (frame out) if defined.

## Routing

For better stitch routing try the extension `Autoroute Running Stitch` in the [stroke tools](/docs/stroke-tools/).

## Patterned Running Stitch

Read the [tutorial](/tutorials/patterned-unning-stitch/) how to create a patterned running stitch.

![patterned running stitch](/assets/images/tutorials/pattern-along-path/copy-paste.png)

## Sample Files Including Running Stitch

{% include tutorials/tutorial_list key="stitch-type" value="Running Stitch" %}

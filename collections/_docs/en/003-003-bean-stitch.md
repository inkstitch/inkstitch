---
title: "Bean Stitch"
permalink: /docs/stitches/bean-stitch/
last_modified_at: 2023-04-18
toc: true
---
## What it is

[![Bean Stitch Dog](/assets/images/docs/bean-stitch-example.jpg){: width="200x"}](/assets/images/docs/bean-stitch.svg){: title="Download SVG File" .align-left download="bean-stitch.svg" }
Bean stitch describes a repetition of running stitches back and forth. This would result in thicker threading.

![Bean Stitch Detail](/assets/images/docs/bean-stitch-detail.jpg){: width="350x" }

## How to Create

1. Select a **dashed stroke** and open `Extensions > Ink/Stitch  > Params`.

2. Set the number of repeats to `Bean stitch number of repeats` when in [running stitch mode](/docs/stitches/running-stitch).

   ![Bean Stitch Params](/assets/images/docs/en/params-bean-stitch.jpg)

   * A value of 1 would triple each stitch (forward, back, forward).
   * A value of 2 would quintuple each stitch, etc.
   * By entering a sequence of space separated integers in Bean stitch number of repeats, it is possible to define a custom stitch. For instance the sequence 0 1 will yield alternating simple and triple stitches (`≡-≡-≡`).

## Params

Open `Extensions > Ink/Stitch  > Params` to change parameters to your needs.

Settings||Description
---|--|---
Running stitch along paths    ||Must be enabled for these settings to take effect.
Method                        ||Choose running stitch for the running stitch type
Manual stitch placement       ||Enable [Manual Stitch Mode](/docs/stitches/manual-stitch/)
Repeats                       ||◦ Defines how many times to run down and back along the path<br />◦ Default: 1 (traveling once from the start to the end of the path)<br />◦ Odd number: stitches will end at the end of the path<br />◦ Even number: stitching will return to the start of the path
Bean stitch number of repeats ||◦ **Enable Bean Stitch Mode**<br>◦ Backtrack each stitch this many times.<br>◦ A value of 1 would triple each stitch (forward, back, forward).<br>◦ A value of 2 would quintuple each stitch, etc.<br>◦ It is possible to define a repeat pattern by entering multiple values separated by a space.
Running stitch length         ||Length of stitches
Running stitch tolerance      ||All stitches must be within this distance from a path. A lower tolerance means stitches will be closer together. A higher tolerance means sharp corner may be rounded.
Allow lock stitches           ||Enables lock stitches in only desired positions
Force lock stitches           ||Sew lock stitches after sewing this element, even if the distance to the next object is smaller than defined in the collapse length value value in the Ink/Stitch preferences.
Tack stitch                 ||Chose your [favorite style](/docs/stitches/lock-stitches/)
Lock stitch                  ||Chose your [favorite style](/docs/stitches/lock-stitches/)
Trim After                    ||Trim the thread after sewing this object.
Stop After                    ||Stop the machine after sewing this object. Before stopping it will jump to the stop position (frame out) if defined.
{: .params-table }

## Sample Files Including Bean Stitch

{% include tutorials/tutorial_list key="stitch-type" value="Bean Stitch" %}

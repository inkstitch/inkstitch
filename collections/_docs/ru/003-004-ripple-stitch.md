---
title: "Ripple Stitch"
permalink: /ru/docs/stitches/ripple-stitch/
last_modified_at: 2023-01-14
toc: true
---
## What it is

[![Ripple butterfly](/assets/images/docs/ripplefly.jpg){: width="200x"}](/assets/images/docs/ripplefly.svg){: title="Download SVG File" .align-left download="ripplefly.svg" }
Ripple stitch is part running stitch and part filling: it behaves like a running stitch (it can be done in triple stitch for example), it is defined from a stroke, but the embroidery result stretches over a surface. Used loosely, the result looks like ripples, hence the name.

<p style="clear: both;">&nbsp;</p>

{% include video id="e1426a71-486a-4e62-a4c7-3b2f25dd1fc0" provider="diode" %}

Closed shapes will be filled with a spiral (circular ripples). Open shapes will be stitched back and forth (linear ripples). Let's have a closer look at both.

## Circular Ripples

* Create one closed path with a stroke color (no combined paths, such has holes)
* Create [target point or guides](#guiding-ripples) (optional)
* Open params dialog (`Extensions > Ink/Stitch > Params`) and set the `method` to `Ripple`.
* Set [params](#params) to your liking and apply

![Circular ripple examples](/assets/images/docs/en/circular-ripple.svg)

[Download examples](/assets/images/docs/en/circular-ripple.svg)

## Linear Ripples

Linear ripples can be created in various ways. It can be a simple curve or it can be constructed like a satin column.

* Create a open shape (simple stroke, two combined strokes or even a satin column)
* Create [target point or guides](#guiding-ripples) (optional)
* Open params dialog (`Extensions > Ink/Stitch > Params`) and set the `method` to `Ripple`.
* Set [params](#params) to your liking and apply

![Linear ripple examples](/assets/images/docs/en/linear-ripple.svg)

[Download examples](/assets/images/docs/en/linear-ripple.svg)

## Looping ripples

Loops are allowed and welcomed in any ripple path. Use loops to achieve special nice effects.

![Looping ripple stitches](/assets/images/docs/en/ripple-loops.svg)

[Download examples](/assets/images/docs/en/ripple-loops.svg)

##  Guiding ripples

Ripples with only **one subpath** (closed shape or a simple bezier curve) can be guided in either of the three following methods.

### Target point

Define a ripple target position with [visual command] (/docs/commands/):

* Open `Extensions > Ink/Stitch > Commands  > Attach Commands to selected objects ...`
* Select `Ripple stitch target position` and apply
* Select the symbol and move it to the desired position

If no guiding information is provided, the center of the path is used as the target.

### Guide line

* In the very same group (no subgroup) of the ripple stitch object create a stroke curve with the bezier tool, starting close to the ripple curve, leading away from it.
* Select that curve and run `Extensions > Ink/Stitch > Edit > Selection to guide line`.
* Select the ripple curve and run params. Adapt the parameters to your liking.

### Satin guide

With satin guides you will have the ability to lead the ripples precisely using the satin rung method. The width of the satin guide will also have an effect on the ripple width. The positioning of the original ripple shape will be ignored and it will start where the satin begins.

* In the very same group of the ripple stitch object create a [satin column](/docs/stitches/satin-column/) like object with rails and rungs.
* Select the newly created object and run `Extensions > Ink/Stitch > Edit > Selection to guide line`.
* Select the ripple object and run params. Adapt parameters to your liking.

## Params

Params||Description
---|---|---
Running stitch along paths      |  ☑ |Must be enabled for these settings to take effect.
Method     || Chose Ripple stitch 
Repeats                        ||◦ Defines how many times to run down and back along the final embroidery path<br />◦ Default: 1 (traveling once from the start to the end of the path)<br />◦ Odd number: stitches will end at the end of the path<br />◦ Even number: stitching will return to the start of the path
Bean stitch number of repeats ||◦ Enable [Bean Stitch Mode](/docs/stitches/bean-stitch/) which also applies to ripple stitching<br>◦ Backtrack each stitch this many times.<br>◦ A value of 1 would triple each stitch (forward, back, forward).<br>◦ A value of 2 would quintuple each stitch, etc.<br>◦ It is possible to define a repeat pattern by entering multiple values separated by a space.
Running stitch length||Length of stitches in [Running Stitch Mode](/docs/stitches/running-stitch/)
Running stitch tolerance||All stitches must be within this distance of the path. A lower tolerance means stitches will be closer together. A higher tolerance means sharp corners may be rounded.
Number of lines|<img src="/assets/images/docs/ripple_only_lines.svg" alt="Nombre de lignes"/>|Chose how many times the ripple replicates. Default value is 10.
◦Skip first lines <br /> ◦Skip last lines  |<img src="/assets/images/docs/ripple_only_skip.svg" alt="Sauter"/>| Skip (do not embroider)  that number of replications at start and/or end of the embroidery.
Line distance exponent|<img src="/assets/images/docs/ripple_only_exponent.svg" alt="Exposant"/>| ◦ With default value of 1 space between replications is constant<br />◦ With a value greater than 1, the space between two consecutive replications increases as one moves away from the original ripple   <br />◦ With a value smaller than 1, the space between two consecutive replications decreases as one moves away from the original ripple.
Flip exponent |☑  or ▢| exchange role of first and last line in the computation of  line distance
Reverse |☑  or ▢|  Reverse the final embroidery path.  Has no effect on the other  parameters.
Grid  size |<img src="/assets/images/docs/ripple_only_grid.svg" alt="Distance"/>| If the size is strictly positive a grid effect is added. The grid size controls how far apart the new  lines are. 
Scale axes|XY or X or Y or None | for guided ripple only
Starting scale| for guided ripple only|How big the first copy of the line should be, in percent. 
Ending scale| for guided ripple only| How big the last copy of the line should be, in percent.
Rotate| ☑  or ▢| for guided ripple only
Join Style|<img src="/assets/images/docs/flat_or_point.svg" alt="Join Stile"/> |for non circular ripple, how the ripples are joined : Flat(top) or Point(bottom)
Allow lock stitches| ☑  or ▢| Enables lock stitches in only desired positions
Force lock stitches| ☑  or ▢| Sew lock stitches after sewing this element, even if the distance to the next object is shorter than defined by the collapse length value in the Ink/Stitch preferences.
Trim After            |☑ | Trim the thread after sewing this object.
Stop After            |☑ | Stop the machine after sewing this object. Before stopping it will jump to the stop position (frame out) if defined.
{: .params-table }

## Ripple Overview

![Many ripples](/assets/images/docs/en/rippleways_en.svg)

[Download](/assets/images/docs/en/rippleways_en.svg){: download="rippleways.svg" }

### Samples Files Including Ripple Stitches

{% include tutorials/tutorial_list key="stitch-type" value="Ripple Stitch" %}




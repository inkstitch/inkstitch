---
title: "Ripple Stitch"
permalink: /docs/stitches/ripple-stitch/
excerpt: ""
last_modified_at: 2022-06-11
toc: true
---
## What it is

[![Ripple butterfly](/assets/images/docs/ripplefly.jpg){: width="200x"}](/assets/images/docs/ripplefly.svg){: title="Download SVG File" .align-left download="ripplefly.svg" }
Ripple stitch is part running stitch and part filling: it behaves like a running stitch (it can be done in triple stitch for example), it is defined from a stroke, but the embroidery result stretches over a surface. Used loosely, the result looks like ripples, hence the name.

<p style="clear: both;">&nbsp;</p>

{% include video id="e1426a71-486a-4e62-a4c7-3b2f25dd1fc0" provider="diode" %}

## How to Create

From a **stroke (stroke color is set and no fill color)** that may be either a simple path (decomposition applied to it has no effect) or a composed path with exactly two subpaths, just like the rails of a satin column.

Le stroke may be dashed or not, here it does not matter.
{: .notice--warning }

* Create a **stroke (stroke color is set and no fill color)** that may be either a simple path (decomposition applied to it has no effect) or a composed path with exactly two subpaths.
* Select this stroke
* Open params dialog (`Extensions > Ink/Stitch > Params`) and select `Ripple stitch` as method.

If the stroke is closed, any hole  will be ignored and the shape  will be filled with a spiral. Open shapes will be stitched back and forth.

Once the path has been created, it becomes possible to guide the way the ripples replicate to fill a shape.

There are many ways to exploit all the possibilities:

![Many ripples](/assets/images/docs/en/rippleways_en.svg)

[Download](/assets/images/docs/en/rippleways_en.svg){: download="rippleways.svg" }

## Params

Params||Description
---|---|---
Running stitch along paths      |  ☑ |Must be enabled for these settings to take effect.
Methode     || Chose Ripple stitch 
Repeats                        ||◦ Defines how many times to run down and back along the final embroidery path<br />◦ Default: 1 (traveling once from the start to the end of the path)<br />◦ Odd number: stitches will end at the end of the path<br />◦ Even number: stitching will return to the start of the path
Bean stitch number of repeats ||◦ Enable [Bean Stitch Mode](/docs/stitches/bean-stitch/)<br />◦ Backtrack each stitch this many times.<br />◦ A value of 1 would triple each stitch (forward, back, forward).<br />◦ A value of 2 would quintuple each stitch, etc.<br />◦ Only applies to running stitch.
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
Enables lock stitches in only desired positions| ☑  ou ▢| Enables lock stitches in only desired positions
Force lock stitches| ☑  or ▢|Sew lock stitches after sewing this element, even if the distance to the next object is shorter than defined by the collapse length value in the Ink/Stitch preferences.
{: .params-table }

##  Guiding 


### For any ripple : guide line
It is always possible to add a guide line to a ripple: 

- Create a ripple
- Create a stroke
- Turn the stroke into guide line :`Extensions > Ink/Stitch  > Edit > Selection to Guide`
- Group the ripple and the guide

The centers of the replications follow  the guide.

If the guide has two sub-paths, distance between the sub-paths determine replications sizes

### For ripple defined from a simple path : target

It is possible to define a ripple stitch target position using  [visual command] (/docs/commands/). If no guiding information is provided, the center of the path is the target.

### [For satin ripple (two subpaths) : rungs](#traverses)

Works similarly to  Satin Columns rungs

### Samples Files Including Ripple Stitches

{% include tutorials/tutorial_list key="stitch-type" value="Ripple Stitch" %}




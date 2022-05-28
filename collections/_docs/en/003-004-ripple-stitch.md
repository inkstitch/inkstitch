---
title: "Ripple stitch"
permalink: /en/docs/stitches/ripple/
excerpt: ""
last_modified_at: 2022-05-20
toc: true
---
{% include upcoming_release.html %}
## What it is
[![Ripple butterfly](/assets/images/docs/ripplefly.jpg){: width="200x"}](/assets/images/docs/ripplefly.svg){: title="Download SVG File" .align-left download="ripplefly.svg" }
Ripple stitch is part running stitch and part filling: it behaves like a running stitch (it can be done in triple stitch for example), it is defined from a stroke, but the embroidery result stretches over a surface. Used loosely, the result looks like ripples, hence the name.

![Have a look at the video teasing](https://youtu.be/cyvby3KJM10)


## How to Create

From a **stroke (stroke color is set and no fill color)** that may be either a simple path (decomposition applied to it has no effect) or a composed path with exactly two subpaths, just like the rails of a satin column.

* Create a **stroke (stroke color is set and no fill color)** that may be either a simple path (decomposition applied to it has no effect) or a composed path with exactly two subpaths.
* Select this stroke
* Open params dialog (`Extensions > Ink/Stitch > Params`) and select `Ripple stitch` as method.

Once the path has been created, it becomes possible to influence the way the ripples replicate to fill a shape.




There are many ways to exploit all the possibilities:



![Many ripples](/assets/images/docs/en/rippleways_en.svg)



## Params
### Params if starting from a simple path

Params||Description
---|---|---
Running stitch along paths      |  ☑ |Must be enabled for these settings to take effect.
Methode     || Chose Ripple stitch 
Repeats                        ||◦ Defines how many times to run down and back along the final embroidery path<br />◦ Default: 1 (traveling once from the start to the end of the path)<br />◦ Odd number: stitches will end at the end of the path<br />◦ Even number: stitching will return to the start of the path
Bean stitch number of repeats |◦ Enable [Bean Stitch Mode](/docs/stitches/bean-stitch/)<br />◦ Backtrack each stitch this many times.<br />◦ A value of 1 would triple each stitch (forward, back, forward).<br />◦ A value of 2 would quintuple each stitch, etc.<br />◦ Only applies to running stitch.
Running stitch length|Length of stitches in [Running Stitch Mode](/docs/stitches/running-stitch/)
Number of line|<img src="/assets/images/docs/ripple_only_lines.svg" alt="Nombre de lignes"/>|Chose how many times the ripple replicates. Default value is 10.
◦Skip first lines <br /> ◦Skip last lines  |<img src="/assets/images/docs/en/ripple_only_skip_en.svg" alt="Sauter"/>| Skip (do not embroider)  that number of replications at start and/or end of the embroidery.
Flip |☑  or ▢|  Flip begin and start of the final embroidery path.  Has some effect on  Skip parameters and  Line distance exponent parameters
Grid distance|| ineffective when starting from a single path
Line distance exponent|<img src="/assets/images/docs/en/ripple_only_exponent_en.svg" alt="Exposant"/>| ◦ With default value of 1 space between replications is constante<br />◦ With a value greater than 1, the space between two consecutive replications increases as one moves away from the original ripple   <br />◦ With a value smaller than 1, the space between two consecutive replications decreases as one moves away from the original ripple 
Allow lock stitches| ☑  ou ▢||Enables lock stitches in only desired positions
Force lock stitches| ☑  ou ▢||Sew lock stitches after sewing this element, even if the distance to the next object is shorter than defined by the collapse length value in the Ink/Stitch preferences.

### Grid distance  (only when starting from a path with two subpaths)
The two subpaths are going to play similarly to the satin colomn rails,  and it is even possible to add rungs 
With or without rungs it is not possible to add to the final embroidery path to get a grid effect

Additional parameter||Description
---|---|---
Grid distance |<img src="/assets/images/docs/ripple_only_grid.svg" alt="Distance"/>| If the distance is strictly positive a grid effect is added. The distance controls how far apart the new  lines are. Flip has no effect on this parameter.  

### Samples Files Including Ripple Stitches

{% include tutorials/tutorial_list key="stitch-type" value="Ripple stitch" %}




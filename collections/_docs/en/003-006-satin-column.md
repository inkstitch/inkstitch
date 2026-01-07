---
title: "Satin Stitch"
permalink: /docs/stitches/satin-column/
last_modified_at: 2025-12-29
toc: true
---
## What it is

Satin stitch is used for borders, letters or small fill areas.

![Stitch Types - Satin Stitch](/assets/images/docs/stitch-type-satincolumn.jpg)

## How to create

Ink/Stitch offers several option to create satin columns. Methods 1 to 4 create convert to a manual satin column which then can be modified as necessary. Method 5 allows for more customization. 

![Methods](/assets/images/docs/satin_methods.svg)

1. [Stroke to Satin](#1-line-to-satin): for equal width satin columns
2. [Stroke to Live Path Effect Satin](#2-line-to-live-path-effect-satin): modifiable satin column with optional patterned outline
3. [Zigzag to Satin](#3-zigzag-line-to-satin): satin column creation for graphic tablets and touch screens
4. [Fill to Satin](#4-fill-to-satin): create satin columns from fills
5. [Manual Satin Column](#5-manual-satin-column): take full control over every part of the satin column

### Method 1 - Stroke to Satin
#### Option 1
* Add a contour to a path object (with no fill).
* Set contour width to the size of the desired satin stitch.
* Run `Extensions > Ink/Stitch > Satin Tools > Convert Stroke to Satin`
* Optionally run use autoroute to optimize `Extensions > Ink/stitch > Satin Tools > Auto-route Satin...`
* Use as-is or customize rungs and/or rails

Get more information about [Stroke to Satin](/docs/satin-tools/#convert-line-to-satin)
{% include upcoming_release.html %}
#### Option 2
* Add a contour to a path object (with no fill).
* Set contour width to the size of the desired satin stitch (or to any width larger than 0.3, you will need pull compensation to reach a correct width)
* Run `Extensions > Ink/Stitch > Params
* Open the Satin Column Tab and activate Custom Satin Columns
  
With Option 2, the position of the nodes can influence how the satin will be rendered:

![Stroke to satin. Same path with different node setups](/assets/images/upcoming/3.3.0/stroke-to-satin-nodes.png){: width="600px"}



### Method 2 - Stroke to Live Path Effect Satin

This can be used to create a satin which can either have a patterned outline or to create a satin which is more easily to adapt in width. Please note, that once you use auto-routing on this type of satin, the live path effect will be applied and the path can only be adapted manually afterwards.

Use `Path > Object to path` to convert this to a standard satin column.

Get more information about [Live Path Effect Satins](/docs/satin-tools/#stroke-to-live-path-effect-satin)

### Method 3 - Zigzag to Satin

This method is convenient when you use a a touch screen or graphic tablet.

Get more information about [Zigzag to Satin](/docs/satin-tools/#zigzag-line-to-satin)

### Method 4 - Fill to Satin

Fill to Satin can be used to convert a fill into a satin stitch. It is a semi-automatic function and requires a little manual work.

Get more information about [Fill to Satin](/docs/satin-tools/#fill-to-satin)

### Method 5 - Manual Satin Column

A satin column is defined by a shape made of **two mostly-parallel lines**. Ink/Stitch will draw zig-zags back and forth between the two lines. Vary the thickness of the column as you like.

* Combine two strokes with `Path > Combine` or hit `Ctrl+K`.
* [Check path directions](/docs/customize/#enabling-path-outlines--direction). For the satin column to work, they have to be equal.

  If they are not equal, select one point of one subpath with the *Node Editor Tool* (`N`) and run `Path > Reverse`. This will reverse only the selected subpath.
* Use node or rung method as described below.
* Then select your satin column and run params through `Extensions > Ink/Stitch  > Params` or a [custom shortcut key](/docs/customize/).

#### Node Method

[![Satin Column Boat](/assets/images/docs/satin-column.jpg){: width="200x"}](/assets/images/docs/satin-column.svg){: title="Download SVG File" .align-left download="satin-column.svg" }
Depending on the complexity of your design, this method might be time consuming, because the two paths must have the **same number of points**. This means that each path will be made up of an equal number of Bezier curves. Each pair of points acts as a "checkpoint": Ink/Stitch will ensure that a "zag" ends up going from one point to the other.

#### Rung Method

[![Satin Column chefshat](/assets/images/docs/satin-column-rungs-example.jpg){: width="200x"}](/assets/images/docs/satin-column-rungs.svg){: title="Download SVG File" .align-left download="satin-column-rungs.svg" }
The rung method will give you more control over the way the satin column is rendered. Good positioning of points on each of the two lines helps getting the stitch directions right. However, there are situations where you need to add direction lines ("rungs") for satin columns:

* Some tricky corner areas
* Complicated drawings where moving points is both difficult and time consuming
* Special situations where you want the stitch directions to be weird
{: style="clear: both;" }

**Manual adding of rungs**

* Make sure the existing satin column path (with the two subpaths) is selected with the Node Editor tool.
* Press `P` or select the Pencil Tool.
* Hold `Shift`.
* Click once at the start of the rung.
* Click a second time at the end of the rung.

  [![Rungs in Action](https://edutechwiki.unige.ch/mediawiki/images/thumb/6/68/InkStitch-round-bird-2.png/300px-InkStitch-round-bird-2.png)](https://edutechwiki.unige.ch/mediawiki/images/6/68/InkStitch-round-bird-2.png)

  Original design by [Liv Iko](https://thenounproject.com/liv_iko/collection/birds/?i=898697) edited by [EDUTECH Wiki](https://edutechwiki.unige.ch/en/InkStitch)
{: style="font-size: 0.5rem;"}

**Info:** We strongly recommend to use at least three rungs. If you use exactly two rungs (and two rails) it is hard for Ink/stitch to decide which is which.
{: .notice--warning }

## Start and end position

Satin columns automatically start at the nearest point to the previous element and end at the nearest point to the next element.

To disable this behavior open the [params dialog](/docs/params/) and disable one or both of the `start/end at nearest point` options.

Alternatively add a start or end point manually by attaching a [command](/docs/commands/#attach-commands-to-selected-objects-) to the satin column.

## Params

Running `Extensions > Ink/Stitch  > Params` will give you the possibility to fine-tune your satin column and to use underlay.

Satin Column supports three kinds of underlay, of which you can use any or all simultaneously.

Read also [this excellent article](https://www.mrxstitch.com/underlay/) on satin column design.

### Asymmetrical parameter

Some satin column parameters are asymmetrical, meaning that different values ​​can be applied to the two rails.

For example, the "Random percentage of satin width increase" is an asymmetrical parameter. If a single value is entered, it applies to both rails; if two values ​​are entered separated by a space, the first applies to the first rail, and the second applies to the second rail.
![asymmetrical parameter](/assets/images/docs/asymetric_parameter.png)


Some of these params are not part of the recent release.
{: .notice--info}

### Satin Top Layer
{% include upcoming_release_params.html %}
Settings||Description
---|---|--
Custom satin column   | ☑ |Must be enabled for these settings to take effect.
Method                | |Chose `Satin Column`
Short stitch inset    | ![Short Stitch example](/assets/images/docs/satin_multiple_short_stitch_inset_values.jpg)| Stitches in areas with high density will be inset by this amount (%) Short stitch inset can take multiple values separated by a space. When multiple values are set, the satin column will use these to level consecutive short stitches 
Short stitch distance | ![Short Stitch example](/assets/images/docs/params-satin-short_stitch_distance.png) | Inset stitches if the distance between stitches is smaller than this (mm).
Zig-Zag spacing       |![Zig-zag spacing example](/assets/images/docs/params-satin-zig-zag-spacing.png)|the peak-to-peak distance between zig-zags
Pull compensation percentage |![Pull compensation example](/assets/images/docs/params-satin-pull_compensation.png)|Additional pull compensation which varies as a percentage of stitch width. Two values separated by a space may be used for an asymetric effect.
Pull compensation     |![Pull compensation example](/assets/images/docs/params-satin-pull_compensation.png)|Satin stitches [pull the fabric together](/tutorials/push-pull-compensation/), resulting in a column narrower than you draw in Inkscape. This setting expands each pair of needle penetrations outward from the center of the satin column by a fixed length. Two values separated by a space may be used for an asymetric effect.
Reverse rails         |![Reverse Rung](/assets/images/docs/satin-reverse-rung.png) | Enabling this may help if your satin renders very strangely. <br />Options are :<br /> ◦ Automatic, the default value aims to detect and fix the problem <br />◦ Don't reverse , disable automatic detection <br />◦ Reverse first rail <br />◦ Reverse second rail <br />◦ Reverse both rails
Swap rails            |☑ | Swaps the first and the second rails of a satin column. Affecting which side the thread finishes on as well as any other sided property.
Stitch length         | |Stitch length (in mm) of the underpaths (connecting lines to the start or end point)
Tolerance             | |Decreasing tolerance helps the underlay to stay behind the top level. However too small a tolerance may create very short stitches.
Running stitch position | |Position of underpath from between the rails. 0% is along the first rail, 50% is centered, 100% is along the second rail.
Start at nearest point  | |Start at nearest point to the previous element. A start position command will overwrite this setting.
End at nearest point    | |End at nearest point to the next element. An end position command will overwrite this setting.
Random percentage of satin width increase |![Random width increase](/assets/images/docs/params-satin-random-width-increase.png)| Lengthen stitch across rails at most this percent. Two values separated by a space may be used for an asymetric effect.
Random percentage of satin width decrease |![Random width decrease](/assets/images/docs/params-satin-random-width-decrease.png)| Shorten stitch across rails at most this percent. Two values separated by a space may be used for an aysmmetric effect.
Random zig-zag spacing percentage         |![Random zigzag spacing](/assets/images/docs/params-satin-random-zigzag-spacing.png)|Amount of random jitter added to zigzag spacing
Split Method |![default](/assets/images/docs/param_split_satin_default.png) ![simple](/assets/images/docs/param_split_satin_simple.png) ![stager](/assets/images/docs/param_split_satin_stagered.png) | Options:<br /> ◦ default  <br />◦ Simple <br />◦ Staggered
Maximum stitch length | ![Maximum stitch length](/assets/images/docs/params-satin-maximum_stitch_length.png) | Stitches wider than this will be split up (split stitches).
Random Jitter for split stitches          |![Random split stitch jitter](/assets/images/docs/params-satin-random-split-stitch-jitter.png)| Randomizes split stitch length if random phase is enabled, stitch position if disabled.
Random Phase for split stitches           |☑ | Controls whether split stitches are centered or with a random phase (which may increase stitch count).
Stagger this many times before repeating|![Stagger example](/assets/images/docs/params-fill-stagger.png) |Stitches are staggered so that neighboring rows of stitches don't all fall in the same column (which would create a distracting valley effect). Setting this dictates the length of the cycle by which successive stitch rows are staggered. Fractional values are allowed and can have less visible diagonals than integer values. **Active only when split method is staggered**
Minimum length for random-phase split     |  | Defaults to maximum stitch length. Smaller values allow for a transition between single-stitch and split-stitch.
Random seed           | | Use a specific seed to compute stitch plan. If empty, the seed is the element ID . Re-roll if you are not happy with the result.
Minimum stitch length | |Overwrite global minimum stitch length setting. Shorter stitches than that will be removed.
Minimum  jump stitch  length             ||Overwrite global minimum jump stitch length setting. Shorter distances to the next object will have no lock stitches
Allow lock stitches   |☑ |Enables lock stitches in only desired positions
Force lock stitches   |☑ | Sew lock stitches after sewing this element, even if the distance to the next object is smaller than defined in the collapse length value value in the Ink/Stitch prefreneces.
Tack stitch           | |Chose your [favorite style](/docs/stitches/lock-stitches/)
Lock stitch           | |Chose your [favorite style](/docs/stitches/lock-stitches/)
Stop After            |☑ | Stop the machine after sewing this object. Before stopping it will jump to the stop position (frame out) if defined.
Trim After            |☑ | Trim the thread after sewing this object.
{: .params-table }

### Center-Walk Underlay

This is a row of running stitch down the center of the column and back. This may be all you need for thin satin columns. You can also use it as a base for more elaborate underlay.

![Params - Center-Walk Underlay Example](/assets/images/docs/params-center-walk-underlay-example.jpg)

Settings      |Description
---|---
Stitch length |Length of stitches (in mm)
Tolerance     |Decreasing tolerance helps the underlay to stay behind the top level. However too small a tolerance may create very short stitches.
Repeats       |Odd numbers of repeats will reverse the stitch direction of the satin column, causing it to start and end at the same position.
Position      |Position of underlay from between the rails. 0% is along the first rail, 50% is centered, 100% is along the second rail.
{: .table-full-width }

### Contour Underlay

This is a row of running stitch up one side of the column and back down the other. The rows are set in from the edge of the column by an amount you specify. For small or medium width satin, this may serve well enough by itself.

![Params - Contour Underlay Example](/assets/images/docs/params-contour-underlay-example.jpg)

Settings      |Description
---|---
Stitch length           |Length of stitches (in mm)
Tolerance         |Decreasing tolerance helps the underlay to stay behind the top level. However too small a tolerance may create very short stitches.
Inset distance (fixed)  |Shrink the outline by a fixed length, to prevent the underlay from showing around the outside of the satin column. Negative values are possible.
Inset distance (proportional |Shrink the outline by a proportion of the column width, to prevent the underlay from showing around the outside of the satin column. Negative values are possible.

### Zig-Zag Underlay

This is essentially a lower-density satin stitch sewn to the end of the column and back to the start. Added with contour underlay, you get the "German Underlay" mentioned in [this article](https://www.mrxstitch.com/underlay/). For wide columns or challenging fabrics, you can use all three underlay types together.

![Params - Zig-Zag Underlay Example](/assets/images/docs/params-zigzag-underlay-example.jpg)

Settings      |Description
---|---
Inset amount (proportional) |Inset to cover the underlay entirely by the top layer. Negative values are possible. Default: half of contour underlay inset. It is possible to enter two space separated values to define different values for each side.
Inset amount (fixed)    |Inset to cover the underlay entirely by the top layer. Negative values are possible. Default: half of contour underlay inset. It is possible to enter two space separated values to define different values for each side.
Maximum stitch length   | ![Maximum stitch length](/assets/images/docs/params-satin-maximum_stitch_length.png) | Stitches wider than this will be split up (split stitches).
Zig-Zag spacing         |The peak-to-peak distance between zig-zags.

## Satin Tools

Make sure to have a look at the [Satin Tools](/docs/satin-tools/). They will make your life with Satin Columns a lot easier.

## Sample Files Including Satin Column

{% include tutorials/tutorial_list key="stitch-type" value="Satin Stitch" %}

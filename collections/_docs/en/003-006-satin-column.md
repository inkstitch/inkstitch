---
title: "Satin Column"
permalink: /docs/stitches/satin-column/
excerpt: ""
last_modified_at: 2023-01-15
toc: true
---
## What it is

Satin stitch is mostly used for borders, letters or small fill areas.

![Stitch Types - Satin Column](/assets/images/docs/stitch-type-satincolumn.jpg)

## How to create

* Add a contour to a path object (with no filling).
* Set contour width to the size you want your satin stitch to be.
* Run `Extensions > Ink/Stitch > Satin Tools > Convert Line to Satin`
* Optionally run `Extensions > Ink/stitch > Satin Tools > Auto-route Satin...`
* Use as-is or customize rungs or rails

## Manual Satin Column
You define a satin column using a shape made of **two mostly-parallel lines**. Ink/Stitch will draw zig-zags back and forth between the two lines. You can vary the thickness of the column as you like.

* Combine two strokes with `Path > Combine` or hit `Ctrl+K`.
* [Check path directions](/docs/customize/#enabling-path-outlines--direction). For the satin column to work, they have to be equal.<br />If they are not, with the *Node Editor Tool* (`N`) select one point of one sub-path and run `Path > Reverse`. This will reverse only the selected sub-path.
* Use node or rung method as described below.
* Then select your satin column and run params through `Extensions > Ink/Stitch  > Params` or a [custom shortcut key](/docs/customize/).

### Node Method

[![Satin Column Boat](/assets/images/docs/satin-column.jpg){: width="200x"}](/assets/images/docs/satin-column.svg){: title="Download SVG File" .align-left download="satin-column.svg" }
Depending on the complexity of your design, this method might be time consuming, because the two paths must have the **same number of points**. This means that each path will be made up of an equal number of Bezier curves. Each pair of points acts as a "checkpoint": Ink/Stitch will ensure that a "zag" ends up going from one point to the other.

### Rung Method

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

## Params

Running `Extensions > Ink/Stitch  > Params` will give you the possibility to fine-tune your satin column and to use underlay.

Satin Column supports three kinds of underlay, of which you can use any or all simultaneously.

Read also [this excellent article](https://www.mrxstitch.com/underlay/) on satin column design.

Some of these params are not part of the recent release.
{: .notice--info}

### Satin Top Layer

Settings||Description
---|---|--
Custom satin column     | ☑ |Must be enabled for these settings to take effect.
"E" stitch              |![E-stitch example](/assets/images/docs/params-e-stitch.png)|Enables "E" stitch instead of satin. Don't forget to enlarge the zig-zag spacing for this stitch type.
Maximum stitch length   | ![Maximum stitch length](/assets/images/docs/params-satin-maximum_stitch_length.png) | Stitches wider than this will be split up (split stitches).
Pull compensation percentage |![Pull compensation example](/assets/images/docs/params-satin-pull_compensation.png)|Additional pull compensation which varies as a percentage of stitch width. Two values separated by a space may be used for an aysmmetric effect.
Pull compensation       |![Pull compensation example](/assets/images/docs/params-satin-pull_compensation.png)|Satin stitches [pull the fabric together](/tutorials/push-pull-compensation/), resulting in a column narrower than you draw in Inkscape. This setting expands each pair of needle penetrations outward from the center of the satin column by a fixed length. Two values separated by a space may be used for an aysmmetric effect.
Short stitch distance |  | Inset stitches if the distance between stitches is smaller than this (mm).
Short stitch inset    |  | Stitches in areas with high density will be inset by this amount (%)
Swap rails            |☑ | Swaps the first and the second rails of a satin column. Affecting which side the thread finishes on as well as any other sided property.
Zig-Zag spacing         |![Zig-zag spacing example](/assets/images/docs/params-satin-zig-zag-spacing.png)|the peak-to-peak distance between zig-zags
Allow lock stitches     |☑ |Enables lock stitches in only desired positions
Force lock stitches   |☑ | Sew lock stitches after sewing this element, even if the distance to the next object is smaller than defined in the collapse length value value in the Ink/Stitch prefreneces.
Trim After            |☑ | Trim the thread after sewing this object.
Stop After            |☑ | Stop the machine after sewing this object. Before stopping it will jump to the stop position (frame out) if defined.
Random percentage of satin width increase | | Lengthen stitch across rails at most this percent. Two values separated by a space may be used for an aysmmetric effect.
Random percentage of satin width decrease | | Shorten stitch across rails at most this percent. Two values separated by a space may be used for an aysmmetric effect.
Random zig-zag spacing percentage         | |Amount of random jitter added to stitch length.
Random Jitter for split stitches          | | Randomizes split stitch length if random phase is enabled, stitch position if disabled.
Random Phase for split stitches           |☑ | Controls whether split stitches are centered or with a random phase (which may increase stitch count).
Minimum length for random-phase split     |  | Defaults to maximum stitch length. Smaller values allow for a transition between single-stitch and split-stitch.
Random seed           | | Use a specific seed for randomized attributes. Uses the element ID if empty. Re-roll if you are not happy with the result.
{: .params-table }

### Center-Walk Underlay

This is a row of running stitch down the center of the column and back. This may be all you need for thin satin columns. You can also use it as a base for more elaborate underlay.

![Params - Center-Walk Underlay Example](/assets/images/docs/params-center-walk-underlay-example.jpg)

Settings      |Description
---|---
Stitch length |Length of stitches (in mm)
Repeats       |Odd numbers of repeats will reverse the stitch direction of the satin column, causing it to start and end at the same position.
Position      |Position of underlay from between the rails. 0% is along the first rail, 50% is centered, 100% is along the second rail.
{: .table-full-width }

### Contour Underlay

This is a row of running stitch up one side of the column and back down the other. The rows are set in from the edge of the column by an amount you specify. For small or medium width satin, this may serve well enough by itself.

![Params - Contour Underlay Example](/assets/images/docs/params-contour-underlay-example.jpg)

Settings      |Description
---|---
Stitch length           |Length of stitches (in mm)
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

---
title: "Satin Column"
permalink: /docs/stitches/satin-column/
last_modified_at: 2026-04-08
toc: true
---
## Description

Satin column are used for borders, letters or small fill areas.

{% include folder-galleries path="butterfly-fill-project/satin/" captions="1:Satin swirl;2:Satin with randomized stitch length and staggered split stitches;3: Mutlicolor-Satin" %}

[<i class="fa fa-download"></i> Download sample files](/assets/images/stitch-type-butterflies/satin_column.zip)

## Creation

Ink/Stitch offers several methods to create satin columns. Method 1 does no conversion but render a stroke as a satin. Methods 2 to 5 convert to a manual satin column which can then be modified as necessary. Method 5 allows for more customization. 

![Methods](/assets/images/docs/satin_methods.svg)

1. [Stroke rendered as Satin](#1-render-stroke-as-satin): for even width satin columns
2. [Stroke to Satin](#2-stroke-to-satin): for even width satin columns
3. [Stroke to Live Path Effect Satin](#3-stroke-to-live-path-effect-satin): modifiable satin column with optional patterned outline
4. [Zigzag to Satin](#4-zigzag-line-to-satin): satin column creation for graphic tablets and touch screens
5. [Fill to Satin](#5-fill-to-satin): create satin columns from fills
6. [Manual Satin Column](#6-manual-satin-column): take full control over every part of the satin column

### 1 - Render a stroke as satin

{% include upcoming_release.html %}

This method renders paths with a stroke color directly as satins and is therefore the easiest one to create uniform width satin columns.

* Add a stroke color to a path object (with no fill).
* Set contour width to the size of the desired satin stitch
  (the value should be larger than 1.5 mm, see [preferences](/docs/preferences/#minimum-satin-stroke-width) for a deeper insight of the minimum satin width value)
* Run `Extensions > Ink/Stitch > Params
* Open the Satin Column Tab and activate Custom Satin Columns

The position of the nodes can influence how the satin is rendered:

![Stroke to satin. Same path with different node setups](/assets/images/upcoming/3.3.0/stroke-to-satin-nodes.png){: width="600px"}

###  2 - Stroke to Satin

* Add a stroke color to a path object (with no fill).
* Set stroke width to the width of the desired satin stitch.
* Run `Extensions > Ink/Stitch > Satin Tools > Convert Stroke to Satin`
* Use as-is or customize rungs and/or rails

Get more information about [Stroke to Satin](/docs/satin-tools/#convert-line-to-satin)

### 3 - Stroke to Live Path Effect Satin

This can be used to create a satin which can either have a patterned outline or to create a satin which is easier to adapt in width. Please note, that once you use auto-routing on this type of satin, the live path effect will be applied and the path can only be adapted manually afterwards.

Use `Path > Object to path` to convert this to a standard satin column.

Get more information about [Live Path Effect Satins](/docs/satin-tools/#stroke-to-live-path-effect-satin)

### 4 - Zigzag Line to Satin

This method is convenient when you use a a touch screen or graphic tablet.

Get more information about [Zigzag to Satin](/docs/satin-tools/#zigzag-line-to-satin)

### 5 - Fill to Satin

Fill to Satin can be used to convert a fill into a satin column. It is a semi-automatic function and requires additional manual work.

Get more information about [Fill to Satin](/docs/satin-tools/#fill-to-satin)

### 6- Manual Satin Column

A satin column is defined by a shape made of **two mostly-parallel lines**. Ink/Stitch will draw zig-zags back and forth between the two lines. The thickness of the column will be based on the distance between the two lines. 

* Combine two strokes with `Path > Combine` or hit `Ctrl+K`.
* [Check path directions](/docs/customize/#enabling-path-outlines--direction).Both rails  should run in the same direction. If not, Ink/stitch by default will automatically reverse one of them, but you will have better control if you reverse one of them, which is done by selecting one point of one rail with the *Node Editor Tool* (`N`) and run `Path > Reverse`. This will reverse only the selected rail.
* Use node or rung method as described below.
* Then select your satin column and run params through `Extensions > Ink/Stitch  > Params` or a [custom shortcut key](/docs/customize/).

### Stitch direction control

#### Node Method

[![Satin Column Boat](/assets/images/docs/satin-column.jpg){: width="200x"}](/assets/images/docs/satin-column.svg){: title="Download SVG File" .align-left download="satin-column.svg" }
Depending on the complexity of your design, this method might be time consuming, because the two paths must have the **same number of points**. This means that each path will be made up of an equal number of Bezier curves. Each pair of points  (one on each rail) acts as a "checkpoint": Ink/Stitch will ensure that a "zag" ends up going from one point to the other.

#### Rung Method

[![Satin Column chefshat](/assets/images/docs/satin-column-rungs-example.jpg){: width="200x"}](/assets/images/docs/satin-column-rungs.svg){: title="Download SVG File" .align-left download="satin-column-rungs.svg" }
The rung method will give you more control over the way the satin column is rendered. Good positioning of points on each of the two lines helps getting the stitch directions right. However, there are situations where you need to add direction lines ("rungs") for satin columns:

* Some tricky corner areas
* Complicated drawings where moving points is both difficult and time consuming
* Special situations where you want the stitch directions to be weird
{: style="clear: both;" }

**Manual addition of rungs**

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

## Parameters

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

{% include params.html stitch_type='satin'%}

### Center-Walk Underlay

This is a row of running stitch down the center of the column and back. This may be all you need for thin satin columns. You can also use it as a base for more elaborate underlay.

![Params - Center-Walk Underlay Example](/assets/images/docs/params-center-walk-underlay-example.jpg)

{% include params.html stitch_type='satin_center_underlay'%}

### Contour Underlay

This is a row of running stitch up one side of the column and back down the other. The rows are set in from the edge of the column by an amount you specify. For small or medium width satin, this may serve well enough by itself.

![Params - Contour Underlay Example](/assets/images/docs/params-contour-underlay-example.jpg)

{% include params.html stitch_type='satin_contour_underlay'%}

### Zig-Zag Underlay

This is essentially a lower-density satin column sewn to the end of the column and back to the start. Added with contour underlay, you get the "German Underlay" mentioned in [this article](https://www.mrxstitch.com/underlay/). For wide columns or challenging fabrics, you can use all three underlay types together.

![Params - Zig-Zag Underlay Example](/assets/images/docs/params-zigzag-underlay-example.jpg)

{% include params.html stitch_type='satin_zigzag_underlay'%}

## Satin Tools

Make sure to have a look at the [Satin Tools](/docs/satin-tools/). They will make your life with Satin Columns a lot easier.

## Sample Files Including Satin Column

{% include tutorials/tutorial_list key="stitch-type" value="Satin Stitch" %}

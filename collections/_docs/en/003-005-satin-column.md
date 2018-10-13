---
title: "Satin Column"
permalink: /docs/stitches/satin-column/
excerpt: ""
last_modified_at: 2018-10-11
toc: true
---
## What it is

![Stitch Types - Satin Column](/assets/images/docs/stitch-type-satincolumn.jpg)

## How to Create
You define a satin column using a shape made of **two mostly-parallel lines**. Ink/Stitch will draw zig-zags back and forth between the two lines. You can vary the thickness of the column as you like.

* Combine two strokes with `Path > Combine` or hit `Ctrl+K`.
* [Check path directions](/docs/customize/#enabling-path-outlines--direction). For the satin column to work, they have to be equal.<br />If they are not, with the *Node Editor Tool* (`N`) select one point of one sub-path and run `Path > Reverse`. This will reverse only the selected sub-path.
* Use node or rung method as described below.
* Then select your satin column and run params through `Extensions > Ink/Stitch > English > Params` or a [custom shortcut key](/docs/customize/).

### Node Method
[![Satin Column Boat](/assets/images/docs/satin-column.jpg){: width="200x"}](/assets/images/docs/satin-column.svg){: title="Download SVG File" .align-left download="satin-column.svg" }

Depending on the complexity of your design, this method might be time consuming, because the two paths must have the **same number of points**. This means that each path will be made up of an equal number of Bezier curves. Each pair of points acts as a "checkpoint": Ink/Stitch will ensure that a "zag" ends up going from one point to the other.

### Rung Method

The rung method will give you more control over the way the satin column is rendered. Good positioning of points on each of the two lines helps getting the stitch directions right. However, there are situations where you need to add direction lines ("rungs") for satin columns:

* Some tricky corner areas
* Complicated drawings where moving points is both difficult and time consuming
* Special situations where you want the stitch directions to be weird

**Auto generated Satin Columns**
* Add a contour to a path object (with no filling).
* Set contour width to the size you want your satin stitch to be.
* The path should not intersect itself. Try [breaking it up](/docs/satin-tools/#cut-satin-column) into multiple paths if needed.
* Run `Extensions > Ink/Stitch > English > Convert Line to Satin`
* Run `Extensions > Ink/stitch > English > Auto-route Satin...`
* Use as-is or customize the rungs or rails

**Manual adding of rungs**

* Make sure the existing satin column path (with the two subpaths) is selected with the Node Editor tool.
* Press `P` or select the Pencil Tool.
* Hold `Shift`.
* Click once at the start of the rung.
* Click a second time at the end of the rung.

  [![Rungs in Action](https://edutechwiki.unige.ch/mediawiki/images/thumb/6/68/InkStitch-round-bird-2.png/300px-InkStitch-round-bird-2.png)](https://edutechwiki.unige.ch/mediawiki/images/6/68/InkStitch-round-bird-2.png)

  Original design by [Liv Iko](https://thenounproject.com/liv_iko/collection/birds/?i=898697) edited by [EDUTECH Wiki](https://edutechwiki.unige.ch/en/InkStitch)
{: style="font-size: 0.5rem;"}

**Info:** Rungs have to be shorter than the satin column itself. Otherwise Ink/Stitch will switch directions or you receive the following message: `error: satin column: One or more of the rungs doesn't intersect both rails.  Each rail should intersect both rungs once.`
{: .notice--warning }

## Params

Running `Extensions > Ink/Stitch > English > Params` will give you the possibility to fine-tune your Satin Column or to use underlay.
For more information read through the [Satin Params](/docs/params/#satin-params) section.

### Underlay
Satin Column also supports three kinds of underlay, of which you can use any or all simultaneously. Read [this excellent article](https://www.mrxstitch.com/underlay/) on Satin Column design.

#### Center Walk Underlay
This is a row of running stitch down the center of the column and back. This may be all you need for thin satin columns. You can also use it as a base for more elaborate underlay.

#### Contour Underlay
This is a row of running stitch up one side of the column and back down the other. The rows are set in from the edge of the column by an amount you specify. For small or medium width satin, this may serve well enough by itself.

#### ZigZag Underlay
This is essentially a lower-density satin stitch sewn to the end of the column and back to the start. Added with contour underlay, you get the "German Underlay" mentioned in the article linked above. For wide columns or challenging fabrics, you can use all three underlay types together.

## Satin Tools

Make sure to have a look at the [Satin Tools](/docs/satin-tools/). They will make your life with Satin Columns a lot easier.

## Sample Files Including Satin Column
{% include tutorials/tutorial_list key="stitch-type" value="Satin Stitch" %}

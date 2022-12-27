---
title: "Tools: Stroke"
permalink: /docs/stroke-tools/
excerpt: ""
last_modified_at: 2022-12-27
toc: true
---
## Autoroute Running Stitch

This tool will **replace** your set of running stitches  with a new set of running stitches in logical stitching order avoiding as many jumps as possible . Under-pathing  will be added as necessary  . The resulting running stitches will retain all of the parameters you had set on the original stitches including stitch length, number of repeats, bean stitch number of repeats, etc. Underpaths will only retain the stitch length, but will be set to only one  repeat and no bean stitch number of repeats.

### Usage

- Select all the running stitches (prepared with parameters)that you wish to organize
- Run `Extensions > Ink/Stitch > Tools : Stroke > Auto-Route Running stitch...`
- Enable desired options and click apply

Tip: By default, it will choose the left-most extreme node as the starting point and the right-most extreme node  as the ending point (even if these are not terminal nodes). You can override this by attaching the "Auto-route running stitch starting/ending position" commands.

### Options

- Enable **Add nodes at intersections** will normally yield a better routing as under-paths will preferably start/end at intersections and terminal nodes.  You should only disable this option if you have manually added nodes where you want the paths to be split.
- Enable **Trim jump stitches** to use trims instead of jump stitches. Trim commands are added to the SVG, so you can modify/delete as you see fit.
- Enable **Preserve order of running stitches** if you prefer to keep your former order. 


## Convert Satin to Stroke

Satin to stroke will convert a satin column to it's centerline. This can be useful, when you decide later in the designing process to turn a satin column into a running stitch. You can also use it to alter the thickness of your satin column, when pull compensation isn't satisfying. In that case use this function to convert your satin column into a running stitch, set stroke width in the fill and stroke panel and run the ["Connvert line to to satin"](#convert-line-to-satin) function. 

This works best on evenly spaced satin columns.

![Satin to Stroke example](/assets/images/docs/en/satin_to_stroke.png)

### Usage

1. Select the satin column(s) you want to convert into a running stitch
2. Run `Extensions > Ink/Stitch > Satin Tools > Convert satin to stroke...`
3. Choose wether you want to keep selected satin column(s) or if you want to replace them
4. Click apply


## Fill to Stroke

{% include upcoming_release.html %}

Fill outlines never look nice when embroidered - but it is a lot of work to convert a fill outline to a satin column or a running stitch. This tool helps you with this operation.

It is comparable to the Inkscape functionality of `Path > Trace bitmap > Centerline tracing` (- and has similar issues.) But instead of converting raster graphics, it will find the centerline of vector based objects with a fill.

You can refine the result by defining cut lines.

### Usage

*  (Optional) Draw cut lines at the intersections/joints. They are simple stroke objects. This is especially useful, when you aim for satin columns. Please note, that each stroke element has to cut the fill element in which that each side of the fill is entirely disconnected.
* Select one or more fill objects which you want to convert to a centerline along with the cut lines if you have defined them ealier.</label>
* Run `Extensions > Ink/Stitch > Tools: Stroke > Fill to Stroke`
* Set options and apply
* Use the node tool to perform corrections if necessary

### Options

* Keep original: enable this option, if you want to keep the original object(s). Otherwise it will be removed.
* Threshold for dead ends (px): This will remove small lines. In most cases the best value is the approximate line width of the original shape in pixels.
* Dashed line: Set to true if you aim for a running stitch outline.
* Line width (px): If you want to convert this directly into a satin column, set this to the satin column width. In most cases you would want to keep this value low, so it will be easier to check and correct the outlines before the conversion.

## Jump to Stroke

{% include upcoming_release.html %}

This will create a running stitch from the end position of the first element to the start position of the second element. Place this running stitch under following top stitches and avoid jump stitches.

### Usage

* Select two or more objects
* Run `Extensions > Ink/Stitch > Tools: Stroke > Jump Stitch to Stroke`

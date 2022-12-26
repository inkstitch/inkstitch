---
title: "Tools: Satin"
permalink: /da/docs/satin-tools/
excerpt: ""
last_modified_at: 2021-10-29
toc: true
---
`Extensions > Ink/Stitch  > Satin Tools` include a number of useful helpers, making it easy to work with [satin columns](/docs/stitches/satin-column/).

**Example:**
* Create a path with the help of the bezier curves tool (`B`)
* Run [Convert Line to Satin](#convert-line-to-satin)
* Use the [Params dialog](/docs/params/#satin-params) to set an underlay
* Run [Auto-Route Satin](#auto-route-satin-columns) to recieve nicely routed satin columns

[![Convert Line to Satin](/assets/images/docs/en/satin-tools.svg)](/assets/images/docs/en/satin-tools.svg){: title="Download SVG File" download="satin-tools.svg" }

**Tip:** For faster access [set shortcuts](/docs/customize/) on specific satin tools.
{: .notice--info}

## Auto-Route Satin Columns...

This tool will replace your satins with a new set of satin columns in logical stitching order. Under-pathing and jump-stitches will be added as necessary and satins will be broken to facilitate jumps. The resulting satins will retain all of the parameters you had set on the original satins, including underlay, zig-zag spacing, etc.

### Usage

1. Select satin columns (prepared with underlay, etc.)
2. Run `Extensions > Ink/Stitch  > Satin Tools > Auto-Route Satin Columns...`
3. Enable desired options and click apply

**Tip:** By default, it will choose the left-most extreme as the starting point and the right-most extreme as the ending point (even if these occur partway through a satin such as the left edge of a letter "o"). You can override this by attaching the ["Auto-route satin stitch starting/ending position" commands](/docs/commands/#--startingending-position-for-auto-route-satin).
{: .notice--info }

### Options

* Enable **Trim jump stitches** to use trims instead of jump stitches. Any jump stitch over 1mm is trimmed. Trim commands are added to the SVG, so you can modify/delete as you see fit.

* If you prefer to keep your previous order (which might be the case if you have overlaying satins), enable the option **Preserve order of Satin Columns**.

## Convert Line to Satin

This extension will convert a stroke into a satin column with a specified width. After the conversion you will see the two rails and (possibly) lots of rungs, depending on the shape of your line.

### Usage

1. Draw a bezier curve (`B`)
2. Set the stroke width in the "Fill and Stroke" panel ("Stroke style" tab), which you can access with `Shift+Ctrl+F`
2. Run `Extensions > Ink/Stitch  >  Tools: Satin > Convert Line to Satin`

## Cut Satin Column

Split a satin column at a specified point. The split happens at a stitch boundary to ensure that the two resulting satins sew just like the original. All parameters set on the original satin remain on the two new satins, and all rungs are retained. If one of the satins would have no rungs left, a new rung is added.

### Usage

1. Select a satin column (simple satin doesn't work)
2. Attach the "Satin split point" command using `Extensions > Ink/Stitch  > Commands > Attach Commands to Selected Objects`.
3. Move the symbol (or just the connector line's endpoint) to point to the exact spot you want the satin to be split at.
4. Select the satin column again.
5. Run `Extensions > Ink/Stitch  > Tools: Satin > Split Satin Column`.
6. The split point command and connector line disappear, and nothing else appears to have happened. Select your satin and you'll see that it's been split.

## Flip Satin Column Rails

This is a little tool to help you to plan your stitch path precisely. E.g. flip satin columns to shorten connections between two sections.

A satin column which originally starts on the left rail and ends on the right, will start on the right rail and end on the left.

![Flip Satin Columns](/assets/images/docs/en/flip-satin-column.jpg)

### Usage

* Select one or more satin column(s)
* Run `Extensions > Ink/Stitch  > Tools: Satin > Flip Satin Columns`


---
title: "Workflow"
permalink: /docs/workflow/
excerpt: ""
last_modified_at: 2021-04-11
toc: true
---
![Ink/Stitch workflow](/assets/images/docs/en/workflow-chart.svg)

## ![Create Icon](/assets/images/docs/workflow-icon-create.png) Step 1: Create a Vector Image

At first you need an idea or an image that you want to transfer into an embroidery file. You can either paint it from scratch or use an existing image.

### Draw in Inkscape

#### Create Paths

Inkscape offers various tools to create vector images. You can use e.g.

* ![freehand lines icon](/assets/images/docs/inkscape-tools-freehand.png) Freehand lines (<key>P</key>)
* ![freehand lines icon](/assets/images/docs/inkscape-tools-bezier.png) Bezier curves (<key>B</key>)

Try also the other tools in the toolbar. For example specific shapes like

* ![square icon](/assets/images/docs/inkscape-tools-square.png) Rectangle
* ![circle icon](/assets/images/docs/inkscape-tools-circle.png) Circle
* ![polygon icon](/assets/images/docs/inkscape-tools-polygon.png) Star/Polygon
* ![spiral icon](/assets/images/docs/inkscape-tools-spiral.png) Spiral

#### Edit Paths

Edit objects and paths with:
* ![node tool icon](/assets/images/docs/inkscape-tools-select.png) Select tool (<key>S</key>) and
* ![node tool icon](/assets/images/docs/inkscape-tools-node.png) Node editor tool (<key>N</key>)

Scale, rotate and move the whole object with the select tool. The node editor tool serves to manipulate selected nodes, etc.

Additionally you could use path effects (`Path > Path Effects...`). Remember to always convert the resulting object back into a path (`Path > Convert object to path`).

### Use Existing Picture/Graphic

When basing a design off an existing picture or graphic, load it into Inkscape in its own layer. Some graphics are amenable to Inkscape's [auto-tracing feature](https://inkscape.org/en/doc/tutorials/tracing/tutorial-tracing.html) (`Path > Trace Bitmap` or `Shift+Alt+B`), especially if you simplify the image in a graphic editor first (e.g. with [GIMP](https://www.gimp.org/)).

After tracing, clean up the vector shapes, using `Path > Simplify` (`Ctrl+L`) and deleting nodes by hand when possible. The goal is to use as few Bezier curves as reasonably possible to represent the image.
Often the tracing function will produce very little objekts which are impossible to embroider. Therefore it is advisable to cleanup your document with `Extensions > Ink/Stitch > Troubleshoot > Cleanup document...`.

When the image is needed to be traced by hand, use the freehand drawing tool. This tool creates paths with a lot of Beziér nodes, so again, simplify the curves as much as possible.

**Tip:** Working with an existing SVG image can save a ton of time, so consider using your search engine with image search filter set to SVG.
{: .notice--info }

### Text

For text, choose a font carefully. It's quite hard to make satin look good when it's 1mm wide or narrower. Sans-serif fonts tend to be the easiest. For text smaller than 4mm tall, you'll have a very difficult time making lowercase letters look good, so consider block-caps. Cursive/script fonts can work well, but it's not going to be as easy as you think.

Ink/Stitch offers ready to use fonts which can be inserted into your document through `Extensions > Ink/Stitch > Lettering`

## ![Vectorize](/assets/images/docs/workflow-icon-vectorize.png) Step 2: Convert to Embroidery Vectors & Parametrize

At this point, you'll have a vector graphic representation of your image. The next thing to do is to convert your vectors into the kind that Ink/Stitch understands.

### The Object Panel

We recommend to make heavy use of layers and groups at this point.

In the object panel (open with <key>Ctrl</key><key>Shift</key><key>O</key>) you can manage layers, groups and objects.

You can save the original image by duplicating the layer:

* Right click on the layer (if you didn't rename the layer it will be called `Layer 1`)
* Click on `Duplicate`
* Close the eye by clicking on it.

This will make the first layer invisible. Any layer, group, or vector shape that is set invisible will be ignored by Ink/Stitch. We will now work with the copy.

![Objects panel](/assets/images/docs/en/objects-panel.png)

### Groups

Use groups to structure your document:

* Select objects with your mouse
* Add or remove objects with <key>shift</key><key>click</key>
* Hit <key>Ctrl</key><key>G</key>

Ungrouping objects works as follows:

* Select the group(s)
* Hit <key>Ctrl</key><key>Shift</key><key>G</key>

### Stitch Types

Ink/Stitch offers various stitch types. Depending on which stitch type you are willing to use, you have to set the fill color, or stroke parameters with `Object > Fill and Stroke...` (<key>Ctrl</key><key>Shift</key><key>F</key>).

Have a look at this table and follow the links to understand how to create a specific stitch type:

Path Object | Stitch Type
---|---
(Dashed) stroke |[running stitch](/docs/stitches/running-stitch/), [manual stitch](/docs/stitches/manual-stitch/), [zig-zag stitch](/docs/stitches/zigzag-stitch/), [bean stitch](/docs/stitches/bean-stitch/)
Two combined strokes (with optional rungs) | [satin column](/docs/stitches/satin-column), [e-stitch](/docs/stitches/e-stitch)
Closed path with a fill color | [fill stitch](/docs/stitches/fill-stitch/)
{: .equal-tables }

### Parametrize

Set parameters using `Extensions > Ink/Stitch  > Params`. You find a description for each parameter in the [Params](/docs/params/) section of this documentation. Each time you change parameter values, you'll be able to see the simulated result in a preview window. Once you are satisfied with the result, click `Apply and close` to save the values into your SVG-file.

At this point, save your SVG file. If Inkscape is starting to become sluggish (due to an Inkscape memory leak), restart it before continuing.


## ![Create Icon](/assets/images/docs/workflow-icon-order.png) Step 3: Plan Stitch Order & Attach Commands

### Stitch Order

When you're designing for embroidery machines that can't cut the thread mid-sew or switch colors automatically, you're going to want to optimize your stitch path to reduce or hide jump stitches and make minimal color changes. Also try to avoid stitching over jump stitches when possible, because it's a total pain to trim them by hand when you do.

The order of stitching also affects how the fabric pulls and pushes. Each stitch will distort the fabric, and you'll need to take this into account and compensate accordingly. [More Information](/tutorials/push-pull-compensation/)

Once you've created all vectors, it's time to put everything in the right order. This is where the Inkscapes Objects tool (`Objects > Objects ...`) comes in useful. Optimize your order to minimize color changes and reduce or hide jump-stitches. Additionally you can make use of the Ink/Stitch [sorting function](/docs/edit/#re-stack-objects-in-order-of-selection).

Ink/Stitch will stitch objects in exactly the order they appear in your SVG document, from lowest to highest in stacking order. If the distance between two objects is long, Ink/Stitch will add a jump-stitch between them automatically. It uses the color of the object to determine thread color, so changes in color from one object to the next will result in a thread-change instruction being added to the embroidery output file.

**Tip:** Inkscape gives you the ability to "raise" and "lower" objects in the stacking order using the PageUp and PageDown keys. The new functions "Stack Up" and "Stack Down" will give you much better control over the stacking order. So we recommend to rather bind PageUp and Page Down to them. [More Information](/docs/customize/#shortcut-keys)
{: .notice--info }

**Info:** You can also manually manipulate the underlying SVG XML structure by using Inkscape's XML Editor pane (`CTRL-SHIFT-X`). Its "Raise" and "Lower" buttons directly manipulate the order of XML tags in the SVG file and are not subject to the same limitations as the original PageUp and PageDown. Note that the ordering of XML tags in the XML Editor tool is the _reverse_ of the order of objects in the Objects tool.
{: .notice--info }

### Commands

[Commands](/docs/commands/) also help to optimize your stitch path. You can set start and ending points, push the frame into defined positions or set trim and cut commands, etc.

## ![Create Icon](/assets/images/docs/workflow-icon-visualize.png)  Step 4: Visualize

Ink/Stitch supports three ways to preview your design:

* [Simulator with (optional) realistic preview](/docs/visualize/#simulator--realistic-preview)
* [Print Preview](/docs/print-pdf/)
* [Stitch Plan Preview](/docs/visualize/#stitch-plan-preview) (Undo with <key>Ctrl</key><key>Z</key>)

## ![Create Icon](/assets/images/docs/workflow-icon-export.png) Step 5: Save the Embroidery File

Once you've got everything in the right order, run `File > Save a copy...` to [export](/docs/import-export/) to a file format supported by your machine. Most machines can support DST, and some Brother machines prefer PES. Do not forget to also save your file in the SVG-format. Otherwise it's going to be difficult to change details later.

## ![Create Icon](/assets/images/docs/workflow-icon-testsew.png) Step 7: Test-sew

There's always room for improvement! To test out your design, prepare a test piece of fabric that matches your final fabric as closely as possible. Use the same stabilizer and the exact same fabric if possible. For t-shirts, try to find a similar fabric (usually knit). Knits need a lot of stabilization.

Sew out the design, watching the machine to make sure that there aren't any surprises. Watch out for gaps that indicate that the fabric has been distorted. Also search for areas where stitches are piling up too closely and the machine is having trouble sewing, which indicates that the stitch density is too high.

## ![Create Icon](/assets/images/docs/workflow-icon-optimize.png) Step 8+: Optimize

Then go back and tweak your design. Hopefully it only takes a few tries to get it how you want it.

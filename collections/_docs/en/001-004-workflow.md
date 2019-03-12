---
title: "Workflow"
permalink: /docs/workflow/
excerpt: ""
last_modified_at: 2018-10-13
toc: true
---
## Step 1: Sketch Design or Use an Image

When basing a design off an existing picture or graphic, load it into Inkscape in its own layer. Some graphics are amenable to Inkscape's [auto-tracing feature](https://inkscape.org/en/doc/tutorials/tracing/tutorial-tracing.html) (`Path > Trace Bitmap` or `Shift+Alt+B`), especially if you simplify the image in a graphic editor first (e.g. with [GIMP](https://www.gimp.org/)).

**Tip:** If you have Linux and need to vectorize a stroke, you could make use of an other Inkscape plugin, which aims to do [centerline tracing](https://github.com/fablabnbg/inkscape-centerline-trace). For embroidery purposes it might only apply to simple shapes.
{: .notice--info }

After tracing, clean up the vector shapes, using `Path > Simplify` (`Ctrl+L`) and deleting nodes by hand when possible. The goal is to use as few Bezier curves as reasonably possible to represent the image.

When the image is needed to be traced by hand, use the freehand drawing tool. This tool creates paths with a lot of Bezier nodes, so again, simplify the curves as much as possible.

**Tip:** Working with an existing SVG image can save a ton of time, so consider using Google image search with the filter set to SVG.
{: .notice--info }

For **text**, choose a font carefully. It's quite hard to make satin look good when it's 1mm wide or narrower. Sans-serif fonts tend to be the easiest. For text smaller than 4mm tall, you'll have a very difficult time making lowercase letters look good, so consider block-caps. Cursive/script fonts can work well, but it's not going to be as easy as you think.


## Step 2: Plan Stitch Path and Color Changes

At this point, you'll have a vector graphic representation of your image. The next thing to do is to convert your vectors into the kind that Ink/Stitch understands and put them in the right order.

When you're designing for embroidery machines that can't cut the thread mid-sew or switch colors automatically, you're going to want to optimize your stitch path to reduce or hide jump stitches and make minimal color changes. Also try to avoid stitching over jump stitches when possible, because it's a total pain to trim them by hand when you do.

The order of stitching also affects how the fabric pulls and pushes. Each stitch will distort the fabric, and you'll need to take this into account and compensate accordingly. [More Information](/tutorials/push-pull-compensation/)

## Step 3: Create the Embroidery Vectors

We recommend to make heavy use of layers and groups at this point. If you've traced an image, leave it as the lowest layer and set it invisible in the Layers or Objects palette. Any layer, group, or vector shape that is set invisible will be ignored by Ink/Stitch.

Keep your initial traced vectors in their own layer and use them as a reference when designing embroidery vectors. Copy and paste then as necessary into a higher layer and work with the copies.

Set parameters using `Extensions > Ink/Stitch > English > Params`. To learn about the stitch types and how to apply them, have a look at the [Params](/docs/params/) section of this documentation. Each time you change parameter values, you'll be able to see the simulated result in a preview window. Once you are satisfied with the result, click `Apply and close` to save the values into your SVG-file.

For a detailed inspection of the result, select a vector path and run `Extensions > Ink/Stitch > English > Embroider...`, which will cause it to show a stitch plan for just the selected object(s). Examine the resulting stitch plan using the node editor tool. Each vertex is a single stitch; the needle will penetrate the fabric and interlock with the bobbin thread at this point. Once done examining the stitch plan, undo the Embroider operation (`Ctrl+Z`) to remove the stitch plan and make your vectors visible again.

At this point, save your SVG file. If Inkscape is starting to become sluggish (due to an Inkscape memory leak), restart it before continuing.

## Step 4: Ordering

Once you've created all vectors and test-embroidered them individually, it's time to put everything in the right order. This is where the Inkscapes Objects tool (`Objects > Objects ...`) comes in useful. Optimize your order to minimize color changes and reduce or hide jump-stitches.

Ink/Stitch will stitch objects in exactly the order they appear in your SVG document, from lowest to highest in stacking order. If the distance between two objects is long, Ink/Stitch will add a jump-stitch between them automatically. It uses the color of the object to determine thread color, so changes in color from one object to the next will result in a thread-change instruction being added to the embroidery output file.

**Tip:** Inkscape gives you the ability to "raise" and "lower" objects in the stacking order using the PageUp and PageDown keys. The new functions "Stack Up" and "Stack Down" will give you much better control over the stacking order. So we recommend to rather bind PageUp and Page Down to them. [More Information](/docs/customize/#shortcut-keys)
{: .notice--info }

**Info:** You can also manually manipulate the underlying SVG XML structure by using Inkscape's XML Editor pane (`CTRL-SHIFT-X`). Its "Raise" and "Lower" buttons directly manipulate the order of XML tags in the SVG file and are not subject to the same limitations as the original PageUp and PageDown. Note that the ordering of XML tags in the XML Editor tool is the _reverse_ of the order of objects in the Objects tool.
{: .notice--info }

## Step 5: Render to a file format supported by your machine

Once you've got everything in the right order, deselect all objects and run *Embroider* again. This will embroider all visible objects in the document. In the extension settings, select a file format supported by your machine. Most machines can support DST, and some Brother machines prefer PES.

*Embroider* will create a file in the specified output directory named after your SVG file, but with the extension changed to `.DST`, `.PES`, or whatever format you selected. It will back up any existing file there, storing up to 5 old copies of each file.

## Step 6: Output

You can either create a stitch file for a selection of objects or for all path objects. To create an embroidery file for the whole design:

* Click into some empty space (in order to deselect)
* Run `Extensions > Ink/Stitch > English > Embroider...`
* Select the right file format for your machine
* Type a directory name where you want to save your output files. E.g. `C:\Users\%USERNAME%\Documents` on Windows. Ink/Stitch will remember this information.

**Info:** With newer versions of Ink/Stitch it is also possible to output your design through `File > Save As...`. You can also export to multiple formats at once.
{: .notice--info }

## Step 7: Test-sew

There's always room for improvement! To test out your design, prepare a test piece of fabric that matches your final fabric as closely as possible. Use the same stabilizer and the exact same fabric if possible. For t-shirts, try to find a similar fabric (usually knit). Knits need a lot of stabilization.

Sew out the design, watching the machine to make sure that there aren't any surprises. Watch out for gaps that indicate that the fabric has been distorted. I'm also watching for areas where stitches are piling up too closely and the machine is having trouble sewing, which indicates that the stitch density is too high.

## Step 8+: iterate

Then go back and tweak your design. Hopefully it only takes a few tries to get it how you want it. Once you're done, copy the final embroidery file from your output directory, just to avoid accidentally overwriting it in the future.


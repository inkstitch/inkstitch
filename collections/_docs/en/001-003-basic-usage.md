---
title: "Basic Usage"
permalink: /docs/basic-usage/
excerpt: ""
last_modified_at: 2018-04-28
toc: true
---
Try the following steps in order to test the extension and to learn about basic functionality.

**Tip:** If you are new to Inkscape, have a look at their [Basic Tutorial](https://inkscape.org/en/doc/tutorials/basic/tutorial-basic.html) first.
{: .notice--info }

## Step 1 - Draw an Object

Create an object, e.g. a circle and make sure it has both a stroke and a fill.

**Info:** You'll learn later, that *using a stroke for satin columns isn't the best way to go*. We used it here only to create an easy example. Read the Stitch Library to get more informations on stitch types.
{: .notice--warning }

![Fill and Stroke](https://edutechwiki.unige.ch/mediawiki/images/thumb/8/86/SVG-yellow-circle-stroke-fill.png/300px-SVG-yellow-circle-stroke-fill.png)

## Step 2 - Convert to Path
Transform **all objects** you want to stitch to paths:

* Select all objects (`Ctrl+A`)
* `Path > Object to Path` or `Ctrl+Alt+C`.<br>

**Info:** Objects that are not of "path" type, are ignored by InkStitch.
{: .notice--warning }

## Step 3 - Parametrize SVG Path for Embroidery

* Select at least one object.
* Open `Extensions > Ink/Stitch > Params` and play with them.
* For now, just accept the defaults or close without saving.

## Step 4 - Create the Embroidery File

You can either create a stitch file for a selection of objects or for all path objects.
To create an embroidery file for the whole design:

* Click into some empty space (in order to deselect)
* Run `Extensions > Ink/Stitch > English > Embroider...`
* Select the right file format for your machine
* Type a directory name where you want to save your output files. E.g. `C:\Users\%USERNAME%\Documents` on Windows. Ink/Stitch will remember this information.

## Step 5 - Inspect in Inkscape

The circle you made will disappear and be replaced with some stripes and zig-zags. Ink/Stitch has hidden all of your layers and created a new one called `Stitch Plan`, in which it has placed a visual representation of the stitch plan it created. It has interpreted your shape as two instructions: Fill and Stroke. Fill is implemented using fill stitching, and Stroke is implemented by running satin stitching along the outline.

Select the horizontal lines using the `Edit Paths by Nodes` tool. Zoom in a bit and you'll see that the lines are actually made up of lots of points. Each point represents one stitch - one needle penetration and interlocking of the top thread with the bobbin thread. Notice how the points all line up nicely in diagonals. This will give the fill stitching a nice, orderly visual appearance.

Now look at the zig-zags. These are the satin stitches. Note that the corners look pretty ugly. This is because satin stitches generated from a shape's stroke are pretty rudimentary and aren't implemented intelligently. *You can exert much greater control over satin stitching using a [**Satin Column**](/docs/stitches/satin/)*.

![Stitch Plan](https://edutechwiki.unige.ch/mediawiki/images/thumb/6/6a/Inkstitch-stitch-plan.png/800px-Inkstitch-stitch-plan.png)

The stitching preview you're looking at just now isn't intended to be permanent. Immediately undo it with `Ctrl-Z` after you've looked at the stitches. The actual work that does, is to output a design file.

## Step 6 - Stitching Out the Design
Where'd the design file go? One of the parameters you were able to specify in the filter settings dialog was the output directory. By default, the directory used is the place where you installed the extension's Python files.

Ink/Stich will create a file named `something.___`, where `something` is the name of your svg file (e.g. `something.svg`) and `___` is the proper extension for the output format you select. If `something.___` already exists, it will be renamed to `something.___.1`, and `something.___.1` will be renamed to `something.___.2`, etc, up to 5 backup copies.

   <span style="color: #3f51b5;">↳ something.___</span><br />
   <span style="color: #ff9800;">↳ something.___</span>, <span style="color: #3f51b5;">something.___.1</span><br />
   <span style="color: #f44336;">↳ something.___</span>, <span style="color: #ff9800;">something.___.1</span>, <span style="color: #3f51b5;">something.___.2</span>
   
When you've got the design the way you like it, save off a copy of <span style="color: #f44336;">`something.___`</span> and feed your machine.

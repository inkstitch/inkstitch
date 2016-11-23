# inkscape-embroidery: An Inkscape plugin for designing machine embroidery patterns
## Introduction
**Want to design embroidery pattern files (PES, DST, etc) using free, open source software?  Hate all the other options?  Try this one.**

I received a really wonderful christmas gift for a geeky programmer hacker: an [embroidery machine](http://www.brother-usa.com/homesewing/ModelDetail.aspx?ProductID=SE400).  It's pretty much a CNC thread-bot... I just had to figure out how to design programs for it.  The problem is, **all free embroidery design software seems to be terrible**, especially when you add in the requirement of being able to run in Linux, my OS of choice.

So I wrote one.

Okay, not really.  I'm pretty terrible at GUIs, but I found this nifty inkscape extension that was created and hacked on by a couple of other folks.  It was pretty rudimentary, but it got the job done, and more importantly, it was super hackable.  I hacked the hell out of it, and at this point **inkscape-embroidery is a viable entry-level machine embroidery design tool**.


## Setup

To use this tool, you're going to need to set it up.  It's an inkscape extension written as a Python file.  Once you get it working, you'll need to learn how to design vectors in the way that inkscape-embroidery expects, and then you can generate your design files.

### Inkscape
First, install Inkscape if you don't have it.  I highly recommend the **development version**, which has a really key feature: the Objects panel.  This gives you a heirarchical list of objects in your SVG file, listed in their stacking order.  This is really important because the stacking order dictates the order that the shapes will be sewn in.

I've had success running version `0.91.0+devel+14591+61`.  Installation instructions are [here](https://inkscape.org/da/release/trunk/).

### Python Dependencies
Make sure you have the `shapely` python module installed.  The `appdirs` python module is also useful but is not required.  On Ubuntu:

```
apt-get install python-shapely python-appdirs
```

### Extension installation
1. Clone the extension source: `git clone https://github.com/lexelby/inkscape-embroidery`
2. Install it as directed [here](https://inkscape.org/da/gallery/%3Dextension/)

I prefer to symbolically link into my git clone, which allows me to hack on the code.  Changes to the Python code take effect the next time the extension is run.  Changes to the extension description files (`*.inx`) take effect the next time Inkscape is restarted

### Optional: conversion program
The extension can output machine embroidery design files directly in Melco format.  I don't even know what that is, so I don't use it.  I prefer to use the **CSV output format** which can be consumed by another awesome open source project: [Embroidermodder2](https://github.com/Embroidermodder/Embroidermodder).  In theory, this project was going to be exactly what I wanted.  In practice, it never got funded on Kickstarter and it's largely incomplete.

However, it contains a really awesome core library that knows pretty much every machine embroidery format and how to convert between them.  I use it to convert the CSV files that inkscape-embroidery outputs into the PES files that my SE400 uses.

Grab the source: `git clone https://github.com/Embroidermodder/Embroidermodder`.  Build just `libembroidery-convert` using the instructions in "3)" in the [Embroidermodder build docs](https://github.com/Embroidermodder/Embroidermodder/wiki/Compiling-parts-of-the-project). You can then use it like this: `./libembroidery-convert your-file.csv your-file.pes`.

Since the CSV + libembroidery-convert method is the only method I use, it's the one I'll assume from here on.  I'm not even sure if the other output formats from inkscape-embroidery still work (or ever worked).

## Usage
### Basic Usage
First things first: I'm going to assume you know a few embroidery terms like "fill stitch" and "satin".  Look those up if you're mentally 404ing, then come back here.  I'm *not* going to assume you know some of the more advanced terms, because I had to learn all that when I started this project, so I might as well teach you too.

1. Open up Inkscape and create a rectangle.
2. Make sure it has both a stroke and a fill.
3. Convert it to a path using **Path -> Object to Path** (because inkscape-embroidery doesn't understand rectangles, circles, and the like, and ignores them).
4. Run **Extensions -> Embroidery -> Embroider**.  Use the default settings.

The rectangle you made will disappear and be replaced with some stripes and zig-zags.  inkscape-embroidery has hidden all of your layers and created a new one called Embroidery, in which it has palced a visual representation of the stitch plan it created.  It has interpreted your shape as two instructions: Fill and Stroke.  Fill is implemented using fill stitching, and Stroke is implemented by running satin stitching along the outline.

Select the horizontal lines using the "Edit Paths by Nodes" tool.  Zoom in a bit and you'll see that the lines are actually made up of lots of points.  Each point represents one stitch -- one needle penetration and interlocking of the top thread with the bobbin thread.  Notice how the points all line up nicely in diagonals.  This will give the fill stitching a nice, orderly visual appearance.

Now look at the zig-zags.  These are the satin stitches.  Note that the corners look pretty ugly.  This is because satin stitches generated from a shape's stroke are pretty rudimentary and aren't implemented intelligently.  You can exert much greater control over satin stitching using a Satin Column, described later.

The stitching preview you're looking at just now isn't intended to be permanent.  I usually immediately undo it (ctrl-Z) after I've looked at the stitches.  The actual work that inkscape-embroidery does is to output a design file.

### Stitching Out the Design
Where'd the design file go?  One of the parameters you were able to specify in the filter settings dialog was the output directory.  By default, the directory used is the place where you installed the extension's Python files.  I output mine to `~/Documents/embroidery/output`.

inkscape-embroidery will create a file named `something.csv`, where `something` is the name of your svg file (e.g. `something.svg`).  If `something.csv` already existed, it will be renamed to `something.csv.1`, and `something.csv.1` will be renamed to `something.csv.2`, etc, up to 5 backup copies.  When you've got the design the way you like it, save off a copy of `something.csv`.

Next, convert it to your machine's format using `libembroidery-convert` (as described above).  Send it to your machine in whatever way one does that for your machine, and try stitching it out!

### Ordering

Copy your rectangle and paste it elsewhere on your canvas.  Deselect any shapes (**Edit -> Deselect**), re-run the extension, and look at the output.  You'll see that both regions have been stitched, and there will be a line connecting them.  That's a jump-stitch, where the machine will move a long distance between stitching the sections.

If you're like me, your machine can't automatically cut the thread between stitching sections, so you'll need to minimize jump stitches as much as possible through careful planning of your stitch path.  If your machine *can* do thread cuts, congratulations!  But you'll need to modify inkscape-embroidery to allow you to specify a thread cut, because there's no way to do that right now.

However, note that inkscape-embroidery pays attention to the colors you use for objects.  If you change colors from one object to the next, inkscape-embroidery will include a color-change instruction using the color you've set for the object.  My machine cuts the thread and waits for me to switch to the new thread color.

#### Reordering

Use the Objects panel to view the stacking order of the objects in your SVG file.  Inkscape-embroidery will stitch them in their stacking order, from lowest to highest.  You can reorder them in the normal way in inkscape to affect the stitching order.

You can also use the Reorder extension.  Hold shift and select the objects you'd like to reorder, one at a time, in the order you'd like them to end up in (lowest to highest).  Run **Embroidery -> Reorder**.  This extension will pull all of the selected objects out of wherever they were in the stacking order and insert them in order at the same place as the *first* object you selected.  This can save you a ton of time.

### Seeing the stitch plan for selected objects

If you have one or more objects selected when you run the **Embroider** extension, only those objects will be embroidered.  This can be useful to help you fine-tune just one small section of your design.

### Embroidery Parameters
When you run **Embroider**, you'll have the option to specify a few parameters like stitch length, fill stitch row spacing, etc.  These are used as defaults for all objects in your design.  You can override these parameters and set many more using the **Embroidery -> Params** extension.

This extension gives you an interface to control many aspects of the stitching of each object individually.  To use it, first select one or more objects.  Parameters will be applied to them all as a group.  If the selected objects already have parameters set, these settings will be pre-loaded into the interface.

Parameters are stored in your SVG file as additional attributes on the XML objects.  You can view these attributes using Inkscape's built-in XML editor panel, but you shouldn't actually need to do this during normal usage.  Inkscape ignores attributes that it doesn't know, so these attributes will be saved right along with your SVG file.  Note that other SVG programs may *not* retain these attributes, so be careful!

I recommend avoiding dependence on the default settings specified in the **Embroider** extension's settings window.  In fact, I bypass it entirely by binding a keystroke (ctrl+e) to "Embroider (no preferences)" in Inkscape's settings.  This way, I can quickly see the stitch plan just by pressing the keystroke.  I also bind a keystroke to **Params** so that I can quickly view and change settings for each object.

### Sidenote on extensions
**Params** is a bit weird, in that the dialog is produced by an entirely separate program (the extension) rather than Inkscape itself.  This is due to the way Inkscape structures extensions.  I wish inkscape-embroidery could have deeper integration into Inkscape's user interface, but it's currently not possible.  This is the price we pay for not having to write an entire vector graphics editor program :)

Another issue is that Inkscape has a memory leak related to extensions.  The more times you run an extension, the more memory Inkscape uses and the slower it gets.  I periodically save my SVG file, close Inkscape, and restart it to work around this issue.  See above re: putting up with this kind of hassle so as not to have a to implement an entire vector graphics editor.  Hopefully they'll fix this bug soon.

### AutoFill

AutoFill is the default method for generating fill stitching.  To use it, create a closed path in Inskcape and add a fill color.

inkscape-embroidery will break the shape up into sections that it can embroider at once using back-and-forth rows of stitches.  It then adds straight-stitching between sections until it's filled in the entire design.  The staggered pattern of stitches is continued seamlessly between sections, so the end result doesn't appear to have any breaks.  When moving from one section to the next, it generates running stitching along the outside edge of the shape.

This algorithm works great for simple shapes, convex or concave.  However, it doesn't work for shapes with holes, because the stitching could get "stuck" on the edge of a hole and be unable to reach any remaining section.  For this reason, AutoFill rejects regions with holes in them.

So what do you do if your shape does have holes?  You have two choices: use manually-routed fill (described below), or break the shape up into one or more shapes without holes.

Here's an example of converting a region with a hole into a region without:
![breaking auto-fill regions with holes](images/autofill_with_holes.png)

An SVG version is available in `images/autofill_hole_example.svg` for you to test out.

Note the thin line drawn from the hole to the edge.  In fact, this is a very thin strip missing from the shape -- thinner than the spacing between the rows of stitches.  This allows the autofill system to travel into and out of the center of the shape if necessary to get from section to section.

Note that I've drawn the gap at exactly the same angle as the fill.  When the autofill system sees that it is traveling in the same direction as the fill, **it places stitches correctly to match the fill pattern**.  This means that the gap will be virtually undetectable because the travel stitches will be hidden in the fill.  This may double- or triple-up one of the fill rows, but it's really hard to tell unless you look very closely.

#### AutoFill parameters

Using the **Params** extension, you can set these parameters:

* **angle**: The angle of the rows of stitches, in degrees.  0 is horizontal, and the angle increases in a counter-clockwise direction.  Negative angles are allowed.
* **row spacing**: distance between rows of stitches
* **maximum stitch length**: the length of each stitch in a row.  "Max" is because a shorter stitch may be used at the start or end of a row.
* **running stitch length**: length of stitches around the outline of the fill region used when moving from section to section
* **staggers**: stitches are staggered so that neighboring rows of stitches don't all fall in the same column (which would create a distracting valley effect).  Setting this dictates how many rows apart the stitches will be before they fall in the same column position.

#### AutoFill Underlay

By default, AutoFill will cover the shape with one layer of stitches.  In almost all cases, this won't look any good.  The individual stitches will sink into the fabric (even if it's thin) and the fill will appear sparse.  The fabric may even stick up between rows.

To solve this, you need underlay: an initial layer of stitches that hold up the final stitches.  Underlay for fill stitch it's usually comprised of fill stitching 90 degrees offset from the final fill (called "top stitching").  The row spacing should be much wider than in the top stitching.  The goal is to flatten out the fabric and give the top stitches "rails" to sit on.

In **Params**, you'll see an underlay tab next to the AutoFill tab.  Enable it by checking the box.  The default settings should be good enough for most cases: 90 degrees offset and row spacing 3x the spacing of the top stitching.

### Manual Fill

Manual Fill is the old mode from before I figured out how to implement automatic fill routing.  In some cases, AutoFill may not be an option, such as when the running stitches between sections are not acceptable for your design.  Usually, fill region edges are covered over by satin, but not always.

In manual fill, the extension will still break up the shape into sections, each of which can be embroidered in one go.  Then these sections will be fill-stitched one at a time, jumping directly between sections.  You'll almost certainly want to break your shape up into smaller shapes and connect then using running stitches (described below).  It's a painstaking process, made moreso because you'll need to do it twice: once for the underlay and again for the top stitching.

The **flip** option can help you with routing your stitch path.  When you enable **flip**, stitching goes from right-to-left instead of left-to-right.  Using **flip** and rotating 180 additional degrees (by adding or subtracting 180 from **angle**), you can cause fill stitching for a given shape to start from any of the four possible corners.


### Running Stitch

Running stitch can be created by setting a dashed stroke on a path.  Any kind of dashes will do the job, and the stroke width is irrelevant.   inkscape-embroidery will create stitches along the path using the stroke width you specify.

In order to avoid rounding corners, ash extra stitch will be added at the point of any sharp corners.

The **repeats** parameter says how many times time run down and back song the path.  An odd number of repeats means that the stitches will end at the end of the path, while an even number means that stitching will return to the start of the path.  The default is one repeat; that is, just traveling once from the start to the end of the path.

If an object consists of multiple paths, they will be stitched in order with a jump between each.

### Simple Satin

A line without dashes will result in satin stitching.  The width of the satin will be dictated by the stroke width.  (For historical reasons, a stroke width less than 0.5 pixels will result in running stitch instead).

This is "simple satin": **Embroider** will plot zig-zags to the left and right of the line from start to end, but it won't do anything special around curves and corners.  Sharper curves and corners will result in sparse stitching around the outside of the curve and dense stitching around the i.  T

This won't look good and may even poke holes in the insides of corners.  I avoid using plain satin entirely; it's just kept in for backward compatibility.  It'll probably work fine for straight lines.

### Satin Column

Satin Column mode gives you much greater control over how the satin is generated.  You define a satin column using a shape made of two mostly-parallel lines.  **Embroider** will draw zig-zags back and forth between the two lines.  You can vary the thickness of the column as you like.

The two paths must have the same number of points.  This means that each path will be made up of an equal number of Bezier curves.  Each pair of points acts as a "checkpoint": **Embroider** will ensure that a "zag" ends up going from one point to the other.

**Embroider** considers each pair of Bezier curves, one at a time.  It picks the longest if the two and determines how many zig-zags will be necessary to satisfy the **zig-zag spacing** setting.  This makes it so that the outside of a curve will never have sparse stitching like with simple satin.  

However, this does mean that the inside of a curve will have a higher stitch density than you specified.  Be careful how you design sharp curves, because **stitching at too high a density may poke a hole in the fabric**!

To avoid this issue, transition your stitching to go around the corner at an angle, like this:

Some embroidery design programs solve this problem differently.  They modify the satin such that some stitches on the inside corner don't go all the way to the edge, to avoid having the make penetrate the fabric too many times in the same spot.  I haven't gotten around to implementing that yet.  Pull requests welcome!

Satin Column supports these settings:

* **zig-zag spacing**: the peak-to-peak distance between zig-zags.
* **pull compensation**: Satin stitches pull the fabric together, resulting in a column narrower than you draw in Inkscape.  This setting expands each pair of needle penetrations outward from the center of the satin column.  You'll have to determine experimentally how much compensation you need for your combination of fabric, thread, and stabilizer.

Satin Column also supports three kinds of underlay, of which you can use any or all simultaneously.  I use the terms defined in [this excellent article](http://www.mrxstitch.com/underlay-what-lies-beneath-machine-embroidery/) on satin column design.

#### Center Walk Underlay

This is a row of running stitch down the center of the column and back.  This may be all you need for thin satin columns.  You can also use it as a base for more elaborate underlay.

#### Contour Underlay

This is a row of running stitch up one side of the column and back down the other.  The rows are set in from the edge of the column by an amount you specify.  For small or medium width satin, this may serve well enough by itself.

#### Zig-Zag Underlay

This is essentially a lower-density satin stitch sewn to the end of the column and back to the start.  Added with contour underlay, you get the "German Underlay" mentioned in the article linked above.  For wide columns or challenging fabrics, you can use all three underlay types together.


## Workflow

Here's how I use inkscape-embroidery to design embroidery patterns.

### Pixels Per Millimeter

My embroidery machine (a Brother SE400) can handle patterns up to 10cm x 10cm (about 4in x 4in).  Most machine embroidery design advice articles I've read talk in terms of millimeters, so that's what I work in.

My machine can (theoretically) position the needle with an accuracy of a tenth of a millimeter.  The Brother PES format cannot encode a position any mute precisely than this.  In practice, even if a machine had finer accuracy than this, the realities of sewing on real fabric, even with the best stabilizer, mean that you can't get any more accurate than this (and you shouldn't bother trying).

I set the Inkscape's default document size to 1000 x 1000 pixels and set the "Pixels Per Millimeter" setting in **Embroider** to ten.  This means that every "pixel" in Inkscape is worth a tenth of a millimeter.  Practically speaking, there's no reason I couldn't choose to have one "pixel" equal one millimeter, because pixels don't really have much meaning in vector graphics.

### Step 1: Sketch design or use an image

First, I get an idea for what I want my finished product to look like.  If I'm basing my design off an existing picture or graphic, I load it into Inkscape in its own layer.  Some graphics are amenable to Inkscape's auto-tracing feature, especially if I simplify the image in GIMP first.

After auto-tracing, I clean up the vector shapes, using "Simplify" and deleting nodes by hand when possible.  My goal is to use as few Bezier curves as reasonably possible to represent the image.

If I need to trace an image by hand, I usually use the freehand drawing tool.  This tool creates paths with a lot of Bezier nodes, so again, I'll simplify the curves as much as possible.

Working with an existing SVG image can save a ton of time, so consider using Google image search with the filter set to SVG.

For text, choose a font carefully.  It's quite hard to make satin look good when it's 1mm wide our narrower.  Sans-serif fonts tend to be the easiest.  For text smaller than 4mm tall, you'll have a very difficult time making lowercase letters look good, so consider block-caps.  Cursive/script fonts can work well, but it's not going to be as easy as you think.  I find that I spend the most time on text by far.


### Step 2: Plan stitch path and color changes

At this point, you'll have a vector graphic representation of your image.  The next thing to do is to convert your vectors into the kind that **Embroider** understands and our then in the right order.

When you're designing for embroidery machines that can't cut the thread mid-sew or switch colors automatically, you're going to want to optimize your stitch path to reduce or hide jump stitches and make minimal color changes.  I also try to avoid stitching over jump stitches when possible, because it's a total pain to trim them by hand when you do.

The order of stitching also affects how the fabric pulls and pushes.  Each stitch will distort the fabric, and you'll need to take this into account and compensate accordingly.  Look for articles on machine embroidery distortion for more info on this.

### Step 3: create the embroidery vectors

I make heavy use of layers and groups at this point.  If I've traced an image, I'll leave it as the lowest layer and set it invisible in the Layers or Objects palette.  Any layer, group, or vector shape that is set invisible will be ignored by **Embroider**.

I keep my initial traced vectors in their own layer and use them as a reference when designing embroidery vectors.  I copy and paste then as necessary into a higher layer and work with the copies.

I use only AutoFill and Satin Columns in my designs.  I begin converting filled areas to AutoFill regions.  Each time I create an AutoFill shape, I set its parameters using **Params**.  Then I select it and run **Embroider**, which will cause it to show a stitch plan for just the selected object(s).

I examine the resulting stitch plan using the node editor tool.  Each node is a single stitch; the needle will penetrate the fabric and interlock with the bobbin thread at this point.  Once I'm done examining the stitch plan, I Undo the **Embroider** operation to remove the stitch plan and make my vectors visible again.  Then I make any changes necessary, re-run **Embroider**, and repeat until it looks right.

At this point, I save my SVG file.  If Inkscape is starting to become sluggish (due to the memory leak described above), I'll restart it before continuing.

Next, I work on Satins.  Remember that a Satin Column is defined by two lines that run along the edges of the column.  It's usually a good idea to run satin along the outside border of a fill region.   Inkscape makes this easy.  I copy and paste the shape from the traced vectors, then disable Fill and enable Stroke.  I set the stroke width to my desired satin width.  Finally, I use the "Stroke to Path" option to convert just the stroke into its own path.

At this point, it's necessary to cut the paths so that they aren't a continuous loop.  The cut will also tell **Embroider** where to start stitching from.  Add a point at the desired cut location by double-clicking on the path with the Node Editor tool active.  Cut at this point by selecting at and pressing shift+j.  Repeat for the second path.

Now you've got an object made of two paths.  They need to be going on the same direction for Satin Column to work.  You can tell what direction the path goes in by enabling direction indicators in Inkscape's preferences.  To reverse one of the paths, select one of its points and choose "Reverse Path".  I bind this to ctrl+r in Inkscape's preferences.


---
title: Transcript - 04 Stitch Types - Beginner Tutorial Series
permalink: /fr/tutorials/resources/beginner-video-tutorials/04-stitch-types-transcript
last_modified_at: 2019-03-11
language: fr
image: "/assets/images/tutorials/video-preview-images/beginner-tutorial-series.png"

toc: true

exclude-from-tutorial-list: true
---
[← Back](/tutorials/resources/beginner-video-tutorials/)

## Welcome to the Ink/Stitch beginner tutorial series.

**In this part we are going to have a closer look which stitch types Ink/Stitch is able to perform.**

We will not explain the stitch types in general, but only how to create them in Ink/Stitch.

Ink/Stitch stitch types can be roughly divided into three sections: stroke, satin and fill.

Here is a complete list, so you can quickly navigate to the stitch type you are interested in.

**Stroke:** This is the tutorial about stroke type stitches.

**Satin:** This is the tutorial about satin columns.

**Fill:**  This is the tutorial about fill stitches.

## Stroke type stitches

Stroke stitches can be used for: outlines, line art embroidery or to add details into your design.

### Zig-zag

Zig-zag stitches are are easy to create. 
We recommend to use them only for straight lines, because they will not stitch nicely around edges.
In most cases, you would prefer a satin column instead.

That said, let's see how they are done.

Hit `B` to enable the bezier curve tool and draw a simple path.
Open the `Fill and Stroke` settings and set the path width in the stroke style tab.
This will define the height of your zig-zag-line.
It should be at least 0.6 mm.

Go to `Extensions > Ink/Stitch  > Params` to open the parameter dialogue.

`Satin stitch along path` has to be enabled in the Stroke tab.
Set zig-zag-spacing to whatever you like it to be.
You can also define the number of repeats.
All other settings will not have any effect on zig-zag stitching.

### Running Stitch

Running stitches are created in a similiar way.
But this time you have to set the stroke style to a dashed line.
Any type of dashes will do the job and stroke width is irrelevant.

Create a path and open the params dialogue.

`Satin stitch along path` has to be enabled in the Stroke tab.
Setting can be applied for `running stitch length` and `repeats`.

### Bean Stitch

Bean stitch creates thicker threading through back and forth repetition of running stitches. 

It works almost the same as running stitches, but you have to set additionally the `bean stitch number of repeats`.

A value of 1 would triple each stitch, because it goes forward, back and forward again.
A value of 2 would results in a quintupled stitch.

### Manual Stitch

In manual stitch mode Ink/Stitch will use each node of a path as a needle penetration point, exactly as you placed them.

Create a path. Line style and width are irrelevant.
We recommend to display all nodes of the corresponding path as corners, since manual stitch will not respect bezier curves.

Run `Params` and enable `Manual stitch placement`.
All other settings will have no effect in manual stitch mode.

Remember to also add tie-in or tie-off stitches, since they are not created automatically in manual stitch mode.

---

We hope you enjoyed this tutorial and got a small overview about all stroke stitch types Ink/Stitch is capable to perform.
You might also want to watch our videos about satin columns and fill stitches.


## Satin Columns

Satin stitch is mostly used for borders, letters or small fill areas.

Ink/Stitch will draw zig-zags back and forth between two lines, while you can vary the thickness of the column as you like.

There are various methods to create satin columns.

We will first show you the very basic and manual way, before we simplify the process with the help from satin tools.

### Satin Path Object

#### Node Method

So let's create two paths and combine them with `Path > Combine` or `Ctrl + K`.

Next we open the params dialogue and switch to the `satin column` tab, where we enable `Custom satin column`.

In our example the simulator shows not what we expected. This is what you get, when path directions aren't the same on both sides of the rails.

Activate the node tool by pressing `N` and select your satin column. If you followed our customize tutorial you will see red sparks indicating the path direction.
Select one node of one path and run `Path > Reverse` or use your custom shortcut key to reverse the path.

If you run params again you will now see the correct satin column being animated.

You can influence the angle with help of the nodes.

But always keep in mind, that on both rails we need the same amount of nodes. TODO
Otherwise you will receive an error message like this.

#### Rung method

This is easy to achieve in a simple path like this. But what if you have a more complex shape and you really don't feel like counting nodes all day.

Well, Ink/Stitch has a solution for this. The "rung"-method.

With the  satin column selected activate the pencil tool by pressing `P`. Hold shift while you draw the rung. Rungs have to cross both rails once.

These rungs will give Ink/Stitch all the information about the stitch angle and no counting of nodes is needed.

### Satin Tools

#### Convert Line to Satin Column

If you want the satin column to be a line of equal width, there is a very fast method to create a satin column.

Create a path.

Make sure it is not a closed path, but has a start and an end.

Set the stroke width to whatever you like your satin column to be. Then run `Extensions > Ink/Stitch  > Satin Tools > Convert Line to Satin Column`.

And that's it.

#### Cut Satin Column

Sometimes you will need to break up your path into pieces.

This can be done manually, but if you want to keep your settings you can use a specific satin tool: `Cut Satin Column`.

To break up your column manually, select two nodes, one on each rail and click on `Break path at selected nodes`. Now you have to seperate the paths by hitting `Ctrl + Shift + K` and recombine your sub-paths with `Ctrl + K`.

Using the satin tools will require two steps. First select your satin column and run `Extensions > Ink/Stitch  > Commands > Attach commands to selected objects...` and enable `Satin cut point` before you click on `Apply`. Move the symbol to the exact point where you want the satin column to split up. It will split where the connector touches the rail. Then run `Extensions > Ink/Stitch  > Satin Tools > Cut Satin Column`. Please note, that in params you already need the satin column to be enabled for this to work.

#### Flip Satin Column Rails

`Flip Satin Column Rails` is a tool to help you plan your stitch path precisely.
A satin column which originally starts on the left rail and ends on the right, will start on the right rail and end on the left.
This might shorten connections between the previous and next stitch object.

Select the satin column and run `Extensions > Ink/Stitch  > Satin Tools > Flip Satin Columns`

#### Auto-Route Satin Columns

Planing the order and connections of stitch objects can be very time consuming.
Therefore Ink/Stitch comes with a tool that will take away a lot of this work.

`Auto-Route Satin Columns` will order your satin columns in logical stitching order.
It will create under-pathing and jump-stitches as necessary.
Single satin columns might also be split up to avoid jump stitches.
Resulting satins will retain all of the parameters you had set on the original satins.

Select satin columns with all parameters set (underlay, etc.).

Run `Extensions > Ink/Stitch  > Satin Tools > Auto-Route Satin Columns...`

Enable desired options and click apply.

You can even define a start and an end point for your ordered satin columns by attaching `Auto-route satin stitch starting` and `ending position` commands.

If this went too fast for you, you might be interested into the visual commands tutorial.

### Params & Underlay

#### Params

Let's have a closer look into the params dialogue and what it offers for satin columns.

`Custom satin column` has to be enabled.

Satin stitches pull the fabric together, resulting in a column narrower than you draw in Inkscape.
With the `Pull compensation` setting you can expand the satin column.
You’ll have to experiment how much compensation you need for your combination of fabric, thread, and stabilizer.

Zig-zag spacing will define the density of your satin column.

Well, now we talked much about the satin column itself. But a very important part is still missing, which is the underlay.
Ink/Stitch supports three kinds of underlay.
For wide columns or challenging fabrics, you can even use all three underlay types together.

#### Center-Walk Underlay

This is a row of running stitch down the center of the column and back.
This may be all you need for thin satin columns.
You can also use it as a base for more elaborate underlay.

#### Contour Underlay

This is a row of running stitch up one side of the column and back down the other.
The rows are set in from the edge of the column by the amount you specify.
For small or medium width satin, this may serve well enough by itself.

#### Zig-Zag Underlay

This is essentially a lower-density satin stitch sewn to the end of the column and back to the start.


### E-Stitch

The biggest purpose for E-stitch is a simple but strong cover stitch for applique items. Mainly for baby cloths as their skin tends to be more sensitive.

E-stitch is created just as a satin column. But in the params dialogue enable the E-stitch option and increase the zig-zag spacing.

Underlay is not needed for this stitch type.

If the points are facing the wrong way, just use the “flip satin column rails” tool as described before.

----   ----

We hope you enjoyed this tutorial and got an overview about satin stitch types.
You might also want to watch our videos about stroke type stitches and fill stitches.


## Fill Stitches

Fill stitch is used to fill big areas with a color.

Ink/Stitch comes with two fill stitch types: manual and auto-fill.

We will not show manual fill in this tutorial.
If you are interested in it, you can read more on our website.

### Auto-Fill Path

Auto-fill is the default method for generating fill stitches.

Create a path with a fill color.
Shapes can also have holes, but should not consist of more than one section.

If you need to fill a shape like the one on the right side, hit `Ctrl + Shift + K` to treat it as two seperate shapes.

### Params

Open the params dialogue and enable `Automatically routed fill stitching`.

Set the stitch angle, while 0 is horizontal. You can also use negative values.

Expand the shape before stitching. This compensates the pull effect and helps to avoid gaps between sections.

Define the maximum fill stitch length. Stitches may be shorter at the end or start of a row.

Set spacing between rows - and running stitch length.

With `Skip last stitch in each row` you will save a hugh amount of stitches.
The last stitch in each row is quite close to the first stitch in the next row.
Skipping it decreases stitch count and density.

Influence the output with the last setting; where you define, how many rows apart stitches will fall into the same column position.

### Underlay

Fill stitch areas also need an underlay.

Switch to the `AutoFill Underlay` tab and enable `Underlay`.

Here you will find  the `Fill angle` setting again.

By default it will be shifted for + 90 deg to the fill stitch.

Prevent underlay from showing around the outside of the fill with `inset`.

Define `max. stitch length` and `row spacing`, wich defaults to 3x the spacing of the top layer.

### Define start and stop position

In embroidery files you want to plan where stitching starts and ends. You can control the start and end position of a fill with visual commands.

If you cannot follow the steps shown here, follow our visual commands tutorial.

----

We hope you enjoyed this tutorial.
You might also want to watch our videos about stroke type stitches and satin columns.

[← Back](/tutorials/resources/beginner-video-tutorials/)

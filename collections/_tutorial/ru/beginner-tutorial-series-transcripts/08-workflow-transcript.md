---
title: Transcript - 08 Workflow - Beginner Tutorial Series
permalink: /ru/tutorials/resources/beginner-video-tutorials/08-workflow-transcript
last_modified_at: 2019-03-12
language: ru
image: "/assets/images/tutorials/video-preview-images/beginner-tutorial-series.png"

toc: true

exclude-from-tutorial-list: true
---
[← Back](/tutorials/resources/beginner-video-tutorials/)

## Welcome to the Ink/Stitch beginner tutorial series.

**In this part we are going to have a look at the Ink/Stitch workflow.**

It includes the following steps, without being too strongly attached to this exact order.

Quiet a few of the shortcut keys used in this tutorial are customly set. Watch the customize video to learn how to establish them.

## Create a Vector Image

The first thing to do is to create a vector image.
You could also use existing images. If you have an PNG-image you could even trace it through 'Path > Trace Bitmap'.

For a brief demonstration we will create the image by ourselves.

To create lines you can either use the pencil tool, which can be activated with 'P' - or the beziér tool enabled with 'B'.
You can also use shapes such as the square or the circle. Convert them to a path with 'Shift + Control + C' or the corresponding symbol in node editor mode.

Fill bounded areas with help of the fill tool. The shortcut key for this is 'U'.

If you installed the Addons you will have color palettes available. Set the fill color by clicking on them. The stroke color can be change with 'Shift + Click'.

## Convert to Embroidery Vectors

Now that the image is done, you should save a copy into an other layer and hide the first one (we skipped this step here).

The next step will be to convert the lines in such way, that Ink/Stitch will understand how it should be sewn out.

At this point we assume that you know how to create satin columns, fills and running stitches. If not, have a look at the corresponding videos.

Set the params as you like and don't forget to use underlay.

## Plan stitch order

Plan your stitch order carefully. It will have a lot of impact on the quality of your design.

While planning the stitch order you try to avoid jump stitches and also color changes.

You don't want to change colors all the time while stitching out the design.

Run the simulator to see if you might need to adjust the direction of some objects.

You can also see the direction through the red sparks when in node editor mode. We have explained them in the customize video.

Change the direction through `Path > Reverse` or use a custom shortcut key.

Ink/Stitch will stitch objects in exactly the order they appear in your SVG document, from lowest to highest in stacking order.
If the distance between two objects is long, Ink/Stitch will add a jump-stitch between them automatically.
It uses the color of the object to determine thread color, so changes in color from one object to the next will result in a thread-change instruction being added to the embroidery output file.

We need to use the objects panel.

We recommend to make heavy use of layers and groups at this point. This will help a lot while reordering objects.

Create a group of objects with 'Ctrl + G' and move through the objects in the desired order, while pushing the next object in line to the bottom of the group.

## Attach commands

Attach commands to give Ink/Stitch additional information.

Trims, Stops, Fill start- and ending points are just some of the options. Watch our visual commands video to get more information.

## Visualize

During the whole process you were already running visualizations through the params dialogue.

Use the simulator as standalone or even the print preview to get an impression on how the design will look in the end.

Most of the time the simulator will do the job just fine. But for fill stitches the print preview is very helpful, f.e. in matter of stitch length and angle.

## Save Embroidery File

Once you are satisfied with the outcome, save the file to your disk.

Choose the file format that your machine can read.

Don't forget to also save the file in the svg file format, just in case you want to improve your design at a later time.

## Test Sew

Transfer the file to your machine.

Perform a test sew with preferably the same fabric that you are planing to use.

The fabric will have influence on the outcome of the design in this way that you most likely will have to adjust your design here and there.

Follow this routine until you are happy and ready to embroider on your best piece of fabric in your house ;)

[← Back](/tutorials/resources/beginner-video-tutorials/)

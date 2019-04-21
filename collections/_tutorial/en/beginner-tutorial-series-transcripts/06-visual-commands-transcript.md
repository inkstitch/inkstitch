---
title: Transcript - 06 Visual Commands - Beginner Tutorial Series
permalink: /tutorials/resources/beginner-video-tutorials/06-visual-commands-transcript
last_modified_at: 2019-03-12
language: en
image: "/assets/images/tutorials/video-preview-images/beginner-tutorial-series.png"

toc: true

exclude-from-tutorial-list: true
---
[← Back](/tutorials/resources/beginner-video-tutorials/)

## Welcome to the Ink/Stitch beginner tutorial series.

**In this tutorial are we going to talk about visual commands.**

Visual commands are used to give Ink/Stitch additional information about the way how your design should be stitched out.

## Installation

Before you can use visual commands you need to run `Install add-ons for Inkscape` in order to make the symbols accessible.


## Command types

There are three types of commands:

1. Commands which effect the entire design
2. Commands which effect the selected layer
3. Commands which influence selected objects

### Design commands

In `Extensions > Ink/Stitch  > Commands > Add commands ...` you will find two options.

#### Stop position

"Stop position" will define a point where your machine will jump to, before every stop command.
This allows for pushing the embroidery frame out towards the user, to make applique steps easier.

#### Origin

The Origin specifies the zero point for embroidery files.
Setting up origins is especially useful for people that have full access to the entire sewing field that their machine is capable of, regardless of what hoop they use.

### Layer commands

`Add Layer commands...` has only one option:

#### Ignore Layer

`Ignore Layer` can be used to ignore an entire layer when converting to an embroidery file.
This can be useful if you want to add extra information into the file, f.e. tutorial instructions - or if you temporarily want to exclude a part of your design.

### Object commands

`Attach commands to selected objects...` will add information to selected objects.

#### Fill: Starting- and Ending Position

For fill stitching we can define starting and ending positions. Select a fill object and enable `starting position for fill` and `ending position for fill`.
Click apply and move the symbols to the desired position.
The connectors endpoint is always in the middle of the object. The effect will be performed where the connector crosses the outline of the shape.

#### Auto-Route Satin: Starting- and Ending Position

As for fills you can also define start and end positions for auto-route satin.
* Select the first satin column and add the `auto-route starting position`-command.
* Select the last satin column and add the `auto-route ending position`-command.
* Move the symbol to the right place and run `Extensions > Ink/Stitch  > Satin Tools > Auto-route satin`

#### Split Satin Column

For satin columns there is also a split functionality.
This is useful if you want to split a satin column while keeping all settings that you have previously made while modifying the path.
* With the satin column selected add a `Split satin column`-command.
* Move the symbol and run `Extensions > Ink/Stitch  > Satin Tools > Cut Satin Column`
This will split your satin column at the predefined position.

#### Trim

The `Trim`-command can be applied to any embroidery shape.
It will tell the machine to trim the thread after sewing this object.

#### Stop

The `Stop` or "Pause" command will cause the machine to move into the position which you have previously defined through the `stop position`-command.
And is therefor useful especially for applique designs.
It can be applied to any object as well.

#### Ignore

Objects with an `ignore`-command will be ignored in the embroidery output.

---

It might happen though, that some machines will ignore certain commands like e.g. the trim command.
Not every machine is capable to follow these instructions.

We hope this tutorial was useful for you and helps you to gain more control over the embroidery output.

[← Back](/tutorials/resources/beginner-video-tutorials/)

---
title: Transcript - 03 Customize - Beginner Tutorial Series
permalink: /tutorials/resources/beginner-video-tutorials/03-customize-transcript
last_modified_at: 2019-03-12
language: en
image: '/assets/images/tutorials/video-preview-images/beginner-tutorial-series.png'

toc: true

exclude-from-tutorial-list: true
---
[← Back](/tutorials/resources/beginner-video-tutorials/)

## Welcome to the Ink/Stitch beginner tutorial series.

**In this part we are going to customize Inkscape.**

The customizations are not mandatory, but they will make it more comfortable working with Ink/Stitch.

This tutorial will teach how to:

*   Install Ink/Stitch Addons for Inkscape
    The Ink/Stitch Add-ons installer will add manufacturer color palettes and Ink/Stitch specific symbols to your Inkscape installation

*   Define shortcut keys for fast and easy access to often used functions

*   Display path outlines to make the stitch direction visible

*   Use grids to align your pattern

*   Create and load templates as a basic page setup

## Add-Ons

Let's start with the Ink/Stitch Add-ons

In fact these Add-ons are two files which need to be placed in specific folders of your Inkscape installation.

Run `Extensions > Ink/Stitch > English > Install add-ons for Inkscape` and click install.

You will have to restart Inkscape for this to have any effect.

### Color Palettes

Open the color palettes panel and you will find a lot of new palettes. They all start with Ink/Stitch, so you can easily recognize them.

Now you can plan your design directly with your thread manufacturers color palettes. Thread names will also be displayed in the browser output so you can share it directly with your customer.

### Visual Commands

The second feature we will get to know better in the visual commands tutorial. It made symbols available, which will be used to give Ink/Stitch more information about the way your design should be stitched out.

Let's add e.g. an ignore symbol to one object. It indicates, that this particular object should not be stitched at all.

Create two objects and run the simulator. Both objects are displayed.

With one object selected go to `Extensions > Ink/Stitch > English > Commands > Attach command to selected Objects`.

Enable the ignore checkbox and click on Apply.

Now run the simulator again. Only one of the two objects is being shown.

There are many more options in the visual commands section, but for now we have more customizations to do.

## Shortcut Keys

In Ink/Stitch there are many functions which you will be frequently using. You do not really want to click through the menu all the time. This means you will be wanting to use keyboard shortcuts.

We will not go through all possibilities here, but only show you how to setup shortcut keys, so you can add more later
There is a list on <https://inkstitch.org> to give you further advice which key combinations you could use.

Open the Preferences through Edit > Preferences. Navigate to `Interface` and choose `Keyboard Shortcuts`.

*   Search for "params". You will find it under `Extensions`. Click into the field below `Shortcut` and enter `Control + Shift + C`.
*   Next search for "simulate" and enter `Control + Shift + L`
*   Then add `Control + R` to "reverse the path direction"
*   and finally `Page down` for "stack down" and `Page up` for "stack up"

Let's have a closer look to the stack up and down functions.

Open the object panel. It displays a full list of all layers, groups and objects in the document in it's `stacking order`.

Remove the ignore symbol that we previously added and move the objects so that they are overlapping each other.

If you use the raise and lower buttons on the first object, you will see, how their stacking order is changing positions.

This doesn't work work if the objects are not overlapping each other.

Now use your newly created shortcut keys and see, that the stacking order is changing again. The up and down buttons in the objects panel will do the same as your keyboard shortcuts.

The objects position will define the order from bottom to top how your pattern is being stitched out and this makes it to be a main feature while carefully planing your design.

## Path Outlines

Path outlines will show you the direction of the path.

The path direction is important for all stitch types except for fill stitches. It defines at which end of the stroke the stitching will begin.

In `Preferences > Tools > Node` enable the following checkboxes `show patch directions on outlines` and `show temporary outline for selected paths`.

With objects selected press `N` to activate the node tool and enable `Show path outline`.

You will see a red path surrounding the objects. The spikes indicate the path direction.

## Grids

You can use grids to align patterns properly.
To activate them open File > Document Properties and switch to the `Grids` tab.
Click on New and change units to mm (this is the common unit used for stitch length etc.) and set the x- and y-spacing to 1.
If you zoom out the major grid line will be displayed. It defaults to 5, change it to 10, then you have 1 cm to be displayed.

Your objects will will snap to the grid edges by default. You can change this by disabling snapping or disable `Snap to grids only`.
If you want to temporarily hide the grid, hit # or change it through the menu: `View > Page Grid`.

Also have a look at the panel `align and distribute` which you can find under Objects in the menu. Here you can find a lot of useful aligning methods.

## Templates

It seems to be no fun to set up the same document properties over and over again.
You would rather like to open a new document and it has the size of your embroidery frame.
Well, that is possible.

Once you organized everything as desired, simply save your file in your templates folder.
Select the template folder path for your operating system from the description below.

You can now access your template through `File > New from template`.

On <https://inkstitch.org> you can even download a predefined template with various hoop sizes.

---

We hope you enjoyed the tutorial. Now you are all set to start your creative work.

If you have any questions about Ink/Stitch, please contact us on GitHub.

[← Back](/tutorials/resources/beginner-video-tutorials/)


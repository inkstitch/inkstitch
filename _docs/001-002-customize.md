---
title: "Customize Ink/Stitch"
permalink: /docs/customize/
excerpt: ""
last_modified_at: 2018-04-14
toc: true
---

## Shortcut keys

Ink/Stitch is even more fun, if you assign shortcut keys. Go to: `Edit > Preferences > Interface > Keyboard Shortcuts` and enter your desired shortcut keys. [More information](http://wiki.inkscape.org/wiki/index.php/Customizing_Inkscape)

The following list was provided by lexelby:

Shortcut&nbsp;Keys | Effect
-------- | --------
**ctrl-shift-O** | Objects panel (Object menu -> Objects)
**ctrl-shift-P** | Params extension, without inkscape's extension preferences dialog
**ctrl-shift-L** | Simulate (mnemonic: Live simulation)
**ctrl-shift-E** | Embroider extension, without inkscape's extension preferences dialog
**PageUp** and **PageDown** | "Stack Up" and "Stack Down", a new feature in inkscape 0.92.2 that allows you to move an object up or down in the stacking order. You get more control than the old "Raise" and "Lower" commands that can only reorder objects if they overlap. Stack Up and Stack Down give me precise control over the order that objects stitch in. Very useful in combination with the Objects panel.
**Ctrl-R** | Reverse the direction of a path. For satins and running stitch, this lets me change which direction the stitches go in. I use this with the Inkscape preference in the Node tool settings, "Show path direction on outlines". If you select just one vertex using the node editor and press Ctrl+R, inkscape will reverse just one path in an object. This lets me make sure that both rails in a satin point the same direction.



### Simulation
Ink/Stitch simulation already comes with shortcut keys included:

Shortcut Keys | Effect
-------- | --------
**↑** | speed up
**↓** | slow down
**r** | restart animation
**q** | close

## Default page size

## Setting up origin with guides

Setting up origins (0, 0) is especially useful for people that have full access to the entire sewing field that their machine is capable of regardless of what hoop they use.

To setup origins Ink/Stitch uses guidelines:
  * Create two guidelines by draging them from the rulers onto the canvas (one horizontal, one vertical).
  * Dobble click on the guides and label them: `embroidery origin`. You can add more text if you like, but the label needs to start with this text.
  * The location of the little circle on the guide is unimportant. The angles of the guides don't matter, either. All that matters is where they intersect. That intersection point is the embroidery origin.

If no guides are found, the origin is at the center in the SVG.
  
You can also create a template containing guides and a canvas the right size for your machine, and put it in your `~/.config/inkscape/templates`.

[Video tutorial]({{ '/tutorials/custom-origins/' | relative_url }})

## Enabling path outlines & direction

Knowing path directions is important working with Ink/Stitch. For this reason we recommend to enable the checkboxes **Always show outline** and **Show path direction on outlines** in `Edit > Preferences > Tools > Node`.

## Working with templates

If you decided to use Ink/Stitch more frequently for your embroidery work, you might get tired of setting up the whole scene over and over again. In this case you are ready to create a template for your basic embroidery setup. Once you organised everything as desired, simply save your file in your `~/.config/inkscape/templates` folder. You can now access it by `File > New from template`.


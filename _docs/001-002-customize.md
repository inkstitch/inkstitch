---
title: "Customize Ink/Stitch"
permalink: /docs/customize/
excerpt: ""
last_modified_at: 2018-04-23
toc: true
---

## Shortcut Keys

You can speed up your work with Ink/Stitch, if you assign shortcut keys. Go to: `Edit > Preferences > Interface > Keyboard Shortcuts` and enter your desired key combinations. [More information](http://wiki.inkscape.org/wiki/index.php/Customizing_Inkscape)

The following list was suggested by lexelby:

Shortcut&nbsp;Keys | Effect
-------- | --------
**ctrl-shift-O** | Objects panel (Object menu -> Objects)
**ctrl-shift-P** | Params extension, without inkscape's extension preferences dialog
**ctrl-shift-L** | Simulate (mnemonic: Live simulation)
**ctrl-shift-E** | Embroider extension, without inkscape's extension preferences dialog
**PageUp** and **PageDown** | "Stack Up" and "Stack Down", a new feature in inkscape 0.92.2 that allows you to move an object up or down in the stacking order. You get more control than the old "Raise" and "Lower" commands that can only reorder objects if they overlap. Stack Up and Stack Down give me precise control over the order that objects stitch in. Very useful in combination with the Objects panel.
**Ctrl-R** | Reverse the direction of a path. For satins and running stitch, this lets me change which direction the stitches go in. I use this with the Inkscape preference in the Node tool settings, "Show path direction on outlines". If you select just one vertex using the node editor and press Ctrl+R, inkscape will reverse just one path in an object. This lets me make sure that both rails in a satin point the same direction.



### Simulation Shortcut Keys
Ink/Stitch simulation already comes with shortcut keys included:

Shortcut Keys | Effect
-------- | --------
**↑** | speed up
**↓** | slow down
**r** | restart animation
**q** | close

## Grids

To align your vector-shapes properly, you might want to make use of the grid functionality of Inkscape. Go to `View` and enable `Page Grid`. In `Snap Controls Bar` make sure `Snap to grids` is enabled. It is also possible to adjust spacing and origin of your grids in `File >  Document Properties > Grids`.

![Grids](https://user-images.githubusercontent.com/11083514/40359052-414d3554-5db9-11e8-8b49-3be75c5e9732.png)

## Setting up Origin with Guides

Setting up origins (0, 0) is especially useful for people that have full access to the entire sewing field that their machine is capable of regardless of what hoop they use.

To setup origins Ink/Stitch uses guidelines:
  * Create two guidelines by draging them from the rulers onto the canvas (one horizontal, one vertical).
  * Dobble click on the guides and label them: `embroidery origin`. You can add more text if you like, but the label needs to start with this text.
  * The location of the little circle on the guide is unimportant. The angles of the guides don't matter, either. All that matters is where they intersect. That intersection point is the embroidery origin.

If no guides are found, the origin is at the center in the SVG.
  
**Info:** You can also create a [template]((/docs/customize/#working-with-templates)) containing guides and a canvas the right size for your machine.
{: .notice--info }

[Video tutorial]({{ '/tutorials/custom-origins/' | relative_url }})

## Enabling Path Outlines & Direction

Knowing path directions is important working with Ink/Stitch. Therefore we recommend to enable the checkboxes **Show path direction on outlines** and **Show temporary outline for selected paths** in `Edit > Preferences > Tools > Node`.

Make sure that also **Show path outline** is enabled in `Tool Controls Bar` as you can see in the image below.

[![Path outlines & directions](https://user-images.githubusercontent.com/11083514/40360721-f294ef0a-5dbe-11e8-9d4d-98f469ff1fba.png)](https://user-images.githubusercontent.com/11083514/40360721-f294ef0a-5dbe-11e8-9d4d-98f469ff1fba.png)

## Working with Templates

If you decided to use Ink/Stitch more frequently for your embroidery work, you might get tired of setting up the whole scene over and over again. In this case you are ready to create a template for your basic embroidery setup. Once you organised everything as desired, simply save your file in your templates folder. You can now access it by `File > New from template`.

Operating system|Template Folder
---|---
Linux|`~/.config/inkscape/templates`
Windows|`C:\Users%USERNAME%\AppData\Roaming\inkscape\templates`

You should confirm the user folder in your inkscape preferences see the [FAQ](/docs/faq/#i-have-downloaded-and-unzipped-the-latest-release-where-do-i-put-it).

**Info:** Get [predefined templates](/tutorials/ressources/templates/) from our tutorial section.
{: .notice--info }


---
title: "Customize Ink/Stitch"
permalink: /da/docs/customize/
last_modified_at: 2021-10-14
toc: true
---

## Shortcut Keys

You can speed up your work with Ink/Stitch, if you assign shortcut keys.

The following list shows shortcut keys provided in the downloadable file below.

Some of the defined shortcut keys will replace others which are native to Inkscape. In the table you will see which they are and how you can still access these functions.
{: .notice--warning }

Shortcut&nbsp;Keys | Effect | Replaces
-------- | --------
<key>PageUp</key>                             | Stack Up* | Object > Raise (see also toolbar buttons)
<key>PageDown</key>                           | Stack Down* | Object > Lower (see also toolbar buttons)
<key>ctrl</key>+<key>R</key>                  | Reverse the direction of a path.**
<key>ctrl</key>+<key>shift</key>+<key>'</key> | Re-stack objects in order of selection 
<key>ctrl</key>+<key>shift</key>+<key>P</key> | Params | Edit > Preferences
<key>ctrl</key>+<key>shift</key>+<key>L</key> | Simulator (Live simulation)
<key>ctrl</key>+<key>shift</key>+<key>></key> | Stitch plan preview (beside of the canvas) | Path > Division (use Strg+/ instead)
<key>ctrl</key>+<key>shift</key>+<key>O</key> | Break apart fill objects... (O for Object) | Object > Object properties
<key>ctrl</key>+<key>shift</key>+<key>I</key> | PDF Export
<key>ctrl</key>+<key>shift</key>+<key>Q</key> | Lettering (Q for QWERTY) | Object > Selectors and CSS
<span style="white-space: nowrap;"><key>ctrl</key>+<key>shift</key>+<key>Del</key></span> | Troubleshoot objects (remove errors)
<key>ctrl</key>+<key>shift</key>+<key>!</key> | Attach commands to selected objects
<key>ctrl</key>+<key>shift</key>+<key>U</key> | Convert line to satin column (U looks like two rails) | Object > Group (use Ctrl+G instead)
<key>ctrl</key>+<key>shift</key>+<key>J</key> | Flip satin column rails (J looks like an arrow)
<key>ctrl</key>+<key>shift</key>+<key>B</key> | Cut satin column (B is cut in half) | Path > Union (use Ctrl++ instead)
<key>ctrl</key>+<key>shift</key>+<key>=</key> | Auto-route satin (puts everything in order)

The Ink/Stitch [simulator](/docs/visualize/#simulation-shortcut-keys) also provides shortcut keys.

\* Stack Up and Stack Down give precise control over the order that objects are stitched in. Very useful in combination with the Objects panel (`Objects > Objects ...`). The stacking order defines, in which order elements are stitched out (from bottom to top).<br><br>** For satins and running stitch, this changes the direction the stitches go in. Use with `Show path direction on outlines` selected in `Edit > Preferences > Tools > Node`. If you select just one vertex using the node editor and press `Ctrl+R`, Inkscape will reverse just one path in an object. This way you can make sure that both rails in a satin point the same direction.
{: .notice--info }
{: style="font-size: 70%" }

### Download and import custom shortcut keys

* [Download the Ink/Stitch shortcut key file](/assets/files/inkstitch.xml)
* Go to `Edit > Preferences > Interface > Keyboard`
* Click on `Import...`
* Select the downloaded file and open

You will now be able to use the shortcut keys described above. They are included into the standard default.xml shortcut file.

If you want to define your own custom shortcut keys simply enter your desired key combinations in the shortcut dialog.
Use the search function to find the extensions quicker. [More information](http://wiki.inkscape.org/wiki/index.php/Customizing_Inkscape)
{: .notice--info }

## Zoom correction factor

For embroidery it is essential to get a sense of the actual size of the design. Inkscape has a setting to adapt zoom levels to your display size.

* Go to `Edit > Preferences > Interface`
* Hold a ruler onto your display and adjust the slider until the length matches
 
![Zoom correction](/assets/images/docs/en/customize-zoom-correction.png)

## Grids

To align your vector-shapes properly, you might want to make use of the grid functionality of Inkscape. Go to `View` and enable `Page Grid`. In `Snap Controls Bar` make sure `Snap to grids` is enabled. It is also possible to adjust spacing and origin of your grids in `File >  Document Properties > Grids`.

![Grids](https://user-images.githubusercontent.com/11083514/40359052-414d3554-5db9-11e8-8b49-3be75c5e9732.png)

## Enabling Path Outlines & Direction

Knowing path directions is important working with Ink/Stitch. Therefore we recommend to enable the checkboxes **Show path direction on outlines** and **Show temporary outline for selected paths** in `Edit > Preferences > Tools > Node`.

Make sure that also **Show path outline** is enabled in `Tool Controls Bar` as you can see in the image below.

[![Path outlines & directions](https://user-images.githubusercontent.com/11083514/40360721-f294ef0a-5dbe-11e8-9d4d-98f469ff1fba.png)](https://user-images.githubusercontent.com/11083514/40360721-f294ef0a-5dbe-11e8-9d4d-98f469ff1fba.png)

## Working with Templates

If you decided to use Ink/Stitch more frequently for your embroidery work, you might get tired of setting up the whole scene over and over again. In this case you are ready to create a template for your basic embroidery setup. Once you organised everything as desired, simply save your file in your templates folder. You can now access it by `File > New from template`.

Operating system|Template Folder
---|---
Linux|`~/.config/inkscape/templates`
Windows|`C:\Users\%USERNAME%\AppData\Roaming\inkscape\templates`

You should confirm the user folder in your inkscape preferences see the [FAQ](/docs/faq/#i-have-downloaded-and-unzipped-the-latest-release-where-do-i-put-it).

**Tip:** Get [predefined templates](/tutorials/resources/templates/) from our tutorial section.
{: .notice--info }

## Install Thread Color Palettes

Ink/Stitch comes with a lot of thread manufacturer color palettes which can be installed into Inkscape. This allows to build the designs with the correct colors in mind.
Colors will appear in the PDF-Output and will also be included into your embroidery file, if your file format supports it. 

[Read more](/docs/thread-color/#install-thread-color-palettes-for-inkscape)

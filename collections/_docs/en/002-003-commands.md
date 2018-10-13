---
title: "Visual Commands"
permalink: /docs/commands/
excerpt: ""
last_modified_at: 2018-10-11
toc: true
---
## Installation

[Install Commands](/docs/addons/) before usage.

## Attach visual commands via extension

It is best practice to add commands through extensions:

* Select one ore more objects
* Run `Extensions > Ink/Stitch > English > Commands > Attach commands ...`
* Enable desired commands and apply
* Start/Stop/Cut commands: The connector's endpoint nearest to the object is the point at which the effect will be performed.

In `Extensions > Ink/Stitch > English > Commands` you will find three options: add commands, add layer commands and attach commands.

### Add Commands ...

These commands effect the entire embroidery design.

![stop position](/assets/images/docs/visual-commands-stop-position.jpg) [Stop Position](#-stop-position)

![origin](/assets/images/docs/visual-commands-origin.jpg) [Origin](#-origin)

#### Add Layer Commands ...

These commands will be added to the currently selected layer.

![ignore layer symbol](/assets/images/docs/visual-commands-ignore-layer.jpg) Ignore layer

#### Attach Commands to Selected Objects ...

These commands will be attached to the currently selected objects.

![starting point symbol](/assets/images/docs/visual-commands-start.jpg) Fill stitch starting point

![ending point symbol](/assets/images/docs/visual-commands-end.jpg) Fill stitch ending point

![trim symbol](/assets/images/docs/visual-commands-trim.jpg) [Trim](#-trim) the thread after sewing this object

![stop symbol](/assets/images/docs/visual-commands-stop.jpg) [Stop](#-stop) (pause) the machine after sewing this object (for applique, etc)

![ignore symbol](/assets/images/docs/visual-commands-ignore.jpg) Ignore object

![satin cut point symbol](/assets/images/docs/visual-commands-satin-cut-point.jpg) [Satin cut point](/docs/commands/#-satin-cut-point) (use with "Cut Satin Column")

![auto route satin starting position symbol](/assets/images/docs/visual-commands-auto-route-satin-stitch-start.jpg) Auto-route satin stitch starting position

![auto route satin starting position symbol](/assets/images/docs/visual-commands-auto-route-satin-stitch-end.jpg) Auto-route satin stitch ending position

**Info:**
Starting and ending point currently apply only to fill-stitch objects, while trim and stop commands take effect on any connected object.
{: .notice--info }

### Attach visual commands manually
* Go to `Object > Symbols` or hit `Shift+Ctrl+Y` to access the markers through the symbols dialog.
* Select "Ink/Stitch Commands" as the symbol set.
![Symbol Set](/assets/images/docs/en/visual-commands-symbol-set.jpg)
* Drag a marker out onto your canvas (doesn't matter where).
* Use the Flow-Chart Tool ("create diagram connectors" `Ctrl+F2`) to draw a connection between the marker and the fill object to which it should apply. This will add a connector path.
* Moving the marker will change the connector's position to match. You can also move the endpoints of the connector manually. The connector's endpoint nearest to the fill object is the point at which stitching will start or end.

  <div style="position: relative; padding-bottom: 50%; height: 0;">
    <iframe src="/assets/video/docs/visual-commands.m4v" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
  </div>
  
  [Download Sample File](/assets/images/docs/visual-commands-fill-stitch.svg){: download="visual-commands-fill-stitch.svg" title="Download Sample File"}

## Visual commands reference

### ![stop symbol](/assets/images/docs/visual-commands-stop.jpg) Stop
Commercial embroidery machines that have multiple needles normally proceed from one color to the next without pausing in between. Sometimes you *want* a pause (e.g. to trim applique fabric), so "STOP after" adds an extra color change which can be assigned to a special stop instruction using the machine's user interface (e.g. C00 on Barudan machines). Common uses for this would be to apply puff foam after doing regular embroidery.  Applying applique fabric and/or even wanting to slow down the machine at a certain spot for certain types of embroidery without having to babysit the machine.

### ![trim symbol](/assets/images/docs/visual-commands-trim.jpg) Trim
"Trim after" tells the embroidery machine to cut the thread after the assigned object has been stitched.  Not all home machines support the trim function within a color block.  Mainly used to prevent long jump stitched between embroidery objects and to avoid post embroidery trimming by the operator.

### ![stop position](/assets/images/docs/visual-commands-stop-position.jpg) Stop position
The embroidery machine jumps to this point before every Stop command.  This allows for pushing the embroidery frame out toward the user to make applique steps easier.

### ![origin](/assets/images/docs/visual-commands-origin.jpg) Origin
Specifies the origin (0,0) point for embroidery files. Setting up origins is especially useful for people that have full access to the entire sewing field that their machine is capable of regardless of what hoop they use.

### ![satin cut point symbol](/assets/images/docs/visual-commands-satin-cut-point.jpg) Satin cut point
Split a Satin Column at the point specified by this command. After attaching run "[Cut Satin Column](/docs/satin-tools/#cut-satin-column)". 


---
title: "Visual Commands"
permalink: /docs/commands/
last_modified_at: 2026-01-22
toc: true
---
Visual commands can be used to specify additional information on how to embroider your design. They can be used e.g. to tell the machine to trim the thread after finishing a specific embroidery element or when to pause and where to stop, so you can add a fabric layer to your appliqué design more conventiently.

Not every embroidery machine will be able to read and process the information given by some of these commands. If this is not working for you, read your machines manual to verify your machines capabilities.
{: .notice--warning }

In `Extensions > Ink/Stitch  > Commands` you will find four options:

* [Add commands](#add-commands-)
* [Add layer commands](#add-layer-commands-)
* [Attach commands to selected objects](#attach-commands-to-selected-objects-)
* [View](#view)

**Need to duplicate objects with commands?** A common way to copy objects in Inkscape is duplicate. Before duplicating objects with commands, ensure that `Relink Duplicated Clones` in `Edit > Preferences > Behavior > Clones` is enabled.
{: .notice--info }

**Positioning of commands** Commands in most use cases are pointers to specific positions. To position a command, just select the symbol and move it with the mouse or arrow keys. When moving with the arrow keys, you can press the Shift key for quick movement, the Alt key is used for fine adjustment.
{: .notice--info }

## Add Commands ...

These commands effect the entire embroidery design.

### ![origin](/assets/images/docs/visual-commands-origin.jpg) Origin

Specifies the origin (0,0) point for embroidery files. Setting up origins is especially useful for people that have full access to the entire sewing field that their machine is capable of regardless of what hoop they use.

### ![stop position](/assets/images/docs/visual-commands-stop-position.jpg) Stop position

The embroidery machine jumps to this point before every stop command. This allows for pushing the embroidery frame out toward the user to make applique steps easier.

## Add Layer Commands ...

These commands will be added to the currently selected layer.

### ![ignore layer symbol](/assets/images/docs/visual-commands-ignore-layer.jpg) Ignore layer

All objects in this layer will not be exported to embroidery files. A common usage of this command would be in tutorial files where you want Ink/Stitch not to render explainatory text.


## Attach Commands to Selected Objects ...

These commands will be attached to the currently selected objects.

* Select one ore more objects
* Run `Extensions > Ink/Stitch  > Commands > Attach commands ...`
* Enable desired commands and apply
* Start/Stop/Cut commands: The center of the symbol marks the point at which the effect will be performed.

### ![starting point symbol](/assets/images/docs/visual-commands-start.jpg) ![ending point symbol](/assets/images/docs/visual-commands-end.jpg) Starting/Ending position

Defines the (1) starting or (2) ending point of a fill stitch area or a satin column.

###  ![auto route starting position symbol](/assets/images/docs/visual-commands-auto-route-running-stitch-start.jpg) ![auto route  ending position symbol](/assets/images/docs/visual-commands-auto-route-running-stitch-end.jpg) Starting/Ending position for auto-route operations

Defines the (1) starting or (2) ending point for an auto route operation.

Use only one starting and one ending point per auto-route operation.
{: .notice--warning }

Auto-route operations can be performed on satins ([Tools: Satin > Auto-route satin](/docs/satin-tools/#auto-route-satin-columns)) or strokes.

Strokes have two different for automated routing:

* [Tools: Stroke > Auto-route running stitch](/docs/stroke-tools/#autoroute-running-stitch) (one or two passes per line section)
* [Tools: Stroke > Redwork](/docs/stroke-tools/#redwork) (exactly two passes for each line section)

Only the starting point is used for Redwork, as Redwork always ends at the starting point.

### ![Target symbol](/assets/images/docs/visual-commands-ripple-target.png) Target position

Defines the target point of a ripple stitch area or of a circular fill.

### ![satin cut point symbol](/assets/images/docs/visual-commands-satin-cut-point.jpg) Satin cut point

Split a Satin Column at the point specified by this command. After attaching run "[Cut Satin Column](/docs/satin-tools/#cut-satin-column)".

### ![stop symbol](/assets/images/docs/visual-commands-stop.jpg) Stop

Commercial embroidery machines that have multiple needles normally proceed from one color to the next without pausing in between. Sometimes you *want* a pause (e.g. to trim applique fabric), so "STOP after" adds an extra color change which can be assigned to a special stop instruction using the machine's user interface (e.g. C00 on Barudan machines). Common uses for this would be to apply puff foam after doing regular embroidery.  Applying applique fabric and/or even wanting to slow down the machine at a certain spot for certain types of embroidery without having to babysit the machine.

### ![trim symbol](/assets/images/docs/visual-commands-trim.jpg) Trim

"Trim after" tells the embroidery machine to cut the thread after the assigned object has been stitched.  Not all home machines support the trim function within a color block.  Mainly used to prevent long jump stitched between embroidery objects and to avoid post embroidery trimming by the operator.

### ![ignore symbol](/assets/images/docs/visual-commands-ignore.jpg) Ignore object

Objects with this command will be excluded from the stitch plan output.

## Delete Commands

### Delete single commands

Select the command-group and delete.

### Delete all commands in the document

* Run `Extensions > Ink/Stitch > Troubleshoot > Remove embroidery settings`
* Choose to remove all or specific command types to remove from the document
* Click on `Apply`

## Jump Stitch to Trim Command

`Commands > Jump Stitch to Trim Command` 

Inserts trim commands to avoid jump stitches
{% include upcoming_release.html %}
You can chose between trim or stop command.

**Info**: Do not to use this option when you can optimize routing instead. Cutting threads should be avoided as much as possible. Learn about the options Ink/Stitch has to offer for a [better routing](/tutorials/routing/).
{: .notice--info }

## View

### Display Hide Object Commands

Toggle visibility of object commands. Commands will still be functional when hidden.

`Extensions > Ink/Stitch > Commands > View > Display|Hide Object Commands`

### Scale Command Symbols

Set the size of command symbols in the entire document: `Extensions > Ink/Stitch > Commands > View > Scale Command Symbols...`

Use live preview to see the effect while scaling.

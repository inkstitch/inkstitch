---
title: "Visualize"
permalink: /docs/visualize/
excerpt: ""
last_modified_at: 2023-02-20
toc: true
---
## Simulator / Realistic Preview

Select the objects you wish to see in a simulated preview. If you want to watch your whole design being simulated, select everything (`Ctrl+A`) or nothing.

Then  run `Extensions > Ink/Stitch  > Visualize and Export > Simulator / Realistic Preview` and enjoy.

![Simulator](/assets/images/docs/en/simulator.jpg)
{: style="border: 2px solid gray; padding: 5px;"}

### Simulation Shortcut Keys

Shortcut Keys | Effect
-------- | --------
<key>space</key> | start animation
<key>p</key> | pause animation
<key>→</key> | forward
<key>←</key> | backward
<key>↑</key> | speed up
<key>↓</key> | slow down
<key>+</key> | one frame forward
<key>-</key> | one frame backward
<key>Page down</key> | Jump to previous command
<key>Page up</key> | Jump to next command

It is also possible to **zoom** and **pan** the simulation with the mouse.

## Stitch Plan Preview

Run `Extensions > Ink/Stitch > Visualize and Export > Stitch Plan Preview...`.
Instead of applying the stitch plan, you can also use the `Live preview` option. Then you don't need to undo your changes afterwards. If you apply the stitch plan, you will have the ability to inspect it and adapt your design as you wish. Use the Undo Stitch Plan extension to remove it afterwards.

You have the following display options:
* **Move stitch plan beside the canvas** Displays the preview on the right side of the canvas. If not enabled, the stitch plan will be placed on top of your design. In that case you may want to update your design visibility to eather hidden or lower opacity.
* **Display layer visibility** defines the visibility of the original design layer.
  * **unchanged** leave it as is
  * **hidden** hide the original design
  * **lower opacity** display original design with lower opacity
* **Needle points** displays needle points if enabled
* **Lock** make stitch plan insensitive to mouse interactions (makes it easier to work on the actual design while the stitch plan is active)

{% include folder-galleries path="stitch-plan/" captions="1:Stitch plan beside canvas;2:Layer visibility set to hidden;3:Layer visibility set to lower opacity;4:Needle points enabled | disabled" caption="<i>Example image from [OpenClipart](https://openclipart.org/detail/334596)</i>" %}

## Undo Stitch Plan

Using a stitch plan overlay with hidden or lower density elements helps to get a visual idea of how the design will look in the end.
Sometimes it can be helpful to keep the stitch plan as a visual help while working on new elements.
But for the export or for changes at existing elements during the workflow you will need the original elements back.
Delete the stitch plan, unhide original elements or reset the opacity to normal isn't a lot of fun.
This extension is meant to help with this workflow.

Run `Extensions > Ink/Stitch > Visualize and Export > Undo Stitch Plan Preview`

## Density Map

* Select objects if you want the density map only for some objects, otherwise run without any selection
* Run `Extensions > Ink/Stitch > Visualize and Export > Density Map`
* Set color ranges and apply
* Inspect (zoom in)
* Undo with `Ctrl + Z`

This will display red, yellow and green dots on top of your elements so you can identify areas of high density easily.

## Print PDF

Information about the print pdf preview are collected in an other section: [more info about the pdf export](/docs/print-pdf)

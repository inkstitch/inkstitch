---
title: "Visualize"
permalink: /docs/visualize/
last_modified_at: 2024-03-13
toc: true
---
## Simulator

Select the objects you wish to see in a simulated preview. If you want to watch your whole design being simulated, select everything (`Ctrl+A`) or nothing.

Then  run `Extensions > Ink/Stitch  > Visualize and Export > Simulator` and enjoy.

![Simulator](/assets/images/docs/en/simulator.jpg)
{: style="border: 2px solid gray; padding: 5px;"}

### Buttons and Shortcut Keys

 
Button  | Effect | Shortcut Keys
-------- | -------- | --------
**Controls**||
|<img src="/assets/images/docs/icons/backward_command.png" height="20">|Go back to previous command| <key>Page down</key>
|<img src="/assets/images/docs/icons/backward_stitch.png" height="20">|Go back one stitch| <key>←</key>
|<img src="/assets/images/docs/icons/forward_stitch.png" height="20">|Go forward one stitch| <key>→</key>
|<img src="/assets/images/docs/icons/forward_command.png" height="20">|Go to next command| <key>Page up</key> 
|<img src="/assets/images/docs/icons/direction.png" height="20">|Switch animation direction| 
|<img src="/assets/images/docs/icons/play2.png"> | start/pause animation |<key>space</key> /  <key>p</key>
|<img src="/assets/images/docs/icons/restart.png" height="20">|restart| 
**Speed**||
|<img src="/assets/images/docs/icons/slower.png" height="20">|render slower| <key>↓</key> 
|<img src="/assets/images/docs/icons/faster.png" height="20">|render faster| <key>↑</key> 
**Show**||
|<img src="/assets/images/docs/icons/npp.png" height="20">|Needle penetration point| 
|<img src="/assets/images/docs/icons/jump.png" height="20">|Jumps| 
|<img src="/assets/images/docs/icons/trim.png" height="20">|Trims| 
|<img src="/assets/images/docs/icons/stop.png" height="20">|Stops| 
|<img src="/assets/images/docs/icons/color_change.png" height="20">|Color Changes| 
**Info**||
|<img src="/assets/images/docs/icons/info.png" height="20">|Design Information| 
**Settings**||
||Change background color| 
|<img src="/assets/images/docs/icons/cursor.png" height="20">|Show crosshair| 
|<img src="/assets/images/docs/icons/page.png" height="20">|Show page| 
|<img src="/assets/images/docs/icons/settings.png" height="20">|Open setting dialog to set speed, line width and needle point size| 



It is also possible to **zoom** and **pan** the simulation with the mouse.

## Stitch Plan Preview

Run `Extensions > Ink/Stitch > Visualize and Export > Stitch Plan Preview...`.
Instead of applying the stitch plan, you can also use the `Live preview` option. Then you don't need to undo your changes afterwards. If you apply the stitch plan, you will have the ability to inspect it and adapt your design as you wish. Use the Undo Stitch Plan extension to remove it afterwards.

### Options

- **Design layer visibility** defines the visibility of the original design layer.
  - **unchanged** leave it as is
  - **hidden** hide the original design
  - **lower opacity** display original design with lower opacity
- **Render Mode**
  - **Simple**: simple line drawing
  - **Realistic**: Realistic preview output as png image into the canvas (8-bit)
  - **Realistic High Quality** Realistic preview output as png image into the canvas (16-bit)
  - **Realistic vector (slow)** Vector output with realistic filters

    Slow means, that it has the capability to slow down Inkscape after the rendering process and even may make it freeze.
    So use with care on complex designs and save your design before you render the stitch plan.
    {: .notice--warning }
- **Move stitch plan beside the canvas**
  Displays the preview on the right side of the canvas. If not enabled,the stitch plan will be placed on top of your design.
  In that case you may want to update your design visibility to eather hidden or lower opacity.
- **Needle points** displays needle points if enabled
- **Lock** make stitch plan insensitive to mouse interactions (makes it easier to work on the actual design while the stitch plan is active)
- **Display command symbols**
- **Overide last stitch plan**
  If checked the new stitch plan will replace the previous one, uncheck if you wish to keep the previous stitch plan

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

### Options

* Red / yellow markers

  Define up from many stitches in which radius should dots should be colored red or yellow
* Design layer visibility

  Define if Ink/Stitch should leave the design layer unchanged, hide id or lower opacity
* Indicator size

  Define the size of the dots in document units

## Display stacking order

This extension inserts numbered labels for selected elements into the document to visualize the stitch order.

* Run `Extensions > Ink/Stitch > Visualize and Export > Display stacking order...`.
* Choose font size
* Click on apply

![Display stacking order](/assets/images/docs/stacking_order.png)

## Print PDF

Information about the print pdf preview are collected in another section: [more info about the pdf export](/docs/print-pdf)

---
permalink: /da/tutorials/autoroute_sashiko/
title: "Sashiko "
language: da
last_modified_at: 2022-05-25
excerpt: "Using Sashiko extension  with autoroute  runningstitch"
image: "/assets/images/tutorials/sashiko/sashiko.jpg"
tutorial-type:
  - Sample File
stitch-type:
  - "Bean Stitch"
techniques:
field-of-use:
user-level: 
---


![Sample](/assets/images/tutorials/sashiko/sashiko.jpg)


[Sashiko Inkscape extension](https://inkscape.org/~FractalLotus/%E2%98%85sashiko-stitching-patterns) combined with "Auto-Route Running Stitch"  
makes it possible to produce sashiko style triple stitch embroidery files in a way so easy it's almost indecent.

First install the Sashiko extension.

Once this extension is installed, run it:


`Extensions > Render > Sashiko' 

![ScreeShot](/assets/images/tutorials/sashiko/Sashiko1-en.jpg)

By enabling "Live preview", you can easily chose pattern, rows and columns.

Then click 'Apply'.

You can now close the Sashiko extension dialog window.

To change from design to triple stitch embroidery
* Select all the paths that the extension just created (there are many)
  * Set all stroke style to dashed
  * `Extensions > Ink/Stitch > Params'
    * Set the length of the running stitch (2 mm for the embroidered sample)
     * Choose the bean stitch number of repeats (1 for the embroidered sample)
  * `Extensions > Ink/Stitch > Tools:Stroke > Auto-Route Running Stitch`
    * Enable "Add node at intersections"
    * Disable "Preserve order of running stitch"
   * Click Apply

**and that's all !!!!**

Instead of the paths created by the Sashiko extension you now have a group  "Auto-Route" that contains a mix of:
* bean stitch paths called  "Auto-Route xyz"
* simple running stitch path  calles "Auto-Route underpath yzt" 

simple running stitch  paths hidden under triple stitch path to allow the design to have as few jumps as possible.


You may wish to also try with this [extension](https://tesselace.com/tools/inkscape-extension/)



 


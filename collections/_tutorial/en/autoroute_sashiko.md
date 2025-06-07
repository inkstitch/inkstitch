---
permalink: /tutorials/autoroute_sashiko/
title: "Sashiko "
language: en
last_modified_at: 2025-02-09
excerpt: "Using Sashiko extension  with autoroute  runningstitch"
image: "/assets/images/tutorials/sashiko/sashiko.jpg"
tutorial-type:
  - Sample File
tool:
  - "Stroke" 
stitch-type:
  - "Bean Stitch"
techniques:
field-of-use:
user-level: 
---
![Sample](/assets/images/tutorials/sashiko/sashiko.jpg)

[Sashiko Inkscape extension for ink/stitch ](https://gitlab.com/kaalleen/sashiko-inkscape-extension) combined with "Auto-Route Running Stitch"  or "Tools: Stroke > Redwork" makes it possible to produce sashiko style  embroidery files in a very easy way.

Note that this extension is different for  the  original [Sashiko Inkscape extension](https://inkscape.org/~FractalLotus/%E2%98%85sashiko-stitching-patterns), as it never generates two copies of the same path one on  top of the other.

First install the Sashiko for ink/stitch extension.

Once this extension is installed, run it:

`Extensions > Render > Sashiko' 

![ScreeShot](/assets/images/tutorials/sashiko/Sashiko1-en.jpg)

By enabling "Live preview", you can easily chose pattern, rows and columns.

Then click 'Apply'.

You can now close the Sashiko extension dialog window.

## If you have chosen a pattern that yields a non conected result (for instance Offset Crosses) 

Use now the "Auto-Route Running Stitch"  extension :

To change from design to triple stitch embroidery
* Select all the paths that the extension just created (there are many)
  * `Extensions > Ink/Stitch > Params'
    * Set the length of the running stitch (2 mm for the embroidered sample)
     * Choose the bean stitch number of repeats (1 for the embroidered sample)
  * `Extensions > Ink/Stitch > Tools:Stroke > Auto-Route Running Stitch`
    * Enable "Add node at intersections"
    * Disable "Preserve order of running stitch"
   * Click Apply

Instead of the paths created by the Sashiko extension you now have a group  "Auto-Route" that contains a mix of:
* bean stitch paths called  "Auto-Route xyz"
* simple running stitch path  calles "Auto-Route underpath yzt" 

simple running stitch  paths hidden under triple stitch path to allow the design to have as few jumps as possible.

## If you have chosen a pattern that yields a connected result (for instance Blue Ocean Weaves) 

Use now the "Redwork"  extension :

Chose your  parameters (0.5mm for the first two parameters is usually a good choice).

If you chose  to combine  and no  bean stitches repeat then you will get a single path that travel everything twice.
If you chose to combine  and have a non null bean stitches repeat value, you will get an alternate sequence of underpath and bean stitch path.

If you do not combine you will get more paths, this should only be done if you want to manipulate the result.

You may wish to also try with other extensions such as :

*[bobbinlace extension](https://d-bl.github.io/inkscape-bobbinlace).
*[Tiling extension](https://inkscape.org/fr/~cwant/%E2%98%85inkscape-tiling-extension+2)


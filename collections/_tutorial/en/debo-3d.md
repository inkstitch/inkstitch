---
title: Debo 3D
permalink: /tutorials/debo-3d/
last_modified_at: 2025-05-12
language: en
excerpt: "Raised embroidery on a cap example file"
image: "/assets/images/tutorials/debo-3d/Final.webp"

tutorial-type:
  - Sample File
  - Text
stitch-type: 
  - Satin Stitch
techniques:
field-of-use:
user-level: Intermediate
---

![Cap with raised embroidery](/assets/images/tutorials/debo-3d/Final.webp)

## Steps

1. Open Inkscape with Ink/Stitch 3.2 or newer.  Using `Extensions>Ink/Stitch>Lettering`,
   choose the Ink/Stitch Masego font andtype in between 2 and 4 letters.

   ![Screen shot of DEBO using Ink/Stitch Masego font](/assets/images/tutorials/debo-3d/DeboLettering.png)

2. Once the text is on the canvas, resize the document by pressing F5 to get the
   text to fill the document.  Then duplicate the text. Hide the top layer. In the
   bottom layer, remove all the columns to just leeave the bean stitches and the
   jump stitches. These will be stitiched first.

   ![Screen short showing two layers, with bottom layer with multiple lines representing jump and bean stitiches](/assets/images/tutorials/debo-3d/BottomLayer.png)

3. Join up the bean stitches on each letter to minimize the number of lock stitches required.  Make
   the jump stitices go through regions that will be covered. Once done, check each stitch using the
   params window `Extensions>Ink/Stitch>Params`. Lock stitches should only be used on the first and
   last stitch.  Check that jumps go in the correct direction.

   ![Screen shot of bean stitch locations](/assets/images/tutorials/debo-3d/BeanStitches.png)

4. Hide the bottom layer and unhide the top layer. Remove the bean and jump stitches from this layer.

   ![Screen shot of areas which will contain satin stitches](/assets/images/tutorials/debo-3d/SatinStitchRegion.png)

5. The raised effect is obtained by using a satin stitch over sponge foam.
   To hold the foam in place, a middle layer is used.  Duplicate the top layer.
   Hide the top layer.  Convert the middle layer to ensure a running stitch is
   used around each boundary of an area where there will be a satin stitch.

   ![Screen shot of boundaries of satin stitch region](/assets/images/tutorials/debo-3d/BoundaryStitch.png)

6. Scale each boundary region in the middle layer by 90%.  Unhide the top layer.  Adjust
   individual nodes so that the spacing between the outer boundary in each satin stitch
   region in the top layer is even.  Once the middle layer is held in place, the outer
   foam will be carefully removed.  Having a small gap enables the thread to completely
   cover the foam so that it is not visible.

   ![Screen shot showing inner running stitich and outer satin stitch regions](/assets/images/tutorials/debo-3d/RunningStitchBoundary.png)

7. Hide the middle layer. Ensure each region in the top layer has stitches that start and end at
   a corner by placing rungs diagonally across the top left and bottom right corners.

   ![Screen shot showing rung placement for satin columns](/assets/images/tutorials/debo-3d/RungPlacement.png)

8. For each region go to `Extensions>Ink/Stitch>Params` choose the type as a Satin column with
   a Contour underlay.  Change the parameters of the satin colum to have 0% short-stitch inset,
   0.0 mm short stitch distance and 0.25 mm/cycle zig-zag spacing.  The high stitch density will
   hide the foam. Make sure each satin column has beginning and ending lock stitches.

   ![Screen shot satin column parameters](/assets/images/tutorials/debo-3d/SatinColumnParameters.png)

9. Make sure each satin column has beginning and ending lock stitches.

   ![Screen shot of showing lock stitch settings for satin columns](/assets/images/tutorials/debo-3d/SatinColumnLockStitches.png)

10. The embroidered region is a little small.  Select all objects, then go to `Object>Transform`
    choose `Scale` and give the entire object a height of 4cm.  This will fit nicely onto a cap.

    ![Screen shot showing rescaled embroidery region](/assets/images/tutorials/debo-3d/Rescaled.png)

11. Add a new layer with the license information

    ```
    CC BY-SA 3.0 Deed Unported
    https://creativecommons.org/licenses/by-sa/3.0/
    Adapted from Masego Font for 3D embroidery
    https://madebydebo.gumroad.com/
    ```

    Choose `Extensions>Ink/Stitch>Commands>Add Layer Commands...` and ignore the
    layer for stitching but leave it visible.

13. Embroider the bottom layer.  Place the foam on the cap. Embroider the
    middle layer.

    ![Image of foam embroidered on top of the cap](/assets/images/tutorials/debo-3d/FoamMiddleLayer.webp)

14. Carefully remove the excess foam.

    ![Excess foam has been removed](/assets/images/tutorials/debo-3d/ExcessFoamRemoved.webp)

15. Stitch the top layer to produce the finished cap.

    ![Cap with 3D embroidery with the word DEBO](/assets/images/tutorials/debo-3d/Final.webp)

*Thanks to [Debo](https://madebydebo.gumroad.com/) for creating the Masego font.
This tutorial has benefitted from the
[Low Tech Linux](https://www.youtube.com/watch?v=oAL3eHtAvrs)
and [Project Anonymous](https://www.youtube.com/watch?v=UwIIx-lHFNs) video tutorials.


### Sample file

[Download](/assets/images/tutorials/samples/Debo3D.svg){: download="Debo3D.svg" }


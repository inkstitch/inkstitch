---
title: Winkler Alternative GNU for 3D on a Cap
permalink: /tutorials/winkler-gnu-3d/
last_modified_at: 2025-09-12
language: en
excerpt: "GNU example file for puff stitch on a cap"
image: "/assets/images/tutorials/winkler-gnu-3d/Stitchout.jpg"

tutorial-type:
  - Sample File
  - Text
stitch-type: 
  - Satin Stitch
techniques: 3D
field-of-use:
user-level: Intermediate
---

![Mockup of final design](/assets/images/tutorials/winkler-gnu-3d/Mockup.jpg)

The design has been tried on 2mm thick embroidery foam, adjustments may be
needed if 1mm or 3mm thick embroidery foam is used.  Regular 40 weight thread
and a regular needle are used. It helps to match the color of the foam to
the color of the thread which covers it.  One first embroiders
the parts that will lay flat on the cap, in this case the text GNU and the
license information.  The foam is then placed on the cap and a first layer
of satin stitches placed on the foam to cut the foam.  Once the foam is cut
by the first layer of stitches, carefully remove the excess leaving the
hat on the machine. Then embroider the second layer of satin stitches
on top of the foam to ensure that it is completely covered.  The second layer
of satin stitches is placed one thread width away from the first to ensure
they do not overlap so that the final finish is neat.  If the
embroidery machine you are using will have a lot of play, skip the
initial cutting layer of stitches and just embroider the final dense satin
stitches.  This may show a little more of the foam when complete though.

## Steps

1. Download the Alternative GNU SVG logo file from
   https://www.gnu.org/graphics/winkler-gnu.svg
   and open it in Inkscape

   ![Screen short of original file](/assets/images/tutorials/winkler-gnu-3d/OpenFile.jpg)

2. Group the first four path elements which correspond to the letters
   `GNU` and the underline. Delete the last rectangle. Convert all
   other rectangles to paths using `Path>Object to Path`

   ![Screen shot showing rectangles have been converted to paths](/assets/images/tutorials/winkler-gnu-3d/RectanglesToPaths.jpg)

3. Using `Path>Union`, combine all the rectangles,

   ![Screen shot of combined rectangles](/assets/images/tutorials/winkler-gnu-3d/CombineRectangles.jpg)

4. Ungroup the last group, and then subtract the middle path from
   the bottom path using `Path>Difference`

   ![Screen shot showing how ungrouped last path before taking difference](/assets/images/tutorials/winkler-gnu-3d/Difference.jpg)

5. Add stroke to the horns and remove the fill

   ![Screen shot showing horns without fill and with stroke](/assets/images/tutorials/winkler-gnu-3d/HornsStroke.jpg)

6. Remove all the interior nodes on the horns, and separate the horns into
   two disjoint left and right horns.

   ![Screen shot showing horns with just an outline](/assets/images/tutorials/winkler-gnu-3d/HornsOutline.jpg)

7. Select the whole image, and rescale it to a height of 4.75cm
   so it can fit on the front of a cap

   ![Screen shot showing rescaled image](/assets/images/tutorials/winkler-gnu-3d/Rescaled.jpg)

8. Go to `File>Document Properties ...` change the document size to fit the rescaled image by
   selecting `Resize to content`

   ![Screen shot showing document size fitted to image](/assets/images/tutorials/winkler-gnu-3d/FitImage.jpg)

9. Zoom in on the image, select the horns and change the stroke width of the horns to 0.4mm
   
   ![Screen shot showing horn stroke width of 0.4mm](/assets/images/tutorials/winkler-gnu-3d/HornsStrokeWidth.jpg)

10. Using `Path>Flatten` flatten the stroke of the forns, to generate a filled region bounded
    by two strokes.

    ![Screen shot showing flattening of the horn strokes](/assets/images/tutorials/winkler-gnu-3d/HornsFlattenedStroke.jpg) 

11. Remove the fill from the horns boundary and make the stroke 0.1mm

   ![Screen shot showing horns boundary without fill](/assets/images/tutorials/winkler-gnu-3d/HornsBoundryNoFill.jpg)

12. Duplicate the layer with the horns.  Move the text to the bottom layer.  Hide the
    top horns layer. Remove the outer boundaries on the bottom horns layer.

   ![Screen shot showing bottom horns layer](/assets/images/tutorials/winkler-gnu-3d/HornsBottom.jpg)

13. Hide the bottom horns layer and unhide the top horns layer. Remove the inner
    boundaries on the top horns layer.

    ![Screen shot sowing top horns layer](/assets/images/tutorials/winkler-gnu-3d/HornsTop.jpg)

14. Create small gaps at the ends of the horns in the top and bottom layers, then
    add rails for a satin stitch.

    ![Screen shot showing rails on the horns](/assets/images/tutorials/winkler-gnu-3d/HornsRails.jpg)

15. Split the top and bottom horns into left and right pieces and put them in their
    own groups.

    ![Screen shot of horns split and grouped](/assets/images/tutorials/winkler-gnu-3d/HornsSplitGrouped.jpg)

16. For the bottom horns, choose one of them, then go to `Extensions>Ink/Stitch>Params`
    and choose `Custom Satin Column` with a short stitch inset of 0%, a short stitch
    distance of 0.0mm, Zig-zag spacing (peak-to-peak) of 0.6 mm/cycle and disable
    the options to start and end at the nearest points, leave other settings as
    default. Examine the stitch placement, adjust the rails to make stitch points as
    evenly spaced as possible.  Repeat for the other horn.

   ![Screen shot showing parameter settings for lower layer right horn](/assets/images/tutorials/winkler-gnu-3d/LowerRightHornSatin.jpg)


17. For the top horns, choose one of them, then go to `Extensions>Ink/Stitch>Params`
    and choose `Custom Satin Column` with a short stitch inset of 0%, a short stitch
    distance of 0.0mm, Zig-zag spacing (peak-to-peak) of 0.18 mm/cycle and disable
    the options to start and end at the nearest points, leave other settings as
    default. Examine the stitch placement, adjust the rails to make stitch points as
    evenly spaced as possible.  Repeat for the other horn.

   ![Screen shot showing parameter settings for upper layer left horn](/assets/images/tutorials/winkler-gnu-3d/UpperLeftHornSatin.jpg)

18. Change the letters `GNU` so that they have no fill and stroke.

   ![Screen shot showing letters GNU with no fill and stroke](/assets/images/tutorials/winkler-gnu-3d/LettersNoFill.jpg)

19. Modify the paths on `N` to have the same outer boundaries, by first
    adding fill and removing stroke, then choose `Path>Flatten`

    ![Screen shot showing `N` with fill and no stroke](/assets/images/tutorials/winkler-gnu-3d/NFillNoStroke.jpg)

    then, remove the fill from the `N` and add stroke

    ![Screen shot showing `N` with no fill and stroke](/assets/images/tutorials/winkler-gnu-3d/NStrokeNoFill.jpg)

20. Put the letters into separate groups and order them so they can be
    stitched in sequence from left to right and ending with the underline.

    ![Screen shot showing grouped letters](/assets/images/tutorials/winkler-gnu-3d/GroupedLetters.jpg)

21. For each letter, start at the left with a small running stitch, then
    cover the letter using a satin stitch. Break the satin stitch at the
    end of the letter and reverse the satin stitches so that the last lock
    stitch is hidden. Use rails to generate well spaced satin stitches. Use
    a stitch density of 0.30mm/cycle.

    ![Screen shot showing letters ready for embroidery](/assets/images/tutorials/winkler-gnu-3d/Letters.jpg)

22. The original file is under the [Licensee Art Libre 1.3](https://artlibre.org/).
    Use `Extensions>Ink/Stitch>Lettering>Lettering` and choose the Glacial Tiny
    AGS font with a size of 50% to add `LAL 1.3` to the hat.  If thin thread and
    a thin needle are not available or should not be used, choose a larger font.

    ![Screen shot showing adding LAL 1.3 text](/assets/images/tutorials/winkler-gnu-3d/LicenseText.jpg)

23. Place the license text in the bottom left of the stitch area.  Choose appropriate
    colors for the horns, GNU text and license text, and place the license text
    as the first item to be embroidered, followed by the GNU text followed by the horns.

    ![Screen shot showing file ready for embroidery](/assets/images/tutorials/winkler-gnu-3d/FinalFile.jpg)

24. Add a new layer with the license information

    ```
    LAL 1.3
    https://artlibre.org/
    Modified for embroidery from the original
    https://www.gnu.org/graphics/winkler-gnu.html
    ```

    Choose `Extensions>Ink/Stitch>Commands>Add Layer Commands...` and ignore the
    layer for stitching but leave it visible.

    ![Screen shot showing license layer (not embroidered)](/assets/images/tutorials/winkler-gnu-3d/License.jpg)

25. Export the file from Inkscape in a format suitable for your embroidery
    machine, for example as a dst file. Embroidery the license and GNU texts.

   ![Screen shot showing stitchout of text](/assets/images/tutorials/winkler-gnu-3d/TextStitchout.jpg)

26. Once the text has been embroidered, place the foam on the hat and embroider
    the first layer of stitches for the horns.

    ![Screen shot showing first layer of stitches for the horns being embroidered](/assets/images/tutorials/winkler-gnu-3d/HornsFirstStitches.jpg)

27. Remove the foam. Then add the final layer of stitches to completely cover
    the foam.

   ![Screen shot showing the second layer of stitches being embroidered on the horns](/assets/images/tutorials/winkler-gnu-3d/HornsSecondStitches.jpg)


*This tutorial has benefitted from many suggestions by Dawood, David and Lexelby.

## Alternative GNU Logo (modified for Ink/Stitch by Benson Muite)

![Alternative GNU logo](/assets/images/tutorials/samples/Winkler-GNU.svg)

[Download](/assets/images/tutorials/samples/Winkler-GNU.svg){: download="Winkler-GNU.svg" }


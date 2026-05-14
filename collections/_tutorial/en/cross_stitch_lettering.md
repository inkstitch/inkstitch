---
permalink: /tutorials/cross_stitch_lettering/
title: "Cross Stitch Lettering"
language: en
last_modified_at: 2026-05-14
excerpt: "Cross Stitch Lettering "
image: "/assets/images/tutorials/tutorial-preview-images/hello.png"
tutorial-type: 
stitch-type: 
 - Cross Stitch
tool:
techniques:
field-of-use:
user-level: 
toc: true
---

{% include upcoming_release.html %}

## Cross Stitch Lettering

### Using the Lettering Tool

The simplest method is to use a ready-to-use cross stitch font from the lettering tool, chosen from the twenty or so available.

It's easy to limit the font selection menu to cross stitch fonts by simply selecting "Cross Stitch" from the dropdown menu in the upper right corner.

![cross stitch font selection](/assets/images/tutorials/cross_stitch_lettering/fr/choix_point_de_croix.jpg)

Then, everything works just like with other fonts.

### Using a Pixel Font for Custom Lettering

Many pixel fonts are available.

You can find some on [fonts.google.com](https://fonts.google.com) by filtering for pixel appearance, but there are many more free pixel fonts on the web.

For this tutorial, we will use the doto font, available on fonts.google.com.

[doto](/assets/images/tutorials/cross_stitch_lettering/doto.jpg)

We will assume that this font is installed on your computer.

Note: If you install a new font on your system to use in **Inkscape**, you may need to restart Inkscape (depending on your system) for it to appear in the dropdown menu of installed fonts for the Inkscape Text tool. This is essential for using the font in Inkscape.

Our aim is to convert each "pixel" of the font into a cross stitch. With standard thread, it's reasonable to produce crosses between 1.8 mm and 4 mm high. Using thinner thread allows you to go below 1.8 mm, while using thicker thread allows for even larger crosses.

#### Instructions
The steps are as follows:

- Verify that in your Inkscape preferences, under the Interface tab, the "Origin at upper left, y-axis pointing downward" option is checked.

- Decide on the size of the crosses: in this example, we will aim for 3mm crosses. This size is suitable for all the types of cross stitch available in Ink/Stitch.

- Display a grid with 3mm horizontal and vertical spacing, either using the document properties or the Cross Stitch Assistant (Deselect everything, then go to Ink/Stitch > Tools: Fill > Cross Stitch Assistant set the horizontal grid spacing in the Parameters tab, and check "Show grid" in the Output Options tab).

- Select the text tool, and make sure its style has a background color and no outline color.
- Select the Doto font from the font dropdown menu.
- Type your text in the canvas.
- If necessary, resize the text until you have one small square ("pixel") per grid cell.

![hello1](/assets/images/tutorials/cross_stitch_lettering/hello1.jpg)

- Convert the text to a path. Here, simply use `Inkscape > Path > Object to Path`.

- Select the created paths, and then `Ink/Stitch > Tools: Fill > Cross Stitch Assistant`.

![hello1](/assets/images/tutorials/cross_stitch_lettering/fr/assistant1.jpg)

In the parameters tab, the important parameters  are:

- Horizontal grid spacing

- Fill coverage percentage: Since the "pixels" are small compared to the grid squares, you should enter a small value in this parameter.

- The chosen cross stitch method will be automatically selected for the parameters of the fill, which can be adjusted in this same operation provided that:

in the Output Options tab:
- the parameters box is checked.

- the pixelate box is checked.

The shapes on thecanvas change appearance and the cross-stitch settings are complete:

![pixelateandparams](/assets/images/tutorials/cross_stitch_lettering/fr/pixelateandparams.jpg)

Each letter has become a unique shape; while embroidering, jumps only occur between letters.

#### Maybe more information that you wish for ?
You can stop reading this section here, but if you like to understand everything, you might be interested in reading further.

As a reminder, the cross stitch assistant has three **independent** functions that we just used:

- Creating a grid on the canvas. This is a visual tool that shows how Ink/Stitch divides the space to calculate filling coverage (color by color). Displaying the grid is entirely optional. This grid can be displayed via the cross stitch assistant or via the document properties.

- Embroidery Parameters. They can be set  via the cross stitch assistant or via the Ink/Stitch Parameters extension. The cross stitch assistant adds a small expansion (0.1) to each shape, which is always a good idea when creating cross stiches shapes.
- 
- Pixelate. This modifies the shapes: each time the coverage  threshold is reached on a square, the shape is enlarged to fill the entire square. If two squares touch, the shapes they contain are merged. In the previous example, after pixelate, each letter becomes a unique shape. Note that the pixelation is done for a given grid spacing; if you later change the size of the cross stitches, it will no longer accurately reflect the shape of the embroidery!

What would have happened if we had only checked the "parameter" box and not the "pixelate" box?



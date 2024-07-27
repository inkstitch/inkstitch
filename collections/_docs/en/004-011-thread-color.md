---
title: "Thread Color Management"
permalink: /docs/thread-color/
last_modified_at: 2024-07-13
toc: true
---
Inkscape supports the usage of color palettes. Color palettes help Ink/Stitch to define color names and save additional information such as thread manufacturer name and the thread catalog number into the exported embroidery file.

Depending on the capabilities of your embroidery machine you will be able to read color names from the display. Please note, that some embroidery formats (for example DST) do not store color information. Other file formats use a mutliple file system to store color information. For EXP files for example it is common to save the color format INF along with the EXP file to transmit the color information to your machine.

Color definitions are shown in the [pdf output](/docs/print-pdf/). It is also possible to [export threadlist information](/docs/threadlist/) into a simple textfile.

Before you can use thread color features you need to install color palettes. You can either [define your own custom palette(s)](/docs/thread-color/#install-custom-palette) or [install the ones delivered with Ink/Stitch](/docs/thread-color/#install-thread-color-palettes-for-inkscape). Whichever method you choose, restart Inkscape after installing color palettes.

## Install Palettes

### Install Thread Color Palettes for Inkscape

Ink/Stitch comes with a lot of thread manufacturer color palettes which can be installed into Inkscape. This allows to build the designs with the correct colors in mind.
Colors will appear in the PDF-Output and will also be included into your embroidery file, if your file format supports it. 

* Go to `Extensions > Ink/Stitch  > Thread Color Management > Install thread color palettes for Inkscape`
* Click `Install`
* Restart Inkscape

**Info**: Just click install if you are not sure where to install the palettes. Ink/Stitch usually discoveres the correct path for your system by itself.
{: .notice--info }

### Install Custom Palette

In case you own a `.gpl` color list of the threads you are actually using. Make it available in Inkscape with this extension: `Extensions > Ink/Stitch > Thread Color Management > Install custom palette...`. You will need to restart Inkscape after this process.

The .gpl color palettes can be generated with [Generate Color Palette](#generate-color-palette). 

## Generate And Edit Custom Color Palettes

### Generate Palette

Inkscape allows to generate `.gpl` color palette files. But it doesn't allow us to order color swatches properly.

This extension will export colors of text elements while using the text as color names and numbers.

1. Import an image with the thread colors you want to use for the color palette.
2. Activate the text tool and copy & paste the color names (if you have them) or type them in.
   Use one line for each color.
   If the last part of a color name is a number, it will be used as the catalog number.
3. Use `Extensions > Ink/Stitch > Thread Color Management > Generate Palette > Split Text` extension to split a text block with multiple lines into separate text elements.
4. Activate the color picker tool (D) and color the text elements, while using tab to select the text elements.
5. Select the text elements and run `Extensions > Ink/Stitch > Thread Color Management > Generate Palette > Generate Color Palette ...`
6. Specify the name for your color palette and click on apply
7. Restart Inkscape to activate the new color palette

{% include video id="4bcRVoKvzAw" provider="youtube" %}

### Palette to Text

Existing palettes can be edited with Ink/Stitch as text.

* Import colors and color names with `Extensions > Ink/Stitch > Thread Color Management > Palette to Text`
* Change colors, update color names or catalog numbers or add more colors.
* Export your palette with `Extensions > Ink/Stitch > Thread Color Management > Generate Palette > Generate Color Palette ...`
* Restart Inkscape

## Working With Palettes

### General Usage

Inkscape palettes are found on the bottom to the right of the color swatches.

![Inkscape Color Palettes](/assets/images/docs/palettes-location.png)

Click on the little arrow to open a list of installed palettes and choose the manufacturer color palette depending on the thread you are willing to use.

To apply a color to an element, select the element and click on the color swatches at the bottom. Use `left click` for a fill color and `shift + left click` for a stroke color. Use the X on the left side to remove colors.

### Apply Palette

This extension applies nearest colors from a specified thread palette on a design. This will also be recognized by the Ink/Stitch embroidery file and pdf output.

* Run `Extensions > Ink/Stitch > Thread Color Management > Apply Palette`
* Select the color palette you wish to apply
* Click on Apply

## Working with Threadlists

### Export Threadlist

Export threadlists and color files using your normal file export routine in Inkscape.
Threadlists can also be exported within the Ink/Stitch zip-file ([batch export](/docs/import-export/#batch-export)).

### Apply Threadlist

Ink/Stitch can apply a threadlist to an embroidery design. This is especially useful, if you want to work on existing embroidery files which do not support color information (e.g. DST).

It could also be helpful, if you are wanting to test different color settings. You can export and import them as you like. But be careful not to change the amount and order of colors. In case you are planing to change these, you'd prefer to save the entire SVG instead.

* Run `Extensions > Ink/Stitch > Thread Color Management > Apply Threadlist`
* Choose a file with the thread color information
* Define wether the color infomration file has been generated with Ink/Stitch or otherwise.

  If otherwise: Select the Ink/Stitch color palette to match colors to.
* Click on Apply

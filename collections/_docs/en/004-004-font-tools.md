---
title: "Font Tools"
permalink: /docs/font-tools/
last_modified_at: 2023-02-20
toc: true
---
A collection of tools suitable for font creators or those who want to add additional fonts to the Ink/Stitch [lettering tool](/docs/lettering).

Read the [Ink/Stitch font creation tutorial](/tutorials/font-creation) for in-depth instrustions.
{: .notice--info }

## Custom Font Directory

This extension allows you to define a directory in your file system where you want to store additional fonts to be used with the lettering tool.

Place each font in a subdiretory of your custom font directory. Each font folder should contain at least one font variant and one json file.
Additionally it is recommended to save a license file as well.

Font variants have to be named with an arrow, indicating the stitch direction it has been created for (`→.svg`, `←.svg`, etc.). It is also possible to create a folder named with an arrow name instead and insert multiple font files for a specific direction.

The json file has to include as a minimum requirement the fonts name.

## Generate JSON

This extension was created to help you to create the json file.
Depending on the way you generated your font file it can include additional kerning information into the json file.
Read [**how to generate a svg font with kerning information**](/tutorials/font-creation).
If you generated your svg file without kerning information this extension can still help you to set up your json file with basic information.

* **Name**: the name of your font (mandatory).
* **Description**: additional information about your font (such as sizing information, etc)
* **Font File** (mandatory): When you have been using FontForge to generate your svg font file, Ink/Stitch will read the kerning information from your font to include it into the json file.
 Additionally the font file will be used to determine the output path.
* **AutoRoute Satin**:
    * enabled: Ink/Stitch will generate a reasonable routing for satin columns in your font when used in the lettering tool. [More information about AutoRoute Satin](/docs/satin-tools/#auto-route-satin-columns)
    * disabled: Ink/Stitch will use the glyphs as is. Disable this option, if you took care for the routing in your font by yourself.
* **Reversible**: wether your font can be stitch forwards and backwards or only forwards
* **Force letter case**:
  * No: Choose this option if your font contains upper and lower case letters (default).
  * Upper: Choose this option if your font only contains upper case letters.
  * Lower: Choose this option if your font only contains lower case letters.
* **Default Glyph**: the glyph to be shown if the user requested glyph isn't available in the font file (missing glyph)
* **Min Scale / Max Scale**: Define how much can your glyphs can be scaled without loosing quality when stitched out

The following fields are optional only necessary, when your svg file doesn't contain kerning information.
If kerning information cannot be found, these values will be used instead.

* **Force custom values**: Do not use the kerning information from the svg file, but use the given values instead.

* **Leading (px)**: Defines the line height of your font. Leave to `0` to let Ink/Stitch read it from your font file (defaults to 100 if the information cannot be found).
* **Word spacing (px)**: The width of the "space" character

A file `font.json` will be saved into the folder of your svg font file.

## Remove Kerning

**⚠ Warning**: Changes made by this tool cannot be reverted. Make sure to save a **copy** of your file before performing these steps.
{: .notice--warning }

Your font is ready to be used. But when you created your font with FontForge it now contains a lot information which isn't necessary for your font to work and could possibly slow it down a little.
Ink/Stitch comes with a tool to clean up your svg font.

1. Make sure you save a **copy** of your font. The additional information may not be necessary for the font to be used, but it can become handy when you want to add additional glyphs.
2. Run `Extensions > Ink/Stitch > Font Tools > Remove Kerning`
3. Choose your font file(s)
4. Click on apply

## Letters to font

"Letters to font" is a tool to convert predigitized embroidery letters into a font for use with the Ink/Stitch lettering tool.

The digitized font needs to meet certain **conditions** to be imported:
* One file for each glyph in an embroidery format that Ink/Stitch can read
* The glyph name needs to be positioned at the end of the file name. A valid file name for the capital A would be e.g. `A.pes` or `Example_Font_A.pes`.

You will often see, that bought fonts are organized in subfolders, because each letter comes in various embroidery file formats. You don't need to change the file structure in this case. Letters to font will search the font files also within the subfolders.
{: .notice--info }

### Usage

* Set the embroidery file format from which you want to import the letters (ideally choose a file format which is capable to store color information)
* Select the font folder in which the letters are stored. If they are organiszed in subfolders, choose the main folder.
* Choose wether you want to import commands or not (warning: imported commands on a large scale will cause a slow down)
* Click on apply - and wait ...
* After the import move the baseline to the correct place and position the letters accordingly. The left border of the canvas will also influence the positioning of the letters through the lettering tool.
* Save your font as `→.svg` in a new folder within your [custom font directory](#custom-font-directory)
* Run [`Generate JSON`](#generate-json) to make the font available for the lettering tool and save the json file into the same folder as your font. Do not check "AutoRoute Satin" for predigitized fonts and leave scaling to 1.

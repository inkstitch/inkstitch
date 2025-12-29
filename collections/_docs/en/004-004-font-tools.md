---
title: "Font Tools"
permalink: /docs/font-tools/
last_modified_at: 2025-12-29
toc: true
---
A collection of tools suitable for font creators or those who want to add additional fonts to the Ink/Stitch [lettering tool](/docs/lettering).

Read the [Ink/Stitch font creation tutorial](/tutorials/font-creation) for in-depth instrustions.
{: .notice--info }


## Convert SVG Font to Glyph Layers
This extension allows you to convert an svg font into glyph layers, as needed by the lettering tool.

## Custom Font Directory

This extension allows you to define a directory in your file system where you want to store additional fonts to be used with the lettering tool.

Place each font in a subdirectory of your custom font directory. Each font folder should contain at least one font variant and one json file.
Additionally it is recommended to save a license file as well.

**Font variants** used to have to be named  with an arrow, indicating the stitch direction it has been created for (`→.svg`, `←.svg`, etc.).
Now, names should be ltr.svg for left to right direction and rtl.svg for right to left direction.

It is also possible to create a folder named ltr (or rtl) instead and insert multiple font files for this specific direction.

As a minimum requirement, the json file must include the font's name.

## Edit JSON

This extension allows you to edit an existing font information file. If the font doesn't have a json file, create one with [generate JSON](#generate-json)

This extension also update the glyph list. 

### Usage

* Run `Extensions > Ink/Stitch > Font Management > Edit JSON`
* Fine tune your font details such as name, description, license information, keywords and kerning information
* Click on apply

## Font Sampling

This extension creates a list of all letters in a font. It helps font creators to test the outcome of a new font.

It only render unlocked (sensitive) glyphs. This allows for partial sampling while creating the font.

### Usage

* Run `Extensions > Ink/Stitch > Font Management > Font Sampling`
* Pick a font, adjust settings
* Click on apply

### Options

* Font: the one you want to use
* Stitch direction:  default is left to right
* Scale: in percent
* Max line width: line breaks will  be chosen accordingly
* Color sort: whether a multicolor font should be color sorted or not (font needs to set the [color sort index](#set-color-index) values)

## Force lock stitches

Small fonts will sometimes unravel if threads are cut after the embroidery machine has finished the work.

Therefore it is important that also diacritics within a smaller distance to the font body than defined by the minimum jump stitch length (default: 3mm) have lock stitches.

This extension helps adding forced lock stitches. One may chose to restrict the addition of lock stitches only to satin columnns.

### Usage

* Run `Extensions > Ink/Stitch > Font Management > Force lock stitches...`
* Update settings according to the font
* Click on apply

### Options

* Restrict to Satin: add forced lock stitches only to satin columns

* Add forced lock stitches by distance
  * Mininum distance (mm): do not add lock stitches if the distance to the next element is smaller than this
  * Maximum distance (mm): do not add lock stitches if the distance to the next element is larger than this

* Add force lock stitches attribute to the last element of each glyph

* Add force lock stitches attribute to the last element of each group

## Generate JSON

This extension was created to help you to create the json file.
Depending on the way you generated your font file it can include additional kerning information into the json file.
Read [**how to generate a svg font with kerning information**](/tutorials/font-creation).
If you generated your svg file without kerning information this extension can still help you to set up your json file with basic information.

### Font Info

|Option                 |Description
|-----------------------|-------------------------------------
|Name (mandatory)       |The name of your font 
|Description            |Additional information about your font
|Font license          | Type of license  for this ink/stitch font
|Original Font name              |name of the underlying ttf font if any|
|Original Font URL                |url of the underlying font.|
|Font File (mandatory)  |When you have been using FontForge to generate your svg font file, Ink/Stitch will read the kerning information from your font to include it into the json file.<br />Additionally the font file will be used to determine the output path.<br/><br/>A file `font.json` will be saved into the folder of your svg font file.
|Keywords               |Enable the categories that apply to your font

### Font Settings

|Option                 |Description|
|-----------------------|-------------------------------------|
|Default Glyph          |the glyph to be shown if the user requested glyph isn't available in the font file (missing glyph)
|AutoRoute Satin        |▸ Enabled<br/>Ink/Stitch will generate a reasonable [routing for satin columns](/docs/satin-tools/#auto-route-satin-columns) in your font when used in the lettering tool.<br/><br/>▸ Disabled<br/>Ink/Stitch will use the glyphs as is. Disable this option, if you took care for the routing in your font by yourself.
|Reversible             |whether your font can be stitch forwards and backwards or only forwards. Check this only if you do have created font variants.
|Sortable               |whether your font can be color sorted or not. This only works, when the elements in your font carry a [color sort index](#set-color-index)
|Combine indices        |a comma separated list of of color sort indices. Elements with this index will be combined into a single element. Useful to reduce color changes for multi-color stitch types such as tartan.
|Force letter case      |▸ No<br/>Choose this option if your font contains upper and lower case letters (default).<br/><br/>▸ Upper<br/>Choose this option if your font only contains upper case letters.<br/><br/>▸ Lower<br/>Choose this option if your font only contains lower case letters.
|Min Scale / Max Scale  |Define how much your glyphs can be scaled without loosing quality when stitched out


### Kerning

The following fields are optional, they are only necessary, when your svg file doesn't contain kerning information.

If the kerning information cannot be found, these values will be used instead.

|Option                 |Description|
|-----------------------|-------------------------------------|
|Force defined values   |Do not use the font file information, but the values defined below.
|Leading (px)           |Defines the line height of your font. Leave to `0` to let Ink/Stitch read it from your font file (defaults to 100 if the information cannot be found).
|Word spacing (px)      |The width of the "space" character


## Letters to font

"Letters to font" is a tool to convert predigitized embroidery letters into a font for use with the Ink/Stitch lettering tool.

The digitized font needs to meet certain **conditions** to be imported:
* One file for each glyph in an embroidery format that Ink/Stitch can read
* The glyph name needs to be positioned at the end of the file name. A valid file name for the capital A would be e.g. `A.pes` or `Example_Font_A.pes`.

Very often, bought fonts are organized in subfolders, because each letter comes in multiple embroidery file formats. You don't need to change the file structure in this case. Letters to font will search the font files also within the subfolders.
{: .notice--info }

### Usage

* Set the embroidery file format from which you want to import the letters (ideally choose a file format which is capable to store color information)
* Select the font folder in which the letters are stored. If they are organiszed in subfolders, choose the main folder.
* Choose whether you want to import commands or not (warning: imported commands on a large scale will cause a slow down)
* Click on apply - and wait ...
* After the import, move the baseline to the correct place and position the letters accordingly. The left border of the canvas will also influence the positioning of the letters through the lettering tool.
* Save your font as `.svg` in a new folder within your [custom font directory](#custom-font-directory)
* Run [`Generate JSON`](#generate-json) to make the font available for the lettering tool and save the json file into the same folder as your font. Do not check "AutoRoute Satin" for predigitized fonts and leave scaling to 1.
* If necessary, you can adjust the kerning information using the [`Font Management > Edit JSON File`](#edit-json) extension.
* If your font is colored, you can make it sortable using [color sort indices](#set-color-index).

## Organize Glyphs
{% include upcoming_release.html %}

The goal of this extension is to help font digitizers organize their work step by step.

At each step, a group of glyphs is placed at the top of the object stack and the font creator must digitize these glyphs before moving on to the next step.

The steps are organized to divide the work into smaller chunks and maximize the reuse of already digitized letters.

You really need to test what you do at a step because it will be copied for other letters and you want to avoid having to correct the same mistake multiple times:

Use font sampling to generate a file with all unlocked letters
- run trouble shooting and correct all detected errors
- Use simulation to detect unwanted jumps. Best done with the letters enlarged as much as allowed
- Realistic preview can help you find mistakes
- But real stitchouts are the ultimate test
 
### Step 1

The code silently removes unwanted layers (e.g., empty paths, or no paths at all).

At this step, you only need to digitize comma, hyphen and period.

### Step 2

At this step, you need to digitize all the letters that have been grouped into the three groups: Uppercase, Lowercase and Other.

For instannce, you'll find a copy of the period in the i and j glyphs; it's up to you to decide if this is useful to you.

Only sinple letters need to be digitized (no accented letters in these groups).

### Step 3

At this step, you need to digitize numbers, symbols and some punctuation.

You'll find pieces of some glyphs already included, for example, in the ";" you'll find the "." and the "," as digitized in step 1. 

It's up to you to position them correctly or delete them. Also, the "1" contains the "l" and the "I." If they're too different from the "1" to be useful, delete them.

### Step 4

Last part of punctuation : creating the closing punctuation using the opening punctuation.

For instance, You'll find the "(" in the ")." It's up to you to return, position and modify what needs to be modified. 

Normally, at this stage, everything is pre-filled with your already done work.

### Step 5

Apostrophes, Quotation Marks and Single Accents

There are several types of apostrophes and quotation marks depending on the language used.

If you have created at least one, the extension adds the others here.

The same goes for quotation marks. Normally, there's nothing to do for them.

At this step, you must digitize single accents; when possible, they are pre-filled with an equivalent symbol that has already been processed. 

In the worst case, the accent is used by letters in the font, but is absent from the font. In this case, a letter that uses it has been inserted into its layer so that you know what to digitize.

Don't forget to remove the unnecessary parts !

### Step 6

Complex Accents:

In this step, you deal with the other diacritical marks.

These reuse work done at the previous step. 

This complex accents are either double accennts or have same shape as a simple one but a different position . 

The layers are pre-filled, but there is some positioning work to be done, which is why a letter using the accent has sometimes been added to indicate where to position the new accent. 

### Step 7

Letters with a single diacritic:

You will find their layer pre-filled with the letter and the diaccritic; it's up to you to compose them to create the composite letter.

### Step 8

Letters with two or more diacritics..... only if you chosed to include some of them.


You can also use this extension with any font file to
- check for duplicates
- organize the letters by category.

Note: yes, you can leave the letters grouped; it doesn't affect the lettering tool

## Remove Kerning

**⚠ Warning**: Changes made by this tool cannot be reverted. Make sure to save a **copy** of your file before performing these steps.
{: .notice--warning }

Your font is ready to be used. But if you created your font with FontForge it now contains a lot information which isn't necessary for your font to work and could possibly slow it down a little.
Ink/Stitch comes with a tool to clean up your svg font.

1. Make sure you save a **copy** of your font. The additional information may not be necessary for the font to be used, but it can become handy when you want to add additional glyphs.
2. Run `Extensions > Ink/Stitch > Font Tools > Remove Kerning`
3. Choose your font file(s)
4. Click on apply

## Set color index

Sets an index to inform the lettering tool on where to position the selected elements when color sorting is enabled.

* In a font file select elements of the same color
* Open the extension `Extensions > Ink/Stitch > Font Management > Set color index`
* Set the index number
* Apply

The JSON-file must specify if a font is color sortable. Use [Edit JSON](#edit-json) and enable the option `Sortable` in the `Font Settings` tab.
{: .notice--warning }

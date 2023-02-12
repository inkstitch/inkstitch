---
title: "Lettering"
permalink: /docs/lettering/
excerpt: ""
last_modified_at: 2022-12-27
toc: true
---
## Lettering Tool

The lettering tool generates multi-line text as satin columns and dynamically routes stitching, breaking up satins if necessary and adding running stitch.

![Lettering Extensions](/assets/images/docs/lettering.jpg)

### Usage

* Run `Extensions > Ink/Stitch  > Lettering`
* Enter your text (multi-line is possible)
* Adjust font family and scaling.<br>
  **⚠ Warning**: For best results please note the limits for scaling in the font description.
* Click on `Apply and Quit`.
* Position your text within the svg document.

### Options

* **Font size filter**<br>
  Fonts are designed for a special range of sizes. The font size filter helps you to reduce the font list to only the fonts fitting to your target size.
  A active font filter (not 0) will set the correct scale value when you select a font.
  {% include upcoming_release.html %}

* **Stitch lines of text back and forth**<br>
  With this option enabled the first line will be stitched from left to right and the second from right to left, etc.
  This will give your machine shorter ways to travel.

* **Add trims**<br>
  Adds TRIM commands according to the chosen option (Never, after each line, after each word, after each letter).

### Presets

You can save and load your favourite font settings.

## Lettering along path

{% include upcoming_release.html %}

Ink/Stitch letters are carefully designed. If you try to transform them with common tools, they may not work as expected. This means placing letters along a path will be a lot of work. Therefore we've created a tool to assist you with that.

### Usage

* Select a path and a lettering group
* Run `Extensions > Ink/Stitch > Lettering along path ...`
* If `stretch` is enabled, Ink/Stitch will stretch the spaces in between the letters, so that the text will use the entire path.
  Otherwise it will keep the distances from the original text.
* Click on apply

## Font library

An overview of available fonts can be found it the [font library](/fonts/font-library/).

## Color Sorting

When embroidering several letters, you may wish to color sort to avoid many changes  of thread.
When the colors appear in the same order in every letter and when each color is only used on consecutive paths within a letter (this is true for all multicolor Ink/Stitch fonts, with the exception of Infinipicto) this is how to quickly color sort a lettering:

* Pick a letter in the objects panel
* Select the first-to-be-embroidered path of this letter (last one for this letter in the objects panel)
* Edit/Select same/ Same color stroke
* Group, this group will end up in the last to embroider letter
* Move this group to the top of  in its letter

repeat until all the colors are grouped, always starting with selecting the last path of a letter.

## Create new fonts for Ink/Stitch

Read the [font creation tutorial](/tutorials/font-creation/).

Contact us if you are willing to publish your font in the Ink/Stitch lettering tool on [GitHub](https://github.com/inkstitch/inkstitch/issues).

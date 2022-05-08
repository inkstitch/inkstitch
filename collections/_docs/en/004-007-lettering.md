---
title: "Lettering Tool"
permalink: /docs/lettering/
excerpt: ""
last_modified_at: 2021-03-05
toc: true
---
The lettering tool generates multi-line text as satin columns and dynamically routes stitching, breaking up satins if necessary and adding running stitch.

![Lettering Extensions](/assets/images/docs/lettering.jpg)

## Usage

* Run `Extensions > Ink/Stitch  > Lettering`
* Enter your text (multi-line is possible)
* Set font and scaling
* Click on `Apply and Quit`

## Options

* **Stitch lines of text back and forth**<br>
  With this option enabled the first line will be stitched from left to right and the second from right to left, etc.
  This will give your machine shorter ways to travel.

* **Add trims**<br>
  With this option enabled Ink/Stitch will add TRIM-commands for each letter.

## Presets

You can save and load your favourite font settings.

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

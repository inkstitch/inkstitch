---
title: "Thread Color Management"
permalink: /ru/docs/thread-color/
excerpt: ""
last_modified_at: 2021-04-11
toc: true
---
## Import Threadlist

Ink/Stitch can apply a threadlists to an embroidery design. This is especially useful, if you want to work on existing embroidery files which do not support color information (e.g. DST).

It could also be helpful, if you are wanting to test different color settings. You can export and import them as you like. But be careful not to change the amount and order of colors. In case you are planing to change these, you'd prefer to save the entire SVG instead.

### Import

Run `Extensions > Ink/Stitch > Thread Color Management > Import Threadlist ...` to apply a threadlist exported by Ink/Stitch.

If you want to import any other threadlist from a txt-file, choose the option "Import other threadlist" and pick a threadlist from the dropdown menu before clicking on apply.

**Tipp:** Install Add-Ons for Ink/Stitch to have more threadlists available.
{: .notice--info }

### Export

Threadlists can only be exported through a zip-file ([batch export](/docs/import-export/#batch-export)).

## Install Thread Color Palettes for Inkscape

Ink/Stitch comes with a lot of thread manufacturer color palettes which can be installed into Inkscape. This allows to build the designs with the correct colors in mind.
Colors will appear in the PDF-Output and will also be included into your embroidery file, if your file format supports it. 

**Install**
* Go to `Extensions > Ink/Stitch  > Thread Color Management > Install thread color palettes for Inkscape`
* Click `Install`
* Restart Inkscape

**Info**: Just click install if you are not sure where to install the palettes. Ink/Stitch usually discoveres the correct path for your system by itself.
{: .notice--info }

### Usage

Inkscape palettes are found on the bottom to the right of the color swatches.

![Inkscape Color Palettes](/assets/images/docs/palettes-location.png)

Click on the little arrow to open a list of installed palettes and choose the manufacturer color palette depending on the thread you are willing to use.

The choice will also take effect on the thread names to appear in the print preview.

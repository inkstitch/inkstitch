---
title: "Install Addons for Inkscape"
permalink: /fr/docs/install-addons/
last_modified_at: 2025-03-28
toc: true
---
{% include upcoming_release.html %}

Installs color palettes or a symbol library for motif stitches into Inkscape

* `Extensions > Ink/Stitch > Install Addons for Inkscape`
* Select what you want to install (thread color palettes and/or symbol libraries)
* Click `Apply`
* Restart Inkscape

## Thread color palettes

Ink/Stitch comes with many thread manufacturer color palettes which can be installed into Inkscape. This allows to build the designs with the correct colors in mind.
Colors will appear in the PDF-Output and will also be included into your embroidery file, if your file format supports color representations.

[How to work with color palettes](/docs/thread-color/#working-with-palettes)

## Symbol libraries

Symbols are re-usable path elements which can be inserted into a document. They can contain simple paths or whole embroidery designs.

Ink/Stitch delivers a symbol library with motif stitches. They can be used with the path effect `Pattern Along Path` to simply generate patterned running stitches.

### Usage

* Open the symbols dialog `Object > Symbols` (Shift+Ctrl+Y)
* Select the Ink/Stitch motif library (inkstitch-motif-library)
* Click on a motif and drag and drop it onto the canvas

For usage with the a path effect

* Select the symbol and use Ctrl+C to copy it into your clipboard (or use right click > copy)
* Select the path which you want to use the pattern on
* Go to `Path > Path effects...` and select `Pattern Along Path`
* For `pattern source` click on the symbol on the right `Link to path in clipboard`
* Set pattern copies to `Repeated` or `Repeated stretched`
* The original symbol is no longer necessary and can be deleted


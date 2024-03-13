---
title: "New Features, Updates and Fixes for Ink/Stitch after the release of v3.0.1"
permalink: /upcoming/
last_modified_at: 2024-03-11
sidebar:
  nav: pages
toc: true
---
## New Extensions

### [Generate Test Swatches from Selection](/docs/edit/#generate-test-swatches-from-selection)

`Edit > Generate Test Swatches from Selection` ([#2528](https://github.com/inkstitch/inkstitch/issues/2528))

This extension allows to easily test different values for embroidery parameters by creating test swatches.

![Example test swatches](/assets/images/docs/test_swatches.png)

### [Outline](/docs/stroke-tools/#outline)

`Stroke tools > Outline` ([#2529](https://github.com/inkstitch/inkstitch/issues/2529))

This extension helps reconstruct an original object from a stitch file.

![Fill to outline](/assets/images/docs/outline.png)

### Apply Palette

`Thread Color Management > Apply Palette` ([#2738](https://github.com/inkstitch/inkstitch/pull/2738))

This extension applies nearest colors from a specified thread palette on a design. This will also be recognized by the Ink/Stitch pdf output.

### [Element info](/docs/troubleshoot/#element-info)

`Troubleshoot > Element info` ([#2544](https://github.com/inkstitch/inkstitch/issues/2544))

This extension informs about various parameters of selected stitch elements.

![Element info](/assets/images/docs/en/element_info.png)

### [Display Stacking order](/docs/visualize/#display-stacking-order)

`Visualize and Export > Display Stacking order` ([#2656](https://github.com/inkstitch/inkstitch/issues/2656))

![Display stacking order](/assets/images/docs/stacking_order.png)

## Extension Updates

### Cleanup document:

* add option to delete empty groups and layers ([#2552](https://github.com/inkstitch/inkstitch/issues/2552))
* add test run option to display names of the elements that will be removed with the current settings ([#2552](https://github.com/inkstitch/inkstitch/issues/2552))

### Density map

* add indicator size option ([#2544](https://github.com/inkstitch/inkstitch/issues/2544))
* add ignore layer command ([#2522](https://github.com/inkstitch/inkstitch/issues/2522))

### Fill to Stroke

* add one centerline group for each selected fill or replace existing fill if it results in only one path ([#2675](https://github.com/inkstitch/inkstitch/issues/2675#issuecomment-1882919122))

### Force lock stitches (Font Management):

* Add "Restrict to Satin" option ([#2773](https://github.com/inkstitch/inkstitch/pull/2773))

### Jump to Stroke

* Add options ([#2733](https://github.com/inkstitch/inkstitch/pull/2733))
    * Min width
    * Max width
    * Connect only within groups or layers
    * Do not connect after trim, stop or forced lock stitches
    * Merge new strokes with previous/next stroke
    * Merge subpaths ([#2750](https://github.com/inkstitch/inkstitch/pull/2750))

### Lettering

* Add glyph filter ([#2400](https://github.com/inkstitch/inkstitch/issues/2400))

### Preferences

* electron -> wxpython ([#2479](https://github.com/inkstitch/inkstitch/issues/2479))

### Remove embroidery settings

* add option to remove only specific commands ([#2494](https://github.com/inkstitch/inkstitch/issues/2494))

### Select embroidery elements

* Option to select satins with no rungs or two rails and two rungs (possible detection conflict) ([#2734](https://github.com/inkstitch/inkstitch/pull/2734))

### Stitch Plan Preview

* Add option to keep/overwrite previous stitch plan ([#2642](https://github.com/inkstitch/inkstitch/issues/#2642))

### Troubleshoot

* Add warning for satins with two rails and two rungs (possible detection conflict) ([#2734](https://github.com/inkstitch/inkstitch/pull/2734))
* Add warning for elements with stroke and fill color ([#2761](https://github.com/inkstitch/inkstitch/pull/2761))

## Fonts

### New fonts

* Chicken Scratch ([#2703](https://github.com/inkstitch/inkstitch/pull/2703))
* Violin Serif ([#2703](https://github.com/inkstitch/inkstitch/pull/2703))

### Font Updates

* Most fonts have now the following glyphs: éèêëÉÈÊËÜÄÖäöüß
  Only exceptions are April en Fleur, Apex Lake, Cherry fonts, Emilio fonts, Fold Inkstitch, Infinipicto, Namskout and Sortefax (they contain only non diacritic glyphs).
* TT-Directors: add Ũ

All fonts have been reworked to be more stable when transformed.

([#2762](https://github.com/inkstitch/inkstitch/pull/2762))
([#2749](https://github.com/inkstitch/inkstitch/pull/2749))
([#2744](https://github.com/inkstitch/inkstitch/pull/2744))
([#2742](https://github.com/inkstitch/inkstitch/pull/2742))
([#2714](https://github.com/inkstitch/inkstitch/pull/2714))
([#2607](https://github.com/inkstitch/inkstitch/issues/2607))
([#2579](https://github.com/inkstitch/inkstitch/issues/2579))
([#2476](https://github.com/inkstitch/inkstitch/issues/2476))
([#2682](https://github.com/inkstitch/inkstitch/pull/2682))

## Pallets

### New Pallets
* Simthread glow in the dark / 15 colors ([#2752](https://github.com/inkstitch/inkstitch/pull/2752))
* Simthread 63 Brother Colours Polyester ([#2752](https://github.com/inkstitch/inkstitch/pull/2752))

## Params

* Improved error reporting ([#2437](https://github.com/inkstitch/inkstitch/issues/2437))

## Simulator

* Improved simulator for params and lettering ([#2481](https://github.com/inkstitch/inkstitch/issues/2481))
* Simulator is now attached to the main window (params or lettering) ([#2557](https://github.com/inkstitch/inkstitch/issues/2557))

  It is detachable and the last state will be remembered.

## Stitch types

### Fill Stitch - family

* Smooth underpath ([#2346](https://github.com/inkstitch/inkstitch/issues/2346))
* Prevent fill stitch from going outside the shape ([#2346](https://github.com/inkstitch/inkstitch/issues/2346))
* [Linear gradient fill](/docs/stitches/linear-gradient-fill/): a new stitch type to stitch gradients ([#2587](https://github.com/inkstitch/inkstitch/issues/2587))

  ![Linear gradient fill](/assets/images/docs/linear-gradient.jpg)
* Meander fill: add zig-zag option ([#2699](https://github.com/inkstitch/inkstitch/pull/2699))

### Satin column - family

* Add stagger option for split stitches ([#2431](https://github.com/inkstitch/inkstitch/issues/2431))
* Convert line to satin: do not split into several parts ([#2418](https://github.com/inkstitch/inkstitch/issues/2418))
* S-Stitch: a new stitch type for the satin stitch type family `|_|▔|_|▔|_|▔|` ([#2431](https://github.com/inkstitch/inkstitch/issues/2431))
* Zig-Zag: a new stitch type for the satin stitch type family `/\/\/\/\/` ([#2431](https://github.com/inkstitch/inkstitch/issues/2431))

## Export

### Zip-Export

* Add input field for custom file names within the zip file ([#2426](https://github.com/inkstitch/inkstitch/issues/2426))
* Add option to export panel ([#2349](https://github.com/inkstitch/inkstitch/issues/2349))

### Inkscape export dialog

* Ink/Stitch file formats are also available from the Inkscape export dialog ([#2489](https://github.com/inkstitch/inkstitch/issues/2489))

## Install

* Windows is now available as 32 bit and 64 bit version ([#2413](https://github.com/inkstitch/inkstitch/issues/2413))

## Developer Features

* [#2715](https://github.com/inkstitch/inkstitch/issues/2715) Multiversion support
* [#2653](https://github.com/inkstitch/inkstitch/issues/2653) Updated debug and profiling procedures

## Bug Fixes

    
* [#2754](https://github.com/inkstitch/inkstitch/issues/2754)  Fix lettering along path when glyphs have subgroups or trims
* [#2683](https://github.com/inkstitch/inkstitch/issues/2683) Select embroidery elements: output error message when python path cannot be found
* [#2675](https://github.com/inkstitch/inkstitch/issues/2675) Fix error message on fill to stroke if small fill artifacts are present
* [#2674](https://github.com/inkstitch/inkstitch/issues/2674) Zip: fix error message when no file format is selected
* [#2644](https://github.com/inkstitch/inkstitch/issues/2644) Letters to font: escape labels to allow import of filenames with quotes
* [#2657](https://github.com/inkstitch/inkstitch/issues/2657) Troubleshoot satin: point on rail and not the center of the element
* [#2643](https://github.com/inkstitch/inkstitch/issues/2643) Fix some networkx errors for fill stitches
* [#2603](https://github.com/inkstitch/inkstitch/issues/2603) fix polyline shape 
* [#2637](https://github.com/inkstitch/inkstitch/issues/2637) Add shape property to clone
* [#2638](https://github.com/inkstitch/inkstitch/issues/2638) Troubleshoot: remove old layer before creating a new one to avoid transform (and other) issues
* [#2647](https://github.com/inkstitch/inkstitch/issues/2647) Ignore multipoints in intersect regions with gratings
* [#2635](https://github.com/inkstitch/inkstitch/issues/2635) [#2645](https://github.com/inkstitch/inkstitch/issues/2645) Fix some networkx no path errors
* [#2624](https://github.com/inkstitch/inkstitch/issues/2624) Replace jumps by running stitches in large satin columns
* [#2578](https://github.com/inkstitch/inkstitch/issues/2578) Auto-route Satin: handle sided properties correctly
* [#2566](https://github.com/inkstitch/inkstitch/issues/2566) Update depcrecated inx file descriptions, so they are translatable now
* [#2550](https://github.com/inkstitch/inkstitch/issues/2550) Lettering: error on empty layer in font file
* [#2527](https://github.com/inkstitch/inkstitch/issues/2527) Stitch plan: multiply sequence error
* [#2502](https://github.com/inkstitch/inkstitch/issues/2502) Gradient Blocks: Unit fix
* [#2499](https://github.com/inkstitch/inkstitch/issues/2499) LPE Satin: width of "normal" straight pattern wasn't correct
* [#2491](https://github.com/inkstitch/inkstitch/issues/2491) Toggle commands: fix if first command in invisible group/layer
* [#2468](https://github.com/inkstitch/inkstitch/issues/2468) Zigzag to satin: do not ignore elements in a group
* [#2467](https://github.com/inkstitch/inkstitch/issues/2467) Render context-stroke and context-fill as black
* [#2461](https://github.com/inkstitch/inkstitch/issues/2461) Letters to font: fix guide line insertion
* [#2460](https://github.com/inkstitch/inkstitch/issues/2460) Satin Column: obey reversed rails when synthesizing rungs
* [#2458](https://github.com/inkstitch/inkstitch/issues/2458) Density Map: add ignore layer command
* [#2434](https://github.com/inkstitch/inkstitch/issues/2434) Ignore commands with "empty-d-connectors"
* [#2404](https://github.com/inkstitch/inkstitch/issues/2404) Render satins with only one subpath as running stitch
* [#2403](https://github.com/inkstitch/inkstitch/issues/2403) ignore small contour fill with single or double spiral

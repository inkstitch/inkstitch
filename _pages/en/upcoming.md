---
title: "New Features, Updates and Fixes for Ink/Stitch after the release of v3.0.1"
permalink: /upcoming/
last_modified_at: 2024-01-01
sidebar:
  nav: pages
toc: true
---
## Extensions

### New Extensions

  * Display Stacking order ([#2656](https://github.com/inkstitch/inkstitch/issues/2656))
  * Element info ([#2544](https://github.com/inkstitch/inkstitch/issues/2544))
  * Stroke tools: Outline([#2529](https://github.com/inkstitch/inkstitch/issues/2529))
  * Test Swatches ([#2528](https://github.com/inkstitch/inkstitch/issues/2528))

### Extension Updates

  * Density map
    * add indicator size option ([#2544](https://github.com/inkstitch/inkstitch/issues/2544))
    * add ignore layer command ([#2522](https://github.com/inkstitch/inkstitch/issues/2522))
  * Remove embroidery settings
    * add option to remove only specific commands ([#2494](https://github.com/inkstitch/inkstitch/issues/2494))
  * Cleanup document:
    * add option to delete empty groups and layers ([#2552](https://github.com/inkstitch/inkstitch/issues/2552))
    * add test run option to display to be removed element names ([#2552](https://github.com/inkstitch/inkstitch/issues/2552))
  * Preferences
    * electron -> wxpython ([#2479](https://github.com/inkstitch/inkstitch/issues/2479))
  * Stitch Plan Preview
    * Add option to keep/overwrite previous stitch plan ([#2642](https://github.com/inkstitch/inkstitch/issues/#2642))

## Lettering

  * Add glyph filter ([#2400](https://github.com/inkstitch/inkstitch/issues/2400))

## Fonts

### Updates

Most fonts have now the following glyphs: éèêëÉÈÊËÜÄÖäöüß
Only exceptions are April en Fleur, Apex Lake, Cherry fonts, Emilio fonts, Fold Inkstitch, Infinipicto, Namskout and Sortefax (they contain only non diacritic glyphs).

Further updates have been made to:

  * AGS Γαραμου Garamond
  * Apex Simple AGS
  * Dinomouse
  * TT Masters
  * TT Directors

([#2607](https://github.com/inkstitch/inkstitch/issues/2607))
([#2579](https://github.com/inkstitch/inkstitch/issues/2579))
([#2476](https://github.com/inkstitch/inkstitch/issues/2476))
([#2682](https://github.com/inkstitch/inkstitch/pull/2682))

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
  * Linear gradient fill: a new stitch type to stitch gradients ([#2587](https://github.com/inkstitch/inkstitch/issues/2587))

### Satin column - family

  * Add stagger option for split stitches ([#2431](https://github.com/inkstitch/inkstitch/issues/2431))
  * Convert line to satin: do not split into several parts ([#2418](https://github.com/inkstitch/inkstitch/issues/2418))
  * S-Stitch: a new stitch type for the satin stitch type family |_|▔|_|▔|_|▔| ([#2431](https://github.com/inkstitch/inkstitch/issues/2431))
  * Zig-Zag: a new stitch type for the satin stitch type family /\/\/\/\/ ([#2431](https://github.com/inkstitch/inkstitch/issues/2431))

## Export

### Zip-Export

  * Add input field for custom file names within the zip file ([#2426](https://github.com/inkstitch/inkstitch/issues/2426))
  * Add option to export panel ([#2349](https://github.com/inkstitch/inkstitch/issues/2349))

### Inkscape export dialog

  * Ink/Stitch file formats are also available from the Inkscape export dialog ([#2489](https://github.com/inkstitch/inkstitch/issues/2489))

## Install

  * Windows is now available as 32 bit and 64 bit version ([#2413](https://github.com/inkstitch/inkstitch/issues/2413))

## Developer Features

  * [#2653](https://github.com/inkstitch/inkstitch/issues/2653) Updated debug and profiling procedures

## Bug Fixes

 * [#2644](https://github.com/inkstitch/inkstitch/issues/2644) Letters to font: escape labels to allow import of filenames with quotes
 * [#2657](https://github.com/inkstitch/inkstitch/issues/2657) Troubleshoot satin: point on rail and not the center of the element
 * [#2603](https://github.com/inkstitch/inkstitch/issues/2603) fix polyline shape 
 * [#2637](https://github.com/inkstitch/inkstitch/issues/2637) Add shape property to clone
 * [#2638](https://github.com/inkstitch/inkstitch/issues/2638) Troubleshoot: remove old layer before creating a new one to avoid transform (and other) issues
 * [#2647](https://github.com/inkstitch/inkstitch/issues/2647) Ignore multipoints in intersect regions with gratings
 * [#2635](https://github.com/inkstitch/inkstitch/issues/2635) [#2645](https://github.com/inkstitch/inkstitch/issues/2645) Fix some networkx no path errors
 * [#2624](https://github.com/inkstitch/inkstitch/issues/2624) Replace jumps by running stitches in large satin columns
 * [#2578](https://github.com/inkstitch/inkstitch/issues/2578) [#2578](https://github.com/inkstitch/inkstitch/issues/2578)Auto-route Satin: handle sided properties correctly
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
 * [#2404](https://github.com/inkstitch/inkstitch/issues/2404) Render satins with only one subpath as running stitch ([#2553](https://github.com/inkstitch/inkstitch/issues/2553))
 * [#2403](https://github.com/inkstitch/inkstitch/issues/2403) ignore small contour fill with single or double spiral

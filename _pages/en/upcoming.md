---
title: "Changes, Updates and Fixes for Ink/Stitch made after the release of v3.0.1"
permalink: /upcoming/
last_modified_at: 2023-10-29
sidebar:
  nav: pages
toc: true
---
## Extensions
### New Extensions
  * Element info
  * Stroke tools: Outline
  * Test Swatches

### Extension Updates
  * Density map
    * add indicator size option
  * Remove embroidery settings
    * add option to remove only specific commands
  * Cleanup document:
    * add option to delete empty groups and layers
    * add test run option to display to be removed element names
  * Preferences
    * electron -> wxpython

## Lettering
  * Add glyph filter

## Fonts

### Updates
  * AGS Γαραμου Garamond
  * Apex Simple AGS
  * TT Masters

## Params
  * Improved error reporting

## Simulator
  * Improved simulator for params and lettering
  * Simulator is now attached to the main window (params or lettering).
    It is detachable and the last state will be remembered.

## Stitch types

### Fill Stitch
  * Smooth underpath
  * Prevent fill stitch from going outside the shape

### Satin column - family
  * Add stagger option for split stitches
  * Convert line to satin: do not split into several parts
  * S-Stitch: a new stitch type for the satin stitch type family

## Export

### Zip-Export
  * Add input field for custom file names within the zip file
  * Add option to export panel

### Inkscape export dialog
  * Ink/Stitch file formats are also available from the Inkscape export dialog 

## Install
  * Windows is now available as 32 bit and 64 bit version
    add embroidery formats to inkscape export dialog
    remove specific commands only

## Bug Fixes
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
 * [#2404](https://github.com/inkstitch/inkstitch/issues/2404) Render satins with only one subpath as running stitch ([#2553](https://github.com/inkstitch/inkstitch/issues/2553))
 * [#2403](https://github.com/inkstitch/inkstitch/issues/2403) ignore small contour fill with single or double spiral


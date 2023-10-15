---
title: "Changes, Updates and Fixes for Ink/Stitch > v3.0.1"
permalink: /upcoming/
last_modified_at: 2023-10-15
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
  * Remove embroidery settings: add option to remove only specific commands
  * Cleanup document: add options to delete empty groups and layers
  * Preferences: electron -> wxpython

## Lettering
  * Add glyph filter

## Fonts
  * Update TT Masters

## Params
  * Improved simulator
  * Improved error reporting

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
 * #2527 Stitch plan: multiply sequence error
 * #2550 Lettering: error on empty layer in font file
 * #2502 Gradient Blocks: Unit fix
 * #2491 Toggle commands: fix if first command in invisible group/layer
 * #2499 LPE Satin: width of "normal" straight pattern wasn't correct
 * #2458 Density Map: add ignore layer command
 * #2460 Satin Column: obey reversed rails when synthesizing rungs
 * #2468 Zigzag to satin: do not ignore elements in a group
 * #2467 Render context-stroke and context-fill as black
 * #2461 Letters to font: fix guide line insertion
 * #2434 Ignore commands with "empty-d-connectors"
 * #2403 ignore small contour fill with single or double spiral
 * #2404 Render satins with only one subpath as running stitch

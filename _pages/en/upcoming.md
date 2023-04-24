---
title: "Changes, Updates and Fixes for the Upcoming Release"
permalink: /upcoming/
last_modified_at: 2023-02-14
sidebar:
  nav: pages
toc: true
---
This page lists **changes made after the latest release**. Latest release: Ink/Stitch v2.2.0

## General

We have good news: Ink/Stitch will be significantly faster due to stitch plan caching.

## Fonts

* [Abril En Fleur AGS](/fonts/abril/)
* [Apex Simple AGS](/fonts/apex-lake/)
* [AGS Γαραμου](/fonts/AGS_greek_garamond/)
* [Emilio 20 simple](/fonts/emilio-20/)
* [Emilio 20 bold](/fonts/emilio-20/)
* [Emilio 20 Applique](/fonts/emilio-20/)

* The font `Grand Hotel` has been renamed to `Auberge`

* Other fonts have been improved

## Element/Stitch types

### New Stitch Types

#### Meander Fill

[Meander fill](/docs/stitches/meander-fill) has its origins in quilting techniques. A beautiful patterned effect results for machine embroidery. Large areas can be filled with relatively few stitches.

#### Circular Fill

[Circular fill](/docs/stitches/circular-fill) fills a shape with an embroidered spiral. The center of the spiral is positioned at the center of the shape. A target point can be used to define a custom spiral center.

### New params

#### Trim and Stop Commands
  * It's not necessary to use symbols for trim and stop commands, they can also be applied through the params dialog
  * [Scale Commands](/docs/commands/#scale-command-symbols): scales marker symbols as well (guide line & pattern symbols)

#### Tack Stitch and Lock Stitch
  * Chose from a list of predefined tack/lock stitches
  * Scale tack/lock stitches
  * Define custom tack/lock stitches

### Clones
  * Fix: automatic fill angle calculation
  * Fix: positioning

### Bean Stitch
  * Add support for [custom repeat patterns](/docs/stitches/bean-stitch/#params) (1 0: ☰-☰-☰-)

### Manual Stitch
  * Enable automated lock stitches through the force lock stitch option
  * Add max stitch length setting

### Fill stitch
  * Add support for [fractional-length stagger cycles in fills](/docs/stitches/fill-stitch/#params)
  * [Multiple underlay angle values](/docs/stitches/fill-stitch/#underlay) are now separated by space, not by a comma anymore
  
    **Please update your svgs if you used multiple fill underlays**
    {: .notice--warning }

  * Fix: 'LineString' object has no attribute 'geoms'
  * Fix: 'Point' object has no attribute 'geoms'
  * Fix: ZeroDivisionError in intersect_region_with_grating
  * Fix: ZoneClose segments can not be changed into curves.
  * Fix: incorrect stagger in guided fill

### Satin Column
  * [Options for randomization](/docs/stitches/satin-column/#satin-top-layer)
      * Stitch length
      * Stitch distance
      * Length/count of split stitches
  * [Pull compensation](/docs/stitches/satin-column/#satin-top-layer)

    Insert multiple values separated by a space.
    Possible for both pull compensations (mm, %)

      * Add suport for pull compensation in percent
      * Add support for asymmetric pull compensation.

  * Add option to [swap rails]((/docs/stitches/satin-column/#satin-top-layer)) quickly directly from the params dialog

  * Fix: don't fail if a satin has a fill, but render the fill as well

### Stroke
  * Improved running stitch algorithm (stitch length is more consistant)
  * Zig-zag: Add warning to the troubleshoot extension to inform about dashed lines if the zig zag is small
  * `svg:line` elements are recognized as normal stroke elements now

## Extensions

### New extensions
  * Extensions > Ink/Stitch > Tools: Fill > [Convert to gradient blocks](/docs/fill-tools/#convert-to-gradient-blocks)

    Splits a shape with a gradient fill color into solid color blocks which can be used to stitch out a gradient
  * Extensions > Ink/Stitch > [Lettering along path](/docs/lettering/#lettering-along-path)

    Places a lettering group along a path without deforming the glyphs
  * Extensions > Ink/Stitch > Tools: Stroke > [Jump to Stroke](/docs/stroke-tools/#jump-to-stroke)

    Generates a running stitch line from end to start position of consecutive elements
  * Extensions > Ink/Stitch > Tools: Stroke > [Fill to Stroke](/docs/stroke-tools/#fill-to-stroke)

    Generates a center line for fill objects

  * Extensions > Ink/Stitch > Tools: Satin: [Stroke to Live Path Effect Satin](/docs/satin-tools/#stroke-to-live-path-effect-satin)

    Converts a Stroke type element into a live path effect satin

  * Extensions > Ink/Stitch > Tools: Satin > [Zigzag line to Satin](/docs/satin-tools/#zigzag-line-to-satin)

    Converts a square or zigzag line into a satin column

### Autorun
  * Fix: Keep settings for underpath running stitch tolerance

### Convert to Satin
  * Fix: Do not fail on mixed element selection
  * Fix macOS: rails point into the same direction again

### Cutwork
  * Add needle info to .inf files so that [Bernina/Bernette machines can display correct needle numbers](/docs/cutwork/#cutwork-with-berninabernette)
  * Fix: Don't fail if the shape has only a fill

### Lettering
  * Add font [size filter](/docs/lettering/#options)
  * Add various [options to include trim commands](/docs/lettering/#options) on all fonts (not only auto routed satin fonts)
  * Allow font folders with multiple files. In this case the font folders are named with the arrows.
    This allows font authors to split up their font file and speed up documents with a lot of elements in them.
    Also it allows them to work at the same font at the same time and exchange only parts of the font.

  * Fix: don't fail on invalid glyphs, but ignore them
  * Fix: don't fail but ignore auto-route if font author defined it for a fill font (just in case the author didn't finish to convert all glyphs but wants to test the new font).

### Params Simulator
  * Simulator reloads faster when params have been changed
  * Doesn't ignore the minimum stitch length anymore

### Preferences
  * It is now possible to set default values for the minimum stitch length and the minimum jump stitch length
  * Define cache size

### Print PDF
  * New view: full page pattern
  * Preselect PDF format in save dialog

### Simulator
  * Uses page background color from Inkscape

### Stitch Plan
  * Add [option to lock stitch plan](/docs/visualize/#stitch-plan-preview) (make it insensitve for mouse interactions)

### Troubleshoot
  * Add size options

## Embroidery Formats
  * Add file name to header of some file formats
  * Fix an issue when stop commands resulted into a mismatch between colors and color blocks

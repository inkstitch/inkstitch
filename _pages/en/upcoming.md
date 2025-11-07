---
title: "New Features, Updates and Fixes for the upcoming Ink/Stitch version"
permalink: /upcoming/
last_modified_at: 2025-10-13
sidebar:
  nav: pages
toc: true
---
Ink/Stitch is in constant development. Here you can see all the changes made after the last official release.

## [Fonts](/fonts/font-library)

### New Fonts

* [Allegria 20](/fonts/allegria/)

  ![Allegria 20](/assets/images/fonts/allegria20.png)
* [Allegria 55](/fonts/allegria/)

  ![Allegria 55](/assets/images/fonts/allegria55.png)
* [Apex simple small AGS](/fonts/apex/)

  ![Apex simple small](/assets/images/fonts/apex_simple_small_AGS.png)
* [Braille](/fonts/braille/)

  ![Braille](/assets/images/fonts/braille.png)
* [Circular 3 letters monogram](/fonts/circular-3letters-monogram/)

  ![Circular 3 letters monogram](/assets/images/fonts/circular_3letters_monogram.png)
* [Cyrillic](/fonts/cyrillic/)

  ![Cyrillic](/assets/images/fonts/cyrillic.png)
* [Neon](/fonts/neon/)

  ![Neon](/assets/images/fonts/neon.png)
* [Neon blinking](/fonts/neon/)

  ![Neon blinking](/assets/images/fonts/neon_blinking.png)
* [Venezia](/fonts/venezia/)

  ![Venezia](/assets/images/fonts/venezia.png)
* [Venezia small](/fonts/venezia/)

  ![Venezia](/assets/images/fonts/venezia_small.png)

### Font updates

Numerous updates to existing fonts were made. Thanks to everyone involved!

## Stitch Type Related Updates

### Satin columns

Simple strokes can be used as satin columns directly [#3874](https://github.com/inkstitch/inkstitch/pull/3874).
* the width of the stroke must be greater than 0.3mm
* the position of the nodes can influence how the satin will be rendered:

  ![Stroke to satin. Same path with different node setups](/assets/images/upcoming/3.3.0/stroke-to-satin-nodes.png)

Short stitch inset can now take more than one value separated by a space.
When multiple values are set, the satin column will use these to level consecutive short stitches [#3987](https://github.com/inkstitch/inkstitch/pull/#3987).

## New extensions

### Organize Glyphs

`Font Management > Organize Glyphs` [#3870](https://github.com/inkstitch/inkstitch/pull/3870)

Helps font digitizers to organize their work in steps so that they can reuse previously digitized letters

[Read more](/docs/font-tools/#organize-glyphs)

## Updated Extensions

### Convert svg font to glyph layers

* Add option for font sizing [#3799](https://github.com/inkstitch/inkstitch/pull/3799)
* Remove option to stop after a specific amount of imported glyphs [#3937](https://github.com/inkstitch/inkstitch/pull/3937)
* Do not convert to layer a glyph that does not render (Z category unicode)
* Try to decypher glyph names from private unicode area [#3883](https://github.com/inkstitch/inkstitch/pull/3883)

[Read more](/docs/font-tools/#convert-svg-font-to-glyph-layers)

### Edit JSON

* Allow a value of `0` for `horiz_adv_x_default` (Use the width of the individual glyphs) [#3965](https://github.com/inkstitch/inkstitch/pull/3965)

### Element Info

* Add option to copy the list to the clipboard (accessable from the help tab) [#3817](https://github.com/inkstitch/inkstitch/pull/3817)

### Font sampling

* only render unlocked (sensitive) glyphs. This allows for partial sampling while creating the font [#3870](https://github.com/inkstitch/inkstitch/pull/3870)
* Save and reload scale settings [#3870](https://github.com/inkstitch/inkstitch/pull/3870)

### Force lock stitches

* add option to include forced lock stitches on the last element of each selected group [#3875](https://github.com/inkstitch/inkstitch/pull/3875)

### Preferences

* add "rotate on export" file setting [#3840](https://github.com/inkstitch/inkstitch/pull/3840)

## Bugfixes

* Fill to satin: do not error out when one of multiple selected fills has no matching rung [#3966](https://github.com/inkstitch/inkstitch/pull/3966)
* Satin: rely more on path length for invalid satins [#3963](https://github.com/inkstitch/inkstitch/pull/3963)
* Stroke: filter invalid paths in clipped path [#3989](https://github.com/inkstitch/inkstitch/pull/3989)
* Meander: fix clamp [#3945](https://github.com/inkstitch/inkstitch/pull/3945)
* Stroke to satin: ensure a good starting point for closed paths [#3944](https://github.com/inkstitch/inkstitch/pull/3944)
* Fill: tag last stitch in a row correctly [#3940](https://github.com/inkstitch/inkstitch/pull/3940)
* Color fixes [#3936](https://github.com/inkstitch/inkstitch/pull/3936)
* Satin: fix crash with tiny satin [#3934](https://github.com/inkstitch/inkstitch/pull/3934)
* Preset-related fixes [#3931](https://github.com/inkstitch/inkstitch/pull/3931)
* Stroke: do not overwrite stroke params with satin column values [#3927](https://github.com/inkstitch/inkstitch/pull/3927)
* Satin: skip contour underlay if there are no pairs [#3912](https://github.com/inkstitch/inkstitch/pull/3912)
* Presets: prevent that "add" overwrites existing presets [#3896](https://github.com/inkstitch/inkstitch/pull/3896)
* Satin: fix first_stitch for invalid paths [#3882](https://github.com/inkstitch/inkstitch/pull/3882)
* Satin: fix empty rail issue [#3863](https://github.com/inkstitch/inkstitch/pull/3863)
* Zigzag to Satin: fix zerodivision error [#3858](https://github.com/inkstitch/inkstitch/pull/3858)
* Switch from NFKC to NFC normalization form in the lettering tool [#3828](https://github.com/inkstitch/inkstitch/pull/3828)
* Set trims=True for pyembroidery.write [#3821](https://github.com/inkstitch/inkstitch/pull/3821)
* Fix issue with bad color names [#3816](https://github.com/inkstitch/inkstitch/pull/3816)
* Fix simulator drawing panel attribute error when no stitch is loaded [#3815](https://github.com/inkstitch/inkstitch/pull/3815)

## Builds, tests, workflows, code quality and house keeping

* README: add contact information (forum, chat) [#3979](https://github.com/inkstitch/inkstitch/pull/3979)
* removed shapely rebuild from macos builds [#3960](https://github.com/inkstitch/inkstitch/pull/3960)
* Rename pyembroidery to pystitch [#3889](https://github.com/inkstitch/inkstitch/pull/3830)
* Fix(test): fix output tests being fluky [#3859](https://github.com/inkstitch/inkstitch/pull/3859) 
* Fix type errors [#3928](https://github.com/inkstitch/inkstitch/pull/3928)
* Ci: add workflow to run tests on pull requests and pushes [#3830](https://github.com/inkstitch/inkstitch/pull/3830)
* Fix package build with Nix package manager [#3826](https://github.com/inkstitch/inkstitch/pull/3826)


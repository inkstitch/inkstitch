---
title: "New Features, Updates and Fixes for the upcoming Ink/Stitch version"
permalink: /upcoming/
last_modified_at: 2025-06-07
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

Simple strokes an be used as satin columns directly (when the stroke with is greater than 0.3mm) [#3874](https://github.com/inkstitch/inkstitch/pull/3874)

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

* fix meander clamp [#3944](https://github.com/inkstitch/inkstitch/pull/3945)
* stroke to satin: ensure a good starting point for closed paths [#3944](https://github.com/inkstitch/inkstitch/pull/3944)
* preset-related fixes [#3931](https://github.com/inkstitch/inkstitch/pull/3931)
* Color fixes [#3936](https://github.com/inkstitch/inkstitch/pull/3936)
* Fill: tag last stitch in a row correctly [#3940](https://github.com/inkstitch/inkstitch/pull/3940)
* Stroke: do not overwrite stroke params with satin column values [#3927](https://github.com/inkstitch/inkstitch/pull/3927)
* Satin: skip contour underlay if there are no pairs [#3912](https://github.com/inkstitch/inkstitch/pull/3912)
* Presets: prevent that "add" overwrites existing presets [#3896](https://github.com/inkstitch/inkstitch/pull/3896)
* Zigzag to Satin: fix zerodivision error [#3858](https://github.com/inkstitch/inkstitch/pull/3858)
* Satin: fix empty rail issue [#3863](https://github.com/inkstitch/inkstitch/pull/3863)
* Fix issue with bad color names [#3816](https://github.com/inkstitch/inkstitch/pull/3816)
* Fix simulator drawing panel attribute error when no stitch is loaded [#3815](https://github.com/inkstitch/inkstitch/pull/3815)
* switch from NFKC to NFC normalization form in the lettering tool [#3828](https://github.com/inkstitch/inkstitch/pull/3828)
* set trims=True for pyembroidery.write [#3821](https://github.com/inkstitch/inkstitch/pull/3821)

## Builds, tests, workflows and code quality

* Satin: fix crash with tiny satin [#3934](https://github.com/inkstitch/inkstitch/pull/3934)
* fix type errors [#3928](https://github.com/inkstitch/inkstitch/pull/3928)
* rename pyembroidery to pystitch [#3889](https://github.com/inkstitch/inkstitch/pull/3830)
* ci: add workflow to run tests on pull requests and pushes [#3830](https://github.com/inkstitch/inkstitch/pull/3830)
* Fix package build with Nix package manager [#3826](https://github.com/inkstitch/inkstitch/pull/3826)


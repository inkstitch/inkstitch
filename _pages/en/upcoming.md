---
title: "New Features, Updates and Fixes for the upcoming Ink/Stitch version"
permalink: /upcoming/
last_modified_at: 2026-01-02
sidebar:
  nav: pages
toc: true
---
Ink/Stitch is in constant development. Here you can see all the changes made after the last official release.

## [Fonts](/fonts/font-library)

### New Fonts

* [Alchemy](/fonts/alchemy/)

  ![Alchemy](/assets/images/fonts/alchemy.jpg)

* [Allegria 20](/fonts/allegria/)

  ![Allegria 20](/assets/images/fonts/allegria20.png)
* [Allegria 55](/fonts/allegria/)

  ![Allegria 55](/assets/images/fonts/allegria55.png)
* [Apex simple small AGS](/fonts/apex/)

  ![Apex simple small](/assets/images/fonts/apex_simple_small_AGS.png)
* [Apesplit](/fonts/apespit/)

  ![Apesplit](/assets/images/fonts/apesplit.jpg)
* [Barstitch crosses](/fonts/barstitch_bold/)

  ![Barstitch  crosses](/assets/images/fonts/barstitch_crosses.jpg)
 
* [Braille](/fonts/braille/)

  ![Braille](/assets/images/fonts/braille.png)
* [Circular 3 letters monogram](/fonts/circular-3letters-monogram/)

  ![Circular 3 letters monogram](/assets/images/fonts/circular_3letters_monogram.png)
* [Cyrillic](/fonts/cyrillic/)

  ![Cyrillic](/assets/images/fonts/cyrillic.png)
* [Handkerchief](/fonts/handkerchief/)

  ![Handkerchief](/assets/images/fonts/handkerchief.png)
* [Jacquard 12](/fonts/jacquard_12/)

  ![Jacquard 12](/assets/images/fonts/jacquard12.png)
* [Jersey 15](/fonts/jersey_15/)

  ![Jersey 15](/assets/images/fonts/jersey15.png)
* [Ladies's present](/fonts/ladies_present/)

  ![Ladies's present](/assets/images/fonts/ladies_present.png)
* [Magic Crosses](/fonts/magic_crosses/)

  ![Magic Crosses](/assets/images/fonts/magic_crosses.png)

* [Montecarlo](/fonts/montecarlo/)

  ![Montecarlo](/assets/images/fonts/montecarlo.png)
* [Nautical](/fonts/nautical/)

  ![Nautical](/assets/images/fonts/nautical.png)
* [Neon](/fonts/neon/)

  ![Neon](/assets/images/fonts/neon.png)
* [Neon blinking](/fonts/neon/)

  ![Neon blinking](/assets/images/fonts/neon_blinking.png)
* [Precious](/fonts/precious/)

  ![Precious](/assets/images/fonts/precious.jpg)
* [Priscilla](/fonts/priscillaa/)

  ![Priscilla](/assets/images/fonts/priscilla.png)
* [Venezia](/fonts/venezia/)

  ![Venezia](/assets/images/fonts/venezia.png)
* [Venezia small](/fonts/venezia/)

  ![Venezia](/assets/images/fonts/venezia_small.png)

### Font updates

Numerous updates to existing fonts were made. Thanks to everyone involved!

## Translations

A big thank you to all translators. We've received new translations into:

* Czech
* Dutch
* French
* German
* Greek
* Hungarian
* Portuguese, Brazilian
* Spanish

[How to translate Ink/Stitch](/developers/localize/)

## New Stitch Types

### Cross Stitch

![Cross stitch frog](/assets/images/upcoming/3.3.0/cross_stitch.jpg){: width="600px" }

[Read more about cross stitch](/docs/stitches/cross-stitch)

## Stitch Type Related Updates

### Legacy Fill

#### Expand shape

* Add expand parameter option [#3988](https://github.com/inkstitch/inkstitch/pull/3988)

  ![Expand](/assets/images/docs/params-fill-expand.png)

[Read more about legacy fill](/docs/stitches/fill-stitch/#legacy-fill)

### Ripple Stitch

#### Adaptive width

* Improved rendering for the adaptive width option [#4079](https://github.com/inkstitch/inkstitch/pull/4079)

  ![Varying width](/assets/images/docs/ripple_adaptive_distance.jpg){: width="600px"}

#### Clipping

* Ripple stitches render as clipped [#4082](https://github.com/inkstitch/inkstitch/pull/4082)

  ![Clipped ripple](/assets/images/docs/ripple_clipped.jpg){: width="600px"}

#### Swap and reverse satin guide rails

* Add swap rail and reverse rail parameter options for satin guides [#4083](https://github.com/inkstitch/inkstitch/pull/4083)

  This will affect pattern and/or stitch direction.

  ![Swap and reverse rails](/assets/images/docs/ripple_swap_reverse_rails.jpg){: width="600px"}

[Read more about ripple stitches](/docs/stitches/ripple-stitch/)

### Running Stitch

#### Stitch length sequence

* Allow a space separated sequence as an input value for the stitch length [#4034](https://github.com/inkstitch/inkstitch/pull/4034).
  This sequence can also be applied to ripple stitches.

  ![Running stitch sequence](/assets/images/docs/running_stitch_length_sequence.jpg)

  _Image above: ripple stitch with a stitch length value of `1 1 5`_


[Read more about running stitches](/docs/stitches/running-stitch/)

### Satin columns

#### Stroke to satin conversion under the hood

Simple strokes can be used as satin columns directly [#3874](https://github.com/inkstitch/inkstitch/pull/3874).
* the width of the stroke must be greater than 0.3mm
* the position of the nodes can influence how the satin will be rendered:

  ![Stroke to satin. Same path with different node setups](/assets/images/upcoming/3.3.0/stroke-to-satin-nodes.png){: width="600px"}

#### Short stitch inset levels

Short stitch inset can now take more than one value separated by a space.
When multiple values are set, the satin column will use these to level consecutive short stitches [#3987](https://github.com/inkstitch/inkstitch/pull/3987).

  ![Satin with two short stitch inset levels](/assets/images/docs/satin_multiple_short_stitch_inset_values.jpg){: width="600px"}

[Read more about satin columns](/docs/stitches/satin-column/)

### Zigzag Stitch (Stroke)

* Add bean stitch parameter option [#4127](https://github.com/inkstitch/inkstitch/pull/4127)

## New extensions

### Apply attribute

`Edit > Apply attribute` [#3983](https://github.com/inkstitch/inkstitch/pull/3983)

An extension for experienced users. Applies a given attribute to all selected elements.

![Apply attribute gui](/assets/images/upcoming/3.3.0/apply_attribute.jpg)

[Read more](/docs/edit/#apply-attributes)

### Organize Glyphs

`Font Management > Organize Glyphs` [#3870](https://github.com/inkstitch/inkstitch/pull/3870)

Helps font digitizers to organize their work in steps so that they can reuse previously digitized letters

[Read more](/docs/font-tools/#organize-glyphs)

### Cross Stitch Helper

This extension helps to generate cross stitches in Ink/Stitch. It can:

* Calculate stitch length for given grid spacing values
* Apply cross stitch parameters to selected fill elements.
* Pixelize outlines of selected fill elements.
* Apply spacing values to page grid.

[Read more](/docs/fill-tools/#cross-stitch-helper)

## Updated Extensions

### Cut Satin

A tool to cut satins at specified spots.

* It is now possible to cut a satin at multiple positions at once. [#4015](https://github.com/inkstitch/inkstitch/pull/4015)

[Read more](/docs/satin-tools/#cut-satin-column)

### Break apart fill objects

A tool to repair and split up simple or complex (self overlapping) fill shapes.

* Add threshold option [##4110](https://github.com/inkstitch/inkstitch/pull/#4110)

  Break apart fill objects will remove elements and holes which are smaller than this value.

### Element Info

A tool to gather embroidery information.

* Add option to copy the list to the clipboard (accessible from the help tab) [#3817](https://github.com/inkstitch/inkstitch/pull/3817)

[Read more](/docs/troubleshoot/#element-info)

### Font Management

#### Font file naming conventions

Previously, font file names declared with arrows the stitch directions. This was troublesome on some operating systems when inkstitch was installed.

Now font files can be named ltr.svg, rtl.svg, ttb.svg, btt.svg to define the font variants [#4087](https://github.com/inkstitch/inkstitch/pull/4087)

#### Convert svg font to glyph layers

This is an extension for embroidery font digitizers.

* Add option for font sizing [#3799](https://github.com/inkstitch/inkstitch/pull/3799)
* Remove option to stop after a specific amount of imported glyphs [#3937](https://github.com/inkstitch/inkstitch/pull/3937)
* Ignore glyphs from Z category unicode, as they do not render
* Try to decypher glyph names from private unicode area [#3883](https://github.com/inkstitch/inkstitch/pull/3883)

[Read more](/docs/font-tools/#convert-svg-font-to-glyph-layers)

#### Edit JSON

A tool for font digitizers. It let's font authors edit font and kerning information.

* It is now possible to set `0` as a value for `horiz_adv_x_default`. This is make Ink/Stitch use the width of the individual glyphs  [#3965](https://github.com/inkstitch/inkstitch/pull/3965)
* New input fields for: original font, original font url and the font license [#4103](https://github.com/inkstitch/inkstitch/pull/4103)

[Read more](/docs/font-tools/#edit-json)

#### Generate JSON

A tool for font digitizers for the initial creation of the JSON file. The JSON file includes all information about the font.

* New input fields for: original font, original font url and the font license [#4103](https://github.com/inkstitch/inkstitch/pull/4103)

[Read more](/docs/font-tools/#generate-json)

#### Font sampling

A tool for font digitizers to validate the font output.

* only render unlocked (sensitive) glyphs. This allows for partial sampling while creating the font [#3870](https://github.com/inkstitch/inkstitch/pull/3870)
* Save and reload scale settings [#3870](https://github.com/inkstitch/inkstitch/pull/3870)

[Read more](/docs/font-tools/#font-sampling)

#### Force lock stitches

A tool for font authors to automatically set the force lock stitch option when an element meets a specified criterion.

* add option to apply forced lock stitches on the last element of each selected group [#3875](https://github.com/inkstitch/inkstitch/pull/3875)

[Read more](/docs/font-tools/#force-lock-stitches)

### Jump Stitch to Trim/Stop command

Converts jumps to trim commands.

* Add option to convert to either a trim or stop command [#4038](https://github.com/inkstitch/inkstitch/pull/4038)

[Read more](/docs/commands/#jump-stitch-to-trim-command)

### Knockdown Fill

Adds a fill underneath selected objects.

* Add stitch length option [#4084](https://github.com/inkstitch/inkstitch/pull/4084)

  Row spacing will adapt accordingly to line up with the stitches.

[Read more](/docs/fill-tools/#knockdown-fill)

### Lettering

Text module to use pre-digitized fonts.

* Add spacing options [#4020](https://github.com/inkstitch/inkstitch/pull/4020)

  ![Image showing the spacing options: letter spacing, word spacing and line height](/assets/images/upcoming/3.3.0/letter_spacing_gui.jpg)

  ![Draw freely written twice, one is normal, the other with adapted letter and word spacing](/assets/images/upcoming/3.3.0/letter_spacing.jpg){: width="600px" }

[Read more](/docs/lettering/)

### Preferences

Defines global settings or settings for the currently open SVG document.

* Add `rotate on export` setting (affects single svg file only) [#3840](https://github.com/inkstitch/inkstitch/pull/3840)

[Read more](/docs/preferences/)

### Troubleshoot Objects

Points to troublesome (or potentially troublesome) spots in the design.

* add display options (errors, warnings, type warnings) [#3969](https://github.com/inkstitch/inkstitch/pull/3969)

[Read more](/docs/troubleshoot/#troubleshoot-objects)

## New Color Palettes

* Magnifico thread palette [#4022](https://github.com/inkstitch/inkstitch/pull/4022)
* Threadart thread palette [#4022](https://github.com/inkstitch/inkstitch/pull/4022)

[Read more about color palettes](/docs/thread-color/#install-palettes)

## Bugfixes

* Fix issue with rgba thread color definitions [#4126](https://github.com/inkstitch/inkstitch/pull/4126)
* Do not save empty embroidery files [#4125](https://github.com/inkstitch/inkstitch/pull/4125)
* Remove embroidery settings: command param along with commands for trim and stop [#4074](https://github.com/inkstitch/inkstitch/pull/4074)
* Fill to satin: process rungs within the fill shape better [#4025](https://github.com/inkstitch/inkstitch/pull/4025)
* fill to satin: fix stroke width [#4005](https://github.com/inkstitch/inkstitch/pull/4005)
* redwork: delete empty groups [#4014](https://github.com/inkstitch/inkstitch/pull/4014)
* empty-d-object: define a default color (black) [#4018](https://github.com/inkstitch/inkstitch/pull/4018)
* jump to stroke: add path label [#4011](https://github.com/inkstitch/inkstitch/pull/4011)
* params: prevent settings error [#4004](https://github.com/inkstitch/inkstitch/pull/4004)
* satin: do no error on one point zigzag underlay segment [#3996](https://github.com/inkstitch/inkstitch/pull/3996)
* fix remove kerning [#3995](https://github.com/inkstitch/inkstitch/pull/3995)
* fix redwork stroke width [#3964](https://github.com/inkstitch/inkstitch/pull/3964)
* Fix transform issues in lettering along path [#3972](https://github.com/inkstitch/inkstitch/pull/3972)
* Gradient color: fix cache key error [#3966](https://github.com/inkstitch/inkstitch/pull/4007)
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

* Move fonts to submodule [#4061](https://github.com/inkstitch/inkstitch/pull/4061)
* debugger vscode adaption [#3981](https://github.com/inkstitch/inkstitch/pull/3981)
* README: add contact information (forum, chat) [#3979](https://github.com/inkstitch/inkstitch/pull/3979)
* removed shapely rebuild from macos builds [#3960](https://github.com/inkstitch/inkstitch/pull/3960)
* Rename pyembroidery to pystitch [#3889](https://github.com/inkstitch/inkstitch/pull/3830)
* Fix(test): fix output tests being fluky [#3859](https://github.com/inkstitch/inkstitch/pull/3859) 
* Fix type errors [#3928](https://github.com/inkstitch/inkstitch/pull/3928)
* Ci: add workflow to run tests on pull requests and pushes [#3830](https://github.com/inkstitch/inkstitch/pull/3830)
* Fix package build with Nix package manager [#3826](https://github.com/inkstitch/inkstitch/pull/3826)


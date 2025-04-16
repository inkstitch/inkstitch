---
title: "New Features, Updates and Fixes for the upcoming Ink/Stitch version"
permalink: /upcoming/
last_modified_at: 2025-04-15
sidebar:
  nav: pages
toc: true
---
Ink/Stitch is in constant development. Here you can see all the changes made after the last official release.

## [Fonts](/fonts/font-library)

### New Fonts

* [Ambigüe](/fonts/ambigue/)

  ![Ambigüe](/assets/images/fonts/ambigue.png)
* [Barstitch bold](/fonts/barstitch_bold/)

  ![Barstitch bold](/assets/images/fonts/barstitch_bold.png)
* [Barstitch cloudy](/fonts/barstitch_bold/)

  ![Barstitch cloudy](/assets/images/fonts/barstitch_cloudy.png)
* [Barstitch mandala](/fonts/barstitch/bold/)

  ![Barstitch mandala](/assets/images/fonts/barstitch_mandala.png)
* [Barstitch regular](/fonts/barstitch_bold)

  ![Barstitch regular](/assets/images/fonts/barstitch_regular.png)
* [Barstitch textured](/fonts/barstitch_bold/)

  ![Barstitch textured](/assets/images/fonts/barstitch_textured.png)
* [Califragilistic](/fonts/califragilistic/)

  ![Califragilistic](/assets/images/fonts/califragilistic.png)
* [Cogs_KOR](/fonts/cogs_KOR)

  ![Cogs_KOR](/assets/images/fonts/cogs_KOR.png)
* [Computer](/fonts/computer/)

  ![Copmuter](/assets/images/fonts/computer.png)
* [Decadent Flower Monogram](/fonts/decadent_flowers_monogram/)

  ![Decadent flower monogram](/assets/images/fonts/decadent_flowers_monogram.png)
* [גופן בינוני](/fonts/hebrew_font/)

  ![גופן בינוני](/assets/images/fonts/hebrew_font_medium.png)
  ![גופן בינוני](/assets/images/fonts/hebrew_font_large.png)
* [פשוט מעוגל](/fonts/hebrew_font/)

  ![פשוט מעוגל](/assets/images/fonts/hebrew_simple_rounded.png)
* [Ink/Stitch Masego](/fonts/inkstitch-masego/)

  ![Ink/Stitch Masego](/assets/images/fonts/inkstitch_masego.png)
* [Magnolia tamed](/fonts/magnolia-script/)

  ![Magnolia tamed preview](/assets/images/fonts/magnolia_tamed.png)
* [Malika](/fonts/malika/)

  ![Malika](/assets/images/fonts/malika.png)
* [Mimosa](/fonts/mimosa/)

  ![Mimosa medium](/assets/images/fonts/mimosa_medium.png)

  ![Mimosa large](/assets/images/fonts/mimosa_large.png)
* [Pixel 10](/fonts/pixel10/)

  ![Pixel 10](/assets/images/fonts/pixel_10.png)
* [Sunset](/fonts/sunset/)

  ![Sunset](/assets/images/fonts/sunset.png)
* [Western light](/fonts/western_light/)

  ![Western light](/assets/images/fonts/western_light.png)

### Font updates

Numerous updates to existing fonts were made. Thanks to everyone involved!

## New Extensions

### Edit JSON

`Font Management > Edit JSON` [#3371](https://github.com/inkstitch/inkstitch/pull/3371)

Edit JSON is part of the Font Management and helps font authors to easily correct data in the json file. It is especially useful for kerning corrections as it simulates a custom text as you update the kerning.

![Edit Kerning (distance between letters](/assets/images/upcoming/3.2.0/edit_json.png)

[Read more](/docs/font-tools/#edit-json)

### Fill to Satin

`Tools: Satin > Fill to Satin...` [#3406](https://github.com/inkstitch/inkstitch/pull/3406)

Converts a fill to a satin. Manual setting of rungs is required.

![Fill to satin](/assets/images/docs/fill_to_satin_bridge.png)

[Read more](/docs/satin-tools/#fill-to-satin)

### Install Addons for Inkscape

`Install Addons for Inkscape` [#3606](https://github.com/inkstitch/inkstitch/pull/3606)

Installs color palettes or a symbol library for motif stitches into Inkscape. Please restart Inkscape after the installation.

![Motif stitches](/assets/images/upcoming/3.2.0/motif-stitches.png)

Replaces `Install thread color palettes for Inkscape`.

[Read more](/docs/install-addons/)

### Remove duplicated points

`Edit > Remove duplicated points` [#3117](https://github.com/inkstitch/inkstitch/pull/3117)

Helps (for example) to remove bean stitches from stitch plans and turn them into simple lines.

![Remove duplicated points](/assets/images/upcoming/3.2.0/remove_duplicated_points.png)

[Read more](/docs/edit/#remove-duplicated-points)

### Selection to Knockdown Fill

`Tools: Fill > Selection to Knockdown Fill` [#3526](https://github.com/inkstitch/inkstitch/pull/3526)

Helper method to generate a fill area underneath of all selected elements, optionally with an offset. This can be very useful when working with high pile fabric.

![A figure with a surrounding knockdown stitch](/assets/images/docs/knockdown.png)

[Read more](/docs/fill-tools/#knockdown-fill)

### Set color sort index

`Font management > Set color sort index` [#3242](https://github.com/inkstitch/inkstitch/pull/3242)

A tool for font authors which sets a specified color sort index on selected elements to control element grouping when the color sorting option is enabled in the lettering tool.

![Color sort index](/assets/images/upcoming/3.2.0/color_sort_index.png)

[Read more](/docs/font-tools/#set-color-index)

### Transform

`Edit > Transform...` [#3657](https://github.com/inkstitch/inkstitch/pull/3657)

Applies transforms to elements (rotate / flip) while also adapting the fill angle.

![Fill element transformed by 45 degrees, fill angle adapted](/lokal/assets/images/docs/transform.png)

## Extension Updates

### General

* Request permission to update old SVG files if the inkstitch svg version attribute is not specified in the file. [#3228](https://github.com/inkstitch/inkstitch/pull/3228)

  This prevents to falsely update copy-pasted content in a new file.
* Ink/Stitch extensions are now shown with icons and descriptions in the extension gallery for easy access [#3287](https://github.com/inkstitch/inkstitch/pull/3287)

  ![Extension gallery](/assets/images/upcoming/3.2.0/extension_gallery.png)

### Auto-route satin

`Tools: Satin > AutoRoute Satin`

* Add option to keep original path elements [#3332](https://github.com/inkstitch/inkstitch/pull/3332)
* Transfer object based minimum jump length value (if present) from satins on auto-generated centerline strokes [#3154](https://github.com/inkstitch/inkstitch/pull/3154)

[Read more](/docs/satin-tools/#auto-route-satin-columns)

### Attach commands to selected objects

* We had a lot of complaints that positioning command symbols is rather difficult. Therefore visual commands are now directed towards the symbol center, rather than the touching point of the command connector [#3542](https://github.com/inkstitch/inkstitch/pull/3542).

  This means, when you position a start symbol, the starting point of the element will be directly at the symbols center. Old files will automatically update.

  ![Hidden connector command](/assets/images/upcoming/3.2.0/hidden_connector_commands.png)
* Unified start and stop commands for various stitch types. Old files will automatically updated.

[Read more](/docs/commands/)

### Convert to gradient blocks

* Insert color blocks into a group and skip small elements [#3584](https://github.com/inkstitch/inkstitch/pull/3584)

[Read more](/docs/fill-tools/#convert-to-gradient-blocks)

### Scale Command Symbols

`Commands > View > Scale Command Symbols`

* Set all commands to a unique size at once (reset previous transform) [#3329](https://github.com/inkstitch/inkstitch/pull/3329)

  Please note that manual transforms on groups with a command may influence the actual size of a symbol.

[Read more](/docs/commands/#scale-command-symbols)

### Font sampling

`Font Management > Font Sampling`

* Add color sort option for multicolor fonts [#3242](https://github.com/inkstitch/inkstitch/pull/3242). The font has to support color sorting.

[Read more](/docs/font-tools/#font-sampling)

### Force lock stitches

`Font Management > Force lock stitches`

* Add option to disable lock stitch insertion by distance
  (for example to add lock stitches only after the last element of the glyph) [#3559](https://github.com/inkstitch/inkstitch/pull/3559)

[Read more](/docs/font-tools/#force-lock-stitches)

### Lettering

`Lettering > Lettering`

* Load with last selected font and remember some other settings [#3498](https://github.com/inkstitch/inkstitch/pull/3498) [#3504](https://github.com/inkstitch/inkstitch/pull/3504)
* Add support for more languages (right to left) [#3432](https://github.com/inkstitch/inkstitch/pull/3358) [#3466](https://github.com/inkstitch/inkstitch/pull/3466)
* Lettering simulator: show accurate start and end points [#3358](https://github.com/inkstitch/inkstitch/pull/3358)
* Uniformed size info (% and mm) [#3346](https://github.com/inkstitch/inkstitch/pull/3346)
* Add color sort option for multicolor fonts [#3242](https://github.com/inkstitch/inkstitch/pull/3242), [#3381](https://github.com/inkstitch/inkstitch/pull/3381). The font has to support color sorting.
* Options for text alignment [#3382](https://github.com/inkstitch/inkstitch/pull/3382)

![Lettering: more options](/assets/images/upcoming/3.2.0/lettering.png)

[Read more](/docs/lettering/)

### Lettering Along Path

`Lettering > Lettering Along Path`

Add option for text position along the path (left, center, right, stretch)

![A text aligned along a path while using the various options](/assets/images/docs/text_along_path_alignment.png)

[Read more](/docs/lettering/#lettering-along-path)

### Multicolor Satin

* Option to adjust underlay [#3152](https://github.com/inkstitch/inkstitch/pull/3152)

[Read more](/docs/satin-tools/#multicolor-satin)

### Redwork

* Add combine option [#3407](https://github.com/inkstitch/inkstitch/pull/3407)
* Add keep originals option [#3407](https://github.com/inkstitch/inkstitch/pull/3407)

[Read more](/docs/stroke-tools/#redwork)

### Simulator

* Add button to toggle crosshair [#3616](https://github.com/inkstitch/inkstitch/pull/3616)
* Option to save and reload simulator speed (optionally) [#3420](https://github.com/inkstitch/inkstitch/pull/3420)
* Save and reload more simulator settings (status for buttons: jump, trim, color change, stop, needle penetration point, page border) [#3323](https://github.com/inkstitch/inkstitch/pull/3323)
* Show page in simulator [#3120](https://github.com/inkstitch/inkstitch/pull/3120)

[Read more](/docs/visualize/#simulator)

### Stitch plan preview

* Improve realistic filter [#3222](https://github.com/inkstitch/inkstitch/pull/3222)

[Read more](/docs/visualize/#stitch-plan-preview)

### Stroke to LPE-Satin

* Take transforms into account (for path specific lpe satins only) [#3500](https://github.com/inkstitch/inkstitch/pull/3500)

[Read more](/docs/satin-tools/#stroke-to-live-path-effect-satin)

### Troubleshoot

* Group pointers. Specific error/warning types can be easily toggled on and off [#3486](https://github.com/inkstitch/inkstitch/pull/3486)
* Add background to troubleshoot text [#3357](https://github.com/inkstitch/inkstitch/pull/3357)

[Read more](/docs/troubleshoot/#troubleshoot-objects)

### Unlink clones

* Add option to group / not group unlinked symbol elements [#3624](https://github.com/inkstitch/inkstitch/pull/3624)

[Read more](/docs/edit/#unlink-clone)

## Removed extensions

### Convert Line to Satin Column

The name was simplified to `Stroke to Satin`.

This is more in the line with the names of the other conversion methods in Ink/Stitch.

### Glyphlist update

Glyphlist update has been part of the font management and was replaced by the much more powerful
[Edit JSON extension](/docs/font-tools/#edit-json)  [#3380](https://github.com/inkstitch/inkstitch/pull/3380)

### Install Thread Color Palettes for Inkscape

Moved to `Install Addons for Inkscape`

[Read more](/docs/install-addons/)

## Stitch Type Related Updates

### Automatic Start- and Endpoints

Fill elements and satin columns now start automatically at the nearest point to the previous element and end at the nearest point to the next element [#3370](https://github.com/inkstitch/inkstitch/pull/3370).

The behaviour is adaptable and of course start- and end commands will still work.

![Two satins joining at one point, rendered without a jump stitch](/assets/images/upcoming/3.2.0/start_at_nearest_point.png)

### Clips

Clips are now easy accessable to Ink/Stitch in all forms. They are especially useful in combination with the redwork tool.

* **Groups:** Ink/Stitch can now also parse clips which are applied on groups [#3261](https://github.com/inkstitch/inkstitch/pull/3261).

  ![cliped groups](/assets/images/tutorials/mandala/lettremandala.svg)
* **Effect clips** allow to use an inverted clip ([#3364](https://github.com/inkstitch/inkstitch/pull/3364)).

  ![interved clips](/assets/images/galleries/fonts/decadent_flowers_monogram/IMG_5211.jpg)

### Clones

* Clones now also clone commands attached to the element and its children [#3086](https://github.com/inkstitch/inkstitch/pull/3086)

[Read more](/docs/stitches/clone/)

### Contour Fill

* Add expand option [#3462](https://github.com/inkstitch/inkstitch/pull/3462)

[Read more](/docs/stitches/contour-fill/)

### Linear gradient fill

* Add randomization options to linear gradient fill [#3311](https://github.com/inkstitch/inkstitch/pull/3311)

[Read more](/docs/stitches/linear-gradient-fill/)

### Manual stitch

* Add bean stitch option to manual stitch [#3312](https://github.com/inkstitch/inkstitch/pull/3312)

[Read more](/docs/stitches/manual-stitch/)

### Ripple Stitch

* Manual stitch placement for ripple patterns [#3256](https://github.com/inkstitch/inkstitch/pull/3256)
* Add stitch grid first option [#3436](https://github.com/inkstitch/inkstitch/pull/3436)
* Satin guided ripples

  ![satin guided ripple](/assets/images/docs/ripple_satin_guide.svg)

  * Option whether to flip each second line of the pattern or not
  * Anchor line to align ripple patterns [#3436](https://github.com/inkstitch/inkstitch/pull/3436)

  [Read more](/docs/stitches/ripple-stitch/#satin-guide)

### Satin Columns

* Starts and ends at nearest points by default [#3423](https://github.com/inkstitch/inkstitch/pull/3423)

  ![Automated start and end point for satin column](/assets/images/upcoming/3.2.0/satin_start_end.png)
* Enable start end commands for satins [#3315](https://github.com/inkstitch/inkstitch/pull/3315)

  ![Start/end command for satin columns](/assets/images/upcoming/3.2.0/satin_start_end_command.png)

[Read more](/docs/stitches/satin-column/)

## Palettes

* Update `InkStitch Madeira Rayon.gpl` [#3444](https://github.com/inkstitch/inkstitch/pull/3444)
* Isacord polyester: added `0713 Lemon` color [#3225](https://github.com/inkstitch/inkstitch/pull/3225)

## Export / Import

See full list of [supported file formats](/docs/file-formats/)

### New Export Formats

TBF

Longarm Quilting: PLT, QCC

### New Import Formats

Longarm Quilting: PLT, QCC, IQP

### GCODE

* Custom RGB values [#3530](https://github.com/inkstitch/inkstitch/pull/3530)
* Custom JUMP

### Batch Lettering

Ink/Stitch can now export multiple files with different texts at once. A path with a specified label within the open document can be used to define text position.

![A patch with four different names](/assets/images/docs/batch-lettering.png)

[More information](/docs/lettering/#batch-lettering)

## Releases

* Windows releases are now signed for free with [SignPath.io](https://about.signpath.io) certificate by [SignPath Foundation](https://signpath.org). We are very greatful for their support.
* Windows 32bit version has been removed as it is no longer supported
* Linux releases available for 64bit and 32bit

## Developer and Build Stuff

* Sew Stack (first steps) [#3133](https://github.com/inkstitch/inkstitch/pull/3133)

  The Sew Stack will ultimately replace Params and contain its functionality. For now, it is invisible in our releases.
  The params dialog as it is now suffers from all the options, we've added over the years. It is now hard to find a specific setting in there
  and even harder if you are not yet familiar with the program. Sew Stack will help to organize parameter settings.

  It is only visible in manual installs and will not render, unless `enable_sew_stack` is enabled in the debug config file.
  Please note, that this will alter the start and end points of the elements and should only be used for development purposes.

* Update update build process [#3652](https://github.com/inkstitch/inkstitch/pull/3652)
  * removed win32 build
  * use geos source build only for linux32
  * set python version to 3.11 for all builds
  * sign only releases for windows
  * sign windows release with release certificate [#3613](https://github.com/inkstitch/inkstitch/pull/3613)
* Mypy type correctness [#3199](https://github.com/inkstitch/inkstitch/pull/3199)
* use get_user_dir [#3549](https://github.com/inkstitch/inkstitch/pull/3549)
* Migrate from appdirs to platformdirs [#3450](https://github.com/inkstitch/inkstitch/pull/3450)
* remove scipy dependency [#3483](https://github.com/inkstitch/inkstitch/pull/3483) [#3481](https://github.com/inkstitch/inkstitch/pull/3481)
* Update translations workflow [#3435](https://github.com/inkstitch/inkstitch/pull/3435)
* Add lmde6 32bit build [#3298](https://github.com/inkstitch/inkstitch/pull/3298)
* Update macos cloud build [#3291](https://github.com/inkstitch/inkstitch/pull/3291)
* Use colormath2 instead of colormath [#3266](https://github.com/inkstitch/inkstitch/pull/3266)
* make hook actually cancel the commit [#3235](https://github.com/inkstitch/inkstitch/pull/3235)
* linux package fix [#3210](https://github.com/inkstitch/inkstitch/pull/3210)
* arm64 python update [#3201](https://github.com/inkstitch/inkstitch/pull/3201)
* only style-check staged changes [#3186](https://github.com/inkstitch/inkstitch/pull/3186)
* Additional CI Improvements [#3174](https://github.com/inkstitch/inkstitch/pull/3174)
* CI: Added pytest, some speed improvements [#3135](https://github.com/inkstitch/inkstitch/pull/3135)

## Bug Fixes

* fix ensure even center walk underlay repeats in auto_satin when value is empty [#3651](https://github.com/inkstitch/inkstitch/pull/3651)
* Prevent unwanted simulator scale transforms [#3637](https://github.com/inkstitch/inkstitch/pull/3637)
* Always update satin param to avoid actual param/rendering mismatch [#3647](https://github.com/inkstitch/inkstitch/pull/3647)
* Lettering, custom directories: do not try to read hidden directories [#3632](https://github.com/inkstitch/inkstitch/pull/3632)
* Simulator on macOS Ventura: update background color correctly [#3621](https://github.com/inkstitch/inkstitch/pull/3621)
* ignore palette files with wrong encoding [#3620](https://github.com/inkstitch/inkstitch/pull/3620)
* fix updater [#3583](https://github.com/inkstitch/inkstitch/pull/3583)
* Element info: take pattern into account [#3581](https://github.com/inkstitch/inkstitch/pull/3581)
* Autosatin: more efforts to keep the stroke width consistant [#3563](https://github.com/inkstitch/inkstitch/pull/3563)
* display stop commands in simulator and print preview [#3545](https://github.com/inkstitch/inkstitch/pull/3545)
* auto-route: apply transforms to ensure stroke width being unchanged [#3538](https://github.com/inkstitch/inkstitch/pull/3538)
* lettering: do not add commands on top of command connectors [#3528](https://github.com/inkstitch/inkstitch/pull/3528)
* Fix jump to trim: NoneType element error [#3525](https://github.com/inkstitch/inkstitch/pull/3525)
* stroke: as_multi_line_string ignore single point paths [#3491](https://github.com/inkstitch/inkstitch/pull/3491)
* Adapt simulator slider symbols to dark theme [#3475](https://github.com/inkstitch/inkstitch/pull/3475)
* Auto-run: try harder to avoid networkx issues [#3457](https://github.com/inkstitch/inkstitch/pull/3457)
* Improve handling of symbols [#3440](https://github.com/inkstitch/inkstitch/pull/3440)
* Lettering: ignore auto-satin setting in the json file when there is no satin [#3434](https://github.com/inkstitch/inkstitch/pull/3434)
* Fix issue in preferences when value is 0.0 [#3430](https://github.com/inkstitch/inkstitch/pull/3430)
* Exclude invisible from node_to_elements directly [#3424](https://github.com/inkstitch/inkstitch/pull/3424)
* Cache: reset on operational error [#3421](https://github.com/inkstitch/inkstitch/pull/3421)
* Update README [#3405](https://github.com/inkstitch/inkstitch/pull/3405)
* Fix an other FloatingPointError [#3404](https://github.com/inkstitch/inkstitch/pull/3404)
* Minimize multi shape tartan jumps [#3386](https://github.com/inkstitch/inkstitch/pull/3386)
* Lettering: prevent duplicated output [#3365](https://github.com/inkstitch/inkstitch/pull/3365)
* Cut satin column: add more rungs when rails are intersecting [#3344](https://github.com/inkstitch/inkstitch/pull/3344)
* Fix jump to stroke transform glitch [#3306](https://github.com/inkstitch/inkstitch/pull/3306)
* Make remove commands more robust for broken commands with active selection [#3288](https://github.com/inkstitch/inkstitch/pull/3288)
* Avoid code repetition in paths detection [#3282](https://github.com/inkstitch/inkstitch/pull/3282)
* Thread catalog: fix broken path [#3281](https://github.com/inkstitch/inkstitch/pull/3281)
* Clone: do not fixup href [#3277](https://github.com/inkstitch/inkstitch/pull/3277)
* Prevent zerodivision error for zero length segments [#3268](https://github.com/inkstitch/inkstitch/pull/3268)
* Set svg version when importing an embroidery file [#3276](https://github.com/inkstitch/inkstitch/pull/3276)
* Redwork/Auto-Run: keep stroke width [#3264](https://github.com/inkstitch/inkstitch/pull/3264)
* Fix 'None'-string confusions in style [#3243](https://github.com/inkstitch/inkstitch/pull/3243)
* Print pdf: prevent rendering original paths [#3262](https://github.com/inkstitch/inkstitch/pull/3262)
* Avoid error message on info panel update [#3246](https://github.com/inkstitch/inkstitch/pull/3246)
* Satin column: ignore single point paths [#3244](https://github.com/inkstitch/inkstitch/pull/3244)
* Fix select redwork top layer [#3230](https://github.com/inkstitch/inkstitch/pull/3230)
* Fix gradient style [#3200](https://github.com/inkstitch/inkstitch/pull/3200)
* Fix clones with NoneType hrefs [#3196](https://github.com/inkstitch/inkstitch/pull/3196)
* Fixed hidden objects being stitched out when cloned (Fix #3167) [#3171](https://github.com/inkstitch/inkstitch/pull/3171)
* Fixed transforms on cloned commands [#3160](https://github.com/inkstitch/inkstitch/pull/3160)
* fill: ensure polygon in pull comp adjusted shape [#3143](https://github.com/inkstitch/inkstitch/pull/3143)
* add wxpython abort message (as alternative to stderr output) [#3145](https://github.com/inkstitch/inkstitch/pull/3145)
* fix fills without underpath and bad start-end positions [#3141](https://github.com/inkstitch/inkstitch/pull/3141)
* satin troubleshoot: do not fail on satins without rails [#3148](https://github.com/inkstitch/inkstitch/pull/3148)
* auto satin: filter zero length strokes as well [#3139](https://github.com/inkstitch/inkstitch/pull/3139)
* Disable darkmode symbols for windows (darkmode in windows doesn't work as excepted) [#3144](https://github.com/inkstitch/inkstitch/pull/3144)
* Fix simulator slider dark theme issue [#3147](https://github.com/inkstitch/inkstitch/pull/3147)
* skip empty gradient blocks [#3142](https://github.com/inkstitch/inkstitch/pull/3142)
* Simulator: toggle info and preferences dialog [#3115](https://github.com/inkstitch/inkstitch/pull/3115)

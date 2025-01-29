---
title: "New Features, Updates and Fixes for the upcoming Ink/Stitch version"
permalink: /upcoming/
last_modified_at: 2025-01-11
sidebar:
  nav: pages
toc: true
---
## [Fonts](/fonts/font-library)

### New Fonts

* [Barstitch bold](/fonts/barstitch_bold/)

  ![Barstitch bold](/assets/images/fonts/barstitch_bold.png)
* [Barstitch mandala](/fonts/barstitch/bold/)

  ![Barstitch mandala](/assets/images/fonts/barstitch_mandala.png)
* [Barstitch textured](/fonts/barstitch_bold/)

  ![Barstitch textured](/assets/images/fonts/barstitch_textured.png)
* [Cogs_KOR](/fonts/cogs_KOR)

  ![Cogs_KOR](/assets/images/fonts/cogs_KOR.png)
* [Magnolia tamed](/fonts/magnolia-script/)

  ![Magnolia tamed preview](/assets/images/fonts/magnolia_tamed.png)
* [Pixel 10](/fonts/pixel10/)

  ![Pixel 10](/assets/images/fonts/pixel_10.png)
* [Sunset](/fonts/sunset/)

  ![Sunset](/assets/images/fonts/sunset.png)
* [Western light](/fonts/western_light/)

  ![Western light](/assets/images/fonts/western_light.png)

### Font updates

* Simplify font description [#3350](https://github.com/inkstitch/inkstitch/pull/3350)
* Namskout: fix Z [#3362](https://github.com/inkstitch/inkstitch/pull/3362)
* Remove unwanted jumps in ink/stitch medium font [#3295](https://github.com/inkstitch/inkstitch/pull/3295)
* Make more fonts sortable [#3280](https://github.com/inkstitch/inkstitch/pull/3280)
* Make most multicolor fonts sortable [#3242](https://github.com/inkstitch/inkstitch/pull/3242)
* Update dinomouse [#3272](https://github.com/inkstitch/inkstitch/pull/3272)
* Shojumaru: make the font more robust in case of deformation [#3234](https://github.com/inkstitch/inkstitch/pull/3234)
* perspective_tricolore_KOR: update font.json [#3202](https://github.com/inkstitch/inkstitch/pull/3202)
* Cooper marif: json corrections [#3194](https://github.com/inkstitch/inkstitch/pull/3194)
* roaring_twenties_KOR: improve kerning [#3136](https://github.com/inkstitch/inkstitch/pull/3136)
* Violin serif: change one rail orientation on capital A [#3129](https://github.com/inkstitch/inkstitch/pull/3129)
* add some punctuation signs to dejavu, learning curve, milli marif and Kaushan script [#3123](https://github.com/inkstitch/inkstitch/pull/3123)


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

### Remove duplicated points

`Edit > Remove duplicated points` [#3117](https://github.com/inkstitch/inkstitch/pull/3117)

Helps (for example) to remove bean stitches from stitch plans and turn them into simple lines.

![Remove duplicated points](/assets/images/upcoming/3.2.0/remove_duplicated_points.png)

[Read more](/docs/edit/#remove-duplicated-points)

### Set color sort index

`Font management Set color sort index` [#3242](https://github.com/inkstitch/inkstitch/pull/3242)

A tool for font authors which sets a specified color sort index on selected elements to control element grouping when the color sorting option is enabled in the lettering tool.

![Color sort index](/assets/images/upcoming/3.2.0/color_sort_index.png)

[Read more](/docs/font-tools/#set-color-index)

## Extension Updates

### General

* Request permission to update if inkstitch svg version is not specified in the svg file. [#3228](https://github.com/inkstitch/inkstitch/pull/3228)
* Ink/Stitch can read now read the clipped path of groups correctly [#3261](https://github.com/inkstitch/inkstitch/pull/3261)<br>
  This works well together with the redwork tool.

  ![cliped groups](/assets/images/tutorials/mandala/lettremandala.svg)
* Add icons and descriptions for extension gallery [#3287](https://github.com/inkstitch/inkstitch/pull/3287)

  ![Extension gallery](/assets/images/upcoming/3.2.0/extension_gallery.png)

### Auto-route satin

`Tools: Satin > AutoRoute Satin`

* add option to keep original path elements [#3332](https://github.com/inkstitch/inkstitch/pull/3332)
* transfer object based min jump length (if present) from satins on auto-generated strokes [#3154](https://github.com/inkstitch/inkstitch/pull/3154)

### Attach commands to selected objects

* Unified start and stop commands for various stitch types (will automatically update older files)

### Scale Command Symbols

`Commands > View > Scale Command Symbols`

* Set all commands to unique size at once (reset previous transform) [#3329](https://github.com/inkstitch/inkstitch/pull/3329)

### Font sampling

`Font Management > Font Sampling`

* Add color sort option [#3242](https://github.com/inkstitch/inkstitch/pull/3242)

### Lettering

`Lettering`

* Lettering simulator: show accurate start and end points [#3358](https://github.com/inkstitch/inkstitch/pull/3358)
* Uniformed size info (% and mm) [#3346](https://github.com/inkstitch/inkstitch/pull/3346)
* Add color sort option for multicolor fonts [#3242](https://github.com/inkstitch/inkstitch/pull/3242), [#3381](https://github.com/inkstitch/inkstitch/pull/3381)
* Options for text alignment [#3382](https://github.com/inkstitch/inkstitch/pull/3382)

![Lettering: more options](/assets/images/upcoming/3.2.0/lettering.png)

### Multicolor Satin

* Option to adjust underlay [#3152](https://github.com/inkstitch/inkstitch/pull/3152)

### Redwork

* Add combine option [#3407](https://github.com/inkstitch/inkstitch/pull/3407)
* Add keep originals option [#3407](https://github.com/inkstitch/inkstitch/pull/3407)

### Select elements

* Fix select redwork top layer [#3230](https://github.com/inkstitch/inkstitch/pull/3230)

### Simulator

* Option to save and reload simulator speed (optionally) [#3420](https://github.com/inkstitch/inkstitch/pull/3420)
* Save and reload more simulator settings (status for buttons: jump, trim, color change, stop, needle penetration point, page border) [#3323](https://github.com/inkstitch/inkstitch/pull/3323)
* Show page in simulator [#3120](https://github.com/inkstitch/inkstitch/pull/3120)

### Stitch plan preview

* Update realistic filter [#3222](https://github.com/inkstitch/inkstitch/pull/3222)

### Troubleshoot

* Add background to troubleshoot text [#3357](https://github.com/inkstitch/inkstitch/pull/3357)

## Removed extensions

### Glyphlist update

Glyphlist update has been part of the font management and was replaced by the much more powerful
[Edit JSON extension](/docs/font-tools/#edit-json)  [#3380](https://github.com/inkstitch/inkstitch/pull/3380)

## Stitch type Updates

* Automated end point calculation for fill and satin (ends at nearest point) [#3370](https://github.com/inkstitch/inkstitch/pull/3370)

### Clones

* Clones now also clone commands attached to element and its children. (#3032, #3121) [#3086](https://github.com/inkstitch/inkstitch/pull/3086)

### Linear gradient fill

* Add randomization options to linear gradient fill [#3311](https://github.com/inkstitch/inkstitch/pull/3311)

### Manual stitch

* Add bean stitch option to manual stitch [#3312](https://github.com/inkstitch/inkstitch/pull/3312)

### Ripple Stitch

* Manual ripple pattern [#3256](https://github.com/inkstitch/inkstitch/pull/3256)

### Satin Columns

* Starts and ends at nearest points by default [#3423](https://github.com/inkstitch/inkstitch/pull/3423)

  ![Automated start and end point for satin column](/assets/images/upcoming/3.2.0/satin_start_end.png)
* Enable start end commands for satins [#3315](https://github.com/inkstitch/inkstitch/pull/3315)

  ![Start/end command for satin columns](/assets/images/upcoming/3.2.0/satin_start_end_command.png)

## Palettes

* Isacord polyester: added 0713 Lemon color [#3225](https://github.com/inkstitch/inkstitch/pull/3225)

## Developer and Build Stuff

* Add build for ubuntu 24.04 [#3299](https://github.com/inkstitch/inkstitch/pull/3299)[#3330](https://github.com/inkstitch/inkstitch/pull/3330)
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

* Exclude invisible from node_to_elements directly [#3424](https://github.com/inkstitch/inkstitch/pull/3424)
* Cache: reset on operational error [#3421](https://github.com/inkstitch/inkstitch/pull/3421)
* Update README [#3405](https://github.com/inkstitch/inkstitch/pull/3405)
* Fix an other FloatingPointError [#3404](https://github.com/inkstitch/inkstitch/pull/3404)
* Minimize multi shape tartan jumps [#3386](https://github.com/inkstitch/inkstitch/pull/3386)
* Lettering: prevent duplicated output [#3365](https://github.com/inkstitch/inkstitch/pull/3365)
* Fix path effect clips (couldn't be used before) [#3364](https://github.com/inkstitch/inkstitch/pull/3364)
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
* Fix gradient style [#3200](https://github.com/inkstitch/inkstitch/pull/3200)
* Fix clones with NoneType hrefs [#3196](https://github.com/inkstitch/inkstitch/pull/3196)
* Fixed hidden objects being stitched out when cloned (Fix #3167) [#3171](https://github.com/inkstitch/inkstitch/pull/3171)
* Fixed transforms on cloned commands [#3160](https://github.com/inkstitch/inkstitch/pull/3160)
* fill: ensure polygon in pull comp adjusted shape [#3143](https://github.com/inkstitch/inkstitch/pull/3143)
* add wxpython abort message (as alternative to stderr output) [#3145](https://github.com/inkstitch/inkstitch/pull/3145)
* fix fills without underpath and bad start-end positions [#3141](https://github.com/inkstitch/inkstitch/pull/3141)
* satin troubleshoot: do not fail on satins without rails [#3148](https://github.com/inkstitch/inkstitch/pull/3148)
* auto satin: filter zero length strokes as well [#3139](https://github.com/inkstitch/inkstitch/pull/3139)
* Disable darkmode symbols for windows (darkmode in windows doesn't work as excepted) (#3144)
* Fix simulator slider dark theme issue [#3147](https://github.com/inkstitch/inkstitch/pull/3147)
* skip empty gradient blocks [#3142](https://github.com/inkstitch/inkstitch/pull/3142)
* Simulator: toggle info and preferences dialog [#3115](https://github.com/inkstitch/inkstitch/pull/3115)

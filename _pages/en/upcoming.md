---
title: "New Features, Updates and Fixes for the upcoming Ink/Stitch version"
permalink: /upcoming/
last_modified_at: 2024-11-30
sidebar:
  nav: pages
toc: true
---
## [Fonts](/fonts/font-library)

### New Fonts

* [Cogs_KOR](/fonts/cogs_KOR)

  ![Cogs_KOR](/assets/images/fonts/cogs_KOR.png)
* [Magnolia tamed](/fonts/magnolia-script/)

  ![Magnolia tamed preview](/assets/images/fonts/magnolia_tamed.png)

### Font updates

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

### Remove duplicated points

`Edit > Remove duplicated points` [#3117](https://github.com/inkstitch/inkstitch/pull/3117)

Helps (for example) to remove bean stitches from stitch plans and turn them into simple lines.

### Set color sort index

`Font management Set color sort index` [#3242](https://github.com/inkstitch/inkstitch/pull/3242)

A tool for font authors which sets a specified color sort index on selected elements to control element grouping when the color sorting option is enabled in the lettering tool.

## Extension Updates

### General

* Request permission to update if inkstitch svg version is not specified in the svg file. [#3228](https://github.com/inkstitch/inkstitch/pull/3228)
* Adapt paths of clipped groups to clip [#3261](https://github.com/inkstitch/inkstitch/pull/3261)
* Add icons and descriptions for extension gallery [#3287](https://github.com/inkstitch/inkstitch/pull/3287)

### Auto-route satin

* transfer object based min jump length (if present) from satins on auto-generated strokes [#3154](https://github.com/inkstitch/inkstitch/pull/3154)

### Font sampling

* Add color sort option [#3242](https://github.com/inkstitch/inkstitch/pull/3242)

### Lettering

* Add color sort option for multicolor fonts [#3242](https://github.com/inkstitch/inkstitch/pull/3242)

### Multicolor Satin

* Option to adjust underlay [#3152](https://github.com/inkstitch/inkstitch/pull/3152)

### Select elements

* Fix select redwork top layer [#3230](https://github.com/inkstitch/inkstitch/pull/3230)

### Simulator

* Show page in simulator [#3120](https://github.com/inkstitch/inkstitch/pull/3120)

### Stitch plan preview

* Update realistic filter [#3222](https://github.com/inkstitch/inkstitch/pull/3222)

## Stitch types

### Stitch type updates

#### Clones

* Clones now also clone commands attached to element and its children. (#3032, #3121) [#3086](https://github.com/inkstitch/inkstitch/pull/3086)

### Linear gradient fill

* Add randomization options to linear gradient fill [#3311](https://github.com/inkstitch/inkstitch/pull/3311)

### Manual stitch

* Add bean stitch option to manual stitch [#3312](https://github.com/inkstitch/inkstitch/pull/3312)

### Ripple Stitch

* Manual ripple pattern [#3256](https://github.com/inkstitch/inkstitch/pull/3256)

## Palettes

* Isacord polyester: added 0713 Lemon color [#3225](https://github.com/inkstitch/inkstitch/pull/3225)

## Developer and Build Stuff

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
* Disable darkmode symbols for windows (darkmode in windows doesn't work as excepted) (#3144), fix slider dark theme issue [#3147](https://github.com/inkstitch/inkstitch/pull/3147)
* skip empty gradient blocks [#3142](https://github.com/inkstitch/inkstitch/pull/3142)
* Simulator: toggle info and preferences dialog [#3115](https://github.com/inkstitch/inkstitch/pull/3115)

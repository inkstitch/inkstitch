---
title: "New Features, Updates and Fixes for the upcoming Ink/Stitch version"
permalink: /upcoming/
last_modified_at: 2024-09-26
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

* Update font.json [#3202](https://github.com/inkstitch/inkstitch/pull/3202)
* json corrections [#3194](https://github.com/inkstitch/inkstitch/pull/3194)
* improve kerning [#3136](https://github.com/inkstitch/inkstitch/pull/3136)
* Update →.svg [#3129](https://github.com/inkstitch/inkstitch/pull/3129)
* add some punctuation signs [#3123](https://github.com/inkstitch/inkstitch/pull/3123)


## New Extensions

### Remove duplicated points

`Edit > Remove duplicated points` [#3117](https://github.com/inkstitch/inkstitch/pull/3117)

Helps (for example) to remove bean stitches from stitch plans and turn them into simple lines.

## Extension Updates

### Auto-route satin

* transfer object based min jump length (if present) from satins on auto-generated strokes [#3154](https://github.com/inkstitch/inkstitch/pull/3154)

### Multicolor Satin

* option to adjust underlay [#3152](https://github.com/inkstitch/inkstitch/pull/3152)

### Simulator

* Show page in simulator [#3120](https://github.com/inkstitch/inkstitch/pull/3120)

## Stitch types

### Stitch type updates

#### Clones

* Clones now also clone commands attached to element and its children. (#3032, #3121) [#3086](https://github.com/inkstitch/inkstitch/pull/3086)

## Developer and Build Stuff

* Rejbasket/linux package fix [#3210](https://github.com/inkstitch/inkstitch/pull/3210)
* Rejbasket/arm64 python update [#3201](https://github.com/inkstitch/inkstitch/pull/3201)
* only style-check staged changes [#3186](https://github.com/inkstitch/inkstitch/pull/3186)
* Additional CI Improvements [#3174](https://github.com/inkstitch/inkstitch/pull/3174)
* CI: Added pytest, some speed improvements [#3135](https://github.com/inkstitch/inkstitch/pull/3135)

## Bug Fixes

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

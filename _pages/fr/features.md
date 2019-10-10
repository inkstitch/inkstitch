---
title: "Ink/Stitch Features"
permalink: /fr/features/
excerpt: "Ink/Stitch features"
last_modified_at: 2019-03-14
sidebar:
  nav: pages
toc: true
---
## Noticeable Features
* Digitize machine embroidery designs using Inkscape (SVG)
* Cross Platform
  * all code libraries built in, no need to install anything else!
* User interface translated to several languages ([translation help appreciated](https://crowdin.com/project/inkstitch)!)
* Import and Export many popular machine embroidery formats
  * including batch export 
* Add Trims and Stops
* Edit Stitch Order
* Set custom origin point as (0, 0) in the design file
* Animated stitch-out preview
  * including live-preview as you adjust settings like row spacing underlay, etc.
* Print to PDF
  * realistic rendering
    * line-drawing mode available as well
  * embroidery machine operator layout with color blocks, thread names, stitch counts, and custom notes
  * client-oriented layout designed for you to send to your customer
  * highly customizable through your web browser
* Thread manufacturer palettes (over 60 manufacturers included)
  * automated installation of Inkscape palettes for use in your designs
  * thread names and catalog numbers included in PDF printouts
* Lettering

## Supported Stitch Types

### Fill Stitch
* automatically fill arbitrary shapes with stitches
* adjust the stitch length, row spacing, and row angle
* underlay

### Satin Stitch
* custom-design your satin column with varying width
* automatic routing (with underpathing running stitch if needed)
* mix and match 3 kinds of underlay
  * center-walk
  * contour
  * zig-zag

* e stitch

### Stroke Type Stitches
* running stitch
* bean stitch
* manual stitch
  * each stitch exactly where you want it

## Supported File Formats

### Writing
CSV, **DST**, **EXP**, **JEF**, PEC, **PES**, SVG, TXT (G-CODE), U01, **VP3**

### Reading
100, 10o, BRO, DAT, DSB, **DST**, DSZ, EMD, **EXP**, EXY, FXY, GT, INB, **JEF**, JPX, KSM, MAX, MIT, NEW, PCD, PCM, PCQ, PCS, PEC, **PES**, PHB, PHC, SEW, SHV, STC, STX, TAP, TBF, TXT (G-CODE), U01, **VP3**, XXX, ZXY

## Roadmap

Here are features we're hoping to add, though not necessarily in this order:

* Gradient Fill (already realised as a [hidden feature](https://github.com/inkstitch/inkstitch/pull/108#issuecomment-369444197))
* Pattern fill [#33](https://github.com/inkstitch/inkstitch/issues/33)
* Multi-Decoration Support [#371](https://github.com/inkstitch/inkstitch/issues/371)
* Automatic splitting of designs for small machines [#182](https://github.com/inkstitch/inkstitch/issues/182)
* Multiple Underlay for Fill [#110](https://github.com/inkstitch/inkstitch/issues/110)
* Split satins [#77](https://github.com/inkstitch/inkstitch/issues/77)
* Running Stitch Autoroute [#373](https://github.com/inkstitch/inkstitch/issues/373)
* 32-bit Linux support (build engineers needed!)


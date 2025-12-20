---
title: "Multiversion Install"
permalink: /developers/inkstitch/multiversion/
last_modified_at: 2024-02-13
toc: true
---
Installing multiple versions of Ink/Stitch can become very handy while development.

It will make it easy to run tests and compase versions

## Setup Ink/Stitch menu files

To install multiple Ink/Stitch versions the Inkscape menu files need a distinct ID.

Here's an example of how to use two Ink/Stitch extensions:

- install Inkstitch in two different locations (e.g. _inkstitch_ and _inkstitch-k_)
- ensure `make inx` is executed in both locations (this will generate also `inx/locale/` files)
- in the second location generate modified inx files: `generate-inx-files -a k`
- install the inx files in Inkscape extensions directory
  - symlink `.config/inkscape/extensions/inkstitch   -> inkstitch`
  - symlink `.config/inkscape/extensions/inkstitch-k -> inkstitch-k`
- modify `.config/inkscape/keys/default.xml` if necessary
- run Inkscape with both Inkstitch extensions enabled
  - first version:  `Extensions > Ink/Stitch`
  - second version: `Extensions > Ink/Stitch-k`


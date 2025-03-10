---
title: "Running Ink/Stitch from Command Line"
permalink: /docs/command-line/
last_modified_at: 2024-07-13
---
Ink/Stitch extensions can be run from command line.

## Example command line code


### Zip-Export

For example if you want to do export your file into a zip-archive (with a dst, pes and threadlist file) you can run the following command:

```
./inkstitch --extension=zip --format-dst=True --format-pes=True --format-threadlist=True input-file.svg > output-file.zip
```

### Stitch Plan

Here an example of outputting a stitch svg for two specific elements, which will hide the original design layers, display the needle points and is positioned right on top of the original design.

```
./inkstitch --extension=stitch_plan_preview --id=path1 --id=path2 --move-to-side=False --layer-visibility=hidden --needle-points=True input.svg > output.svg
```

## Inkscape command line options

For a full manual on inkscape command line options check out their [man page](https://inkscape.org/doc/inkscape-man.html)

Please note, that you can also access inkstitch combined with other inkscape actions. You can view the full list of available actions through

```
inkscape --action-list
```

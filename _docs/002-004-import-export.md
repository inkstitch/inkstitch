---
title: "Import and Export Files"
permalink: /docs/import-export/
excerpt: ""
last_modified_at: 2018-06-10
---

Ink/Stitch supports many embroidery formats. It can import and export files to the formats listed below.

## Supported File Formats (A - Z):

BRO, COL, CSD, DAT, DSB, DST, DSZ, EDR, EMD, EXP, EXY, FXY, GT, HUS, INB, INF, JEF, KSM, MAX, MIT, NEW, OFM, PCD, PCM, PCQ, PCS, PEC, PES, PHB, PHC, PLT, RGB, SEW, SHV, SST, STX, T01, T09, TAP, THR, U00, VIP, VP3, XXX, ZSK

## Import Embroidery Files

Open an embroidery file as you would open any SVG file in Inkscape: `File > Open...` > choose your file and click `Open`.

It will open your file with in [Manual Stitch Mode](/docs/stitches/stroke/#manual-stitch-mode). You can edit individual points and finetune your design. Once your are satisfied, save the file as described below.

## Export Embroidery Files

To export your designs run `Extensions > Embroidery > Embroider...`.

![Embroider...](/assets/images/docs/embroider.jpg)

Settings|Description
---|---
Collapse length (mm)|0.0 - 10.0
Hide other layers|Wether or not hide your original design layers while presenting the newly generated stitch plan
Output File Format|Choose a file format that your embroidery machine can read
Directory|Type your directory path, where you would like to save your file. By default, the directory used is the place where you installed the extension's Python files.

**Info:** For file format conversion Ink/Stitch uses *libembroidery* from the [Embroidermodder](https://github.com/Embroidermodder/Embroidermodder) project.
{: .notice--info }

---
title: "Import and Export Files"
permalink: /docs/import-export/
excerpt: ""
last_modified_at: 2018-06-23
toc: true
---

Ink/Stitch supports many embroidery formats. It can import and export files to the formats listed below.

## Supported File Formats (A - Z):

### Writing
DST, EXP, JEF, PEC, PES, VP3

#### Reading
100, 10o, BRO, DSB, DST, DSZ, EMD, EXP, INB, JEF, KSM, PEC, PES, SEW, SHV, STX, TAP, TBF, u01, VP3, XXX

## Import Embroidery Files

Open an embroidery file as you would open any SVG file in Inkscape: `File > Open...` > choose your file and click `Open`.

It will open your file in [Manual Stitch Mode](/docs/stitches/stroke/#manual-stitch-mode). You can edit individual points and finetune your design. Once your are satisfied, save the file as described below.

## Export Embroidery Files

### Method 1

Ink/Stitch version 1.10.0 introduced the possibility to export files directly through Inkscapes `File > Save as...` (`Ctrl + Shift + S`) dialog.

Select a file format that your embroidery machine can read and `Save` the file in your desired output directory.

![File Format Field](/assets/images/docs/export-selection-field.jpg)

For later changes make sure that you keep an SVG version of your design as well.

### Method 2 (Display Stitch Plan)
To export your designs run `Extensions > Embroidery > Embroider...`.

![Embroider...](/assets/images/docs/embroider.jpg){: width="450" }

Settings|Description
---|---
Collapse length (mm)|0.0 - 10.0
Hide other layers|Wether or not hide your original design layers while presenting the newly generated stitch plan
Output File Format|Choose a file format that your embroidery machine can read
Directory|Type your directory path, where you would like to save your file. By default, the directory used is the place where you installed the extension's Python files.

**Info:** For file format conversion Ink/Stitch uses *libembroidery* from the [Embroidermodder](https://github.com/Embroidermodder/Embroidermodder) project.
{: .notice--info }

## Batch Export

**Info:** Since Ink/Stitch version 1.10.0 it is possible to export to multiple file formats at once.
{: .notice--info }

Go to `File > Save as...` and click on the little arrow on the file format selection field to open a list of available file formats.

Navigate to your desired output folder and choose the Ink/Stitch ZIP file format. Click `Save`. You then will be asked which file formats you wish to be included.

![Batch Export](/assets/images/docs/export-batch.jpg)



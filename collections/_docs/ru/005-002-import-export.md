---
title: "Import and Export Files"
permalink: /ru/docs/import-export/
excerpt: ""
last_modified_at: 2020-10-01
toc: true
---

## Export Embroidery Files

### Method 1

Export files directly through Inkscapes `File > Save as...` (`Ctrl + Shift + S`) dialog.

Select a file format that your embroidery machine can read and `Save` the file in your desired output directory.

![File Format Field](/assets/images/docs/en/export-selection-field.jpg)

For later changes make sure that you keep an SVG version of your design as well.

### Method 2 (Display Stitch Plan)
To export your designs run `Extensions > Ink/Stitch  > Visualize and Export > Embroider...`.

![Embroider...](/assets/images/docs/en/embroider.jpg){: width="450" }

Settings|Description
---|---
Collapse length (mm)|0.0 - 10.0
Hide other layers|Wether or not hide your original design layers while presenting the newly generated stitch plan
Output File Format|Choose a file format that your embroidery machine can read
Directory|Type your directory path, where you would like to save your file. By default, the directory used is the place where you installed the extension's Python files.

**Info:** For file format conversion Ink/Stitch uses [*pyembroidery*](https://github.com/inkstitch/pyembroidery).
{: .notice--info }

Ink/Stich will create a file named `something.___`, where `something` is the name of your svg file (e.g. `something.svg`) and `___` is the proper extension for the output format you select. If `something.___` already exists, it will be renamed to `something.___.1`, and `something.___.1` will be renamed to `something.___.2`, etc, up to 5 backup copies.

   <span style="color: #3f51b5;">↳ something.___</span><br />
   <span style="color: #ff9800;">↳ something.___</span>, <span style="color: #3f51b5;">something.___.1</span><br />
   <span style="color: #f44336;">↳ something.___</span>, <span style="color: #ff9800;">something.___.1</span>, <span style="color: #3f51b5;">something.___.2</span>

**Info:** In future versions this extension will be renamed to *`Show Stitch Plan`* and will not save an embroidery file anymore.
{: .notice--info}

## Batch Export

**Info:** Since Ink/Stitch version 1.10.0 it is possible to export to multiple file formats at once.
{: .notice--info }

Go to `File > Save as...` and click on the little arrow on the file format selection field to open a list of available file formats.

Navigate to your desired output folder and choose the Ink/Stitch ZIP file format. Click `Save`. You then will be asked which file formats you wish to be included.

![Batch Export](/assets/images/docs/en/export-batch.jpg)

## Import

### Embroidery Files

Open an embroidery file as you would open any SVG file in Inkscape: `File > Open...` > choose your file and click `Open`.

It will open your file in [Manual Stitch Mode](/docs/stitches/manual-stitch/). You can edit individual points and finetune your design. Once your are satisfied, save the file as described below.

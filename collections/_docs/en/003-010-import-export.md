---
title: "Import and Export Files"
permalink: /docs/import-export/
excerpt: ""
last_modified_at: 2020-05-12
toc: true
---

Ink/Stitch supports many embroidery formats. It can import and export files to the formats listed below.

## Supported File Formats (A - Z):

### Writing

CSV, **DST**, **EXP**, **JEF**, PEC, **PES**, SVG, TXT (G-CODE), U01, **VP3**

### Reading

100, 10o, BRO, DAT, DSB, **DST**, DSZ, EMD, **EXP**, EXY, FXY, GT, INB, **JEF**, JPX, KSM, MAX, MIT, NEW, PCD, PCM, PCQ, PCS, PEC, **PES**, PHB, PHC, SEW, SHV, STC, STX, TAP, TBF, TXT (G-CODE), U01, **VP3**, XXX, ZXY

**Info:** Detailed information about embroidery file formats is available in the [EduTechWiki](http://edutechwiki.unige.ch/en/Embroidery_format).
{: .notice--info }

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

## Threadlist

You can also apply a thread list to an embroidery file in Ink/Stitch. This is especially useful, if you want to work on existing embroidery files without color information (such as DST).

It could also be helpful, if you are wanting to test different color settings. You can export and import them as you like. But be careful not to change the amount and order of colors. In case you are planing to change these, you'd prefer to save the entire SVG instead.

### Usage
Run `Extensions > Ink/Stitch > Import Threadlist ...` to apply a threadlist exported by Ink/Stitch.

If you want to import any other threadlist from a txt-file, choose the option "Import other threadlist" and pick a threadlist from the dropdown menu before clicking on apply.

**Tipp:** Install Add-Ons for Ink/Stitch to have more threadlists available.
{: .notice--info }

## Import

* Run `Extensions > Ink/Stitch > Import Threadlist`
* In the dialog enter the path to your file (this dialog will be improved when we update to Inkscape 1.0)
* Choose a method depending on your file you are wanting to import. It should be a simple textfile (txt).
* If you want to import a threadlist which wasn't created through Ink/Stitch, also select a color palette to match colors
* Apply

## Export

Threadlists can only be **exported** through a zip-file ([batch export](/docs/import-export/#batch-export)).




## Print Preview

## Accessing the Print Preview

Run `Extensions > Ink/Stitch  > Print` to export the design for printing. You have the possibility to adjust some settings, choose from different templates and send it to your (PDF) printer once you are done.

## Customizations

### Editable Fields and Custom Logo
You will notice many editable fields within the print preview. Click with your mouse on the fields and enter your text. Header field customizations will populate automatically on each page.

Don't forget to pick your own logo by clicking on the Ink/Stitch logo. This will open a file picker, choose your logo and click `Open`.

**Tip:** If you change the object-order after filling in operator notes, use cut (`Ctrl+X`) and paste (`Ctrl+V`) to move them to the correct places.
{: .notice--warning }

### Stitch Preview

The design preview also has different options. You can adjust the size either by clicking on `Fit`, `100%` or by `Ctrl + Scroll` to scale seemlessly. Grab your design with the mouse and move it inside the canvas to a different place. It is also possible to apply the transformations to all pages by clicking `Apply to all`.

By default the print preview uses the line drawing mode. Check `Realistic` if you wish a realistic rendering preview. It will take a little while to calculate this view, but it's worth waiting. This setting needs to be activated to each single page where you want to use it.

![Line Drawing and Realistic render](/assets/images/docs/en/print-realistic-rendering.jpg){: width="450x" }

### Settings

Click `Settings` to access the following options.

#### Page Setup

Setting|Description
---|---
Printing Size|You can choose between `Letter` and `A4`.
Print Layouts|There are two different layout types:<br />⚬ **Embroidery machine operator layout** with color blocks, thread names, stitch counts, and custom notes<br />⚬ **Client oriented layout** designed for you to send to your customer<br />⚬ **Custom page** offers space for free text (e.g. instructions for in-the-hoop projects)
Save as defaults|*Page Setup* settings can be saved as defaults. Next time you open a print preview it will use your default settings. Linux e.g. would save it default print settings to `~/.config/inkstitch/print_settings.json`.

#### Design

Setting|Description
---|---
Thread Palette|Change the thread manufacturer palette. Ink/Stitch will choose matching color names according to your choice. It will delete all changes, which you might have previously made.

## Print / Export to PDF

Click on `Print` to open the page in your PDF-viewer from where you can print your documents. Make sure the printing size fits to your settings.  Alternatively click on `Save PDF`. This will save a PDF-output.

## Return to Inkscape

Close the print preview window to return to Inkscape.

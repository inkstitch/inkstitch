---
title: "Print PDF"
permalink: /docs/print-pdf/
last_modified_at: 2020-10-01
toc: true
---

## Accessing the Print Preview

Run `Extensions > Ink/Stitch  > Visualise and Export > Print PDF` to export the design for printing. You have the possibility to adjust some settings, choose from different templates and send it to your (PDF) printer once you are done.

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
Print Layouts|There are various layout types available:<br />⚬ **Operator layout** with color blocks, thread names, stitch counts, and custom notes for machine operators<br />⚬ **Client oriented layout** designed for you to send to your customer<br />⚬ **Full page pattern view** A whole page showing the design only, optionally displays the footer<br />⚬ **Custom page** offers space for free text (e.g. instructions for in-the-hoop projects)
Save as defaults|*Page Setup* settings can be saved as defaults. Next time you open a print preview it will use your default settings. Linux e.g. would save it default print settings to `~/.config/inkstitch/print_settings.json`.

#### Design

Setting|Description
---|---
Thread Palette|Change the thread manufacturer palette. Ink/Stitch will choose matching color names according to your choice. It will delete all changes, which you might have previously made.

## Print / Export to PDF

Click on `Print` to open the page in your PDF-viewer from where you can print your documents. Make sure the printing size fits to your settings.  Alternatively click on `Save PDF`. This will save a PDF-output.

## Return to Inkscape

Close the print preview window to return to Inkscape.

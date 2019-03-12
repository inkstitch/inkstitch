---
title: Transcript - 07 Visualize and Export - Beginner Tutorial Series
permalink: /tutorials/resources/beginner-video-tutorials/07-visualize-export-transcript
last_modified_at: 2019-03-12
language: en
image: "/assets/images/tutorials/video-preview-images/beginner-tutorial-series.png"

toc: true

exclude-from-tutorial-list: true
---
[← Back](/tutorials/resources/beginner-video-tutorials/)

## Welcome to the Ink/Stitch Beginner Tutorial Series

**In this part we are going to learn how to display your design and finally save it into an embroidery format that your machine can read.**

## Simulator

Whenever you are running the params dialogue in Ink/Stitch you will see the simulator.
This is very important while planing your design, since you can visually see the changes as you make them.

The simulator can also run without the params dialogue. In the customize tutorial we created a shortcut to open it with Ctrl+Shift+L, but this is a custom shortcut key and not available by default.
If you don't have the shortcut key set, open the simulator through `Extensions > Ink/Stitch > English > Simulator`.

- It will simulate selected objects, or - if none is selected - the whole design.
- You can speed up and slow down the simulation with arrow up and arrow down or by using the corresponding buttons.
- You can swith the playback to be backwards or forwards with arrow left or right.
- Pause and restart the animation with the space bar.
- Move the animation step by step with plus or minus.
- Restart the animation with `R`.
- You can also grab the slider and move it to an other position or jump to an specific point by entering a number.
  You should pause the simulaton before doing so.

During the animation you can see the current speed in the status bar, beside of the information if the current command is fe. a stitch, trim or stop command.

When you are done, close the simulator with `Q`.

## Print and realistic preview

While the simulator is very useful, you sometimes will need to see a realistic preview of your design. This way you can get a better impression of your stitch length settings, etc.
In Ink/Stitch you will have access to a realistic preview through the print function. The print function will open in your default browser.

Run `Extensions > Ink/Stitch > English > Print`.

The print sheet that you will see is meant to be used either by operator or customer. But before we look into these options we want to discover the realistic preview.

Move your mouse over the embroidery image. On the bottom of the canvas you will see different options to scale the design.
You can also hit Ctrl and scroll the mouse-wheel to scale it up and down. With the left mouse button you can grab it and move it somewhere else.
`Fit` will scale the design to fit into the canvas. 100% will scale it to real size. Once you are satisfied with scaling and position you can apply the transforms to all other pages where the design is displayed.

Finally we enable the `Realistic` checkbox. It may take a while before it is being displayed.

Now let's have a look into the other settings in the print sheet.

Go to settings.
First you will see basic page setup options. Depending on your country you will want to choose either `Letter` or `A4` paper format.
Then you have different layout options, depending on the purpose you want to use the print-out for.

The operator detailed view comes with an other option, where you can define the size of the thumbnails through a slider.

In the branding tab you can change the page header logo. And enter your contact information which will be displayed in the page footer.

Open the estimated time tab. Here you can specify information about your machine and workflow to roughly calculate the time that will be needed to stitch out the design.
You might not want this information to be displayed on every layout type. Disable those, where it shouldn't appear.

In the design tab you can change the thread palette. If you used palettes while editing your design in Inkscape, the print preview will already use these colors. In other cases or if you want to change the displayed thread palette you can edit the setting here. All colors in the design will be recalculated and previous changes will be lost.

Page Setup, Branding and Estimated Time settings can be saved as defaults and be used for every new design.

Close the settings dialogue and have a look to the page header.

You will see fields indicating that you can enter custom text. So you can define a title for this particular design, enter the clients name and purchase order.
On detailed views you can also change the thread and color name manually.
The operator detailed view also has a field for custom notes for each thread.

When you are done with all settings use the print button. You can print it with your printer, but in most cases you would want to print to PDF, so you can send the PDF-file to your customer or operator.

When everything is done, click on the close button to regain access to Inkscape, which has been locked while you were editing the print preview.
All settings you've made in the print preview will be saved into the SVG file, so you don't have to do everything twice in case you want to change your design.

## Embroider ...

Embroider is an older function which has been very important before the simulator existed. With the new functionality you will rarely be using it. But still there might be possible usecases.
* Open `Extensions > Ink/Stitch > English > Embroider`
The dialogue comes with a few options. You will want to set the output file format to one, that your machine can read. If you leave `Directory` empty, the output file will be saved in the Inkscape's extensions directory. You might want to change this. Enter a path.
When you hit `Apply` Ink/Stitch will perform two actions:
1. It will save an embroidery file on your computer
2. It will display the output in Inkscape - while hiding all other layers if the option was enabled in the embroider dialogue.

Now you can inspect and modify the output in Inkscape. The so newly created path is a stroke with manual stitch placement enabled.

## Save file ...

A more comfortable way to export to an embroidery file is to use the `File > Save as...` export function.
Here you can choose the file format for your machine. All file format names start with Ink/Stitch, so you can easily find them in the list.
Enter the filename and click on `Save`.
Don't forget to also save your design in the SVG file format, just in case you want to perform changes at a later time.

## Import

You can also open embroidery files with Ink/Stitch.
Just right click on the file in your file browser and choose `Open with > Inkscape`.

An other possibility would be to open Inkscape and go to `File > Open...`, choose your file in the dialgoue and click on `Open`.

Imported embroidery files will be displayed as a stroke in manual stitch mode.
For certain file formats like `dst` colors may vary from your expectations, because they cannot save color information.

We hope you enjoyed the tutorial. Now you have seen all the Ink/Stitch functions.
In the next video we will demonstrate a typical workflow and put all the pieces together.

[← Back](/tutorials/resources/beginner-video-tutorials/)

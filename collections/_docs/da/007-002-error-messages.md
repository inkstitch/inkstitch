---
title: "Error Messages"
permalink: /da/docs/error-messages/
excerpt: ""
last_modified_at: 2018-12-14
toc: true
classes: equal-tables
---

## Embroider

Error Message|Description
---|---
Seeing a 'no such option' message?<br />Please restart Inkscape to fix.|
No embroiderable paths selected.<br />Tip: use Path -> Object to Path to convert non-paths before embroidering.|Ink/Stitch will ignore every non-path object. Converting your shape to a path will solve the problem (`Ctrl+Shift+C`).
No embroiderable paths found in document.<br />Tip: use Path -> Object to Path to convert non-paths before embroidering.|Ink/Stitch will ignore every non-path object. Converting your shape to a path will solve the problem: Select all objects with `Ctrl+A` and hit `Ctrl+Shift+C` for conversion.

## Threads

Error Message|Description
---|---
Thread palette installation failed|Create an GitHub issue and describe the steps you've done so far.
Installation Failed|Create an GitHub issue and describe the steps you've done so far.

## Params

Error Message|Description
---|---
Some settings had different values across objects.  Select a value from the dropdown or enter a new one.|
Preset "%s" not found.|Preset with the given name is not existent. View a list of all available presets by clicking on the arrow beside the input field.
Preset "%s" already exists.<br />Please use another name or press "Overwrite"|You cannot `Add` presets with existent names. If you want to keep the old preset settings, change the name - otherwise use `Overwrite`.
No embroiderable paths selected.<br />Tip: use Path -> Object to Path to convert non-paths before embroidering.|Ink/Stitch will ignore every non-path object. Converting your shape to a path will solve the problem.
No embroiderable paths found in document.<br />Tip: use Path -> Object to Path to convert non-paths before embroidering.|Ink/Stitch will ignore every non-path object. Converting your shape to a path will solve the problem.

## Units

Error Message|Description
---|---
parseLengthWithUnits: unknown unit %s|
Unknown unit: %s|

## Simulate

Error Message|Description
---|---
No embroiderable paths selected.<br />Tip: use Path -> Object to Path to convert non-paths before embroidering.|Ink/Stitch will ignore every non-path object. Converting your shape to a path will solve the problem.
No embroiderable paths found in document.<br />Tip: use Path -> Object to Path to convert non-paths before embroidering.|Ink/Stitch will ignore every non-path object. Converting your shape to a path will solve the problem.

## Satin Column

Error Message|Description
---|---
One or more rails crosses itself, and this is not allowed.<br />Please split into multiple satin columns.|With *Node Edit Tool* select a node at the position where you want to split your path. Click on `Break path at selected nodes` within the *Tool Controls Bar*.<br /><br />![Split Path](/assets/images/docs/en/split-path.jpg)<br />Hit `Ctrl+Shift+K` to seperate all pieces. Recombine selected rails and rungs with `Ctrl+K`. Then apply param settings to both seperated satin columns. 
satin column: One or more of the rungs doesn't intersect both rails.|Make sure rungs intersect both rails.<br />[More information](/docs/stitches/satin-column/#rung-method)
Each rail should intersect both rungs once.|Make sure rungs intersect both rails once.<br />[More information](/docs/stitches/satin-column/#rung-method)
satin column: One or more of the rungs intersects the rails more than once.|Make sure rungs intersect rails only once. If this is already the case and you still are receiving this message, one or more rungs might be longer than the rails. In this case you should consider using the [node method](/docs/stitches/satin-column/#node-method) or to prolong the rails.
satin column: object %s has a fill (but should not)|Remove the fill color from the object:<br />`Object > Fill and Stroke...` The dialog will appear on the right side. Click the x within the fill tab.
satin column: object %(id)s has two paths with an unequal number of points (%(length1)d and %(length2)d)|Getting this message, you should consider to use the advantages of the [rung method](/docs/stitches/satin-column/#rung-method), which allows an unequal amount of nodes. Otherwise check on every node if there are dublications and count all nodes on each path.

## Stroke

Error Message|Description
---|---
Legacy running stitch setting detected!<br />It looks like you're using a stroke smaller than 0.5 units to indicate a running stitch, which is deprecated.  Instead, please set your stroke to be dashed to indicate running stitch.  Any kind of dash will work.|More information on [running stitch mode](/docs/stitches/running-stitch/)

## AutoFill

Error Message|Description
---|---
Unable to autofill.<br />This most often happens because your shape is made up of multiple sections that aren't connected.|[Fills](/docs/stitches/fill-stitch/) should be assigned to closed paths with a fill color, but there seems to be at least two gaps in your shape.<br />To find out where your path is not connected, select one node with the node edit tool and hit `Ctrl+A`. It will select all connected nodes and gaps become obvious where the selection ends.
Unexpected error while generating fill stitches. Please send your SVG file to lexelby@github.|This error message indicates that you discovered an unkown bug. Please report back to us and help Ink/Stitch to improve.

## Print

Error Message|Description
---|---
No embroiderable paths found in document.<br />Tip: use Path -> Object to Path to convert non-paths before embroidering.|Ink/Stitch will ignore every non-path object. Converting your shape to a path will solve the problem.
⚠ lost connection to Ink/Stitch|The browser lost connection to Ink/Stitch. You will still be able to print and apply changes to the document, but any changes will be lost the next time you open the print preview.

---
title: "Error Messages"
permalink: /docs/error-messages/
excerpt: ""
last_modified_at: 2018-06-12
toc: true
classes: equal-tables
---

## Embroider

Error Message|Description
---|---
Seeing a 'no such option' message?<br />Please restart Inkscape to fix.|
No embroiderable paths selected.<br />Tip: use Path -> Object to Path to convert non-paths before embroidering.|Ink/Stitch will ignore every non-path object. Converting your shape to a path will solve the problem.
No embroiderable paths found in document.<br />Tip: use Path -> Object to Path to convert non-paths before embroidering.|Ink/Stitch will ignore every non-path object. Converting your shape to a path will solve the problem.

## Threads

Error Message|Description
---|---
Thread palette installation failed|
Installation Failed|

## Params

Error Message|Description
---|---
Some settings had different values across objects.  Select a value from the dropdown or enter a new one.|
Preset "%s" not found.|
Preset "%s" already exists.  Please use another name or press "Overwrite"|

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
One or more rails crosses itself, and this is not allowed.<br />Please split into multiple satin columns.|
satin column: One or more of the rungs doesn't intersect both rails.|
Each rail should intersect both rungs once.|
satin column: One or more of the rungs intersects the rails more than once.|
satin column: object %s has a fill (but should not)|Remove the fill color from the object.
satin column: object %(id)s has two paths with an unequal number of points (%(length1)d and %(length2)d)|Getting this message, you should consider to use the advantages of the [rung method](/docs/stitches/satin/#rung-method), which allows an unequal amount of nodes. Otherwise check on every node if there are dublications and count all nodes on each path.

## Stroke

Error Message|Description
---|---
Legacy running stitch setting detected!<br />It looks like you're using a stroke smaller than 0.5 units to indicate a running stitch, which is deprecated.  Instead, please set your stroke to be dashed to indicate running stitch.  Any kind of dash will work.|More information on [running stitch mode](/docs/stitches/stroke/#running-stitch-mode)

## AutoFill

Error Message|Description
---|---
Unable to autofill.<br />This most often happens because your shape is made up of multiple sections that aren't connected.|[Fills](/docs/stitches/fill/) should be assigned to closed paths with a fill color.
Unexpected error while generating fill stitches. Please send your SVG file to lexelby@github.|This error message indicates that you discovered an unkown bug. Please report back to us and help Ink/Stitch to improve.

## Print

Error Message|Description
---|---
No embroiderable paths found in document.<br />Tip: use Path -> Object to Path to convert non-paths before embroidering.|Ink/Stitch will ignore every non-path object. Converting your shape to a path will solve the problem.
⚠ lost connection to Ink/Stitch|The browser lost connection to Ink/Stitch. You will still be able to print and apply changes to the document, but any changes will be lost the next time you open the print preview.

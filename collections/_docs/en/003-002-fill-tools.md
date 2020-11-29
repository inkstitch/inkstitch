---
title: "Fill Tools"
permalink: /docs/fill-tools/
excerpt: ""
last_modified_at: 2020-11-29
toc: true
---
## Break Apart Fill Objects

Fill objects can be treated best, if they are single elements without any crossing borders. Sometimes these rules are not easy to meet and your shape will have tiny little loops which are impossible to see in Inkscape.

Therefore error messages for fill areas happen quiet often and are annoying for users. This extension will help you to fix broken fill shapes. Run it on every fill shape which is causing trouble for you. It will repair your fill element and separate shapes with crossing borders into it's pieces if necessary.


### Usage

* Select one or more fill objects
* Run: Extensions > Ink/Stitch  > Fill Tools > Break Apart Fill Objects

## Simple or Complex

* *Simple* will handle holes, unconnected shapes and crossing border issues. Combined paths will split up into separate objects.

* *Complex* will handle everything in the same way as simple but it will additionally handle multiple path objects.

![Break apart fill objects](/assets/images/docs/en/break_apart.jpg)
[Download SVG](/assets/images/docs/en/break_apart.svg)

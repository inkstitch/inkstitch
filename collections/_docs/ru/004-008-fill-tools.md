---
title: "Fill Tools"
permalink: /ru/docs/fill-tools/
excerpt: ""
last_modified_at: 2020-12-31
toc: true
---
## Break Apart Fill Objects

Fill objects can be treated best, if they are single elements without any crossing borders. Sometimes these rules are not easy to meet and your shape will have tiny little loops which are impossible to see in Inkscape.

Therefore error messages for fill areas happen quiet often and are annoying for users. This extension will help you to fix broken fill shapes. Run it on every fill shape which is causing trouble for you. It will repair your fill element and separate shapes with crossing borders into it's pieces if necessary.

### Usage

* Select one or more fill objects
* Run: Extensions > Ink/Stitch  > Fill Tools > Break Apart Fill Objects

## Simple or Complex

Always prefer `simple` when possible. It retains holes and repairs the "border crossing error" by splitting up loops into separate objects or deletes them if they are too small to embroider.

While "simple" splits up loops, it will not respect overlapping subpaths. It will treat them as separate objects. `Complex` is capable to recognize overlapping paths and treat them well.

"Break apart fill objects" can be expressed in native Inkscape functions:
1. Path > Union (Solve subpath issues)
2. Path > Break apart (Separate objectes)
3. Delete objects which are too small to embroider
4. Path > Combine (if you want to preserve holes)
5. Path > Combine (if you want to preserve even more holes)

**Info:** For overlapping paths step 1 is only performed by `complex`.
{: .notice--info}

![Break apart fill objects](/assets/images/docs/en/break_apart.jpg)
[Download SVG](/assets/images/docs/en/break_apart.svg)

## Convert to gradient blocks

Convert to gradient blocks will split a fill with a linear gradient into multiple blocks of solid color and adapted row spacing.

### Usage

1. Apply a linear fill color gradient to an element.

   ![linear gradient](/assets/images/docs/en/linear-gradient.png)
2. Run `Extensions > Ink/Stitch > Tools: Fill > Convert to gradient blocks

   ![color blocks](/assets/images/docs/color_blocks.png)

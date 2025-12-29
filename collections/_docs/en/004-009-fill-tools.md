---
title: "Tools: Fill"
permalink: /docs/fill-tools/
last_modified_at: 2025-12-29
toc: true
---
## Break Apart Fill Objects

Fill objects can be treated best, if they are single elements without any crossing borders. Sometimes these rules are not easy to meet and your shape will have tiny little loops which are impossible to see in Inkscape.

Therefore error messages for fill areas happen quiet often and are annoying for users. This extension will help you to fix broken fill shapes. Run it on every fill shape which is causing trouble for you. It will repair your fill element and separate shapes with crossing borders into it's pieces if necessary.

### Usage

* Select one or more fill objects
* Run: Extensions > Ink/Stitch  > Fill Tools > Break Apart Fill Objects

### Simple or Complex

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

## Knockdown Fill

Helper method to generate either
- a fill area underneath all selected elements, optionally with a positive or a negative offset. This can be very useful when working with high pile fabric (usually with a positive offset) or to create global underlay (usually with a negative offset)
- a rectangle or a circle area around all selected elements (but not underneath). This can be useful to create an embossing effect.
  
![A figure with a surrounding knockdown stitch](/assets/images/docs/knockdown.png)

* Select elements
* Open `Extensions > Ink/Stitch > Tools: Fill > Selection to Knockdown Fill`
* Adapt settings (row spacing will be computed according to stitch length)
* Click apply
* Adapt fill settings in the params dialog (`Extensions > Ink/Stitch > Params`)

 
### Settings

#### Options tab

* Keep holes: Chose whether the shape should contain holes
* Offset: The offset (mm) around the selection. Offset can be positive or negative
* Method (round, miter, bevel): Influences how edges will look like
* Miter limit:  Influences how edges will look like


#### Embossing tab
* Shape: If None, the extension creates a knockdown fill area underneath the selected elements, taking into account the offset (from options tab) value. If on the other hand, you wish an embossing effect, chose between rectangle and circle to create a knockdown fill around the selected elements, excluding the area underneath the selected elements (still taking the offset into account).
* Shape offset : Any positive value will extend the embossing area. The excluded area may be modified by using the offset parameter in the options tab.
* Method (round, miter, bevel): Influences how edges will look like

Note : if the shape parameter is set to circle or rectangle, the excluded area is exactly what the knockdown fill with Shape set to None would be. If the shape offset is 0, the embossing shape is the smallest circle/rectangle that contains the excluded area.  If shape offset is positive, the outside border of the circle/rectangle is extended in every direction according to this value. The excluded area is unchanged.
## Tartan

The Stripe Editor can be found in `Extensions > Ink/Stitch > Tools: Fill > Tartan`

![A seahorse rendered with tartan fill](/assets/images/docs/en/tartan_stripe_editor.png)

### Customize

#### Positioning

The pattern can be rotated, scaled (%) and translated (mm) as a whole

#### Pattern Settings

* Symmetry: Patterns can be reflected or repeated.
  * A reflected pattern will reverse the stripes every second time (without repeated the pivot point). This means a pattern with three colors (green, black, yellow) will be rendered as follows:
  green, black, yellow, black, green, black, yellow, ...
  * A repeating sett will simply repeat the whole pattern over and over again: green black yellow, green, black, yellow, green, ...

* Equal threadcount for warp and weft
  * if disabled you can define different color setts for warp and weft
  * if enabled warp and weft are the same

#### Stripes

* Add colors with the `Add` button
* Remove colors by clicking on `X` behind a stripe
* Alter stripe positions by click and drag `⁝` (use with care)
* Enable, disable stripe rendering with the checkbox (☑)
* When equal threadcount is disabled: warp defines the vertical lines, weft defines the horizontal lines
* Click on the colored field to select an other color
* When you want to change a color in multiple stripes at once, enable `Link colors` and equal colors will update simultanously

### Palette Code

The Ink/Stitch code is what will be saved into the svg, but can also be edited directly.

A palette code looks for example like this: `(#000000)/5.0 (#FFFFFF)/?5.0`.

* Stripes are separated by spaces
* Each color is encapsulated in round brackets `(#000000)`
* A slash (`/`) indicates a symmetrical/reflective order, whereas three points at the start and end of the code (`...`) represent a asymmetrical/repeating sett `...(#000000)5.0 (#FFFFFF)?5.0...`.
* A pipe (`|`) is a separator for warp and weft and should only be used if they differ in threadcount

**Info**: The [Scottish Register of Tartans](https://www.tartanregister.gov.uk/) has a huge collection of registered tartan patterns. Ink/Stitch is capable to use their code which they send out per mail and convert it into the Ink/Stitch color code. Please respect their particular license regulations. Make sure to define the width of one tartan thread before you click on `Apply Code`.<br><br>Here's an example code you can try out: `...B24 W4 B24 R2 K24 G24 W2...` ([source](https://www.tartanregister.gov.uk/threadcount))
{: .notice--info}

### Embroidery Settings

In the embroidery settings you can decide if you want to render the tartan as a single embroidery element or if you want to receive multiple svg elements which you can edit and transform afterwards to your liking.

#### Embroidery Element

Rendering a tartan as a embroidery element will result in a uniform look with optimal stitch placement. You can set various parameters which can also be refined in the params dialog.

Please refer to the params listed on the [tartan fill page](/docs/stitches/tartan-fill/).

The only param that will only show up here is the `Minimum stripe width for fills`. Stripes smaller than this value will be rendered a running stitch/bean stitch on top of the fill stripes.

#### SVG Elements

* Define a stitch type (Legacy Fill or AutoFill) and choose your prefered stitch settings. Stripes smaller than the `Minimum stripe width for fills` value will turn into strokes (running stitches). Elements can be edited on canvas after clicking on `Apply`.

**Info**: For AutoFill the final routing will be better than shown in the simulator. Hit `Apply` can run the stitch plan to see the final result.
{: .notice--info}

## Tutorials using Tools: Fill

{% include tutorials/tutorial_list key="tool" value="Fill" %}

---
title: "Guided Fill"
permalink: /docs/stitches/guided-fill/
last_modified_at: 2024-05-06
toc: true
---
## What it is

Generate curved fill with guide lines.

![Fill stitch detail](/assets/images/docs/guided-fill-detail.jpg)

## How to Create

* Create a **closed path with a fill color**. This shape may have holes.
* Create a guide line to define stitch directions:
    * draw a line with a stroke color and without a fill color
    * select that line
    * run `Extensions > Ink/Stitch > Edit > Selection to guide line`
* Select both and group them together (`Ctrl + G`).
* Open the params dialog (`Extensions > Ink/Stitch > Params`) and select `Guided fill` as the fill method.

Each group is allowed to contain more than one fill object, but only one guide line is effective and will be used to guide all the shapes of the group, guiding each shape with the intersection of the shape and the guide line. In that case, a shape that does not intersect the guide line will be filled with a regular auto fill. The group is also allowed to contain regular stroke objects. On the canvas, a  marker allows to distinguish a guide line from a regular stroke.

![Guided Fill Group](/assets/images/docs/guided-fill-group.svg)

If the group contains several guide lines, only one is effective. If the guide line is a composite path, only one  subpath is used as a guide line. However it is possible to use sinuous guide line , that may even cross the shape border many times.

![Guided fill group](/assets/images/docs/guided-fill-complex.svg)

## Filling Strategies

Two filling strategies are allowed for guided fill:

### Copy

Copy (the default) will fill the shape with shifted copies of the line. Sometimes, in particular is the guide line has sharp angles, it may result in a very irregular covering.

### Parallel offset

Parallel offset will ensure that each line is always a consistent distance from its neighbor. Sharp corners may be introduced.

## Set Start and End Point

Set start and end points for autofill objects with [Visual commands](/docs/commands/).

## Params

Run `Extensions > Ink/Stitch  > Params` to tweak the settings to your needs.

Settings||Description
---|---|---
Automatically routed fill stitching| ☑ |Must be enabled for these settings to take effect.
Fill method                        |Guided Fill| Guided Fill must be selected.
Guided Fill Strategy               |![Guided Fill Strategies](/assets/images/docs/guidedfillstrategies.svg)| Copy( default), top, fill the shape with copies of the guide lines.  Parallel offset, bottom, will ensure that each line is always a consistent distance from its neighbor. Sharp corners may be introduced.
Expand                             ||Expand the shape before fill stitching, to compensate for gaps between shapes.
Maximum fill stitch length         ||The length of each stitch in a row. "Max" is because a shorter stitch may be used at the start or end of a row.
Spacing between rows               ||Distance between rows of stitches
Stagger rows this many times before repeating|![Stagger example](/assets/images/docs/params-fill-stagger.png) |Stitches are staggered so that neighboring rows of stitches don't all fall in the same column (which would create a distracting valley effect). Setting this dictates the length of the cycle by which successive stitch rows are staggered. Fractional values are allowed and can have less visible diagonals than integer values.
Skip last stitch in each row       |![Skip example](/assets/images/docs/params-fill-skip_stitches.png) |The last stitch in each row is quite close to the first stitch in the next row. Skipping it decreases stitch count and density.
Underpath                          |![Unterpath example](/assets/images/docs/params-fill-underpathing.png)|Must be enabled to let running stitches travel inside shape instead of around the border when moving from section to section
Running stitch length              ||Length of stitches used when moving from section to section
Running Stitch tolerance           |![Tolerance Sample](/assets/images/docs/contourfilltolerance.svg) |All stitches must be within this distance of the path.  A lower tolerance means stitches will be closer together.  A higher tolerance means sharp corners may be rounded.
Randomize stitches  |☑  |Randomize stitch length and phase instead of dividing evenly or staggering. This is recommended for closely-spaced curved fills to avoid Moiré artefacts.
Random stitch length jitter | |Amount to vary the length of each stitch by when randomizing.
Random Seed| |Rolling the dice or setting a new value will change the random stitches
Minimum stitch length         ||Overwrite global minimum stitch length setting. Shorter stitches than that will be removed.
Minimum  jump stitch  length             ||Overwrite global minimum jump stitch length setting. Shorter distances to the next object will have no lock stitches.
Allow lock stitches                ||Enables lock stitches in only desired positions
Force lock stitches                |☑ |Sew lock stitches after sewing this element, even if the distance to the next object is shorter than defined by the collapse length value in the Ink/Stitch preferences.
Tack stitch                        ||Chose your [favorite style](/docs/stitches/lock-stitches/)
Lock stitch                        ||Chose your [favorite style](/docs/stitches/lock-stitches/)
Trim After                         |☑ |Trim the thread after sewing this object.
Stop After                         |☑ |Stop the machine after sewing this object. Before stopping it will jump to the stop position (frame out) if defined.
{: .params-table }

## Underlay

Underlay in Guided Fill doesn't follow the guide line, but uses the fill angle which can be defined in the underlay [params](/docs/stitches/fill-stitch#underlay).

## Sample Files Including Guided Fill Stitches

{% include tutorials/tutorial_list key="stitch-type" value="Guided Fill" %}

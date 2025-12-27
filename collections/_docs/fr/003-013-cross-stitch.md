---
title: "Cross Stitch"
permalink: /fr/docs/stitches/cross-stitch/
last_modified_at: 2025-12-26
toc: true
---

{% include upcoming_release.html %}

## What it is


# How to Create


### Set Start and End Point

By default, an automatic fill starts as close as possible to the previous embroidery element and ends as close as possible to the next embroidery element.

To change this behavior, set start and end points for autofill objects with [Visual commands](/docs/commands/).

### Params

Run `Extensions > Ink/Stitch  > Params` to tweak the settings to your needs.

Settings||Description
---|---|---
Automatically routed fill stitching| ☑      |Must be enabled for these settings to take effect.
Fill method                        |Cross Stitch|Must be set to cross stitch.
Expand                             |![Expand example](/assets/images/docs/params-fill-expand.png) |Expand the shape before fill stitching, to compensate for gaps between shapes.
Maximum fill stitch length         |![Stitch length example](/assets/images/docs/params-fill-stitch_length.png) |The length of each stitch in a row. "Max" is because a shorter stitch may be used at the start or end of a row.
Minimum stitch length              ||Overwrite global minimum stitch length setting. Shorter stitches than that will be removed.
Minimum  jump stitch  length       ||Overwrite global minimum jump stitch length setting. Shorter distances to the next object will have no lock stitches
Allow lock stitches                ||Enables lock stitches in only desired positions
Force lock stitches                |☑ |Sew lock stitches after sewing this element, even if the distance to the next object is shorter than defined by the collapse length value in the Ink/Stitch preferences.
Tack stitch                        ||Chose your [favorite style](/docs/stitches/lock-stitches/)
Scale Tack stitch                  ||
Lock stitch                        ||Chose your [favorite style](/docs/stitches/lock-stitches/)
Scale Lock stitch                  ||
Trim After                         |☑ |Trim the thread after sewing this object.
Stop After                         |☑ |Stop the machine after sewing this object. Before stopping it will jump to the stop position (frame out) if defined.
{: .params-table }

### Sample Files Including Fill Stitches

{% include tutorials/tutorial_list key="stitch-type" value="Cross Stitch" %}

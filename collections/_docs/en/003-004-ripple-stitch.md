---
title: "Ripple Stitch"
permalink: /docs/stitches/ripple-stitch/
last_modified_at: 2025-12-29
toc: true
---
## Description

Ripple stitch is part running stitch and part fill. It behaves like a running stitch, in that it follows a path/stroke. It also behaves like a fill, in that it spreads outward from the line to cover or fill an area. It creates soft bands that resemble ripples, hence the name.

Closed shapes will be filled with a spiral (circular ripples). Open shapes will be stitched back and forth (linear ripples).

{% include folder-galleries path="butterfly-fill-project/ripple/" captions="1:Simple ripple from a closed shape;2:Satin guided ripple" %}

[<i class="fa fa-download"></i> Download sample files](/assets/images/stitch-type-butterflies/ripple_stitch.zip)

## Creation

{% include video id="cyvby3KJM10" provider="youtube" %}

### Circular Ripples

1. Create one closed path and apply a stroke color.
2. Keep it as a single path only. Avoid combined paths like shapes with holes.
3. Optional: Create [target point or guides.](#guiding-ripples)
4. Open the Params dialog: Extensions, Ink/Stitch, then [Params](#params). 
5. Set Method to Ripple.
6. Adjust the Ripple settings as you wish.
7. Click Apply.

![Circular ripple examples](/assets/images/docs/circular-ripple.svg)

[Download examples](/assets/images/docs/circular-ripple.svg){: download="circular-ripples.svg" }

### Linear Ripples

Linear ripples can be created in various ways. It can be a simple curve or it can be constructed like a satin column.

* Create a open shape (simple stroke, two combined strokes or even a satin column)
* Create [target point or guides](#guiding-ripples) (optional)
* Open params dialog (`Extensions > Ink/Stitch > Params`) and set the `method` to `Ripple`.
* Set [params](#params) to your liking and apply

![Linear ripple examples](/assets/images/docs/linear-ripple.svg)

[Download examples](/assets/images/docs/linear-ripple.svg){: download="linear-ripples.svg" }

## Looping ripples

Loops are allowed and welcomed in any ripple path. Use loops to achieve special nice effects.

![Looping ripple stitches](/assets/images/docs/ripple-loops.svg)

[Download examples](/assets/images/docs/ripple-loops.svg){: download="ripple-loop.svg" }

## Guiding ripples

Ripples with only **one subpath** (closed shape or a simple bezier curve) can be guided in either of the three following methods.

## Target point

Define a ripple target position with [visual command](/docs/commands/):

* Open `Extensions > Ink/Stitch > Commands > Attach Commands to selected objects ...`
* Select `Target position` and apply
* Select the symbol and move it to the desired position

If no guiding information is provided, the center of the path is used as the target.

## Guide line

* In the very same group (no subgroup) of the ripple stitch object create a stroke curve with the bezier tool, starting close to the ripple curve, leading away from it.
* Select that curve and run `Extensions > Ink/Stitch > Edit > Selection to guide line`.
* Select the ripple curve and run params. Adapt the parameters to your liking.

## Satin guide

With satin guides you will have the ability to lead the ripples precisely using the satin rung method. The width of the satin guide will also have an effect on the ripple width. The positioning of the original ripple shape will be ignored and it will start where the satin begins.

* In the very same group of the ripple stitch object create a [satin column](/docs/stitches/satin-column/) like object with rails and rungs.
* Select the newly created object and run `Extensions > Ink/Stitch > Edit > Selection to guide line`.
* Select the ripple object and run params. Adapt parameters to your liking.

The pattern for satin guided ripples can be adjusted in its direction with the help of a so-called anchor line.

* Draw a line from top to bottom across the pattern. The positioning corresponds to the satin rungs.
* Select the line and mark it as an anchor line via `Extensions > Ink/Stitch > Edit > Selection to anchor line`.

![satin guided ripple](/assets/images/docs/ripple_satin_guide.svg)

[Download](/assets/images/docs/ripple_satin_guide.svg){: download="satin_guided_ripples.svg" }

## Clipping

{% include upcoming_release.html %}

Ripple stitches can be clipped to form the outline.

* Create the ripple stitch
* Create the clip shape (must be on top of the ripple stitch)
* Select both and run `Object > Clip > Set clip`

## Parameters

{% include upcoming_release_params.html %}

{% include params.html stitch_type='ripple-stitch'%}

## Sample Files Including Ripple Stitches

{% include tutorials/tutorial_list key="stitch-type" value="Ripple Stitch" %}

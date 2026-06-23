---
title: "Running Stitch / Bean Stitch"
permalink: /docs/stitches/running-stitch/
last_modified_at: 2026-06-18
toc: true
---
## Description

Running stitch produces a series of small stitches following a line or curve.
A simple repetition is most of the time too thin, so that the running stitch is usually executed as a bean stitch instead. This makes the line wider and more distinct.

{% include folder-galleries path="butterfly-fill-project/running/" captions="1:Running stitch mandala (redwork)" %}

## Creation

Running stitch is created from a path with a stroke color.

The stitch direction is impacted by the [path direction](/docs/customize/#enabling-path-outlines--direction). If you want to swap the start and end points of your running stitch, use  `Path > Reverse`.

If an object consists of multiple paths, they will be stitched in order with a jump between each.

### Bean Stitch

Enable bean stitch by entering a value for the Param-Option `Bean stitch number of repeats`

## Parameters

Open `Extensions > Ink/Stitch  > Params` to update the parameters.

{% include upcoming_release_params.html %}

{% include params.html stitch_type='running-stitch'%}

## Routing

For better stitch routing of consecutives running stitches, try the extensions `Autoroute Running Stitch` and `Redwork` in the [stroke tools](/docs/stroke-tools/).

## Patterned Running Stitch

Read the [tutorial](/tutorials/patterned-unning-stitch/) how to create a patterned running stitch.

![patterned running stitch](/assets/images/tutorials/pattern-along-path/copy-paste.png)

## Sample Files Including Running Stitch

{% include tutorials/tutorial_list key="stitch-type" value="Running Stitch" %}

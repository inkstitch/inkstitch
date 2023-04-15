---
title: "Tack and Lock Stitches"
permalink: /ru/docs/stitches/lock-stitches/
excerpt: ""
last_modified_at: 2023-02-26
toc: true
---
{% include upcoming_release.html %}

Tack and lock stitches are small stitches at the beginning (tack) or the end (lock) of a color block or before and after jump stitches or trim commands. They help to secure the thread.

Ink/Stitch offers various types of tack and lock stitches and even allows to define your own.

## Default lock stitches

![Lock stitch variants](/assets/images/docs/lock-stitches.png)
{: .img-half }

1. Half stitch. This is the default and the only lock stitch available in older Ink/Stitch versions. It has no scaling option but it is relative to the stitch length: two half stitches back and two half stitches forth.
2. Arrow, scales in %
3. Back and forth, scales in mm
4. Bowtie, scales in %
5. Cross, scales in %
6. Star, scales in %
7. Triangle, scales in %
8. Zigzag, scales in %
9. Custom. Scales in % or mm depending on the path type.

## Custom lock stitches

Custom lock stitches can be defined by an svg path in mm units (scale: %) or with relative units of steps to go back and forth (scale: mm).

### Custom svg path

The svg path is always build as if it was a tack (start) lock stitching, if positioned at the end it will be reversed.

At the end of the svg path there is an extra node to indicate in which angle the path connects to the lock stitch. It will be removed when the angle has been processed.

### Custom mm path

Custom mm values are separated by a space. E.g. a custom lock stitch with a path value of 1 1 -1 -1 with a scale setting 0.7 mm will travel 0.7 mm forward (twice) and 0.7 mm backwards (twice). Path values can also be floats (e.g. 0.5 2.2 -0.5 -2.2) if the user wants to travel only fractions of the size setting.

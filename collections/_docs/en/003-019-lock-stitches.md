---
title: "Tack and Lock Stitches"
permalink: /docs/stitches/lock-stitches/
last_modified_at: 2024-09-01
toc: true
---
## What it is

Tack and lock stitches are small stitches at the beginning (tack) or the end (lock) of a color block or before and after jump stitches or trim commands. They help to secure the thread.

## Influencing Factors (When Lock Stitches Apply)

The embroidery file contains several embroidery objects which will be embroidered one after another. Lock stitches are set when between objects there is either a color change, a trim command or a long distance. `Allow lock stitches` can prevent the usage of lock stitches, while `force lock stitches` will ensure that they are present.

### Minimum Jump Stitch Length

The minimum jump stitch length value can be set in `Extension > Ink/Stitch > Preferences` and object based in the params dialog.

It defines whether the stitch between two objects is a jump stitch or a normal stitch.
Only if the distance between two objects is greater than the `minimum jump stitch length` value, a jump stitch is applied. Only if a jump stitch is used, lock stitches are added at the end of the first object and tack stitches at the begining of the second object.

![Three lines, first distance is 1mm, second distance 3mm, minimum jump stitch length is set to 2. There are no lock stitches at the first object and no tack stitches at the second](/assets/images/docs/lock_stitch_min_jump.svg)
{: .border-shadow }

But there are more parameters which can influence the question wheter tack- and lock stitches are applied.

### Color Changes

Lock and tack stitchesVerriegelungs- und Heftstiche werden vor und nach einem Farbwechsel angewendet.are applied before and after a color change.

### Trim Commands

Ink/Stitch inserts lock stitches on the object with the trim command and tack stitches on the next object.

![Three lines, distances are 1mm, minimal jump stitch lengt is set to 2. The middle line has a trim command which sets lock stitches to it and tack stitches to the next object](/assets/images/docs/lock_stitch_trim.svg)
{: .border-shadow }

Trim commands can be applied with two different methods

* either as a visual command  using  `Extension > Ink/Stitch > Commands > Attach commands to selected objects`
* or by ckecking `Trim after` in the params dialog

### Allow Lock Stitches

`Allow lock stitches` can suppress tack and/or lock stitches when they normally would apply.
{: .notice--info }

![Three lines, distances are 3 mm, minimum jump stitch length is set to 2. The middle line is set to allow lock stitches at the end only. Therefore it has no tack stitches.](/assets/images/docs/lock_stitch_allow.svg)
{: .border-shadow }

The allow lock stitch parameter can prevent lock stitches before or after the object (or both). So when the distance between two objects is big enough for a jump stitch, but the first object has set the allow lock stitches parameter to `Before`, no lock stitches will be set at the end of this object.

### Force Lock Stitches

It is however possible to force lock and tack stitches even for objects with small distances. Check the `force lock stitch` parameter of the first object to add lock stitches before the jump and tack stitches after the jump (to the second object).

![Three lines, distances are 1 mm, minimum jump stitch length is set to 2. The middle line has a force jump stitch setting, which sets lock stitches to it and tack stitches to the next one](/assets/images/docs/lock_stitch_force.svg)
{: .border-shadow }

Beware not to check force lock stitch on the second object, as you would then force the "lock stitches" for it, not the "tack stitches", plus you would force lock stitches for next object, whatever its distance from after jump object.

`Force lock stitches` will always apply lock stitches and overides the `allow lock stitches` parameter.
{: .notice--info }

## Types of Lock Stitch

Ink/Stitch offers various types of tack and lock stitches and even allows to define your own.

### Default Lock Stitches

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

### Custom lock stitches

Custom lock stitches can be defined by an svg path in mm units (scale: %) or with relative units of steps to go back and forth (scale: mm).

#### Custom svg path

The svg path is always built as if it is a tack (start) lock stitching, if positioned at the end it will be reversed.

At the end of the svg path there is an extra node to indicate in which angle the path connects to the lock stitch. It will be removed when the angle has been processed.

For instance the triangle lock stitches corresponds to the custom path  M -0.26,0.33 H 0.55 L 0,0.84 V 0 L 0.34,0.82 (this is the d attribute of the path). 
On next image, they are the black paths, on one copy the last segment is green colored for clarity.

![Triangle lock stitch](/assets/images/docs/triangle_lock.png)

Both red and blue path have a triangle tack down.

The custom svg path is rotated in such away that its last segment (green) has the same direction as the begining of red and blue paths. It is only used to compute this rotation angle, and is not part of the actual tack down, and will not be embroidered.

#### Custom mm path

Custom mm values are separated by a space. E.g. a custom lock stitch with a path value of 1  1  -1  -1 with a scale setting 0.7 mm will travel 0.7 mm forward (twice) and 0.7 mm backwards (twice). Path values can also be floats (e.g. 0.5 2.2 -0.5 -2.2) if the user wants to travel only fractions of the size setting.

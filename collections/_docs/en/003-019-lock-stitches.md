---
title: "Tack and Lock Stitches"
permalink: /docs/stitches/lock-stitches/
last_modified_at: 2024-02-25
toc: true
---
Tack and lock stitches are small stitches at the beginning (tack) or the end (lock) of a color block or before and after jump stitches or trim commands. They help to secure the thread.

Ink/Stitch allows you to add trim commands

*  either as a visual command  using  Extension < Ink/Stitch < Commands < Attach commands to selected objects
* or by ckecking "Trim after" in the parameters dialog
  
The embroidery file contains several embroidery objects that will be embroidered one after another. 

When the distance between the end of an object and the begining of the next one is larger than the  "minimum  jump stitch length"  as defined in Extension > Ink/Stitch > Preferences, then there is a jump in between the objects. In that  case,   lock stitches are added  at the end of the first object and tack stitches at the begining of the second one except if their respective  "allow lock stitches" parameter do not  allow one (or both) of them.

If this distance is smaller thant the "minimum jump stitch length", then the needle move to go from first object to second object is not a jump, but a regular stitch and no tack down stitches is added to the first object and no lock stitches to the second one, regardless their respective "allow lock stitch parameter" value.

It is however possible to force small distance jumps to have  lock and tack stitches. Check the "force lock stitch" parameter of the **before jump** object to add lock stitches before jump and tack stitches after jump. This overides the "allow lock stitches"  parameters. Beware not to check "force lock stitch" on  the after jump object, as you would then force the "lock stitches" for it, not the "tack stitches", plus you would force lock stitches for next object, whatever its distance from after jump object.



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

The svg path is always built as if it is a tack (start) lock stitching, if positioned at the end it will be reversed.

At the end of the svg path there is an extra node to indicate in which angle the path connects to the lock stitch. It will be removed when the angle has been processed.

For instance the triangle lock stitches corresponds to the custom path  M -0.26,0.33 H 0.55 L 0,0.84 V 0 L 0.34,0.82 (this is the d attribute of the path). 
On next image, this are the black paths, on one copy its last segment is colored green for clarity.

![Triangle lock stitch](/assets/images/docs/triangle_lock.png)

Both red and blue path have a triangle tack down.

The custom svg path is rotated in such away that its last segment (green) has the same direction as the begining of red and blue paths. It is only used to compute this rotation angle, and is not part of the actual tack down, and will not be embroidered.

### Custom mm path

Custom mm values are separated by a space. E.g. a custom lock stitch with a path value of 1  1  -1  -1 with a scale setting 0.7 mm will travel 0.7 mm forward (twice) and 0.7 mm backwards (twice). Path values can also be floats (e.g. 0.5 2.2 -0.5 -2.2) if the user wants to travel only fractions of the size setting.

---
title: "Preferences"
permalink: /docs/preferences/
last_modified_at: 2025-12-29
toc: true
---
The preferences are found in `Extensions > Ink/Stitch > Preferences`.

You may either set global values which will be applied to every new svg document or set document specific values that overide global ones. 
If you chose a local value as default, it will set the glocal value to the local value.

**All elements of the document are affected by theses parameters.**

## Output Settings

### Minimum jump stitch length (mm)

If a jump between two consecutive paths is shorter than this value, lock stitches at ending of first path and tack stiches at starting point of second path are only created if *Force lock stitches* is enabled in the corresponding path.  If the jump is longer, lock stitches and tack stitches are true to their settings.

Up from v 3.1.0 it is possible to overwrite the global value for single elements in the [params dialog](/doc/params).

### Minimum stitch length (mm)

#### What it is

Stitches smaller than this value will be dropped (exception: lock stitches). This value is only used at the very end of the stitch plan computation to filter too short stitches. Be aware that the behavior may not be what you expected : for instance if Minimum stitch length is set to 2mm and you have running stitches with maximum stitch length of 1.5mm, every other stich is droped, yielding a running path  with 3mm stiches.

Simulation take these parameters into account.

These are  the results of simulation for 1.5mm *running stitch length* running stitches with  *minimum stitch length* set to 0.5mm  in preference and then set to 2mm.

![simulation](/assets/images/docs/preference_msl_paths.png)

When *Minimum stitch length* is set to 2mm, except for lock stitchs, every other stitch  is dropped,  as  1.5 is smaller than 2 and 1.5+1.5 is larger than 2. The number of stitches is divided by two. Should we set *minimum stitch length* to 3.1, then we would get  4.5mm running stitches.

Up from v 3.1.0 it is possible to overwrite the global value for single elements in the [params dialog](/doc/params).

#### How it affects embroidery 

*Minimum stitch length*  also affects the **sides of fills** (in a similar way as skip last stitch of row, - a good option for dense fills) if set to value smaller than the *row spacing*. It also affects **sharp corners** of running stitches where actual stitch length may be much lower than *running  stitch  length* (tolerance is important there).

*Minimum stitch length* |  automatic fill with 0.25 row spacing| guided fill with 0.25 row spacing|running stitch length 1.5mm but very small design(10mm width)
---|---|---|---
0|![square 0](/assets/images/docs/preference_fill_0.png)|![square 0](/assets/images/docs/preference_guided_0.png)|![running_0](/assets/images/docs/preference_running_stitch_0.png)
0.5|![square 0.5](/assets/images/docs/preference_fill_half.png)|![square 0.5](/assets/images/docs/preference_guided_half.png)|![running_0](/assets/images/docs/preference_running_stitch_half.png)
1|![square 1](/assets/images/docs/preference_fill_1.png)|![square 1](/assets/images/docs/preference_guided_1.png)|![running_0](/assets/images/docs/preference_running_stitch_1.png)

It also affects **Satin stiches** and threfore lettering fonts. You do not want that on **small fonts** such as *Ink/Stitch small* or *Glacial Tiny* :

*Minimum stitch length* |*Ink/Stitch Small*|*Glacial Tiny*
---|---|---
0 or 0.5 |![ink_stitch_O](/assets/images/docs/preference_ink_small_0.png)|![glacial_O](/assets/images/docs/preference_glacial_0.png)
1|![ink_stitch_1](/assets/images/docs/preference_ink_small_1.png)|![glacial_1](/assets/images/docs/preference_glacial_1.png)

**Manual stitches** are also affected by minimum stitch length preference. You can take advantage of this to reduce manual  stitches without getting very short stitches. Some deformation may happen, but usually the result is quite good.

**W6 machine owners:** Set your global minimum stitch length value at least to 0.3 mm, otherwise your stitch out may have missing stitches where you wouldn't expect them.
{: .notice--warning }

### For this document only : Rotate on export
{% include upcoming_release.html %}
This option rotates the embroidery 90°. Is useful when the embroidery  machine does not automatically rotate to fit the hoop.

### Global only: Cache size (mb)

Defines how much space on your harddrive can be occupied with cached stitch plans. 

The higher the value the more stitch plans can be cached. 

A cached stitch plan doesn't need to be rendered again which will speed up rendering time significantly.

Defaults to 100.

You may clear cache from global preferences.




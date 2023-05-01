---
title: "Preferences"
permalink: /docs/preferences/
excerpt: ""
last_modified_at: 2023-04-30
toc: false
---
The current version (v 2.2.0) does not have global settings.

{% include upcoming_release.html %}

The preferences are found in `Extensions > Ink/Stitch > Preferences`.

You can either set global values which will be applied to every new svg document. Also you can set document specific values.

## Output Settings


* **Minimum jump stitch length (mm)**: 
  *  Any shorter jump between subpaths of a composite path will be treated as a normal stitch (no lock stitches added)
  *  In case of a jump beetween two succcesive paths, if the jump between the two paths is shorter than this value, lock stitches at ending point and tack stiches at starting point are only created if Force lock stitches is enabled in the corresponding path.  If the jump is longer, lock stitches and tack stitches are true to their settings.
  
* **Minimum stitch length (mm)**: Stitches smaller than this value will be dropped (exception: lock stitches). This value is only used at the very end of the stitch plan computation to filter too short stitches. Be aware that the behavior is may be not what you expected : for instance if Minimum stitch length is set to 2mm and you have running stitches with maximum stitch length of 1.5mm, every other stich is dropped, yielding a running path  with 3mm stiches. 

Simulation take these parameters into account.


* Global only: **Cache size (mb)** defines how much space on your harddrive can be occupied with cached stitch plans. The higher the value the more stitch plans can be cached. A cached stitch plan doesn't need to be rendered again which will speed up rendering time significantly. Defaults to 100.

**W6 machine owners:** Set your global minimum stitch length value at least to 0.3 mm, otherwise your stitch out may have missing stitches where you wouldn't expect them.
{: .notice--warning }

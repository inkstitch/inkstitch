---
title: "Preferences"
permalink: /da/docs/preferences/
excerpt: ""
last_modified_at: 2022-06-24
toc: false
---
The current version (v 2.2.0) does not have global settings.

{% include upcoming_release.html %}

The preferences are found in `Extensions > Ink/Stitch > Preferences`.

You can either set global values which will be applied to every new svg document. Also you can set document specific values.

## Output Settings

* **Minimum jump stitch length (mm)**: Jump stitches smaller than this will be treated as normal stitches (no lock stitches).
* **Minimum stitch length (mm)**: Stitches smaller than this value will be dropped (exception: lock stitches).

* Global only: **Cache size (mb)** defines how much space on your harddrive can be occupied with cached stitch plans. The higher the value the more stitch plans can be cached. A cached stitch plan doesn't need to be rendered again which will speed up rendering time significantly. Defaults to 100.

**W6 machine owners:** Set your global minimum stitch length value at least to 0.3 mm, otherwise your stitch out may have missing stitches where you wouldn't expect them.
{: .notice--warning }

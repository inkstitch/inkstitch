---
title: "Auberge Marif"
permalink: /fonts/auberge_marif/
last_modified_at: 2023-04-24
toc: false
preview_image:
  - url: /assets/images/fonts/auberge_small.jpg
    height: 20
  - url: /assets/images/fonts/auberge_marif.jpg
    height: 50
---
{%- assign font = site.data.fonts.auberge_marif.font -%}

![auberge_marif](/assets/images/fonts/auberge_marif.jpg)

![auberge_small](/assets/images/fonts/auberge_small.jpg)

## Glyphs

This font contains  {{ font.glyphs.size }} glyphs:

```
{{ font.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Dimensions:

At a scale of 100% this font has an approximate height of {{ font.size }} mm. 

It can be scaled from {{ font.min_scale | times: 100 | floor }}% ({{ font.size | times: font.min_scale }} mm)
up to {{ font.max_scale | times: 100 | floor }}% ({{ font.size | times: font.max_scale }} mm).

![Dimensions Auberge](/assets/images/fonts/Sizing/aubergesizing.jpg)

Don't try to scale it further down. 

Auberge Small  is a variation of this font with different embroidery settings. Pull compensation, density and underlays are different to allow to scale down between 55% (28mm,  1 inch) and 25% (12mm ,1/2 inch). 

That's why in the lettering dialog window, if using Auberge Small, you will have to pick up a scale between 25 and 55%. 

Contrarily to Auberge Marif, Auberge Small font **MUST** be embroidered with thread and needle smaller than usual.
A USA 8 (EUR 60) size needle, and 60WT thread **MUST** be used.

## In real life
From 25% on the T shirt to full size on the apron and the label

{% include folder-galleries path="fonts/grand_hotel_marif/" %}


[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/auberge_marif/LICENSE)

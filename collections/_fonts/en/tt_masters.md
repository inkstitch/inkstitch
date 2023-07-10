---
title: "TT Masters"
permalink: /fonts/tt_masters/
last_modified_at: 2022-05-26
toc: false
preview_image:
  - url: /assets/images/fonts/tt_masters.jpg
    height: 20
---
{%- assign font = site.data.fonts.tt_masters.font -%}

![TT Masters](/assets/images/fonts/tt_masters.jpg)

## Glyphs

This font contains  {{ font.glyphs.size }} glyphs:

{% for glyph in font.glyphs %}
{{ glyph }}
{%- endfor %}

## Dimensions

At 100%, this font is approximatively 20 mm (approx 0.8 inch) tall.

It may be scaled up to  300% (approx 60 mm 2.5 inches ) but should not be scaled down.

## Remarks
This font use Auto Route Satin.

It is possible to stitch lines of text back and forth.


## In real life 
{% include folder-galleries path="fonts/TT_masters/" %}




[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/tt_masters/LICENSE)

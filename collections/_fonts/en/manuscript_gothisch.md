---
title: "Manuskript Gothisch"
permalink: /fonts/manuscript_gothisch/
last_modified_at: 2022-05-27
toc: false
preview_image:
  - url: /assets/images/fonts/manuscript_gothisch.jpg
    height: 30
---
{%- assign font = site.data.fonts.manuskript_gotisch.font -%}
![ManuscriptGothisch](/assets/images/fonts/manuscript_gothisch.jpg)

## Glyphs

This font contains  {{ font.glyphs.size }} glyphs:

{% for glyph in font.glyphs %}
{{ glyph }}
{%- endfor %}

## Dimensions

At 100%, this font is approximatively 30 mm (1 1/4 inch) high.

It can be scaled up to 140% (approx. 42 mm, 1 2/3  inches) or scaled down to  70% (approx.  21 mm, 0.8 inch).


## In real life


{% include folder-galleries path="fonts/manuscript_gothisch/" %}

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/manuskript_gotisch/LICENSE)

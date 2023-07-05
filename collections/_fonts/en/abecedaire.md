---
title: "Abecedaire"
permalink: /fonts/abecedaire/
last_modified_at: 2022-05-26
toc: false
preview_image:
  - url: /assets/images/fonts/abecedaire.jpg
    height: 14
---
{%- assign font = site.data.fonts.abecedaire.font -%}
![Abecedaire](/assets/images/fonts/abecedaire.jpg)

## Glyphs

This font contains  {{ font.glyphs.size }} glyphs:

{% for glyph in font.glyphs %}
{{ glyph }}
{%- endfor %}

## Dimensions

At a scale of 100% this font has an approximate height of {{ font.size }} mm. 

It can be scaled from {{ font.min_scale | times: 100 | floor }}% ({{ font.size | times: font.min_scale }} mm)
up to {{ font.max_scale | times: 100 | floor }}% ({{ font.size | times: font.max_scale }} mm).


## In real life

{% include folder-galleries path="fonts/abecedaire/" %}



[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/abecedaire/LICENSE)

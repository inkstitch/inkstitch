---
title: "Baumans FI"
permalink: /fonts/baumans/
last_modified_at: 2022-05-26
toc: false
preview_image:
  - url: /assets/images/fonts/baumans_fi.jpg
    height: 32
---
{%- assign font = site.data.fonts.baumans_FI.font -%}
![Baumans](/assets/images/fonts/baumans_fi.jpg)

## Glyphs

This font contains  {{ font.glyphs.size }} glyphs:

{% for glyph in font.glyphs %}
{{ glyph }}
{%- endfor %}
 
## Remark

Baumans FI is reversible : a multi line embroidery  may be  embroidered in alternate directions

## Dimensions

At 100%, this font is roughly 32 mm high (1.25 in).

It may be scaled up to 150% (approx. 48 mm, 2 inches) or down to 80% (approx. 25mm , 1 inch)


## In real life

{% include folder-galleries path="fonts/baumans/" %}

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/baumans_FI/LICENSE)

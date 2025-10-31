---
title: "גופן בינוני"
permalink: /fonts/hebrew_font/
last_modified_at: 2025-02-17
toc: false
preview_image:
  - url: /assets/images/fonts/hebrew_font_large.png
    height: 35
  - url: /assets/images/fonts/hebrew_font_medium.png
    height: 23

data_title:
  - hebrew_font_large
  - hebrew_font_medium
---
{%- assign font1 = site.data.fonts.hebrew_font_large.font -%}

{%- assign font2 = site.data.fonts.hebrew_font_medium.font -%}

<img 
     src="/assets/images/fonts/hebrew_font_large.png"
     alt="hebrew_font_large" height="35">

<img 
     src="/assets/images/fonts/hebrew_font_medium.png"
     alt="Emilio20" height="23">

## Glyphs

These fonts contain  {{ font1.glyphs.size }} glyphs:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Dimensions

### Large

At a scale of 100% this font has an approximate height of {{ font1.size }} mm.

It can be scaled from {{ font1.min_scale | times: 100 | floor }}% ({{ font1.size | times: font1.min_scale }} mm)
up to {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm).

### Medium

It can be scaled from {{ font2.min_scale | times: 100 | floor }}% ({{ font2.size | times: font2.min_scale }} mm)
up to {{ font2.max_scale | times: 100 | floor }}% ({{ font2.size | times: font2.max_scale }} mm).

## Special features

Each glyph contains the  original letter, in the form of a hidden path with red fill. These fills are not intended to be embroidered as is, but to help anyone who wants to modify this font. They can be ignored safely.

## In real life

{% include folder-galleries path="fonts/hebrew_font/" %}

## License

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/hebrew_font_medium/LICENSE)

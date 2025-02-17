---
title: "פשוט מעוגל"
permalink: /fonts/hebrew_simple_rounded/
last_modified_at: 2025-02-17
toc: false
preview_image:
  - url: /assets/images/fonts/hebrew_simple_rounded.png
    height: 23
  - url: /assets/images/fonts/hebrew_simple_rounded_small.png
    height: 6

data_title:
  - hebrew_simple_rounded
  - hebrew_simple_rounded_small
---
{%- assign font1 = site.data.fonts.hebrew_simple_rounded.font -%}

{%- assign font2 = site.data.fonts.hebrew_simple_rounded_small.font -%}

{% include upcoming_release.html %}

<img 
     src="/assets/images/fonts/hebrew_simple_rounded.png"
     alt="Hebrew simple  rounded " height="23">
     

## Glyphs

These fonts contain  {{ font1.glyphs.size }} glyphs:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Dimensions

### Computer

At a scale of 100% this font has an approximate height of {{ font1.size }} mm.

It can be scaled from {{ font1.min_scale | times: 100 | floor }}% ({{ font1.size | times: font1.min_scale }} mm)
up to {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm).

### Computer Small
It can be scaled from {{ font2.min_scale | times: 100 | floor }}% ({{ font2.size | times: font2.min_scale }} mm)
up to {{ font2.max_scale | times: 100 | floor }}% ({{ font2.size | times: font2.max_scale }} mm).

This font **requires thin thread (60) and thin needle (60)**


## Special features
Each glyph contains the  original letter, in the form of a hidden black path. These paths are not intended to be embroidered as is, but to help anyone who wants to modify this font. They can be ignored safely.

## In real life

{% include folder-galleries path="fonts/hebrew_simple_rounded/" %}

## License

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/hebrew_simple_rounded/LICENSE)

---
title: "Ink/Stitch Masego"
permalink: /fonts/inkstitch-masego/
last_modified_at: 2025-03-14
toc: false
preview_image:
  - url: /assets/images/fonts/inkstitch_masego.png
    height: 17
data_title:
  - inkstitch_masego
---
{%- assign font = site.data.fonts.inkstitch_masego.font -%}

{% include upcoming_release.html %}

![Inkstitch Masego](/assets/images/fonts/inkstitch_masego.png)

## Glyphs

This font contains  {{ font.glyphs.size }} glyphs:

```
{{ font.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Dimensions

At a scale of 100% this font has an approximate height of {{ font.size }} mm. 

It can be scaled from {{ font.min_scale | times: 100 | floor }}% ({{ font.size | times: font.min_scale }} mm)
up to {{ font.max_scale | times: 100 | floor }}% ({{ font.size | times: font.max_scale }} mm).

## In real life

{% include folder-galleries path="fonts/inkstitch_masego/" %}

## License

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/inkstitch_masego/LICENSE)

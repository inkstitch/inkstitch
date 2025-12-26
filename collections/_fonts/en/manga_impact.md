---
title: "Shojumaru"
permalink: /fonts/manga_impact/
last_modified_at: 2025-12-26
toc: false
preview_image:
  - url: /assets/images/fonts/manfa_impact.png
    height: 20
data_title:
  - manga_impact
---
{%- assign font = site.data.fonts.manga_impact.font -%}
![Manga Impact](/assets/images/fonts/manga_impact.png)

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

{% include folder-galleries path="fonts/manga_impact/" %}

## License

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/manga_impact/LICENSE)

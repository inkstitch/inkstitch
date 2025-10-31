---
title: "Bluenesia Satin"
permalink: /fonts/bluenesia/
last_modified_at: 2025-05-05
toc: false
preview_image:
  - url: /assets/images/fonts/bluenesia_satin.png
    height: 24
data_title:
  - bluenesia
---
{%- assign font = site.data.fonts.bluenesia.font -%}

![Bluenesia](/assets/images/fonts/bluenesia_satin.png)

## Glyphs

This font contains {{ font.glyphs.size }} glyphs:

```
{{ font.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Dimensions

At a scale of 100% this font has an approximate height of {{ font.size }} mm. 

It can be scaled from {{ font.min_scale | times: 100 | floor }}% ({{ font.size | times: font.min_scale }} mm)
up to {{ font.max_scale | times: 100 | floor }}% ({{ font.size | times: font.max_scale }} mm).

## In real life

{% include folder-galleries path="fonts/bluenesia_satin/" %}

## License

[Download font license](https://github.com/inkstitch/inkstitch/tree/main/fonts/bluenesia_satin/LICENSE)

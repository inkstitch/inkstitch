---
title: "Pixel 10"
permalink: /fonts/pixel10/
last_modified_at: 2025-01-04
toc: false
preview_image:
  - url: /assets/images/fonts/pixel_10.png
    height: 53
data_title:
  - pixel10
---
{%- assign font = site.data.fonts.pixel10.font -%}

{% include upcoming_release.html %}

![Pixel 10](/assets/images/fonts/pixel_10.png)

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

{% include folder-galleries path="fonts/pixel10/" %}

## License

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/pixel10/LICENSE)

---
title: "Western light"
permalink: /fonts/western_light/
last_modified_at: 2025-01-04
toc: false
preview_image:
  - url: /assets/images/fonts/western_light.png
    height: 53
data_title:
  - western_light
---
{%- assign font = site.data.fonts.western_light.font -%}

![Western light](/assets/images/fonts/western_light.png)

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

{% include folder-galleries path="fonts/western_light/" %}

## License

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/western_light/LICENSE)

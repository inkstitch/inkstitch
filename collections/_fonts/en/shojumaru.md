---
title: "Shojumaru"
permalink: /fonts/shojumaru/
last_modified_at: 2024-06-18
toc: false
preview_image:
  - url: /assets/images/fonts/shojumaru.png
    height: 20
---
{%- assign font = site.data.fonts.shojumaru.font -%}

{% include upcoming_release.html %} ![Shojumaru](/assets/images/fonts/shojumaru.png)

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

{% include folder-galleries path="fonts/shojumaru/" %}



[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/shojumaru/LICENSE)

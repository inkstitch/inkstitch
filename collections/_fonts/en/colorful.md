---
title: "Colorful"
permalink: /fonts/colorful/
last_modified_at: 2024-05-11
toc: false
preview_image:
  - url: /assets/images/fonts/colorful.png
    height: 40
---
{%- assign font = site.data.fonts.colorful.font -%}

{% include upcoming_release.html %} 

![colorful](/assets/images/fonts/colorful.png)

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

## Too much work ?
Each letter has its own tartan, therefore embroidering it as is, is not for the faint of heart ! Quite a few threads changes are required. However for a less work intense (but also less colorful) variation with only one tartan shared by all leters (or only a few tartans, each shared by several letters) see [this](https://inkstitch.org//fr/tutorials/make_tartan_font_easier/) 



## In real life

{% include folder-galleries path="fonts/colorful/" %}



[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/colorful/LICENSE)

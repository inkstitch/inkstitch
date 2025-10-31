---
title: "Gingo200"
permalink: /fonts/gingo200/
last_modified_at: 2025-05-28
toc: false
preview_image:
  - url: /assets/images/fonts/gingo200.png
    height: 36
data_title:
  - gingo200
---
{%- assign font = site.data.fonts.gingo200.font -%}
![gingo200](/assets/images/fonts/gingo200.png)

## Glyphs

This font contains  {{ font.glyphs.size }} glyphs:

```
{{ font.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Dimensions

At a scale of 100% these fonts have an approximate height of {{ font.size }} mm. 

They can be scaled from {{ font.min_scale | times: 100 | floor }}% ({{ font.size | times: font.min_scale }} mm)
up to {{ font.max_scale | times: 100 | floor }}% ({{ font.size | times: font.max_scale }} mm).

## In real life

{% include folder-galleries path="fonts/gingo200/" %}

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/gingo200/LICENSE)

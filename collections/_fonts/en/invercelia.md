---
title: "Invercelia"
permalink: /fonts/invercelia/
last_modified_at: 2024-05-12
toc: false
preview_image:
  - url: /assets/images/fonts/invercelia.png
    height: 19
---
{%- assign font = site.data.fonts.invercelia.font -%}

{% include upcoming_release.html %} 

![Invercellia](/assets/images/fonts/invercelia.png)

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

{% include folder-galleries path="fonts/invercelia/" %}



[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/invercelia/LICENSE)

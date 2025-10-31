---
title: "Chicken Scratch"
permalink: /fonts/chicken_scratch/
last_modified_at: 2024-04-24
toc: false
preview_image:
  - url: /assets/images/fonts/chicken_scratch.jpg
    height: 28
data_title:
  - chicken_scratch
---
{%- assign font = site.data.fonts.chicken_scratch.font -%}

![chicken_scratch](/assets/images/fonts/chicken_scratch.jpg)

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

{% include folder-galleries path="fonts/chicken_scratch/" %}

## License

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/chicken_scratch/LICENSE.txt)

---
title: "Cats"
permalink: /fonts/cats/
last_modified_at: 2024-04-27
toc: false
preview_image:
  - url: /assets/images/fonts/cats.jpg
    height: 40
data_title:
  - cats
---
{%- assign font = site.data.fonts.cats.font -%}

![Cats](/assets/images/fonts/cats.jpg)

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

The cats' ruffled hairs are due to the addition of randomness parameters on the satin columns. For more relaxed cats, copy the setting of a non  random satin  to all the random satins.

## In real life

{% include folder-galleries path="fonts/cats/" %}

## License

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/cats/LICENSE)

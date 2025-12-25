---
title: "Abecedaire"
permalink: /fonts/abecedaire/
last_modified_at: 2025-11-02
toc: false
preview_image:
  - url: /assets/images/fonts/abecedaire.jpg
    height: 14
data_title:
  - abecedaire
---
{%- assign font = site.data.fonts.abecedaire.font -%}

![Abecedaire](/assets/images/fonts/abecedaire.jpg)

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

## Origin of the font

The letters are inspired by a page from the book (late 19th century) Dessins de broderie - Stickmuster buch Heft 185

## In real life

{% include folder-galleries path="fonts/abecedaire/" %}


## License

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/abecedaire/LICENSE)

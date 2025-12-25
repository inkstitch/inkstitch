---
title: "Mai En Fleur AGS"
permalink: /fonts/mai_en_fleur/
last_modified_at: 2025-12-25
toc: false
preview_image:
  - url: /assets/images/fonts/mai_en_fleur.jpg
    height: 100
data_title:
  - mai_en_fleur
---
{%- assign font = site.data.fonts.mai_en_fleur.font -%}
![April En Fleur AGS](/assets/images/fonts/mai_en_fleur.jpg)

## Glyphs

This font contains {{ font.glyphs.size }} glyphs:

```
{{ font.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Dimensions

At a scale of 100% this font has an approximate height of {{ font.size }} mm.

It can be scaled from {{ font.min_scale | times: 100 | floor }}% ({{ font.size | times: font.min_scale }} mm) up to {{ font.max_scale | times: 100 | floor }}% ({{ font.size | times: font.max_scale }} mm).


## Origin of the font

This font is a derivative of Abril FatFace regular 400pt (141mm) (https://fonts.google.com/specimen/Abril+Fatface?family=Abril+Fatface)


## In real life

{% include folder-galleries path="fonts/abril/" %}

## License

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/abril/LICENSE)

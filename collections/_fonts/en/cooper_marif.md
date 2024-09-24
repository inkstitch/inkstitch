---
title: "CooperMarif"
permalink: /fonts/cooper_marif/
last_modified_at: 2024-06-23
toc: false
preview_image:
  - url: /assets/images/fonts/cooper_marif.png
    height: 90
data_title:
  - cooper_marif
---
{%- assign font = site.data.fonts.cooper_marif.font -%}
![Cooper Marif](/assets/images/fonts/cooper_marif.png)

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

{% include folder-galleries path="fonts/cooper_marif/" %}

## License

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/cooper_marif/LICENSE)

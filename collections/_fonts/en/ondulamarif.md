---
title: "Ondulamarif"
permalink: /fonts/ondulamarif/
last_modified_at: 2024-05-12
preview_image:
  - url: /assets/images/fonts/ondulamarif_XL.png
    height: 110
  - url: /assets/images/fonts/ondulamarif_Medium.png
    height: 70
---
{%- assign font2 = site.data.fonts.ondulamarif_Medium.font -%}
{%- assign font1 = site.data.fonts.ondulamarif_XL.font -%}


## Ondulamarif XL

![Ondulamarif XL](/assets/images/fonts/ondulamarif_XL.png)

### Glyphs

This font contains  {{ font1.glyphs.size }} glyphs:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }
### Dimensions
At a scale of 100% this font has an approximate height of {{ font1.size }} mm. 

It can be scaled from {{ font1.min_scale | times: 100 | floor }}% ({{ font1.size | times: font1.min_scale }} mm)
up to {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm).

## Ondulamarif Medium
![Ondulamarif Medium](/assets/images/fonts/ondulamarif_Medium.png)

### Glyphs

This font contains  {{ font2.glyphs.size }} glyphs:

```
{{ font2.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

### Dimensions
This variation allow for a smaller scale

It can be used  from {{ font2.min_scale | times: 100 | floor }}% ({{ font1.size | times: font2.min_scale }} mm)
up to {{ font2.max_scale | times: 100 | floor }}% ({{ font2.size | times: font1.max_scale }} mm).

## In real life

{% include folder-galleries path="fonts/ondulamarif/" %}

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/ondulamarif_XL/LICENSE)

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/ondulamatif_Medium/LICENSE)

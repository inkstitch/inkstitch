---
title: "Venezia"
permalink: /fonts/venezia/
last_modified_at: 2025-09-07
toc: false
preview_image:
 - url: /assets/images/fonts/venezia.png
   height: 17
 - url: /assets/images/fonts/venezia_small.png
   height: 12
data_title:
  - venezia
  - venezia_small
---
{%- assign font1 = site.data.fonts.venezia.font -%}
{%- assign font2 = site.data.fonts.venezia_small.font -%}

{% include upcoming_release.html %}

![Venezia](/assets/images/fonts/venezia.png)

![Venezia Small](/assets/images/fonts/venezia_small.png)

## Glyphs

### Venezia

This font contains  {{ font1.glyphs.size }} glyphs:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

### Venezia Small

This font contains  {{ font2.glyphs.size }} glyphs:

```
{{ font2.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Dimensions

### Venezia

At a scale of 100% this font has an approximate height of {{ font1.size }} mm. 

It can be scaled from {{ font1.min_scale | times: 100 | floor }}% ({{ font1.size | times: font1.min_scale }} mm)
up to {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm).

### Venezia Small

At a scale of 100% this font has an approximate height of {{ font2.size }} mm. 

It can be scaled from {{ font2.min_scale | times: 100 | floor }}% ({{ font2.size | times: font2.min_scale }} mm)
up to {{ font2.max_scale | times: 100 | floor }}% ({{ font2.size | times: font2.max_scale }} mm).

## In real life 

{%include folder-galleries path="fonts/neon/" %}

## License

[Download Venezia License](https://github.com/inkstitch/inkstitch/tree/main/fonts/neon/LICENSE)

[Download Venezia Small Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/neon_blinking/LICENSE)

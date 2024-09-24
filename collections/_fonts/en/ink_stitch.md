---
title: "Ink/Stitch"
permalink: /fonts/ink_stitch/
last_modified_at: 2020-12-31
toc: false
preview_image:
  - url: /assets/images/fonts/inkstitch_small.jpg
    height: 6
    title: "Ink/Stitch small"
  - url: /assets/images/fonts/inkstitch_medium.jpg
    height: 19
    title: "Ink/Stitch Medium"
data_title:
  - small_font
  - medium_font
---
{%- assign font1 = site.data.fonts.small_font.font -%}
{%- assign font2 = site.data.fonts.medium_font.font -%}

![Ink/Stitch Small](/assets/images/fonts/inkstitch_small.jpg)
![Ink/Stitch Medium](/assets/images/fonts/inkstitch_medium.jpg)

## Glyphs

Both fonts contain {{ font1.glyphs.size }} glyphs:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Dimensions

### Ink/Stitch Small

At 100%, Ink/Stitch Small is about 6 mm (1/4 inch) high.

It can be used  from {{ font2.min_scale | times: 100 | floor }}% ({{ font1.size | times: font2.min_scale }} mm)
up to {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font2.max_scale }} mm)
but should not be scaled down.

### Ink/Stitch Medium

At 100%, Ink/Stitch Medium is about  19 mm (3/4 inch) high.

It can be scaled from {{ font2.min_scale | times: 100 | floor }}% ({{ font2.size | times: font2.min_scale }} mm)
up to {{ font2.max_scale | times: 100 | floor }}% ({{ font2.size | times: font2.max_scale }} mm).

## Remark

Both fonts are reversible : a multi line embroidery  may be  embroidered in alternate directions

## In real life

{% include folder-galleries path="fonts/inkstitch/" %}

## License

[Download Ink/Stitch Small Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/small_font/LICENSE)

[Download Ink/Stitch Medium Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/medium_font/LICENSE)

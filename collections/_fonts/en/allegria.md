---
title: "Allegria"
permalink: /fonts/allegria/
last_modified_at: 2025-10-02
toc: false
preview_image:
 - url: /assets/images/fonts/allegria20.png
   height: 20
 - url: /assets/images/fonts/allegria55.png
   height: 55
data_title:
  - allegria20
  - allegria55
---
{%- assign font = site.data.fonts.allegria20.font -%}
{%- assign font2 = site.data.fonts.allegria55.font -%}

{% include upcoming_release.html %}

![Allegria20](/assets/images/fonts/allegria20.png)

![Allegria 55](/assets/images/fonts/allegria55.png)


## Glyphs

### Allegria 20

This font contains  {{ font.glyphs.size }} glyphs:

```
{{ font.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

### Allegria 55

This font contains  {{ font2.glyphs.size }} glyphs:

```
{{ font2.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Dimensions

### Allegria 20

At a scale of 100% this font has an approximate height of {{ font.size }} mm. 

It can be scaled from {{ font.min_scale | times: 100 | floor }}% ({{ font.size | times: font.min_scale }} mm)
up to {{ font.max_scale | times: 100 | floor }}% ({{ font.size | times: font.max_scale }} mm).

### Allegria 55

At a scale of 100% this font has an approximate height of {{ font2.size }} mm. 

It can be scaled from {{ font2.min_scale | times: 100 | floor }}% ({{ font2.size | times: font2.min_scale }} mm)
up to {{ font2.max_scale | times: 100 | floor }}% ({{ font2.size | times: font2.max_scale }} mm).



## Legal Information

This font is a derivative of [{{font.original_font}}]({{font.original_font_url}}) and is licensed under {{font.font_license}}.

[Download Allegria 20 Font License](https://github.com/inkstitch/embroidery-fonts/blob/main/src/allegria20/LICENSE)

[Download Allegria 55 Font License](https://github.com/inkstitch/embroidery-fonts/blob/main/src/allegria55/LICENSE)

## In real life 

{%include folder-galleries path="fonts/allegria/" %}


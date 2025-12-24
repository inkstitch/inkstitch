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
{%- assign font1 = site.data.fonts.allegria20.font -%}
{%- assign font2 = site.data.fonts.allegria55.font -%}

{% include upcoming_release.html %}

![Allegria20](/assets/images/fonts/allegria20.png)

![Allegria 55](/assets/images/fonts/allegria55.png)

## Glyphs

### Allegria 20

This font contains  {{ font1.glyphs.size }} glyphs:

```
{{ font1.glyphs | sort | join: ' ' }}
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

At a scale of 100% this font has an approximate height of {{ font1.size }} mm. 

It can be scaled from {{ font1.min_scale | times: 100 | floor }}% ({{ font1.size | times: font1.min_scale }} mm)
up to {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm).

### Allegria 55

At a scale of 100% this font has an approximate height of {{ font2.size }} mm. 

It can be scaled from {{ font2.min_scale | times: 100 | floor }}% ({{ font2.size | times: font2.min_scale }} mm)
up to {{ font2.max_scale | times: 100 | floor }}% ({{ font2.size | times: font2.max_scale }} mm).


## In real life 

{%include folder-galleries path="fonts/allegria/" %}

## Legal Information

This font is a derivative of [{{font1.original_font}}]({{font1.original_font_url}}) and is licensed under {{font1.font_license}}.

[Download Allegria 20 Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/allegria20/LICENSE)

[Download Allegria 55 Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/allegria55/LICENSE)

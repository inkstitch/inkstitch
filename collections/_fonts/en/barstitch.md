---
title: "Barstitch"
permalink: /fonts/barstitch_bold/
last_modified_at: 2025-01-04
toc: false
preview_image:
  - url: /assets/images/fonts/barstitch_bold.png
    height: 12
  - url: /assets/images/fonts/barstitch_textured.png
    height: 20
data_title:
  - barstitch_bold
  - barstitch_textured
---
{%- assign font1 = site.data.fonts.barstitch_bold.font -%}
{%- assign font2 = site.data.fonts.barstitch_textured.font -%}
{% include upcoming_release.html %}

<img 
     src="/assets/images/fonts/barstitch_bold.png"
     alt="Barstitch Bold" height="23">

<img 
     src="/assets/images/fonts/barstitch_textured.png"
     alt="Barstitch textured" height="40">

## Glyphs

These fonts contains  {{ font1.glyphs.size }} glyphs:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Dimensions
### Barstitch Bold

At a scale of 100% this font has an approximate height of {{ font1.size }} mm. 

It can be scaled from {{ font1.min_scale | times: 100 | floor }}% ({{ font1.size | times: font1.min_scale }} mm)
up to {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm).

### Barstitch textured

At a scale of 100% this font has an approximate height of {{ font2.size }} mm. 

It can be scaled from {{ font2.min_scale | times: 100 | floor }}% ({{ font2.size | times: font2.min_scale }} mm)
up to {{ font2.max_scale | times: 100 | floor }}% ({{ font2.size | times: font2.max_scale }} mm).


## In real life

{% include folder-galleries path="fonts/barstitch/" %}

## License

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/barstitch_bold/LICENSE)

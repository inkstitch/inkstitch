---
title: "Barstitch"
permalink: /fr/fonts/barstitch_bold/
last_modified_at: 2025-02-10
toc: false
preview_image:
  - url: /assets/images/fonts/barstitch_bold.png
    height: 12
  - url: /assets/images/fonts/barstitch_regular.png
    height: 12
  - url: /assets/images/fonts/barstitch_textured.png
    height: 20
  - url: /assets/images/fonts/barstitch_mandala.png
    height: 45
  - url: /assets/images/fonts/barstitch_cloudy.png
    height: 45
data_title:
  - barstitch_bold
  - barstitch_regular
  - barstitch_textured
  - barstitch_mandala
  - barstitch_cloudy
---
{%- assign font1 = site.data.fonts.barstitch_bold.font -%}
{%- assign font2 = site.data.fonts.barstitch_textured.font -%}
{%- assign font3 = site.data.fonts.barstitch_mandala.font -%}

<img
     src="/assets/images/fonts/barstitch_bold.png"
     alt="Barstitch Bold" height="23">

<img
     src="/assets/images/fonts/barstitch_regular.png"
     alt="Barstitch Bold" height="23">

<img
     src="/assets/images/fonts/barstitch_textured.png"
     alt="Barstitch textured" height="40">

<img
     src="/assets/images/fonts/barstitch_mandala.png"
     alt="Barstitch textured" height="90">

<img
     src="/assets/images/fonts/barstitch_cloudy.png"
     alt="Barstitch textured" height="90">

## Glyphes

Ces fontes comportent  {{ font1.glyphs.size }} glyphes:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Dimensions

### Barstitch Bold et Barstitch Regular

A une échelle de  100% ces fontes ont une hauteur approximative de  {{ font1.size }} mm. 

Elle peuvent être redimensionnées de {{ font1.min_scale | times: 100 | floor }}% ({{ font1.size | times: font1.min_scale }} mm)
à {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm).

### Barstitch textured

A une échelle de  100% cette fonte a une hauteur approximative de  {{ font2.size }} mm. 

Elle peut être redimensionnée de {{ font2.min_scale | times: 100 | floor }}% ({{ font2.size | times: font2.min_scale }} mm)
à  {{ font2.max_scale | times: 100 | floor }}% ({{ font2.size | times: font2.max_scale }} mm).

### Barstitch Mandala et Barstitch Cloudy

A une échelle de  100% ces fontes ont une hauteur approximative de  {{ font3.size }} mm. 

Elle peuvent être redimensionnées de {{ font3.min_scale | times: 100 | floor }}% ({{ font3.size | times: font3.min_scale }} mm)
à  {{ font3.max_scale | times: 100 | floor }}% ({{ font3.size | times: font3.max_scale }} mm).

## Dans la vraie vie 

{% include folder-galleries path="fonts/barstitch/" %}

## License

[Télécharger la license](https://github.com/inkstitch/inkstitch/tree/main/fonts/barstitch_bold/LICENSE)

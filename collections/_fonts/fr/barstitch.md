---
title: "Barstitch"
permalink: /fr/fonts/barstitch_bold/
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

## Glyphes

Ces fontes comportent  {{ font.glyphs.size }} glyphes:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }


## Dimensions
### Barstitch Bold

A une échelle de  100% cette fonte a une hauteur approximative de { {{ font1.size }} mm. 

Elle peut être redimensionnée de {{ font1.min_scale | times: 100 | floor }}% ({{ font1.size | times: font1.min_scale }} mm)
à {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm).

### Barstitch textured

A une échelle de  100% cette fonte a une hauteur approximative de  {{ font2.size }} mm. 

Elle peut être redimensionnée de {{ font2.min_scale | times: 100 | floor }}% ({{ font2.size | times: font2.min_scale }} mm)
à  {{ font2.max_scale | times: 100 | floor }}% ({{ font2.size | times: font2.max_scale }} mm).


## Dans la vraie vie 

{% include folder-galleries path="fonts/barstitch/" %}

## License

[Télécharger la license](https://github.com/inkstitch/inkstitch/tree/main/fonts/barstitch_bold/LICENSE)

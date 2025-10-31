---
title: "גופן בינוני"
permalink: /fr/fonts/hebrew_font/
last_modified_at: 2025-02-17
toc: false
preview_image:
  - url: /assets/images/fonts/hebrew_font_large.png
    height: 35
  - url: /assets/images/fonts/hebrew_font_medium.png
    height: 23

data_title:
  - hebrew_font_large
  - hebrew_font_medium
---
{%- assign font1 = site.data.fonts.hebrew_font_large.font -%}

{%- assign font2 = site.data.fonts.hebrew_font_medium.font -%}

<img 
     src="/assets/images/fonts/hebrew_font_large.png"
     alt="hebrew_font_large" height="35">

<img 
     src="/assets/images/fonts/hebrew_font_medium.png"
     alt="Emilio20" height="23">

## Glyphes

Ces fontes contiennent  {{ font1.glyphs.size }} glyphes:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Dimensions

### Large

A une échelle de 100% cette fonte mesure environ {{ font1.size }} mm de haut.
Peut être diminuée jusqu'à  {{ font1.min_scale | times: 100 | floor }}% ({{ font1.size | times: font1.min_scale }} mm)
et agrandie jusqu'à  {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm).

### Medium

Peut être utilisée  de  {{ font2.min_scale | times: 100 | floor }}% ({{ font2.size | times: font2.min_scale }} mm)
à {{ font2.max_scale | times: 100 | floor }}% ({{ font2.size | times: font2.max_scale }} mm). 

## Particularités

Chaque glyphe contient la forme de la lettre originelle, sous forme d'un remplissage rouge caché. 
Ces chemins ne sont pas prévus pour être brodés tels quels, mais pour aider qui voudrait modifier cette fonte. 

Ils peuvent être ignorés sans souci.

## Dans la vraie vie

{% include folder-galleries path="fonts/hebrew_font/" %}

## License

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/hebrew_font_medium/LICENSE)

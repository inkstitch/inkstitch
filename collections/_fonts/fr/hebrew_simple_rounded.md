---
title: "פשוט מעוגל"
permalink: /fr/fonts/hebrew_simple_rounded/
last_modified_at: 2025-02-17
toc: false
preview_image:
  - url: /assets/images/fonts/hebrew_simple_rounded.png
    height: 23
  - url: /assets/images/fonts/hebrew_simple_rounded_small.png
    height: 6

data_title:
  - hebrew_simple_rounded
  - hebrew_simple_rounded_small
---
{%- assign font1 = site.data.fonts.hebrew_simple_rounded.font -%}

{%- assign font2 = site.data.fonts.hebrew_simple_rounded_small.font -%}

<img
     src="/assets/images/fonts/hebrew_simple_rounded.png"
     alt="Hebrew simple  rounded " height="23">

<img
     src="/assets/images/fonts/hebrew_simple_rounded_small.png"
     alt="Hebrew simple  rounded " height="10">     

## Glyphes

Ces fontes contiennent  {{ font1.glyphs.size }} glyphes:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Dimensions

### Hebrew Simple Rounded Font

A une échelle de 100% cette fonte mesure environ {{ font1.size }} mm de haut.
Peut être diminuée jusqu'à  {{ font1.min_scale | times: 100 | floor }}% ({{ font1.size | times: font1.min_scale }} mm)
et agrandie jusqu'à  {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm).

### Hebrew Simple Rounded  Font Small

Peut être utilisée  de  {{ font2.min_scale | times: 100 | floor }}% ({{ font2.size | times: font2.min_scale }} mm)
à {{ font2.max_scale | times: 100 | floor }}% ({{ font2.size | times: font2.max_scale }} mm). 
**Cette fonte necessite l'usage de fil fin (60) et d'une aiguille fine (60)**

## Particularités

Chaque glyphe contient la forme de la lettre originelle, sous forme d'un chemin noir caché. 
Ces chemins ne sont pas prévus pour être brodés tels quels, mais pour aider qui voudrait modifier cette fonte. 

Ils peuvent être ignorés sans souci.

## Dans la vraie vie

{% include folder-galleries path="fonts/hebrew_simple_rounded/" %}

## License

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/hebrew_simple_rounded/LICENSE)

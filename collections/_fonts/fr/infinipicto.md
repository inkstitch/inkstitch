---
title: "InfiniPicto"
permalink: /fr/fonts/infinipicto/
last_modified_at: 2022-05-08
toc: false
preview_image:
  - url: /assets/images/fonts/infinipicto.png
    height: 70
data_title:
  - infinipicto
---
{%- assign font = site.data.fonts.infinipicto.font -%}
![InfiniPicto](/assets/images/fonts/infinipicto.png)

## Glyphes

Cette fonte comporte  {{ font.glyphs.size }} glyphes:

```
{{ font.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Description
Infinipicto est une collection de pictogrammes. Chaque lettre représente un objet stylisé dont elle est l'initiale en français : A pour Arrosoir, B pour Bateau...

![Sample ](/assets/images/fonts/infinipicto3.jpg)

## Dimensions

A une échelle de  100% cette fonte a une hauteur approximative de  {{ font.size }} mm. 

Elle peut être redimensionnée  de {{ font.min_scale | times: 100 | floor }}% ({{ font.size | times: font.min_scale }} mm)
à {{ font.max_scale | times: 100 | floor }}% ({{ font.size | times: font.max_scale }} mm).



## Tri des couleurs

À cause de la variété de lettres, rien ne garantit que les couleurs puissent être facilement triées. Faire attention, donc.

## Dans la vraie vie 

InfiniPicto sur un T shirt.

{% include folder-galleries path="fonts/infinipicto/" %}


[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/infinipicto/LICENSE)

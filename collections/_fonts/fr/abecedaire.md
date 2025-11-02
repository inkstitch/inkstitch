---
title: "Abécédaire"
permalink: /fr/fonts/abecedaire/
last_modified_at: 2025-11-02
toc: false
preview_image:
  - url: /assets/images/fonts/abecedaire.jpg
    height: 14
data_title:
  - abecedaire
---
{%- assign font = site.data.fonts.abecedaire.font -%}

![Abecedaire](/assets/images/fonts/abecedaire.jpg)

## Glyphes

Cette fonte comporte  {{ font.glyphs.size }} glyphes:

```
{{ font.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }


## Dimensions

A une échelle de  100% cette fonte a une hauteur approximative de  {{ font.size }} mm. 

Elle peut être redimensionnée  de {{ font.min_scale | times: 100 | floor }}% ({{ font.size | times: font.min_scale }} mm)
à {{ font.max_scale | times: 100 | floor }}% ({{ font.size | times: font.max_scale }} mm).

### Origine de la fonte

Ce lettrage a été inspiré par une page du livre Dessins de broderie - Stickmuster buch Heft 185 (fin 19ème siècle)


## Dans la vraie vie 

{% include folder-galleries path="fonts/abecedaire/" %}



[Télécharger la license de la police](https://github.com/inkstitch/inkstitch/tree/main/fonts/abecedaire/LICENSE)

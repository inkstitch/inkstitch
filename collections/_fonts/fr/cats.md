---
title: "Cats"
permalink: /fr/fonts/cats/
last_modified_at: 2024-04-28
toc: false
preview_image:
  - url: /assets/images/fonts/cats.jpg
    height: 40
data_title:
  - cats
---
{%- assign font = site.data.fonts.cats.font -%}

![Cats](/assets/images/fonts/cats.jpg)

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

Les poils ébouriffés des chats sont dus à l'ajout d'aléatoire sur les colonnes satin. Pour des chats plus relaxés, recopier le paramétrage d'un satin sans aléatoire sur tous les satins aléatoires.


## Dans la vraie vie

{% include folder-galleries path="fonts/cats/" %}

[Télécharger la licence](https://github.com/inkstitch/inkstitch/tree/main/fonts/cats/LICENSE)

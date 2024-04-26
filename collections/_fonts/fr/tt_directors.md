---
title: "TT Directors"
permalink: /fr/fonts/tt_directors/
last_modified_at: 2022-05-27
toc: false
preview_image:
  - url: /assets/images/fonts/tt_directors.jpg
    height: 20
---
{%- assign font = site.data.fonts.tt_directors.font -%}
![TT Directors](/assets/images/fonts/tt_directors.jpg)

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

## Remarque
Cette fonte utilise l'arrangement automatique des colonnes satin. 
Pour un texte multiligne il est possible de broder alternativement de la gauche vers la droite  et de la droite vers la gauche.
Il est possible d'ajouter des commandes de coupe de fil.

	


[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/tt_directors/LICENSE)

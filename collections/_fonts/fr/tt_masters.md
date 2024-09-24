---
title: "TT Masters"
permalink: /fr/fonts/tt_masters/
last_modified_at: 2022-05-27
toc: false
preview_image:
  - url: /assets/images/fonts/tt_masters.jpg
    height: 20
data_title:
  - tt_masters
---
{%- assign font = site.data.fonts.tt_masters.font -%}
![TT Masters](/assets/images/fonts/tt_masters.jpg)
# Glyphes

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

## Dans la vraie vie 
{% include folder-galleries path="fonts/TT_masters/" %}

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/tt_masters/LICENSE)

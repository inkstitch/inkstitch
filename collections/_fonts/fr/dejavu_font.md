---
title: "DejaVu Serif"
permalink: /fr/fonts/dejavu_font/
last_modified_at: 2022-05-05
toc: false
preview_image:
  - url: /assets/images/fonts/dejavu_serif.jpg
    height: 22
---
{%- assign font = site.data.fonts.dejavufont.font -%}
## Serif Semi-condensed

![Deja Vue Serif Semi-condensed](/assets/images/fonts/dejavu_serif.jpg)

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



## Particularité

Déja Vu peut être brodée de gauche à droite, de droite à gauche, de haut en bas, de bas en haut.

## Dans la vraie vie

Utilisée seule ou en compagnie d'*Amitaclo* et de *Magnolia KOR* sur les pots de conserves.

{% include folder-galleries path="fonts/dejavu/" %}


[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/dejavufont/LICENSE)

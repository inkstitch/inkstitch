---
title: "Magnolia KOR"
permalink: /fr/fonts/magnolia-script/
last_modified_at: 2024-05-29
toc: false
preview_image:
  - url: /assets/images/fonts/magnolia_small.jpg
    height: 15
  - url: /assets/images/fonts/magnolia_KOR.jpg
    height: 31
  - url: /assets/images/fonts/magnolia_bicolor.png
    height: 47
  - url: /assets/images/fonts/magnolia_tamed.png
    height: 47
data_title:
  - magnolia_KOR
  - magnolia_small
  - magnolia_bicolor
  - magnolia_tamed
---
{%- assign font = site.data.fonts.magnolia_KOR.font -%}
{%- assign font2 = site.data.fonts.magnolia_small.font -%}
{%- assign font3 = site.data.fonts.magnolia_bicolor.font -%}
{%- assign font4 = site.data.fonts.magnolia_tamed.font -%}

<img 
     src="/assets/images/fonts/magnolia_small.jpg"
     alt="Magnolia small" height="50">

<img 
     src="/assets/images/fonts/magnolia_KOR.jpg"
     alt="Magnolia KOR" height="100">

<img 
     src="/assets/images/fonts/magnolia_bicolor.png"
     alt="Magnolia bicolor" height="150">

<img 
     src="/assets/images/fonts/magnolia_tamed.png"
     alt="Magnolia tamed" height="150">

## Glyphes

Ces fontes comportent  {{ font.glyphs.size }} glyphes:

```
{{ font.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Dimensions

### Magnolia KOR

A une échelle de  100% cette fonte a une hauteur approximative de  {{ font.size }} mm. 

Elle peut être redimensionnée  de {{ font.min_scale | times: 100 | floor }}% ({{ font.size | times: font.min_scale }} mm)
à {{ font.max_scale | times: 100 | floor }}% ({{ font.size | times: font.max_scale }} mm).

### Magnolia Smalll

La fonte Magnolia Small est une déclinaison de  Magnolia KOR avec des paramètres de broderie différents. La densité, la compensation et les sous-couches ont été modifiées pour permettre de broder cette fonte en plus petite taille.

Dans la fenêtre de dialogue du lettrage, il vous sera demandé si vous choisissez  Magnolia Small d'indiquer un redimensionnement entre {{ font2.min_scale | times: 100 | floor }} et {{ font2.max_scale | times: 100 | floor }}% de la taille de la fonte  Magnolia KOR initiale, passant ainsi de lettres d'environ {{ font2.size }} mm de haut à des lettres mesurant entre  ({{ font2.size | times: font2.min_scale }} et  ({{ font2.size | times: font2.max_scale }} mmm.

Contrairement à  Magnolia KOR, cette fonte diminuée DOIT être brodée avec un fil et une aiguille plus fins que d'ordinaire. Une aiguille de taille 8 (USA), 60 (EUR) et un fil 60 WT DOIVENT être utilisés.

### Magnolia Bicolor 

A une échelle de  100% cette fonte a une hauteur approximative de  {{ font3.size }} mm. 

Elle peut être redimensionnée  de {{ font3.min_scale | times: 100 | floor }}% ({{ font3.size | times: font3.min_scale }} mm)
à {{ font3.max_scale | times: 100 | floor }}% ({{ font3.size | times: font3.max_scale }} mm).


### Magnolia tamed

A une échelle de  100% cette fonte a une hauteur approximative de  {{ font4.size }} mm. 

Elle peut être redimensionnée  de {{ font4.min_scale | times: 100 | floor }}% ({{ font4.size | times: font4.min_scale }} mm)
à {{ font4.max_scale | times: 100 | floor }}% ({{ font4.size | times: font4.max_scale }} mm).

## Tri des couleurs

Si vous utilisez Magnolia bicolor / Magnolia tamed, vous pouvez souhaiter trier les couleurs.
C'est possible à condition que le tri respecte l'ordre  des couleurs de chaque lettre. [Voici un moyen de le faire](https://inkstitch.org/fr/docs/lettering/#color-sorting)

## Dans la vraie vie

{% include folder-galleries path="fonts/magnolia_KOR/" %}

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/magnolia_KOR/LICENSE)

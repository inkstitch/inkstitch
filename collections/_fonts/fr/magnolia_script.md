---
title: "Magnolia KOR"
permalink: /fr/fonts/magnolia-script/
last_modified_at: 2022-05-27
toc: false
preview_image:
  - url: /assets/images/fonts/magnolia_small.jpg
    height: 11
  - url: /assets/images/fonts/magnolia_KOR.jpg
    height: 31

---
{%- assign font = site.data.fonts.magnolia_KOR.font -%}

<img 
     src="/assets/images/fonts/magnolia_small.jpg"
     alt="Magnolia_small" height="50">

<img 
     src="/assets/images/fonts/magnolia_KOR.jpg"
     alt="Magnolia" height="100">     
     

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

{% include upcoming_release.html %}

La fonte Magnolia Small est une déclinaison de  Magnolia KOR avec des paramètres de broderie différents. La densité, la compensation et les sous-couches ont été modifiées pour permettre de broder cette fonte en plus petite taille.

Dans la fenêtre de dialogue du lettrage, il vous sera demandé si vous choisissez  Magnolia Small d'indiquer un redimensionnement entre 25 et 50% de la taille de la fonte  Magnolia KOR initiale, passant ainsi de lettres d'environ 22 mm de haut à des lettres mesurant entre 8 et 15 mm.

Contrairement à  Magnolia KOR, cette fonte diminuée DOIT être brodée avec un fil et une aiguille plus fins que d'ordinaire. Une aiguille de taille 8 (USA), 60 (EUR) et un fil 60 WT DOIVENT être utilisés.

## Dans la vraie vie

{% include folder-galleries path="fonts/magnolia_KOR/" %}

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/magnolia_%20KOR/LICENSE)

---
title: "Excalibur KOR"
permalink: /fr/fonts/excalibur_kor/
last_modified_at: 2024-04-21
toc: false
preview_image:
  - url: /assets/images/fonts/excalibur_KOR.jpg
    height: 19
  - url: /assets/images/fonts/excalibur_small.jpg
    height: 7
data_title:
  - excalibur_KOR
  - excalibur_small
---
{%- assign font = site.data.fonts.excalibur_KOR.font -%}
![ExcaliburKOR](/assets/images/fonts/excalibur_KOR.jpg)

![Excalibursmall](/assets/images/fonts/excalibur_small.jpg)

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

La fonte Excalibur Small  est une déclinaison de Excalibur KOR avec des paramètres de broderie différents. La densité, la compensation et les sous-couches ont été modifiées pour permettre de broder cette fonte en plus petite taille. 

Dans la fenêtre de dialogue du lettrage, il vous sera demandé si  vous choisissez Excalibur Small  d'indiquer un redimensionnement entre 25 et 50% de la taille de la fonte Excalibur KOR initiale, passant ainsi de lettres d'environ 20 mm de haut à des lettres mesurant entre 5 et 10 mm.

Contrairement à Excalibur KOR, cette fonte diminuée **DOIT** être brodée avec un fil et une aiguille plus fins que d'ordinaire. Une aiguille de taille 8 (USA), 60 (EUR) et un fil 60 WT **DOIVENT** être utilisés.

## Dans la vraie vie
{% include folder-galleries path="fonts/excalibur_KOR/" %}

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/excalibur_KOR/LICENSE)

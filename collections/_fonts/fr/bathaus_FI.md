---
title: "Bathaus FI"
permalink: /fr/fonts/bathaus_FI/
last_modified_at: 2025-12-25
toc: false
preview_image:
  - url: /assets/images/fonts/bathaus_FI.png
    height: 32
  - url: /assets/images/fonts/bathaus_FI_small.png
    height: 10
data_title:
  - bathaus_FI
  - bathaus_FI_Small
---
{%- assign font = site.data.fonts.bathaus_FI.font -%}
![Bathauss](/assets/images/fonts/bathaus_FI.png)

![Bathaus](/assets/images/fonts/bathaus_FI_small.png)

## Glyphes

Cette fonte comporte  {{ font.glyphs.size }} glyphes:

```
{{ font.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

 
## Particularités

Si la broderie fait plusieurs lignes, elle peut  être brodée  alternativement dans les deux sens pour éviter les longs sauts de fil.

## Dimensions

A une échelle de  100% cette fonte a une hauteur approximative de  {{ font.size }} mm. 

Elle peut être redimensionnée  de {{ font.min_scale | times: 100 | floor }}% ({{ font.size | times: font.min_scale }} mm)
à {{ font.max_scale | times: 100 | floor }}% ({{ font.size | times: font.max_scale }} mm).

La fonte Bathaus FI Small  est une déclinaison de Bathaus FI avec des paramètres de broderie différents. La densité, la compensation et les sous-couches ont été modifiées pour permettre de broder cette fonte en plus petite taille. 

Dans la fenêtre de dialogue du lettrage, il vous sera demandé si  vous choisissez Bathaus FI Small d'indiquer un redimensionnement entre 15 et 30% de la taille de la fonte Bathaus FI initiale, passant ainsi de lettres d'environ 32 mm de haut à des lettres mesurant entre 5 et 10 mm.

Contrairement à Bathaus FI, cette fonte diminuée **DOIT** être brodée avec un fil et une aiguille plus fins que d'ordinaire. Une aiguille de taille 8 (USA), 60 (EUR) et un fil 60 WT **DOIVENT** être utilisés.


## Dans la vraie vie

{% include folder-galleries path="fonts/bathaus_FI/" %}


[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/bathaus_FI/LICENSE)

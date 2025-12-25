---
title: "Mai En Fleur AGS"
permalink: /de/fonts/mai_en_fleur/
last_modified_at: 2025-12-25
toc: false
preview_image:
  - url: /assets/images/fonts/mai_en_fleur_AGS.jpg
    height: 100
data_title:
  - mai_en_fleur
---
{%- assign font = site.data.fonts.mai_en_fleur.font -%}
![Mai En Fleur AGS](/assets/images/fonts/mai_en_fleur_AGS.jpg)

## Ursprung der Schriftart

Diese Schriftart wurde auf Grundlage der Schriftart Abril FatFace regular 400pt (141 mm) für Ink/Stitch entwickelt (https://fonts.google.com/specimen/Abril+Fatface?family=Abril+Fatface).

## Schriftzeichen

Diese Schrift enthält  {{ font.glyphs.size }} Schriftzeichen:

```
{{ font.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Maße

Bei einer Skalierung von 100% hat die Schrift eine ungefähre Höhe von {{ font.size }} mm.

Sie kann von {{ font.min_scale | times: 100 | floor }}% ({{ font.size | times: font.min_scale }} mm) bis zu {{ font.max_scale | times: 100 | floor }}% ({{ font.size | times: font.max_scale }} mm) skaliert werdens.

Bei einer Skalierung von 100% hat die Schrift eine ungefähre Höhe von {{ font1.size }} mm.

Sie kann von {{ font1.min_scale | times: 100 | floor }}% ({{ font1.size | times: font1.min_scale }} mm) bis zu {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm) skaliert werdens.

## Impressionen

{% include folder-galleries path="fonts/mai_en_fleur/" %}

## Lizenz

[Lizenz herunterladen](https://github.com/inkstitch/inkstitch/tree/main/fonts/abril/LICENSE)

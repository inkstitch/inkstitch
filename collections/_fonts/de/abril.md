---
title: "Abril En Fleur AGS"
permalink: /de/fonts/abril/
last_modified_at: 2023-04-24
toc: false
preview_image:
  - url: /assets/images/fonts/abril_en_fleur.jpg
    height: 100
data_title:
  - abril
---
{%- assign font = site.data.fonts.abril.font -%}
![April En Fleur AGS](/assets/images/fonts/abril_en_fleur.jpg)

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

{% include folder-galleries path="fonts/abril/" %}

## Lizenz

[Lizenz herunterladen](https://github.com/inkstitch/inkstitch/tree/main/fonts/abril/LICENSE)

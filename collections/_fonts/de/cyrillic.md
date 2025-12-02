---
title: "Кирилиця"
permalink: /de/fonts/cyrillic/
last_modified_at: 2025-09-07
toc: false
preview_image:
 - url: /assets/images/fonts/cyrillic.png
   height: 25
data_title:
  - cyrillic
---
{%- assign font1 = site.data.fonts.cyrillic.font -%}

{% include upcoming_release.html %}

![Cyrillic](/assets/images/fonts/cyrillic.png)

## Schriftzeichen

Diese Schrift enthält {{ font1.glyphs.size }} Schriftzeichen:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Maße

Bei einer Skalierung von 100% hat die Schrift eine ungefähre Höhe von {{ font1.size }} mm. 

Sie kann von {{ font1.min_scale | times: 100 | floor }}% ({{ font1.size | times: font1.min_scale }} mm)
bis zu {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm) skaliert werdens.

## Impressionen

{%include folder-galleries path="fonts/cyrillic/" %}

## Lizenz

[Lizenz herunterladen (Cyrillic)](https://github.com/inkstitch/inkstitch/tree/main/fonts/cyrillic/LICENSE)

---
title: "Venezia"
permalink: /de/fonts/venezia/
last_modified_at: 2025-09-07
toc: false
preview_image:
 - url: /assets/images/fonts/venezia.png
   height: 17
 - url: /assets/images/fonts/venezia_small.png
   height: 12
data_title:
  - venezia
  - venezia_small
---
{%- assign font1 = site.data.fonts.venezia.font -%}
{%- assign font2 = site.data.fonts.venezia_small.font -%}

{% include upcoming_release.html %}

![Venezia](/assets/images/fonts/venezia.png)

![Venezia Small](/assets/images/fonts/venezia_small.png)

## Schriftzeichen

### Venezia

Diese Schrift enthält {{ font1.glyphs.size }} Schriftzeichen:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

### Venezia Small

Diese Schrift enthält {{ font2.glyphs.size }} Schriftzeichen:

```
{{ font2.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Maße

### Venezia

Bei einer Skalierung von 100% hat die Schrift eine ungefähre Höhe von {{ font1.size }} mm. 

Sie kann von {{ font1.min_scale | times: 100 | floor }}% ({{ font1.size | times: font1.min_scale }} mm)
bis zu {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm) skaliert werdens.

### Venezia Small

Bei einer Skalierung von 100% hat die Schrift eine ungefähre Höhe von {{ font2.size }} mm. 

Sie kann von {{ font2.min_scale | times: 100 | floor }}% ({{ font2.size | times: font2.min_scale }} mm)
bis zu {{ font2.max_scale | times: 100 | floor }}% ({{ font2.size | times: font2.max_scale }} mm) skaliert werdens.

## Impressionen

{%include folder-galleries path="fonts/neon/" %}

## Lizenz

[Lizenz herunterladen (Venezia)](https://github.com/inkstitch/inkstitch/tree/main/fonts/neon/LICENSE)

[Lizenz herunterladen (Venezia Small Font)](https://github.com/inkstitch/inkstitch/tree/main/fonts/neon_blinking/LICENSE)

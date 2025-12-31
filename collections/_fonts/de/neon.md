---
title: "Neon"
permalink: /de/fonts/neon/
last_modified_at: 2025-09-07
toc: false
preview_image:
 - url: /assets/images/fonts/neon.png
   height: 50
 - url: /assets/images/fonts/neon_blinking.png
   height: 30
data_title:
  - neon
  - neon_blinking
---
{%- assign font1 = site.data.fonts.neon.font -%}
{%- assign font2 = site.data.fonts.neon_blinking.font -%}

{% include upcoming_release.html %}

![Neon](/assets/images/fonts/neon.png)

![Neon Blinking](/assets/images/fonts/neon_blinking.png)

## Schriftzeichen

### Neon

Diese Schrift enthält {{ font1.glyphs.size }} Schriftzeichen:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

### Neon Blinking

Diese Schrift enthält {{ font2.glyphs.size }} Schriftzeichen:

```
{{ font2.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Maße

### Neon

Bei einer Skalierung von 100% hat die Schrift eine ungefähre Höhe von {{ font1.size }} mm. 

Sie kann von {{ font1.min_scale | times: 100 | floor }}% ({{ font1.size | times: font1.min_scale }} mm)
bis zu {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm) skaliert werdens.

### Neon Blinking

Bei einer Skalierung von 100% hat die Schrift eine ungefähre Höhe von {{ font2.size }} mm. 

Sie kann von {{ font2.min_scale | times: 100 | floor }}% ({{ font1.size | times: font2.min_scale }} mm)
bis zu {{ font2.max_scale | times: 100 | floor }}% ({{ font2.size | times: font2.max_scale }} mm) skaliert werdens.

## Impressionen

{%include folder-galleries path="fonts/neon/" %}

## Lizenz

[Lizenz herunterladen (Neon)](https://github.com/inkstitch/inkstitch/tree/main/fonts/neon/LICENSE)

[Lizenz herunterladen (Neon Blinking)](https://github.com/inkstitch/inkstitch/tree/main/fonts/neon_blinking/LICENSE)

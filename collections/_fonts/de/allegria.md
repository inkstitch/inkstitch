---
title: "Allegria"
permalink: /de/fonts/allegria/
last_modified_at: 2025-09-07
toc: false
preview_image:
 - url: /assets/images/fonts/allegria20.png
   height: 20
 - url: /assets/images/fonts/allegria55.png
   height: 55
data_title:
  - allegria20
  - allegria55
---
{%- assign font1 = site.data.fonts.allegria20.font -%}
{%- assign font2 = site.data.fonts.allegria55.font -%}

{% include upcoming_release.html %}

![Allegria20](/assets/images/fonts/allegria20.png)

![Allegria 55](/assets/images/fonts/allegria55.png)

## Schriftzeichen

### Allegria 20

Diese Schrift enthält {{ font1.glyphs.size }} Schriftzeichen:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

### Allegria 55

Diese Schrift enthält {{ font2.glyphs.size }} Schriftzeichen:

```
{{ font2.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Maße

### Allegria 20

Bei einer Skalierung von 100% hat die Schrift eine ungefähre Höhe von {{ font1.size }} mm. 

Sie kann von {{ font1.min_scale | times: 100 | floor }}% ({{ font1.size | times: font1.min_scale }} mm)
bis zu {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm) skaliert werdens.

### Allegria 55

Bei einer Skalierung von 100% hat die Schrift eine ungefähre Höhe von {{ font2.size }} mm. 

Sie kann von {{ font2.min_scale | times: 100 | floor }}% ({{ font2.size | times: font2.min_scale }} mm)
bis zu {{ font2.max_scale | times: 100 | floor }}% ({{ font2.size | times: font2.max_scale }} mm) skaliert werdens.

## Impressionen

{%include folder-galleries path="fonts/allegria/" %}

## Lizenz

[Lizenz herunterladen (Allegria 20)](https://github.com/inkstitch/inkstitch/tree/main/fonts/allegria20/LICENSE)

[Lizenz herunterladen (Allegria 55)](https://github.com/inkstitch/inkstitch/tree/main/fonts/allegria55/LICENSE)

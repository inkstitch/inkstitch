---
title: Gingo200
permalink: /de/fonts/gingo200/
last_modified_at: 2025-05-28
toc: false
preview_image:
  - url: /assets/images/fonts/gingo200.png
    height: 36
data_title:
  - gingo200
---
{%- assign font = site.data.fonts.gingo200.font -%}
![gingo200](/assets/images/fonts/gingo200.png)

## Schriftzeichen

Diese Schrift enthält  {{ font.glyphs.size }} Schriftzeichen:

```
{{ font.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Maße

Bei einer Skalierung von 100 % ist diese Schrift {{ font.size }} mm groß.

Sie kann bis auf {{ font.min_scale | times: 100 | floor }}% ({{ font.size | times: font.min_scale }} mm) herunterskaliert und bis zu {{ font.max_scale | times: 100 | floor }}% ({{ font.size | times: font.max_scale }} mm) hochskaliert  werden.

## Impressionen

{% include folder-galleries path="fonts/gingo200/" %}

## Lizenz

[Lizenz herunterladen](https://github.com/inkstitch/inkstitch/tree/main/fonts/gingo200/LICENSE)


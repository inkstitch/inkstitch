---
title: "Ink/Stitch Masego"
permalink: /de/fonts/inkstitch-masego/
last_modified_at: 2024-05-12
toc: false
preview_image:
  - url: /assets/images/fonts/inkstitch_masego.png
    height: 17
data_title:
  - inkstitch_masego
---
{%- assign font = site.data.fonts.inkstitch_masego.font -%}

![Invercellia](/assets/images/fonts/inkstitch_masego.png)

## Schriftzeichen

Diese Schrift enthält  {{ font.glyphs.size }} Schriftzeichen:

```
{{ font.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Maße

Bei einer Skalierung auf 100 % ist diese Schrift ungefähr {{ font.size }} mm groß.

Sie kann bis auf {{ font.max_scale | times: 100 | floor }}% ({{ font.size | times: font.max_scale }} mm) hochskaliert 
und bis zu {{ font.min_scale | times: 100 | floor }}% ({{ font.size | times: font.min_scale }} mm) herunterskaliert werden.

## Impressionen

{% include folder-galleries path="fonts/inkstitch_masego/" %}

## Lizenz

[Lizenz herunterladen](https://github.com/inkstitch/inkstitch/tree/main/fonts/inkstitch_masego/LICENSE)

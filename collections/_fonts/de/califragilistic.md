---
title: "Califragilistic"
permalink: /de/fonts/califragilistic/
last_modified_at: 2025-01-27
toc: false
preview_image:
  - url: /assets/images/fonts/califragilistic.png
    height: 50
data_title:
  - califragilistic
---
{%- assign font = site.data.fonts.califragilistic.font -%}

![Califragilistic](/assets/images/fonts/califragilistic.png)

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

{% include folder-galleries path="fonts/califragilistic/" %}

## Lizenz

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/califragilistic/LICENSE)

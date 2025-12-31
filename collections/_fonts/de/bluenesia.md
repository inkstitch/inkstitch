---
title: "Bluenesia Satin"
permalink: /de/fonts/bluenesia/
last_modified_at: 2025-05-05
toc: false
preview_image:
  - url: /assets/images/fonts/bluenesia_satin.png
    height: 24
data_title:
  - bluenesia
---
{%- assign font = site.data.fonts.bluenesia_satin.font -%}

![Bluenesia](/assets/images/fonts/bluenesia_satin.png)

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

{% include folder-galleries path="fonts/bluenesia_satin/" %}

## Lizenz

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/bluenesia_satin/LICENSE)

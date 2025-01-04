---
title: "Pixel 10"
permalink: /fonts/pixel10/
last_modified_at: 2025-01-04
toc: false
preview_image:
  - url: /assets/images/fonts/pixel_10.png
    height: 50
data_title:
  - pixel10
---
{%- assign font = site.data.fonts.pixel10.font -%}

{% include upcoming_release.html %}

![Pixel 10](/assets/images/fonts/pixel_10.png)

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

{% include folder-galleries path="fonts/pixel10/" %}

## Lizenz


[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/pixel10/LICENSE)

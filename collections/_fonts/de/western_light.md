---
title: "Western light"
permalink: /fonts/western_light/
last_modified_at: 2025-01-04
toc: false
preview_image:
  - url: /assets/images/fonts/western_light.png
    height: 14
data_title:
  - western_light
---
{%- assign font = site.data.fonts.western_light.font -%}

{% include upcoming_release.html %}

![Western light](/assets/images/fonts/western_light.png)
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


{% include folder-galleries path="fonts/western_light/" %}

## Lizenz


[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/western_light/LICENSE)

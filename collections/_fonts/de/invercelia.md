---
title: "Invercelia"
permalink: /de/fonts/invercelia/
last_modified_at: 2024-05-12
toc: false
preview_image:
  - url: /assets/images/fonts/invercelia.png
    height: 60
data_title:
  - invercelia
---
{%- assign font = site.data.fonts.invercelia.font -%}

![Invercellia](/assets/images/fonts/invercelia.png)

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

{% include folder-galleries path="fonts/invercelia/" %}

## Lizenz

[Lizenz herunterladen](https://github.com/inkstitch/inkstitch/tree/main/fonts/invercelia/LICENSE)

---
title: "CooperMarif"
permalink: /de/fonts/cooper_marif/
last_modified_at: 2024-06-23
toc: false
preview_image:
  - url: /assets/images/fonts/cooper_marif.png
    height: 90
data_title:
  - cooper_marif
---
{%- assign font = site.data.fonts.cooper_marif.font -%}
![Cooper Marif](/assets/images/fonts/cooper_marif.png)

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

{% include folder-galleries path="fonts/colorful/" %}


## Lizenz

[Lizenz herunterladen](https://github.com/inkstitch/inkstitch/tree/main/fonts/cooper_marif/LICENSE)

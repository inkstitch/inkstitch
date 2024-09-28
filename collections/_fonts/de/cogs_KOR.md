---
title: "Cogs_KOR"
permalink: /de/fonts/cogs_KOR/
last_modified_at: 2024-09-28
toc: false
preview_image:
  - url: /assets/images/fonts/cogs_KOR.png
    height: 38
data_title:
  - cogs_KOR
---
{%- assign font = site.data.fonts.cogs_KOR.font -%}
![cogs_KOR](/assets/images/fonts/cogs_KOR.png)

## Schriftzeichen

Diese Schrift enthält {{ font.glyphs.size }} Schriftzeichen:

```
{{ font.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }
 
## Besonderheiten

Cogs_KOR ist eine Steampunk-Satin-Schrift.

## Maße

Bei einer Skalierung von 100% ist die Schrift ungefährt {{ font.size }} mm hoch.

Sie kann von {{ font.min_scale | times: 100 | floor }}% ({{ font.size | times: font.min_scale }} mm)
bis zu {{ font.max_scale | times: 100 | floor }}% ({{ font.size | times: font.max_scale }} mm) skaliert werden.

## Impressionen

{% include folder-galleries path="fonts/cogs_KOR/" %}

## Lizenz

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/cogs_KOR/LICENSE)

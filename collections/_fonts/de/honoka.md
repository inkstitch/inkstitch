---
title: "コリンの書き方"
permalink: /de/fonts/honoka/
last_modified_at: 2024-05-25
toc: false
preview_image:
  - url: /assets/images/fonts/honoka.jpg
    height: 20
data_title:
  - honoka
---
{%- assign font = site.data.fonts.honoka.font -%}

![Honoka](/assets/images/fonts/honoka.jpg)

## Schriftzeichen

Diese Schrift umfasst  {{ font.glyphs.size }} Zeichen:

```
{{ font.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

Zum jetzigen Zeitpunkt umfasst diese Schrift  hiragana, katakana, Satzzeichen und 
viele kanjis.

## Maße

Bei einer Skalierung von 100% hat die Schrift eine Höhe von {{ font.size }} mm. 

Die Schrift kann von {{ font.min_scale | times: 100 | floor }}% ({{ font.size | times: font.min_scale }} mm)
bis zu {{ font.max_scale | times: 100 | floor }}% ({{ font.size | times: font.max_scale }} mm) skaliert werden.

## Impressionen

{% include folder-galleries path="fonts/honoka/" %}

## Lizenz

[Lizenz herunterladen](https://github.com/inkstitch/inkstitch/tree/main/fonts/honoka/LICENSE)

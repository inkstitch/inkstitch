---
title: "Malika"
permalink: /de/fonts/malika/
last_modified_at: 2025-04-13
toc: false
preview_image:
  - url: /assets/images/fonts/malika.png
    height: 23
data_title:
  - malika
---
{%- assign font = site.data.fonts.malika.font -%}

![malika](/assets/images/fonts/malika.png)

## Schriftzeichen

Diese Schrift enthält  {{ font.glyphs.size }} Schriftzeichen:

```
{{ font.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Maße

Bei einer Skalierung von 100 % ist diese Schrift {{ font.size }} mm groß.

Sie kann bis auf {{ font.min_scale | times: 100 | floor }}% ({{ font.size | times: font.min_scale }} mm) 
herunterskaliert und bis zu {{ font.max_scale | times: 100 | floor }}% ({{ font.size | times: font.max_scale }} mm) hochskaliert  werden.

## Besonderheiten

Jeder Buchstaben enthält das Originalzeichen in einem versteckten Element mit einer roten Füllung. Diese Elemente sind nicht zum Sticken gedacht, können aber für Schriftmodifizierungen genutzt werden. Sie können aber auch einfach ignoriert werden.

## Impressionen

{% include folder-galleries path="fonts/malika/" %}

## Lizenz

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/malika/LICENSE)


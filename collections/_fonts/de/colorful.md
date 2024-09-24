---
title: "Colorful"
permalink: /de/fonts/colorful/
last_modified_at: 2024-05-25
toc: false
preview_image:
  - url: /assets/images/fonts/colorful.png
    height: 35
data_title:
  - colorful
---
{%- assign font = site.data.fonts.colorful.font -%}

![colorful](/assets/images/fonts/colorful.png)

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

## Zu viel Arbeit?

Jeder Buchstabe hat ein eigenes Tartan-Muster. Daher ist das Sticken dieser Schrift nichts für schwache Nerven, denn es gibt sehr viele Farbwechsel. Durch eine Variation mit nur einem Tartan-Muster, kann dieser Prozess kann erheblich vereinfacht werden - allerdings wird das Stockergebnis dadurch auch weniger farbenfroh. Mehr Informationen wie das geht gibt es im Tutorial [Farbwechsel bei Tartan-Schriften reduzieren](https://inkstitch.org/de/tutorials/make_tartan_font_easier/)

## Impressionen

{% include folder-galleries path="fonts/colorful/" %}

## Lizenz

[Lizenz herunterladen](https://github.com/inkstitch/inkstitch/tree/main/fonts/colorful/LICENSE)

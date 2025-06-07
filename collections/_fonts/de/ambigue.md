---
title: "Ambigüe"
permalink: /de/fonts/ambigue/
last_modified_at: 2025-04-13
toc: false
preview_image:
  - url: /assets/images/fonts/ambigue.png
    height: 26
data_title:
  - ambigue
---
{%- assign font = site.data.fonts.ambigue.font -%}

![Ambigue](/assets/images/fonts/ambigue.png)
## Schriftzeichen

Diese Schrift enthält  {{ font.glyphs.size }} Schriftzeichen:

```
{{ font.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Maße

Bei einer Skalierung von 100 % ist diese Schrift {{ font.size }} mm groß.

Sie kann bis auf {{ font.min_scale | times: 100 | floor }}% ({{ font.size | times: font.min_scale }} mm) herunterskaliert und bis zu {{ font.max_scale | times: 100 | floor }}% ({{ font.size | times: font.max_scale }} mm) hochskaliert  werden.

## Besonderheiten

Jedes Zeichen enthält eine Konturlinie des Originalbuchstabens in einem versteckten schwarzen Pfad. Diese Pfade sind nicht für das Sticken bestimmt, können aber jedem helfen, der die Schrift modifizieren will, z.B. um Embossing zu erstellen. Diese Pfade können einfach ignoriert werden.

## Impressionen

{% include folder-galleries path="fonts/ambigue/" %}

## Lizenz

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/ambigue/LICENSE)

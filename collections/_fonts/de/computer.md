---
title: "Computer"
permalink: /de/fonts/computer/
last_modified_at: 2025-04-13
toc: false
preview_image:
  - url: /assets/images/fonts/computer.png
    height: 23
  - url: /assets/images/fonts/computer.png
    height: 6

data_title:
  - computer
  - computer_small
---
{%- assign font1 = site.data.fonts.computer.font -%}

{%- assign font2 = site.data.fonts.computer_small.font -%}

<img 
     src="/assets/images/fonts/computer.png"
     alt="Emilio20" height="23">

## Schriftzeichen

Diese Schrift enthält  {{ font1.glyphs.size }} Schriftzeichen:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Maße

### Computer

Bei einer Skalierung von 100 % ist diese Schrift {{ font1.size }} mm groß.

Sie kann bis auf {{ font1.min_scale | times: 100 | floor }}% ({{ font1.size | times: font1.min_scale }} mm) herunterskaliert und 
bis zu {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm) hochskaliert  werden.

### Computer Small

Sie kann bis auf {{ font2.min_scale | times: 100 | floor }}% ({{ font2.size | times: font2.min_scale }} mm) herunterskaliert und 
bis zu {{ font2.max_scale | times: 100 | floor }}% ({{ font2.size | times: font1.max_scale }} mm) hochskaliert  werden.

Im Gegensatz zu Computer MUSS diese verkleinerte Schrift mit einem dünneren Faden und einer dünneren Nadel als üblich gestickt werden. Es MUSS eine Nadel der Größe 8 (USA), 60(EUR) und ein Garn 60WT verwendet werden.

## Besonderheiten

Jedes Zeichen enthält eine Konturlinie des Originalbuchstabens in einem versteckten schwarzen Pfad. Diese Pfade sind nicht für das Sticken bestimmt, können aber jedem helfen, der die Schrift modifizieren will. Diese Pfade können einfach ignoriert werden.

## Impressionen

{% include folder-galleries path="fonts/computer/" %}

## Lizenz

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/computer/LICENSE)

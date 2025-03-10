---
title: "פשוט מעוגל"
permalink: /de/fonts/hebrew_simple_rounded/
last_modified_at: 2025-03-10
toc: false
preview_image:
  - url: /assets/images/fonts/hebrew_simple_rounded.png
    height: 23
  - url: /assets/images/fonts/hebrew_simple_rounded_small.png
    height: 6

data_title:
  - hebrew_simple_rounded
  - hebrew_simple_rounded_small
---
{%- assign font1 = site.data.fonts.hebrew_simple_rounded.font -%}

{%- assign font2 = site.data.fonts.hebrew_simple_rounded_small.font -%}

{% include upcoming_release.html %}

<img 
     src="/assets/images/fonts/hebrew_simple_rounded.png"
     alt="Hebrew simple  rounded " height="23">
     
## Schriftzeichen

Diese Schrift enthält  {{ font1.glyphs.size }} Schriftzeichen:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Maße

### Hebrew simple rounded font
Bei einer Skalierung von 100 % ist diese Schrift {{ font1.size }} mm groß.

Sie kann bis auf {{ font1.min_scale | times: 100 | floor }}% ({{ font1.size | times: font1.min_scale }} mm) herunterskaliert und 
bis zu {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm) hochskaliert  werden.

### Small simple rounded font
Sie kann bis auf {{ font2.min_scale | times: 100 | floor }}% ({{ font2.size | times: font2.min_scale }} mm) herunterskaliert und 
bis zu {{ font2.max_scale | times: 100 | floor }}% ({{ font2.size | times: font1.max_scale }} mm) hochskaliert  werden.

Im Gegensatz zu Hebrew sinple rounded font MUSS diese verkleinerte Schrift mit einem dünneren Faden und 
einer dünneren Nadel als üblich gestickt werden. Es MUSS eine Nadel der Größe 8 (USA), 60(EUR) und ein Garn 60WT verwendet werden.

## Besonderheiten

Jedes Zeichen enthält die ursprünglichen Pfadinformationen in einem versteckten Pfad. Diese Pfade sind nicht zum Sticken vorgesehen, aber sie können bei einer späteren Schrift-Modifikation behilflich sein. Sie können ohne Weiteres ignoriert werden.

## Impressionen

{% include folder-galleries path="fonts/hebrew_simple_rounded/" %}

## Lizenz

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/hebrew_simple_rounded/LICENSE)

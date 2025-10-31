---
title: "גופן בינוני"
permalink: /de/fonts/hebrew_font/
last_modified_at: 2025-04-13
toc: false
preview_image:
  - url: /assets/images/fonts/hebrew_font_large.png
    height: 35
  - url: /assets/images/fonts/hebrew_font_medium.png
    height: 23

data_title:
  - hebrew_font_large
  - hebrew_font_medium
---
{%- assign font1 = site.data.fonts.hebrew_font_large.font -%}

{%- assign font2 = site.data.fonts.hebrew_font_medium.font -%}

<img 
     src="/assets/images/fonts/hebrew_font_large.png"
     alt="hebrew_font_large" height="35">

<img 
     src="/assets/images/fonts/hebrew_font_medium.png"
     alt="hebrew_font_medium" height="23">

## Schriftzeichen

Diese Schrift enthält  {{ font1.glyphs.size }} Schriftzeichen:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Maße

### Large

Bei einer Skalierung von 100 % ist diese Schrift {{ font1.size }} mm groß.

Sie kann bis auf {{ font1.min_scale | times: 100 | floor }}% ({{ font1.size | times: font1.min_scale }} mm) herunterskaliert und 
bis zu {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm) hochskaliert  werden.

### Medium

Sie kann bis auf {{ font2.min_scale | times: 100 | floor }}% ({{ font2.size | times: font2.min_scale }} mm) herunterskaliert und 
bis zu {{ font2.max_scale | times: 100 | floor }}% ({{ font2.size | times: font1.max_scale }} mm) hochskaliert  werden.

## Besonderheiten

Jeder Buchstaben enthält das Originalzeichen in einem versteckten Element mit einer roten Füllung. Diese Elemente sind nicht zum Sticken gedacht, können aber für Schriftmodifizierungen genutzt werden. Sie können aber auch einfach ignoriert werden.

## Impressionen

{% include folder-galleries path="fonts/hebrew_font/" %}

## Lizenz

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/hebrew_font_medium/LICENSE)

---
title: "Braille"
permalink: /de/fonts/braille/
last_modified_at: 2025-09-07
toc: false
preview_image:
- url: /assets/images/fonts/braille.png
  height: 7
data_title:
- braille
---
{%- assign font1 = site.data.fonts.braille.font -%}

{% include upcoming_release.html %}

![Braille](/assets/images/fonts/braille.png)

## Schriftzeichen

Diese Schrift enthält {{ font1.glyphs.size }} Schriftzeichen:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Anmerkungen

Font for the visually impaired with Braille key combinations according to DT 2024 INSEI specifications for French 6 dots Braille. It is also possible to use Unicode Braille. In this case, it is convenient to use one of the web's Braille translators to create a text in Braille unicode.

## Maße

Bei einer Skalierung von 100% hat die Schrift eine ungefähre Höhe von {{ font1.size }} mm. 

Sie kann von {{ font1.min_scale | times: 100 | floor }}% ({{ font1.size | times: font1.min_scale }} mm)
bis zu {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm) skaliert werdens.

## Impressionen

{%include folder-galleries path="fonts/braille/" %}

## Lizenz

[Lizenz herunterladen (Braille Font)](https://github.com/inkstitch/inkstitch/tree/main/fonts/braille/LICENSE)

---
title: "Roman AGS"
permalink: /de/fonts/roman_ags/
last_modified_at: 2023-04-24
toc: false
preview_image: 
preview_image:
  - url: /assets/images/fonts/roman_AGS.jpg
    height: 28
  - url: /assets/images/fonts/roman_AGS_bicolor.jpg
    height: 28
 
---
{%- assign font1 = site.data.fonts.roman_ags.font -%}
{%- assign font2 = site.data.fonts.roman_ags_bicolor.font -%}

![Roman AGS](/assets/images/fonts/roman_AGS.jpg)
![Roman AGS_bicolor](/assets/images/fonts/roman_AGS_bicolor.jpg)

## Schriftzeichen

### Roman AGS 

Diese Schrift enthält  {{ font1.glyphs.size }} Schriftzeichen:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

### Roman AGS Bicolor

Diese Schrift enthält  {{ font2.glyphs.size }} Schriftzeichen:

```
{{ font2.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Maße

Bei einer Skalierung auf 100 % sind diese Schriften ungefähr 28 mm (1 Zoll) groß.
Sie können bis auf 130% (~37 mm, 1.5 Zoll) hochskaliert und bis zu 80% (~22 mm, 0.8 Zoll) herunterskaliert werden.

## Impressionen

{% include folder-galleries path="fonts/roman_AGS/" %}

## Lizenz

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/roman_ags_bicolor/LICENSE)

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/roman_ags/LICENSE)

---
title: "Geneva Simple"
permalink: /de/fonts/geneva_simple/
last_modified_at: 2023-04-24
toc: false
preview_image:
  - url: /assets/images/fonts/geneva_simple_sans.jpg
    height: 13
  - url: /assets/images/fonts/geneva_simple_sans_rounded.jpg
    height: 13
---
{%- assign font2 = site.data.fonts.geneva_rounded.font -%}
{%- assign font1 = site.data.fonts.geneva_simple.font -%}


## Sans

![Geneva Simple Sans](/assets/images/fonts/geneva_simple_sans.jpg)

### Schriftzeichen

Diese Schrift enthält  {{ font1.glyphs.size }} Schriftzeichen:

```
{{ font1.glyphs | join: ' ' }}
```
{: .font-glyphs }

## Sans Rounded

![Geneva Simple Sans](/assets/images/fonts/geneva_simple_sans_rounded.jpg)

### Schriftzeichen

Diese Schrift enthält  {{ font2.glyphs.size }} Schriftzeichen:

```
{{ font2.glyphs | join: ' ' }}
```
{: .font-glyphs }
## Maße

Bei einer Skalierung von 100 % sind diese Schriften ungefähr 14 mm (1/2 Zoll) groß.

Sie können bis auf 200% (~28mm, 1 Zoll) hochskaliert und bis zu 75% (~9mm, 1/3 Zoll) herunterskaliert werden.

## Gestickte Beispiele

{% include folder-galleries path="fonts/geneva/" %}

## Lizenz

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/geneva_simple/LICENSE)

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/geneva_rounded/LICENSE)

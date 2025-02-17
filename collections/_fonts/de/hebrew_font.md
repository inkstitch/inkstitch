---
title: "גופן בינוני"
permalink: /de/fonts/hebrew_font/
last_modified_at: 2025-02-16
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

{% include upcoming_release.html %}

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


## Special features
Each glyph contains the  original letter, in the form of a hidden path with red fill. These fills are not intended to be embroidered as is, but to help anyone who wants to modify this font. They can be ignored safely.

## Impressionen

{% include folder-galleries path="fonts/hebrew_font/" %}

## Lizenz

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/hebrew_font/LICENSE)

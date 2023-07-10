---
title: "Sortefax"
permalink: /fonts/sortefax/
last_modified_at: 2022-05-26
toc: false
preview_image: 
  - url: /assets/images/fonts/sortefaxXL.jpg
    height: 150
  - url: /assets/images/fonts/sortefax_medium.jpg
    height: 90
---
{%- assign font = site.data.fonts.sortefaxXL.font -%}
![SortefaxXL](/assets/images/fonts/sortefaxXL.jpg)

![Sortefax_medium](/assets/images/fonts/sortefax_medium.jpg)

## Glyphs

Both fonts contain  {{ font.glyphs.size }} glyphs:

```
{{ font.glyphs | join: ' ' }}
```
{: .font-glyphs }

**Remark:** :;,.(){}[]  are used to store frames.
{: .notice--info }

## Dimensions

### Sortefax XL Initials

At 100%, this font is approximatively 150 mm (6 inches) tall.
It can been scaled up to 200% (approx 300 mm, 12 inches) or down to 70% (approx 100 mm, 4 inches).

### Sortefax Medium Initials

At 100%, this font is approximatively 90 mm (3.5 inches) tall.
It can be scaled up to 200% (approx 180 mm, 7 inches) or down to 70% (approx 60 mm, 2.5 inches).

## Description

### Sortefax XL Initials

Sortefax XL Initials is meant to be used one letter at a time.
To get a framed letter, simply type the letter and any "frame" letter in the lettering dialog window (same line, no space).

Beware, not all frames can directly be used with all letters, in particular large letters such as M or W, or tall letters such as J.

Of course, using Inkscape,  you may easily reposition the frame or resize it or even transform a circle frame  into an ellipse for a tall letter.

### Sortefax Medium Initials

Sortefax Médium Initials is  smaller but  also simplier.

It is still possible to use frames, but the arranging of the frame and the letter is  not as good as for the XL font.
But this font may be used to write whole words with a correct kerning and not only single letters.

## To access the frames, use the corresponding keys:

Frame|Key
---|---
![ouvrante](/assets/images/fonts/sortefax/ouvrante.png)|<key>(</key>
![fermante](/assets/images/fonts/sortefax/fermante.png)|<key>)</key>
![ouvrantecarre](/assets/images/fonts/sortefax/square-bracket-open.png)|<key>[</key>
![fermantecarre](/assets/images/fonts/sortefax/square-bracket-open.png)|<key>]</key>
![accolade_ouvrante](/assets/images/fonts/sortefax/curly-bracket-open.png)|<key>{</key>
![accolade_fermante](/assets/images/fonts/sortefax/curly-bracket-close.png)|<key>}</key>
![Point](/assets/images/fonts/sortefax/point.png)|<key>.</key>
![Virgule](/assets/images/fonts/sortefax/virgule.png)|<key>,</key>
![DeuxPoints](/assets/images/fonts/sortefax/deuxpoints.png)|<key>:</key>
![PointVirgule](/assets/images/fonts/sortefax/pointvirgule.png)|<key>;</key>

## In real life 

{% include folder-galleries path="fonts/sortefax/" %}

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/sortefaxXL/LICENSE)

---
title: "Roman AGS"
permalink: /fonts/roman_ags/
last_modified_at: 2022-05-26
toc: false
preview_image:
  - url: /assets/images/fonts/roman_AGS.jpg
    height: 28
  - url: /assets/images/fonts/roman_AGS_bicolor.jpg
    height: 28
---
{%- assign font1 = site.data.fonts.roman_ags.font -%}
{%- assign font2 = site.data.fonts.roman_ags_bicolor.font -%}

<img 
     src="/assets/images/fonts/roman_AGS.jpg"
     alt="Roman AGS" height="60">
     
<img 
     src="/assets/images/fonts/roman_AGS_bicolor.jpg"
     alt="Roman AGS_bicolor" height="60">


## Glyphs
### Roman AGS 
This font contains  {{ font1.glyphs.size }} glyphs:

{% for glyph in font1.glyphs %}
{{ glyph }}
{%- endfor %}

### Roman AGS Bicolor

This font contains  {{ font2.glyphs.size }} glyphs:

{% for glyph in font2.glyphs %}
{{ glyph }}
{%- endfor %}

## Dimensions
At 100%, these fonts are approximatively  28 mm (1 inch) tall .
They may be scaled up to 130% (approx. 37 mm, 1.5 inches) or down to 80% (approx.  22 mm, 0.8 inch).

## Using the two fonts together

Whenever a glyph is present in both fonts, the design shape and size of the glyphs are exactly the same. It is therefore very easy to use them together:

- Do a lettering of the whole text unsing Roman AGS only
- Do a letterng using  Roman AGS bicolore with the only the letters you wish to be bicolors.
- Put each bicolor letter exactly on top of the corresponding monocolor letter  
- Hide those monocolor letters

## Color sorting
If you use bicolor  letters, you may wish to color sort. It is possible, providing the sorting respects the relative order inside each letter. [This is a way to do it](https://inkstitch.org/en/docs/lettering/#color-sorting)


## In real life
{% include folder-galleries path="fonts/roman_AGS/" %}

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/roman_ags_bicolor/LICENSE)

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/roman_ags/LICENSE)

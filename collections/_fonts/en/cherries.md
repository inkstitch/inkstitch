---
title: "Cherries"
permalink: /fonts/cherries/
last_modified_at: 2022-05-26
toc: false
preview_image:
  - url: /assets/images/fonts/cherry_for_inkstitch.jpg
    height: 65
  - url: /assets/images/fonts/cherryforkaalleen.jpg
    height: 75
---
{%- assign font1 = site.data.fonts.cherryforinkstitch.font -%}
{%- assign font2 = site.data.fonts.cherryforkaalleen.font -%}


<img 
     src="/assets/images/fonts/cherry_for_inkstitch.jpg"
     alt="Roman AGS" height="48">
     
<img 
     src="/assets/images/fonts/cherryforkaalleen.jpg"
     alt="Roman AGS_bicolor" height="72">


## Glyphes
### Cherry for Ink/Stitch

This font contains  {{ font1.glyphs.size }} glyphs:

{% for glyph in font1.glyphs %}
{{ glyph | escape }}
{%- endfor %}

### Cherry for Kaalleen

This font contains  {{ font2.glyphs.size }} glyphs:

{% for glyph in font2.glyphs %}
{{ glyph | escape }}
{%- endfor %}

## Dimensions
### Cherry for Ink/Stitch
At 100%, this font is approximatively  50 mm (2 inches) high. 
It can be scaled up to 180% ( approx 90mm 3.5 inches) or scaled down to 80% (approx 1.5 inch)
### Cherry for Kaalleen
At 100%, this font is approximatively 75 mm high (3 inches)
It can be scaled up to 130% (approx 100 mm, 4 inches ) or scaled down to 80% (approx 60 mm, 2 inches).

## Color sorting
If you embroider several letters, you may wish to color sort. It is possible, providing the sorting respects the relative order inside each letter. [This is a way to do it](https://inkstitch.org/en/docs/lettering/#color-sorting)


## In real life

They may be used together or independantly

{% include folder-galleries path="fonts/cherries/" %}


[Download Cherry for inkstitch Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/cherryforinkstitch/LICENSE)

[Download Cherry for Kaalleen Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/cherryforkaalleen/LICENSE)

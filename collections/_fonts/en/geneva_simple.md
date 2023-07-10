---
title: "Geneva Simple"
permalink: /fonts/geneva_simple/
last_modified_at: 2022-05-26
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

### Glyphs

This font contains  {{ font1.glyphs.size }} glyphs:

```
{{ font1.glyphs | join: ' ' }}
```
{: .font-glyphs }

## Sans Rounded

![Geneva Simple Sans](/assets/images/fonts/geneva_simple_sans_rounded.jpg)

### Glyphes

This font contains  {{ font2.glyphs.size }} glyphs:

```
{{ font2.glyphs | join: ' ' }}
```
{: .font-glyphs }

## Dimensions

At 100%, these fonts are approximatively  14 mm (1/2 inch) tall.

They can be scaled up to  200% (approx 28 mm, 1 inch) or scaled down to 75% (approx 9 mm, 1/3 inch).

## In real life

{% include folder-galleries path="fonts/geneva/" %}

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/geneva_simple/LICENSE)

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/geneva_rounded/LICENSE)

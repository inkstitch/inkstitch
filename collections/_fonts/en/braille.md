---
title: "Braille"
permalink: /fonts/braille/
last_modified_at: 2025-09-07
toc: false
preview_image:
- url: /assets/images/fonts/braille.png
  height: 7
data_title:
- braille
---
{%- assign font1 = site.data.fonts.braille.font -%}

![Allegria20](/assets/images/fonts/braille.png)

## Glyphs

This font contains  {{ font1.glyphs.size }} glyphs:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Remarks

Font for the visually impaired with Braille key combinations according to DT 2024 INSEI specifications for French 6 dots Braille. It is also possible to use Unicode Braille. In this case, it is convenient to use one of the web's Braille translators to create a text in Braille unicode.

## Dimensions

At a scale of 100% this font has an approximate height of {{ font1.size }} mm. 

It can be scaled from {{ font1.min_scale | times: 100 | floor }}% ({{ font1.size | times: font1.min_scale }} mm)
up to {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm).

## In real life 

{%include folder-galleries path="fonts/braille/" %}

## License

[Download Braille Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/braille/LICENSE)

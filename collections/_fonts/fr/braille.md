---
title: "Braille"
permalink: /fr/fonts/braille/
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

## Glyphes

Cette fonte comporte {{ font1.glyphs.size }} glyphes:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Particularités

Font for the visually impaired with Braille key combinations according to DT 2024 INSEI specifications for French 6 dots Braille. It is also possible to use Unicode Braille. In this case, it is convenient to use one of the web's Braille translators to create a text in Braille unicode.

## Dimensions

A une échelle de 100% cette fonte a une hauteur approximative de {{ font1.size }} mm. 

Elle peut être redimensionnée de {{ font1.min_scale | times: 100 | floor }}% ({{ font1.size | times: font1.min_scale }} mm)
à {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm).

## Dans la vraie vie

{%include folder-galleries path="fonts/braille/" %}

## License

[Télécharger la license d'Braille](https://github.com/inkstitch/inkstitch/tree/main/fonts/braille/LICENSE)

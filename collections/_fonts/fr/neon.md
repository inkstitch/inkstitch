---
title: "Neon"
permalink: /fr/fonts/neon/
last_modified_at: 2025-09-07
toc: false
preview_image:
 - url: /assets/images/fonts/neon.png
   height: 50
 - url: /assets/images/fonts/neon_blinking.png
   height: 30
data_title:
  - neon
  - neon_blinking
---
{%- assign font1 = site.data.fonts.neon.font -%}
{%- assign font2 = site.data.fonts.neon_blinking.font -%}

{% include upcoming_release.html %}

![Neon](/assets/images/fonts/neon.png)

![Neon Blinking](/assets/images/fonts/neon_blinking.png)

## Glyphes

### Neon

Cette fonte comporte {{ font1.glyphs.size }} glyphes:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

### Neon Blinking

Cette fonte comporte {{ font2.glyphs.size }} glyphes:

```
{{ font2.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Dimensions

### Neon

A une échelle de 100% cette fonte a une hauteur approximative de {{ font1.size }} mm. 

Elle peut être redimensionnée de {{ font1.min_scale | times: 100 | floor }}% ({{ font1.size | times: font1.min_scale }} mm)
à {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm).

### Neon Blinking

A une échelle de 100% cette fonte a une hauteur approximative de {{ font2.size }} mm. 

Elle peut être redimensionnée de {{ font2.min_scale | times: 100 | floor }}% ({{ font1.size | times: font2.min_scale }} mm)
à {{ font2.max_scale | times: 100 | floor }}% ({{ font2.size | times: font2.max_scale }} mm).

## Dans la vraie vie

{%include folder-galleries path="fonts/neon/" %}

## License

[Télécharger la license d'Neon](https://github.com/inkstitch/inkstitch/tree/main/fonts/neon/LICENSE)

[Télécharger la license d'Neon Blinking](https://github.com/inkstitch/inkstitch/tree/main/fonts/neon_blinking/LICENSE)

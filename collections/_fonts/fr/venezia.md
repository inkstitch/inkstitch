---
title: "Venezia"
permalink: /fr/fonts/venezia/
last_modified_at: 2025-09-07
toc: false
preview_image:
 - url: /assets/images/fonts/venezia.png
   height: 17
 - url: /assets/images/fonts/venezia_small.png
   height: 12
data_title:
  - venezia
  - venezia_small
---
{%- assign font1 = site.data.fonts.venezia.font -%}
{%- assign font2 = site.data.fonts.venezia_small.font -%}

{% include upcoming_release.html %}

![Venezia](/assets/images/fonts/venezia.png)

![Venezia Small](/assets/images/fonts/venezia_small.png)

## Glyphes

### Venezia

Cette fonte comporte  {{ font1.glyphs.size }} glyphes:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

### Venezia Small

Cette fonte comporte  {{ font2.glyphs.size }} glyphes:

```
{{ font2.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Dimensions

### Venezia

A une échelle de 100% cette fonte a une hauteur approximative de {{ font1.size }} mm. 

Elle peut être redimensionnée de {{ font1.min_scale | times: 100 | floor }}% ({{ font1.size | times: font1.min_scale }} mm)
à {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm).

### Venezia Small

A une échelle de 100% cette fonte a une hauteur approximative de {{ font2.size }} mm. 

Elle peut être redimensionnée de {{ font2.min_scale | times: 100 | floor }}% ({{ font1.size | times: font2.min_scale }} mm)
à {{ font2.max_scale | times: 100 | floor }}% ({{ font2.size | times: font2.max_scale }} mm).

## Dans la vraie vie

{%include folder-galleries path="fonts/neon/" %}

## License

[Télécharger la license de Venezia](https://github.com/inkstitch/inkstitch/tree/main/fonts/venezia/LICENSE)


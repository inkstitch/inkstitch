---
title: "Bluenesia Satin"
permalink: /fr/fonts/bluenesia/
last_modified_at: 2025-05-05
toc: false
preview_image:
  - url: /assets/images/fonts/bluenesia_satin.png
    height: 24
data_title:
  - bluenesia
---
{%- assign font = site.data.fonts.bluenesia.font -%}

![Bluenesia](/assets/images/fonts/bluenesia_satin.png)

## Glyphes

Cette fonte comporte  {{ font.glyphs.size }} glyphes:

```
{{ font.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Dimensions

A une échelle de  100% cette fonte a une hauteur approximative de  {{ font.size }} mm. 

Elle peut être redimensionnée  de {{ font.min_scale | times: 100 | floor }}% ({{ font.size | times: font.min_scale }} mm)
à {{ font.max_scale | times: 100 | floor }}% ({{ font.size | times: font.max_scale }} mm).

## Dans la vraie vie 

{% include folder-galleries path="fonts/bluenesia_satin/" %}

## License

[Télécharger la license de la police](https://github.com/inkstitch/inkstitch/tree/main/fonts/bluenesia_satin/LICENSE)

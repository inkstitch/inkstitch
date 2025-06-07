---
title: "Pixel 10"
permalink: /fr/fonts/pixel10/
last_modified_at: 2025-01-04
toc: false
preview_image:
  - url: /assets/images/fonts/pixel_10.png
    height: 50
data_title:
  - pixel10
---
{%- assign font = site.data.fonts.pixel10.font -%}

![Pixel 10](/assets/images/fonts/pixel_10.png)

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

{% include folder-galleries path="fonts/pixel10/" %}

## License

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/pixel10/LICENSE)

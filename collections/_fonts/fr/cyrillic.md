---
title: "Кирилиця"
permalink: /fr/fonts/cyrillic/
last_modified_at: 2025-09-07
toc: false
preview_image:
 - url: /assets/images/fonts/cyrillic.png
   height: 25
data_title:
  - cyrillic
---
{%- assign font1 = site.data.fonts.cyrillic.font -%}

{% include upcoming_release.html %}

![Cyrillic](/assets/images/fonts/cyrillic.png)

## Glyphes

Cette fonte comporte {{ font1.glyphs.size }} glyphes:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Dimensions

A une échelle de 100% cette fonte a une hauteur approximative de {{ font1.size }} mm. 

Elle peut être redimensionnée de {{ font1.min_scale | times: 100 | floor }}% ({{ font1.size | times: font1.min_scale }} mm)
à {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm).

## Dans la vraie vie

{%include folder-galleries path="fonts/cyrillic/" %}

## License

[Download Cyrillic Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/cyrillic/LICENSE)

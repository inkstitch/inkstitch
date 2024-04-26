---
title: "Manuskript Gothisch"
permalink: /fr/fonts/manuscript_gothisch/
last_modified_at: 2022-05-27
toc: false
preview_image:
  - url: /assets/images/fonts/manuscript_gothisch.jpg
    height: 30
---
{%- assign font = site.data.fonts.manuskript_gotisch.font -%}
![ManuscriptGothisch](/assets/images/fonts/manuscript_gothisch.jpg)

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

{% include folder-galleries path="fonts/manuscript_gothisch/" %}


[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/manuskript_gotisch/LICENSE)

---
title: "Manga Impact"
permalink: /fr/fonts/manga_impact/
last_modified_at: 2025-12-26
toc: false
preview_image:
  - url: /assets/images/fonts/manfa_impact.png
    height: 20
data_title:
  - manga_impact
---
{%- assign font = site.data.fonts.manga_impact.font -%}
![Manga Impact](/assets/images/fonts/manga_impact.png)

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
{% include folder-galleries path="fonts/manga_impact/" %}



[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/manga_impact/LICENSE)

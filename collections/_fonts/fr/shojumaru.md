---
title: "Shojumaru"
permalink: /fr/fonts/shojumaru/
last_modified_at: 2024-06-19
toc: false
preview_image:
  - url: /assets/images/fonts/shojumaru.png
    height: 20
---
{%- assign font = site.data.fonts.shojumaru.font -%}


{% include upcoming_release.html %} 
![Shojumaru](/assets/images/fonts/shojumaru.png)

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

{% include folder-galleries path="fonts/shojumaru/" %}



[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/shojumaru/LICENSE)

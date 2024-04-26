---
title: "Milli Marif Bold"
permalink: /fr/fonts/milli-marif-bold/
last_modified_at: 2024-04-21
toc: false
preview_image:
  - url: /assets/images/fonts/milli_marif.jpg
    height: 20

---
{%- assign font = site.data.fonts.milli_marif_bold.font -%}

![Milli_Marif](/assets/images/fonts/milli_marif.jpg)

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

{% include folder-galleries path="fonts/milli_marif_bold/" %}

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/milli_marif_bold/LICENSE.txt)

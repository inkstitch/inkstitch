---
title: "Violin Serif"
permalink: /fr/fonts/violin_serif/
last_modified_at: 2024-04-24
toc: false
preview_image:
  - url: /assets/images/fonts/violin_serif.jpg
    height: 19
data_title:
  - violin_serif
---
{%- assign font = site.data.fonts.violin_serif.font -%}

![violin serif](/assets/images/fonts/violin_serif.jpg)

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

{% include folder-galleries path="fonts/violin_serif/" %}



[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/violin_serif/LICENSE.txt)

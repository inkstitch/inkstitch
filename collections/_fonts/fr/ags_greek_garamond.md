---
title: "AGS Γαραμου Garamond"
permalink: /fr/fonts/AGS_greek_garamond/
last_modified_at: 2023-05-03
toc: false
preview_image:
  - url: /assets/images/fonts/garamond.png
    height: 20
data_title:
  - ags_garamond_latin_grec
---
{%- assign font = site.data.fonts.ags_garamond_latin_grec.font -%}
![AGS garamond](/assets/images/fonts/garamond.png)


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

{% include folder-galleries path="fonts/ags_greek_garamond/" %}



[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/ags_garamond_latin_grec/LICENSE)

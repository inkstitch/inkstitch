---
title: "Lobster AGS"
permalink: /fr/fonts/lobster_ags/
last_modified_at: 2022-05-27
toc: false
preview_image: /assets/images/fonts/lobster_two_bold_italic.png
preview_image:
  - url: /assets/images/fonts/lobster_AGS.jpg
    height: 27
data_title:
  - lobster_AGS
---
{%- assign font = site.data.fonts.lobster_AGS.font -%}
## Bold Italic

![Lobster AGS](/assets/images/fonts/lobster_AGS.jpg)

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
{% include folder-galleries path="fonts/lobster_ags/" %}

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/lobster_AGS/LICENSE)

---
title: "Pisankris"
permalink: /fr/fonts/pisankris/
last_modified_at: 2022-05-27
toc: false
preview_image:
  - url: /assets/images/fonts/pisankris.png
    height: 30
data_title:
  - pisankris
---
{%- assign font = site.data.fonts.pisankris.font -%}

![Pisankris](/assets/images/fonts/pisankris.png)

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

{% include folder-galleries path="fonts/pisankris/" %}


[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/pisankris/LICENSE)

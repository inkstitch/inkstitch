---
title: "Gingo200"
permalink: /fr/fonts/gingo200/
last_modified_at: 2025-05-28
toc: false
preview_image:
  - url: /assets/images/fonts/gingo200.png
    height: 36
data_title:
  - gingo200
---
{%- assign font = site.data.fonts.gingo200.font -%}
![gingo200](/assets/images/fonts/gingo200.png)

## Glyphes

Cette fonte comporte  {{ font.glyphs.size }} glyphes:

```
{{ font.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }


## Dimensions

A une échelle de  100% ces fontes ont une hauteur approximative de  {{ font.size }} mm. 

Elle peuvent être redimensionnées de {{ font.min_scale | times: 100 | floor }}% ({{ font.size | times: font.min_scale }} mm)
à {{ font.max_scale | times: 100 | floor }}% ({{ font.size | times: font.max_scale }} mm).

## Dans la vraie vie 

{% include folder-galleries path="fonts/gingo200/" %}

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/gingo200/LICENSE)

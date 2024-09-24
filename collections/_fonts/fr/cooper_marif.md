---
title: "CooperMarif"
permalink: /fr/fonts/cooper_marif/
last_modified_at: 2024-06-23
toc: false
preview_image:
  - url: /assets/images/fonts/cooper_marif.png
    height: 90
data_title:
  - cooper_marif
---
{%- assign font = site.data.fonts.cooper_marif.font -%}
![Cooper Marif](/assets/images/fonts/cooper_marif.png)

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

{% include folder-galleries path="fonts/cooper_marif/" %}



[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/cooper_marif/LICENSE)

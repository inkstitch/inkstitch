---
title: "MAM Script"
permalink: /fr/fonts/mam_script/
last_modified_at: 2025-12-26
toc: false
preview_image:
  - url: /assets/images/fonts/mam_script.png
    height: 36
data_title:
  - mam_script
---
{%- assign font = site.data.fonts.kaushan_script_MAM.font -%}

![MAM Script](/assets/images/fonts/mam_script.png)


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

Ici, la date est brodée avec MAM Script , le reste avec *Cherry for Ink/Stitch* et *Cherry for Kaalleen*.

{% include folder-galleries path="fonts/mam_script/" %}

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/mam_script_MAM/LICENSE)

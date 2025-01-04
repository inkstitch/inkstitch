---
title: "Western light"
permalink: /fr/fonts/western_light/
last_modified_at: 2025-01-04
toc: false
preview_image:
  - url: /assets/images/fonts/western_light.png
    height: 53
data_title:
  - western_light
---
{%- assign font = site.data.fonts.western_light.font -%}

{% include upcoming_release.html %}

![Western light](/assets/images/fonts/western_light.png)

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

{% include folder-galleries path="fonts/western_light/" %}

## License

[Télécharger la license de la police](https://github.com/inkstitch/inkstitch/tree/main/fonts/western_light/LICENSE)

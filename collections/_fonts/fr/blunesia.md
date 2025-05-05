---
title: "Blunesia 72"
permalink: /fr/fonts/blunesia/
last_modified_at: 2025-05-O5
toc: false
preview_image:
  - url: /assets/images/fonts/blunesia_72.png
    height: 24
data_title:
  - blunesia
---
{%- assign font = site.data.fonts.blunesia.font -%}

{% include upcoming_release.html %}

![Blunesia](/assets/images/fonts/blunesia_72.png)

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

{% include folder-galleries path="fonts/blunesia/" %}
## License

[Télécharger la license de la police](https://github.com/inkstitch/inkstitch/tree/main/fonts/blunesia/LICENSE)

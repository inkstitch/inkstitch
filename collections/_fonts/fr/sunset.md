---
title: "Sunset"
permalink: /fr/fonts/sunset/
last_modified_at: 2025-01-04
toc: false
preview_image:
  - url: /assets/images/fonts/sunset.png
    height: 53
data_title:
  - sunset
---
{%- assign font = site.data.fonts.sunset.font -%}

{% include upcoming_release.html %}

![Sunset](/assets/images/fonts/sunset.png)

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
{% include folder-galleries path="fonts/sunset/" %}

## License

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/sunset/LICENSE)

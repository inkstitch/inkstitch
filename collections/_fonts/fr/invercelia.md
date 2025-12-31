---
title: "Invercelia"
permalink: /fr/fonts/invercelia/
last_modified_at: 2024-05-13
toc: false
preview_image:
  - url: /assets/images/fonts/invercelia.png
    height: 60
data_title:
  - invercelia
---
{%- assign font = site.data.fonts.invercelia.font -%}

![Invercellia](/assets/images/fonts/invercelia.png)

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

{% include folder-galleries path="fonts/invercelia/" %}

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/invercelia/LICENSE)

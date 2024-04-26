---
title: "Fold Ink/Stitch"
permalink: /fr/fonts/fold_inkstitch/
last_modified_at: 2022-05-27
toc: false
preview_image:
  - url: /assets/images/fonts/fold_inkstitch.jpg
    height: 63
---
{%- assign font = site.data.fonts.fold_inkstitch.font -%}
![FoldInkstitch](/assets/images/fonts/fold_inkstitch.jpg)

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

{% include folder-galleries path="fonts/fold_inkstitch/" %}

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/fold_inkstitch/license)

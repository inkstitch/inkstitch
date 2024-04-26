---
title: "Learning Curve"
permalink: /fr/fonts/learning-curve/
last_modified_at: 2022-05-27
toc: false
preview_image:
  - url: /assets/images/fonts/learning_curve.jpg
    height: 25
---
{%- assign font = site.data.fonts.learning_curve.font -%}
![LearningCurve](/assets/images/fonts/learning_curve.jpg)

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

{% include folder-galleries path="fonts/learning_curve/" %}

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/learning_curve/LICENSE)

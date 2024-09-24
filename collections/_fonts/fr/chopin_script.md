---
title: "Chopin Script"
permalink: /fr/fonts/chopin/
last_modified_at: 2022-05-27
toc: false
preview_image:
  - url: /assets/images/fonts/chopin_script.jpg
    height: 59
data_title:
  - chopin
---
{%- assign font = site.data.fonts.chopin.font -%} 
![Chopin Script](/assets/images/fonts/chopin_script.jpg)


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

Sur des coussins, mais aussi sur serviette, polo, T Shirt, polaire.

{% include folder-galleries path="fonts/chopin/" %}

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/chopin/LICENSE)

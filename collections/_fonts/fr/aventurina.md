---
title: "Aventurina"
permalink: /fr/fonts/aventurina/
last_modified_at: 2022-05-27
toc: false
preview_image:
  - url: /assets/images/fonts/aventurina.jpg
    height: 20
data_title:
  - aventurina
---
{%- assign font = site.data.fonts.aventurina.font -%}
![Aventurina](/assets/images/fonts/aventurina.jpg)

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
Marque page, essuie-mains...

{% include folder-galleries path="fonts/aventurina/" %}



[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/aventurina/LICENSE)

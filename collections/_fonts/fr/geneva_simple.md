---
title: "Geneva Simple"
permalink: /fr/fonts/geneva_simple/
last_modified_at: 2022-05-27
toc: false
preview_image:
  - url: /assets/images/fonts/geneva_simple_sans.jpg
    height: 13
  - url: /assets/images/fonts/geneva_simple_sans_rounded.jpg
    height: 13
data_title:
  - geneva_rounded
  - geneva_simple
---
{%- assign font2 = site.data.fonts.geneva_rounded.font -%}
{%- assign font1 = site.data.fonts.geneva_simple.font -%}


## Sans

![Geneva Simple Sans](/assets/images/fonts/geneva_simple_sans.jpg)



### Glyphes

Cette fonte comporte  {{ font1.glyphs.size }} glyphes:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Sans Rounded

![Geneva Simple Sans](/assets/images/fonts/geneva_simple_sans_rounded.jpg)



### Glyphes

Cette fonte comporte  {{ font2.glyphs.size }} glyphes:

```
{{ font2.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Dimensions

A une échelle de  100% cesfontes ont une hauteur approximative de  {{ font.size }} mm. 

Elles peuvet être redimensionnées  de {{ font.min_scale | times: 100 | floor }}% ({{ font.size | times: font.min_scale }} mm)
à {{ font.max_scale | times: 100 | floor }}% ({{ font.size | times: font.max_scale }} mm).


## Dans la vraie vie

{% include folder-galleries path="fonts/geneva/" %}

[Download Font License Geneva Simple](https://github.com/inkstitch/inkstitch/tree/main/fonts/geneva_simple/LICENSE)

[Download Font License Geneva Rounded](https://github.com/inkstitch/inkstitch/tree/main/fonts/geneva_rounded/LICENSE)



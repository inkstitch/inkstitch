---
title: "Ondulamarif"
permalink: /fr/fonts/ondulamarif/
last_modified_at: 2024-05-13
preview_image:
  - url: /assets/images/fonts/ondulamarif_XL.png
    height: 110
  - url: /assets/images/fonts/ondulamarif_Medium.png
    height: 82
  - url: /assets/images/fonts/ondulamarif_small.png
    height: 44
---
{%- assign font3 = site.data.fonts.ondulamarif_S.font -%}
{%- assign font2 = site.data.fonts.ondulamarif_Medium.font -%}
{%- assign font1 = site.data.fonts.ondulamarif_XL.font -%}


## Ondulamarif XL

![Ondulamarif XL](/assets/images/fonts/ondulamarif_XL.png)
## Glyphes

Cette fonte comporte  {{ font1.glyphs.size }} glyphes:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }


## Dimensions

A une échelle de  100% cette fonte a une hauteur approximative de  {{ font1.size }} mm. 

Elle peut être agrandie jusqu'à   {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm), mais ne doit pas être diminuée




## Ondulamarif Medium
![Ondulamarif Medium](/assets/images/fonts/ondulamarif_Medium.png)
## Glyphes

Cette fonte comporte  {{ font2.glyphs.size }} glyphes:

```
{{ font2.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }


## Dimensions

Cette variation d'ondulamarif XL   peut être utilisée 
 de {{ font2.min_scale | times: 100 | floor }}% ({{ font1.size | times: font2.min_scale }} mm)
à {{ font2.max_scale | times: 100 | floor }}% ({{ font1.size | times: font2.max_scale }} mm).

## Ondulamarif Small
![Ondulamarif Small](/assets/images/fonts/ondulamarif_small.png)
## Glyphes

Cette fonte comporte  {{ font2.glyphs.size }} glyphes:

```
{{ font2.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }


## Dimensions

Cette variation d'ondulamarif XL   peut être utilisée 
 de {{ font3.min_scale | times: 100 | floor }}% ({{ font1.size | times: font3.min_scale }} mm)
à {{ font3.max_scale | times: 100 | floor }}% ({{ font1.size | times: font3.max_scale }} mm).



## Dans la vraie vie


{% include folder-galleries path="fonts/ondulamarif/" %}

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/ondulamarif_XL/LICENSE)

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/ondulamatif_Medium/LICENSE)

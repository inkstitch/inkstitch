---
title: "Ondulamarif"
permalink: /fr/fonts/ondulamarif/
last_modified_at: 2024-05-22
preview_image:
  - url: /assets/images/fonts/ondulamarif_xl.png
    height: 55
  - url: /assets/images/fonts/ondulamarif_medium.png
    height: 41
  - url: /assets/images/fonts/ondulamarif_small.png
    height: 22
data_title:
  - ondulamarif_S
  - ondulamarif_Medium
  - ondulamarif_XL
---
{%- assign font3 = site.data.fonts.ondulamarif_S.font -%}
{%- assign font2 = site.data.fonts.ondulamarif_Medium.font -%}
{%- assign font1 = site.data.fonts.ondulamarif_XL.font -%}


## Ondulamarif XL
<img 
     src="/assets/images/fonts/ondulamarif_xl.png"
     alt="Ondulamarif XL " height="77">
     
**Ondulamarif XL à 100% présente un nombre d’ondulations  égal à  6 et ce nombre augmente lorsque la fonte  est agrandie.**

### Glyphes

Cette fonte comporte  {{ font1.glyphs.size }} glyphes:

```
{{ font1.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }


### Dimensions

A une échelle de  100% cette fonte a une hauteur approximative de  {{ font1.size }} mm. 

Elle peut être agrandie jusqu'à   {{ font1.max_scale | times: 100 | floor }}% ({{ font1.size | times: font1.max_scale }} mm), mais ne doit pas être diminuée

## Ondulamarif Medium

<img 
     src="/assets/images/fonts/ondulamarif_medium.png"
     alt="Ondulamarif Medium " height="61">
     
**Ondulamarif Medium  présente un nombre d’ondulations toujours égal à  6.**

### Glyphes

Cette fonte comporte  {{ font2.glyphs.size }} glyphes:

```
{{ font2.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }



###  Dimensions

Cette variation d'ondulamarif XL   peut être utilisée 
 de {{ font2.min_scale | times: 100 | floor }}% ({{ font1.size | times: font2.min_scale }} mm)
à {{ font2.max_scale | times: 100 | floor }}% ({{ font1.size | times: font2.max_scale }} mm).

## Ondulamarif Small
<img 
     src="/assets/images/fonts/ondulamarif_small.png"
     alt="Ondulamarif Small " height="33">

**Ondulamarif Small présente un nombre d’ondulations toujours égal à  4.**

### Glyphes

Cette fonte comporte  {{ font2.glyphs.size }} glyphes:

```
{{ font2.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }


### Dimensions

Cette variation d'ondulamarif XL   peut être utilisée 
 de {{ font3.min_scale | times: 100 | floor }}% ({{ font1.size | times: font3.min_scale }} mm)
à {{ font3.max_scale | times: 100 | floor }}% ({{ font1.size | times: font3.max_scale }} mm).

## Trier les couleurs 

Si vous souhaitez trier les  couleurs [voici comment faire](https://inkstitch.org/fr/docs/lettering/#tri-des-couleurs)

## Broder en monochrome.... ou pas

Vous pouvez aussi broder ondulamarif avec une seul fil. Dans ce cas, ne triez pas les couleurs, mais donnez la même couleur de contour à tous les objets du lettrage, cela vous épargnera beaucoup de stops et sauts inutiles. 

Cela ne signifie pas qu'ondulamarif devient alors monocolore, car elle est très jolie brodée avec un fil multicolore.



## Dans la vraie vie


{% include folder-galleries path="fonts/ondulamarif/" %}

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/ondulamarif_XL/LICENSE)

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/ondulamarif_Medium/LICENSE)

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/ondulamarif_S/LICENSE)

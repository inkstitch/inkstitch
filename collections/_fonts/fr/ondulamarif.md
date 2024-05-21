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
<img 
     src="/assets/images/fonts/ondulamarif_XL.png"
     alt="Ondulamarif XL " height="55">
     
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

<img 
     src="/assets/images/fonts/ondulamarif_Medium.png"
     alt="Ondulamarif XL " height="41">

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
<img 
     src="/assets/images/fonts/ondulamarif_small.png"
     alt="Ondulamarif XL " height="22">

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

## Ajouter de la couleur  à Ondulamarif.

Une manière très simple d'ajouter de la couleur à Ondulamarif est d'utiliser un fil multicolore. 

Mais elle est aussi  très jolie  bicolore en utilisant un fil différent pour les contours. 

Il est  facile  de sélectionner tous les contours:
* soit en utilisant Ink/Stitch  > Édition > Sélection des éléments de broderie et en recherchant  les  points droits qui sont paramètrés en point triple (mais actuellement cette méthode ne fonctionne pas pour les utilisateurs de mac)
* soit en utilisant Inkscape >  Édition  >  Rechercher et Remplacer et rechercher "contour" (sans les guillements). La recherche doit être étendue aux propriétés, et il faut cocher "valeur de l'attribut" dans Propriétés. Après avoir cliquer sur Rechercher, tous les contours sont sélectionnés et leur couleur peut-être facilement modifiée.

* Si vous souhaitez ensuite trier les  couleurs [voici comment faire](https://inkstitch.org/fr/docs/lettering/#tri-des-couleurs)



## Dans la vraie vie


{% include folder-galleries path="fonts/ondulamarif/" %}

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/ondulamarif_XL/LICENSE)

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/ondulamarif_Medium/LICENSE)

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/ondulamarif_S/LICENSE)

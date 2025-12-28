---
title: "Initials"
permalink: /fr/fonts/initials/
last_modified_at: 2025-12-26
toc: false
preview_image: 
  - url: /assets/images/fonts/initials_xl.jpg
    height: 150
  - url: /assets/images/fonts/initials_medium.jpg
    height: 90
data_title:
  - initials_medium
  - initials_xl
---
{%- assign font = site.data.fonts.initials_medium.font -%}

![Initials XL](/assets/images/fonts/initials_xl.jpg)

![Initials medium](/assets/images/fonts/initials_medium.jpg)

## Glyphes

Chacune de ces deux fontes comporte {{ font.glyphs.size }} glyphes:

```
{{ font.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

Remarque : Les glyphes ;:,.(){}[] sont utilisés pour stocker des cadres.

## Dimensions
### Initials XL 
Utilisée à 100%, cette fonte fait environ 150 mm.
Elle peut être agrandie jusqu'à 200% (env 300 mm) ou diminuée jusqu'à 70% (env 100 mm).
### Initials Medium 
Utilisée à 100%, cette fonte fait environ 90 mm.
Elle peut être agrandie jusqu'à 200% (env 180 mm) ou diminuée jusqu'à 70% (env 60 mm).

## Description

### Initials XL 

La fonte Initials XL est prévue pour être utilisée une seule lettre à la fois.
Pour obtenir une lettre encadrée, taper cette lettre et une des "lettres cadres" dans la fenêtre de lettrage, sur la même ligne, sans espace entre les deux. 

Attention : tous les cadres ne conviennent pas à toutes les lettres, en particulier aux lettres très larges comme le M ou le W, ou aux lettres très hautes comme le J. Il est bien sûr très facile dans Inkscape de modifier le positionnement de la lettre par rapport au cadre si elle ne convient pas, ou de modifier la forme d'un cadre, par exemple en transformant un cercle en ellipse pour accueillir un J récalcitrant.

### Initials Medium 

Cette fonte est réduite et simplifiée. On garde la possibilité d'encadrer une lettre, mais le positionnement de la lettre par rapport au cadre est plus approximatif que dans la fonte XL. En revanche il est tout à fait possible d'écrire des mots avec des lettres correctement positionnées, ce qui n'est pas le cas avec la fonte XL.

## Tableau de correspondance des cadres

Frame|Key
---|---
![ouvrante](/assets/images/fonts/sortefax/ouvrante.png)|<key>(</key>
![fermante](/assets/images/fonts/sortefax/fermante.png)|<key>)</key>
![ouvrantecarre](/assets/images/fonts/sortefax/square-bracket-open.png)|<key>[</key>
![fermantecarre](/assets/images/fonts/sortefax/square-bracket-open.png)|<key>]</key>
![accolade_ouvrante](/assets/images/fonts/sortefax/curly-bracket-open.png)|<key>{</key>
![accolade_fermante](/assets/images/fonts/sortefax/curly-bracket-close.png)|<key>}</key>
![Point](/assets/images/fonts/sortefax/point.png)|<key>.</key>
![Virgule](/assets/images/fonts/sortefax/virgule.png)|<key>,</key>
![DeuxPoints](/assets/images/fonts/sortefax/deuxpoints.png)|<key>:</key>
![PointVirgule](/assets/images/fonts/sortefax/pointvirgule.png)|<key>;</key>


## Dans la vraie vie

{% include folder-galleries path="fonts/initials/" %}


[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/initials_xl/LICENSE)

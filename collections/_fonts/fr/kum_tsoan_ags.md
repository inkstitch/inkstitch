---
title: "Kum Tsoan  AGS"
permalink: /fr/fonts/kum_tsoan_ags/
last_modified_at: 2024-06-22
toc: false
preview_image:
  - url: /assets/images/fonts/kum_tsoan.jpg
    height: 90
  - url: /assets/images/fonts/kum_tsoan_tartan.jpg
    height: 90
  - url: /assets/images/fonts/kum_tsoan_relief.png
    height: 90
data_title:
  - kum_tsoan_ags
  - kum_tsoan_relief
  - kum_tsoan_tartan
---
{%- assign font = site.data.fonts.kum_tsoan_ags.font -%}

{%- assign font2 = site.data.fonts.kum_tsoan_relief.font -%}

![Kum Tsoan AGS](/assets/images/fonts/kum_tsoan.jpg)

![Kum Tsoan _relief](/assets/images/fonts/kum_tsoan_relief.png)

![Kum Tsoan Tartan](/assets/images/fonts/kum_tsoan_tartan.jpg)



## Glyphes

Ces fontes comportent  {{ font.glyphs.size }} glyphes:

```
{{ font.glyphs | sort | join: ' ' }}
```
{: .font-glyphs }

## Dimensions

A une échelle de  100% ces fontes ont une hauteur approximative de  {{ font.size }} mm. 

Kum Tsoan  AGS et Kum Tsoan  Tartan  peuvent être redimensionnées  de {{ font.min_scale | times: 100 | floor }}% ({{ font.size | times: font.min_scale }} mm)
à {{ font.max_scale | times: 100 | floor }}% ({{ font.size | times: font.max_scale }} mm).

Kum Tsoan  relief est beaucoup plus tolérante et peut être redimensionnée de {{ font2.min_scale | times: 100 | floor }}% ({{ font2.size | times: font2.min_scale }} mm)
à {{ font2.max_scale | times: 100 | floor }}% ({{ font2.size | times: font2.max_scale }} mm). La vraie limite supérieure est celle du cadre de broderie.



## Comment les utiliser
### Kum Tsoan AGS
Kum Tsoan  AGS est une fonte d'appliqué

Les trois couleurs de cette version correspondent à trois étapes de broderie :
* première étape, rouge , indique ou poser le tissu de l'appliqué. Peut aussi être utilisé pour créer un fichier pour les machines de découpe.
* deuxième étape, vert, fixe le tissu avec un petit zigzag. Après cette étape, il faut découper le tissu.
* troisième étape, noir, brode le satin autour des lettres. 


### Kum Tsoan Relief
Telle quelle Kum Tsoan Relief est prévue pour être utilisée ainsi  
*  placer une doublure sur le stabilisateur.
*  broder la première couleur (rouge). C'est un positionnement, en point droit,  qui indique où poser  la mousse pour obtenir un effet relief.
*  poser la mousse puis broder la seconde couleur (verte) : ce point triple va découper la mousse.
*  enlever l'excès de mousse et poser le tissu "définitif".
*  broder la dernière couleur (bleue): Un point quintuple est brodé autour des lettres.
  

Si vous brodez plusieurs lettres, il est possible de trier les couleurs. [Voici comment faire](https://inkstitch.org/fr/docs/lettering/#tri-des-couleurs)


Si vous supprimez la couleur de contour des chemins verts et la remplacez par une couleur de remplissage,  vous pouvez aussi utiliser la fonte de la manière suivante :
*  placer le tissu définitif sur le stabilisateur.
*  broder le remplissage (par exemple un remplissage tartan ou un remplissage en dégradé linéaire).
*  scotcher la mousse au dos du stabilisateur.
*  broder la seconde couleur (rouge) : ce point triple va découper la mousse.
*  enlever l'excès de mousse et poser une doublure sous la de mousse .
*  broder la dernière couleur (bleue): Un point quintuple est brodé autour des lettres, prenant la mousse en sandwich entre la doublure et le tissu définitif.

[Vous trouverez ici  plus de détails pour utiliser cette fonte.](https://lyogau.over-blog.com/2024/06/broderie-en-relief-mousse-puffy-ou-autre.html)

###  Kum Tsoan Tartan

Cette  version tente de ressembler à un appliqué de tissus écossais (tartan). Elle utilise un tartan différent par lettre, ce qui induit un grand nombre de changements de fils.  Il existe [une technique](https://inkstitch.org//fr/tutorials/make_tartan_font_easier/) pour utiliser le même tartan pour toutes les lettres et ainsi réduire très fortement le nombre de changements de fils.


## Dans la vraie vie

{% include folder-galleries path="fonts/kum_tsoan_ags/" %}

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/kum_tsoan_AGS/LICENSE)

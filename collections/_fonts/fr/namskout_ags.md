---
title: "Namskout AGS"
permalink: /fr/fonts/namskout_ags/
last_modified_at: 2022-05-28
toc: false
preview_image:
  - url: /assets/images/fonts/namskout_AGS.jpg
    height: 90
  - url: /assets/images/fonts/namskout_tartan.png
    height: 90
---
{%- assign font = site.data.fonts.namskout_AGS.font -%}
![NamskoutAGS](/assets/images/fonts/namskout_AGS.jpg)

![NamskoutTartan](/assets/images/fonts/namskout_tartan.png)




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

## Comment les utiliser
### Namskout  AGS
Namskout AGS est une fonte d'appliqué

Les trois couleurs de cette version correspondent à trois étapes de broderie :
* première étape, rouge , indique ou poser le tissu de l'appliqué. Peut aussi être utilisé pour créer un fichier pour les machines de découpe.
* deuxième étape, vert, fixe le tissu avec un petit zigzag. Après cette étape, il faut découper le tissu.
* troisième étape, noir, brode le satin autour des lettres. 


###  Namskout Tartan

Cette  version tente de ressembler à un appliqué de tissus écossais (tartan). Elle utilise un tartan différent par lettre, ce qui induit un grand nombre de changements de fils.  Il existe [une technique](https://inkstitch.org//fr/tutorials/make_tartan_font_easier/) pour utiliser le même tartan pour toutes les lettres et ainsi réduire très fortement le nombre de changements de fils.


## Dans la vraie vie

{% include folder-galleries path="fonts/namskout_ags/" %}

[Download Font License](https://github.com/inkstitch/inkstitch/tree/main/fonts/namskout_AGS/LICENSE)

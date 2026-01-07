---
title: Mélange de couleurs
permalink: /fr/tutorials/color-blending/
last_modified_at: 2026-01-07
language: fr
excerpt: "Dégradés de couleur"
image: "/assets/images/tutorials/tutorial-preview-images/blend.png"
tutorial-type:
  - Sample File
stitch-type: 
  - Fill Stitch
techniques:
field-of-use:
tool:
  -Fill Stitch
user-level:
---
Les remplissages automatiques ne sont pas forcement des aplats de couleurs, il est possible d'avoir des remplissages en dégradé. 

## Remplissage en dégradé linéaire

La génération de dégradés de couleurs avec Ink/Stitch est devenue facile. La meilleure qualités sera obtenue en utilisant le
[remplissage en dégradé linéaire](/fr/docs/stitches/linear-gradient-fill/), qui cherche à produire un remplissage aussi régulier que possible en terme de position des points et des rangées malgré les changements  de couleur.

* Créez un remplissage avec un dégradé linéaire dans Inkscape
* Dans le dialogue de paramétrage, choisir la méthode "remplissage en dégradé linéaire"

## Extension : Convertir en blocs de dégradés
Ink/Stitch dispose aussi d'un outil qui permet de séparer  des remplissages dégradés en plusieurs blocs monochromes indépendant. La qualité ne sera pas aussi bonne qu'avec un remplissage en dégradé linéaire, mais cela peut parfois être utile.Voir l'extension [Convertir en blocs de dégradés](/fr/docs/fill-tools/#convert-to-gradient-blocks)

* Créer une forme dont la couleur est un dégradé Inkscape, choisissez l'angle du dégradé sur le canevas  en mode édition de noeuds à l'aide des poignées du dégradé, c'est cette direction qui détermine l'*angle* du remplissage.
* Choisir la méthode de remplissage **automatique** et vos autres paramètres de remplissage (mais l'angle ou l'espacement final entre les rangées seront ignorés, et toute sous-couche sera ignorée)
* Sélectionner la forme
* `Extensions > Ink/Stitch > Outils : Remplissage> Convertir en blocs de dégradés`
* Choisir l'espacement final des rangées dans la fenêtre qui s'ouvre

Plus d'informations [ici](/fr/docs/fill-tools/#convertir-en-blocs-de-dégradés)


{% include folder-galleries path="color-blending/" captions="1:Dégradé inkscape;2:Résultat de l'extension ;3:Vision éclatée;" %}
Si le dégradé comporte n+1 couleurs, l'extension découpe la forme en n parties et empile deux blocs de dégradé sur chaque partie.

Dans la broderie, cela produira n+1 blocs de couleurs.
Ces 2n blocs de dégradé ont tous un espacement variable. Si l'on regarde deux blocs superposés, l'espacement de la première couleur diminue au fur et a mesure que l'espacement de la seconde augmente, produisant  l'impression d'un dégradé de la première à la seconde couleur.




### A quoi est du l'espacement variable entre les rangées ?

Donner une valeur au paramètre *Espacement final entre les rangées* déclenche un espacement variable entre les rangées.
En regardant perpendiculairement à l'*angle* de remplissage, l'espacement entre les rangées varie linéairement depuis la valeur  *espacement entre les rangées* jusqu'à la valeur *espacement final entre les rangées*.

Les deux blocs de dégradés que `Extensions > Ink/Stitch > Outils : Remplissage> Convertir en blocs de dégradés` empile sur chaque partie de la forme ont en fait le mêmes valeurs pour  *espacement entre les rangées* et  *espacement final entre les rangées*, mais leur *angles*  de remplissage sont opposés, remplissant ainsi les conditions d'obtention d'un dégradé. Les valeurs de ces paramètre dépendent du paramétrage initial de la forme, et visent à maintenir la densité de points souhaités. Il n'y a pas de sous-couche, sauf éventuellement sur les parties monochromes du dégradé.


### Ajuster le résultat

Utiliser l'extension plutôt que créer manuellement le découpage de la forme en  blocs de dégradés  est un énorme gain de temps. 
Vous pouvez modifier précautionneusement les valeurs des paramètres *espacement entre les rangées* et  *espacement final entre les rangées* pour obtenir un effet de dégradé différent, mais soyez attentif à de possibles problèmes de densité . Souvenez vous que la densité dépend de l'inverse de l'*espacement entre les rangées*. Si les deux couleurs confondues, vous souhaitez un certain *espacement entre les rangées* **e**, la somme des inverses des espacement entre les rangées des deux blocs dégradés doit être égale à **1/e**, de même que la somme des inverses des *espacements finaux entre les rangées*.



Ceci est une vue partielle d'un fichier contenant 100 rectangles, chacun d'entre eux recouvert de remplissages à espacement variable rouge et bleu, pour différentes valeurs des deux paramètres

![Download Sample File](/assets/images/tutorials/samples/end_row_spacing_2_colors_blending.svg)
[Télécharger l'example](/assets/images/tutorials/samples/end_row_spacing_2_colors_blending.svg) 



## Dégradé manuel
Si vous souhaiter réaliser manuellement un dégradé, voici deux techniques possibles

### Faux Remplissage dégradé

1. Un faux dégradé a une couche de remplissage régulier en bas et chaque couche suivante a des paramètres de densité variables
2. Assurez-vous que toutes les couches ont le même angle de point, c'est ce qui permet le mélange
3. Lorsque vous faites plus de 2 couches, chaque couche utilise moins de densité que la couche précédente.
4. Gardez les mêmes points de départ et d'arrivée pour chaque couche. Par exemple, si la couche de base commence tout en haut et se termine en bas à droite, suivez la même séquence pour chaque couche.
5. La sous-couche n'est généralement pas nécessaire, mais cela dépend du projet individuel.
6. En règle générale, il est préférable de passer des couleurs claires aux couleurs sombres, mais cela dépend du design et de l'aspect final souhaité.
7. Bien qu'il ne s'agisse pas d'un véritable dégradé, dans la plupart des cas, ce type de mélange est suffisant pour obtenir l'aspect final souhaité.
8. Les valeurs de densité dans cet exemple ne sont pas figées, mais juste pour illustrer le concept. Les véritables paramètres dépendent du design, du tissu utilisé et de la taille du design.

[Télécharger le fichier exemple](/assets/images/tutorials/samples/Faux_Fill_Blend.svg){: download="/assets/images/tutorials/samples/Faux_Fill_Blend.svg" }

### Véritable dégradé

1. Beaucoup de conditions des faux dégradés s'appliquent également ici. Angle de point, séquence de début / fin, passage des couleurs claires aux couleurs sombres (dépend également du motif)
2. La plus grande différence réside dans les mathématiques et plus le dégradé est compliqué, plus les calculs sont compliqués. Il suffit de s’assurer que chaque couche d’une section donnée correspond à 100% de la densité de cette section.
3. Cela peut impliquer plus de couches de couleurs et plus d'incréments de variation de densité. Le facteur le plus important est la taille / forme de la conception et les spécificités du projet.
4. Ce qui en fait un véritable dégradé par rapport à un faux est que chaque section des couches se mélange réellement.

[Télécharger le fichier exemple](/assets/images/tutorials/samples/True_Blend.svg){: download="True_Blend.svg" }



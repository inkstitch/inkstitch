---
title: Mélange de couleurs
permalink: /fr/tutorials/color-blending/
last_modified_at: 2023-05-0
language: fr
excerpt: "Dégradés de couleur"
image: "/assets/images/tutorials/samples/True_Blend.svg"

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
Les remplissages ne sont pas forcement des aplats de couleurs, il est possible d'avoir des remplissage en dégradé.
Le plus simple est d'utiliser  l'extension Ink/Stitch

## [Convertir en blocs de dégradés](docs/fill-tools/#convert-to-gradient-blocks)
* Créer une forme dont la couleur est un dégradé Inkscape
* Choisir vos paramètres de remplissage
* Sélectionner la forme
* `Extensions > Ink/Stitch > Outils : Remplissage> Convertir en blocs de dégradés`

Plus d'informations [ici](/fr/docs/fill-tools/#convertir-en-blocs-de-dégradés)



![Download Sample File](/assets/images/tutorials/samples/inkstitch_gradient_extension.svg)

[Download Sample File](/assets/images/tutorials/samples/inkstitch_gradient_extension.svg).



On each subshape, while first color row spacing decreases,  second color row spacing increases, yielding a gradient fill from first color to second color. 


The gradient direction dictates the fill *angle*. 




## How is varying row spacing achieved ?

Setting *End row spacing* parameter allows for a varying row spacing fill. 
Looking perpendicularly to the fill angle, the  row spacing starts at *spacing between rows*  and ends up at *end row spacing*, varying linearly in between.

The two gradient blocks the `Convert to gradient blocks` stacks on each subshape have same *spacing between rows* and *end row spacing* but opposite fill angles, therefore achieving the gradient effect. The actual values of these parameters depends on the initial parameters of the shape, aiming to respect the overall row spacing.

## Tweaking the result

Using the extension instead of manually creating the subshapes and the gradient blocks is a huge time saver. 
You may carefully change the values of *spacing between rows* and *end row spacing* to achieve a different blending effect, but be aware of possible density issue, as you are filling each subshape twice.


These is part of a file containing 100 rectangles each covered by a red varying spacing fill and a blue varying spacing fill, for different values of the parameters

![Download Sample File](/assets/images/tutorials/samples/end_row_spacing_2_colors_blending.svg)

[Dowload the sample  ](/assets/images/tutorials/samples/end_row_spacing_2_colors_blending.svg) 



## Manual blending
If you wish to go the manual way and have total control
## Faux Remplissage dégradé

1. Un faux dégradé a une couche de remplissage régulier en bas et chaque couche suivante a des paramètres de densité variables
2. Assurez-vous que toutes les couches ont le même angle de point, c'est ce qui permet le mélange
3. Lorsque vous faites plus de 2 couches, chaque couche utilise moins de densité que la couche précédente.
4. Gardez les mêmes points de départ et d'arrivée pour chaque couche. Par exemple, si la couche de base commence tout en haut et se termine en bas à droite, suivez la même séquence pour chaque couche.
5. La sous-couche n'est généralement pas nécessaire, mais cela dépend du projet individuel.
6. En règle générale, il est préférable de passer des couleurs claires aux couleurs sombres, mais cela dépend du design et de l'aspect final souhaité.
7. Bien qu'il ne s'agisse pas d'un véritable dégradé, dans la plupart des cas, ce type de mélange est suffisant pour obtenir l'aspect final souhaité.
8. Les valeurs de densité dans cet exemple ne sont pas figées, mais juste pour illustrer le concept. Les véritables paramètres dépendent du design, du tissu utilisé et de la taille du design.

[Télécharger le fichier exemple](/assets/images/tutorials/samples//assets/images/tutorials/samples/Faux_Fill_Blend.svg){: download="/assets/images/tutorials/samples/Faux_Fill_Blend.svg" }

## Véritable dégradé

1. Beaucoup de conditions des faux dégradés s'appliquent également ici. Angle de point, séquence de début / fin, passage des couleurs claires aux couleurs sombres (dépend également du motif)
2. La plus grande différence réside dans les mathématiques et plus le dégradé est compliqué, plus les calculs sont compliqués. Il suffit de s’assurer que chaque couche d’une section donnée correspond à 100% de la densité de cette section.
3. Cela peut impliquer plus de couches de couleurs et plus d'incréments de variation de densité. Le facteur le plus important est la taille / forme de la conception et les spécificités du projet.
4. Ce qui en fait un véritable dégradé par rapport à un faux est que chaque section des couches se mélange réellement.

[Télécharger le fichier exemple](/assets/images/tutorials/samples/True_Blend.svg){: download="True_Blend.svg" }

## End Row Spacing

Ink/Stitch a une fonctionnalité cachée pour effectuer les dégradés de couleurs.

[Read more](/docs/features/#color-blending)

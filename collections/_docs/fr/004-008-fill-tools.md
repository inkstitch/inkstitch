---
title: "Outils Remplissage"
permalink: /fr/docs/fill-tools/
excerpt: ""
last_modified_at: 2023-04-15
toc: true
---
## Briser les objets de remplissage

Les objets de remplissage peuvent être traités au mieux s'ils sont des éléments uniques sans bordures qui se croisent. Parfois, ces règles ne sont pas faciles à respecter et votre forme aura de minuscules petites boucles impossibles à découvrir dans Inkscape.

Par conséquent, les messages d'erreur pour les zones de remplissage sont souvent peu parlants et ennuyeux pour les utilisateurs. Cette extension vous aidera à corriger les formes de remplissage défectueuses. Exécutez-la sur toutes les formes de remplissage qui vous causent des problèmes. Elle réparera votre élément de remplissage et séparera les formes avec des bordures croisées en les partageant en plusieurs parties si nécessaire.


### Usage

* Selectionner un remplissage ou plus
* Exécutez: Extensions > Ink/Stitch  > Outils de remplissage > Briser les objets de remplissage
* Pour la plupart des formes `simple` sera suffisant. Si vous avez encore des problèmes essayez `complex`.

### Simple ou Complexe

Toujours préférer simple si c'est possible. Il conserve les trous et répare "bordure se croise" en divisant les boucles en objets séparés ou en les supprimant si elles sont trop petites pour être brodées.

Bien que "simple" divise les boucles, il ne respectera pas les sous-chemins qui se chevauchent. Il les traitera comme des objets séparés. Complexe est capable de reconnaître les chemins qui se chevauchent et de bien les traiter

"Briser les objets de remplissage" peut être traduit dans les fonctions natives d'Inkscape:

 1. Chemin > Union (Résout les problèmes de sous-chemin)
 2. Chemin > Briser (Séparer les objets)
 3. Supprimer les objets trop petits pour être brodés
 4. Chemin > Combiner (si vous voulez maintenir les trous)
 5. Chemin > Combiner (si vous voulez conserver encore plus de trous)

Info: Pour les chemins qui se chevauchent, l'étape 1 n'est effectuée que par complexe.
{: .notice--info}

![Break apart fill objects](/assets/images/docs/en/break_apart.jpg)
[Download SVG](/assets/images/docs/en/break_apart.svg)

## Convertir en blocs de dégradé 

{% include upcoming_release.html %}

Convertir en blocs de dégradé va découper un remplissage dont la couleur de fond est un dégradé linéaire en plusieurs blocs monochromes avec un espacement de ligne adequat pour rendre l'effet de dégradé.



### Usage

1. Depuis Fond et Contour, appliquez un dégradé linéaire comme couleur de fond à un élement.

   ![linear gradient](/assets/images/docs/en/linear-gradient.png)
   
2. Lancez `Extensions > Ink/Stitch > Outils: Remplissage > Convertir en blocs de dégradé

   ![color blocks](/assets/images/docs/color_blocks.png)
   

{% include tutorials/tutorial_list key="tools" value="Stroke" %}

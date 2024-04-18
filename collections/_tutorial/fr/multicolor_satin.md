---
title: Satin Multicolore
permalink: /fr/tutorials/multicolor_satin/
last_modified_at: 2024-04-18
language: fr
excerpt: "Simuler des colonnes satin multicolore"
image: "assets/images/tutorials/multicolor_satin/snake.jpg"
tutorial-type:
stitch-type: 
  - Satin Stitch
techniques:
field-of-use:
user-level: 
---

# Simuler une colonne satin multicolore.
On parle ici de simulation, car il ne s'agit pas d'une seule colonne satin  multicolore, mais d'un effet simiaire obtenu en 
utilisant plusieurs  copies superposées d'une même colonne satin, simplement en modifiant les paramètrages.

## Pourcentage de compensation d'étirement négatif asymètrique
Pour obtenir des colonnes satin multicolores, on va utiliser le paramètre "pourcentage de compensation d'étirement".

C'est un paramètre asymétrique, c'est à dire qu'il est possible de lui donner deux valeurs différentes (séparées par un espace), la premère valeur s'appliquant au  premier rail, la seconde valeur s'appliquant au second rail.

Il  est courant de donner des valeurs positives aux compensations, mais il est aussi possible de leur donner des valeurs négatives, au lieu d'augmener la largeur de la colonne satin, on la réduit.

Voici trois exemples de valeurs pour le paramètre pourcentage de compensation d'étirement, et le résultat
![compensation](/assets/images/tutorials/multicolor_satin/compensation.png)

Ici le premier rail est le bord gauche du satin.

Quand le paramètre vaut "0 -75" (en vert) on ne touche pas au bord gauche, mais tout se passe comme si le bord droit avait été rapproché régulièrement pour réduire la distance entre les deux rails au quart de la valeur initiale.

Quand le paramétre vaut "-25  -25" (en rouge) les deux bords se rapporchent du centre et la largeur de la colonne est uniformément réduite de moitié.

Quand le paramétre vaut "-75  0" (en bleu) on ne touche pas au bord gdroit, mais tout se passe comme si le bord gauche avait été rapproché régulièrement pour réduire la distance entre les deux rails au quart de la valeur initiale.

Si l'on superpose ces trois colonnes, on obtient un serpent tricolore

![tricolor](/assets/images/tutorials/multicolor_satin/tricolor_snake.png)


**Remarque** Il est tout à fait possible d'utiliser sur la même colonne satin, une compensation d'étirement en mm et une compensation en pourcentage. Les deux paramètres sont asymétriques. Les deux paramètres acceptent des valeurs négatives.
{: .notice--info }


## Augmentation (et Diminution) de la largeur aléatoire de satin (en pourcentage)






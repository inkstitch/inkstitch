---
title: "Points d'arrêt"
permalink: /fr/docs/stitches/lock-stitches/
last_modified_at: 2025-01-04
toc: true
---

## Qu'est ce que c'est
Les points d'arrêt sont des petits points au début (point d'arrêt initial) ou à la fin (point d'arrêt final) d'une couleur ou d'un saut de fil ou d'une commande de coupe. Ils aident à sécuriser le fil.

## Facteurs d'influence (autrement dit quand y-a-t-il des points d'arrêt)


Le fichier de broderie est composé de multiples objets brodés consécutivement. Il y aura des points d'arrêts entre deux objets consécutifs parce qu'il y a un changement de couleur ou une commande de coupe ou parce que les objets sont distants l'un de l'autre. `Autorisez les points d'arrêt` permet l'interdiction des points d'arrêts tandis que `forcer les points d'arrêts` permet de s'assurer de leur présence.


### Longueur minimum de saut

La longueur minimum de saut peut être réglée globalement dans `Extension > Ink/Stitch > Préférences` ou objet par objet dans le dialogue de paramétrage.

C'est elle qui définie si un point entre deux objets est un saut ou bien un point normal.

Ce n'est que si la distance entre deux objets consécutifs est plus grande que la `longueur minimum de saut` qu'il y a un saut entre eux. Ce n'est que lorsqu'il y a un saut que des points d'arrêt sont ajouter : points d'arrêt finaux au premier objet et points d'arrêt initiaux au second objet.

![Trois traits, la première distance est 1 mm, la seconde distance 3 mm, et la longueur minimum de saut est 2. Il n'y a pas de point d'arrêt à la fin du premier objet et pas de point d'arrêt au début du second objet](/assets/images/docs/lock_stitch_min_jump.svg)
{: .border-shadow }

Mais d'autres paramètres peuvent influencer la question de savoir si des points d'arrêts sont appliqués.



### Changements de couleur 

Il y a toujours des points d'arrêts avant et après un changement de couleur.

### Commandes de coupe

Ink/Stitch insert des points d'arrêt finaux sur un objet porteur de la commande "couper après" et des points d'arrêts initiaux sur l'objet suivant.

![Trois traits, les distances sont de 1 mm, la longueur minimum de saut est à 2. Le trait central a une commande de coupe qui implique des points d'arrêt finaux pour lui et initiaux pour le trait suivant](/assets/images/docs/lock_stitch_trim.svg)
{: .border-shadow }

Ink/Stitch permet d'ajouter des commandes de coupe:

* soit sous forme de commande visuelle en utilisant Extension < Ink/Stitch < Commandes < Attacher des commandes à des objets sélectionnés.
* soit en cochant la case "couper après" dans le dialogue de paramétrage.


### Autoriser les points d'arrêt.

`Autoriser les points d'arrêt` peut supprimer les points d'arrêt initiaux ou finaux qui devraient normalement être appliqués.
{: .notice--info }

![Trois traits, les distances sont de 3 mm, la longueur minimum de saut est à 2. Le trait central est paramètré pour n'autoriser les points d'arrêts qu'à la fin. De ce fait, il n'a pas de points d'arrêt initiaux.](/assets/images/docs/lock_stitch_allow.svg)
{: .border-shadow }

Le paramètre `Autoriser les points d'arrêt` peut empêcher les points d'arrêt initiaux et/ou finaux. Ainsi quand la distance entre deux objets est suffisamment grande pour qu'il y ait un saut, mais que le paramètre `Autoriser les points d'arrêt` du premier objet est réglé sur `Avant`, il n'y aura pas de points d'arrêts finaux pour lui. 
### Forcer les points d'arrêt 

Il est aussi possible de forcer des points d'arrêts initiaux ou finaux pour des objets très proches. Cocher le paramètre `forcer les points d'arrêt` **du premier objet** lui ajoutera des points d'arrêt terminaux ET des points d'arrêt initiaux pour l'objet suivant.

![Trois traits, les distances sont de 1 mm, la longueur minimum de saut est à 2. Le paramètre `forcer les points d'arrêt` est coché pour le trait central, ce qui implique des points d'arrêt finaux pour lui et des points d'arrêt initiaux pour l'objet suivant.](/assets/images/docs/lock_stitch_force.svg)
{: .border-shadow }

Attention, ne cochez pas aussi ce paramètre pour l'objet situé après le saut, car alors en plus de son point d'arrêt initial, vous forcez un point d'arrêt final sur le deuxième objet, et de plus un point d'arrêt initial sur l'objet suivant, quelque soit la distance entre les deux.

`Forcer les points d'arrêt ` forcera toujours les points d'arrêt est prioritaire sur le paramètre `autoriser les points d'arrêt`.
{: .notice--info }




Ink/Stitch offre divers types pour les points d'arrêt et vous permet même de définir le votre.

## Points d'arrêts prédéfinis

![Variantes de points d'arrêt](/assets/images/docs/lock-stitches.png)
{: .img-half }

1. Demi-point. Ceci est le point par défaut, et le seul style disponible dans les versions précédentes d'Ink/Stitch. Il n'a pas d'option de redimensionnement, mais sa taille est relative à la longueur du point : deux demi points en arrière et deux demi points en avant.
2. Flèche, se redimensionne en %
3. Arrière puis avant, se redimensionne en mm
5. Noeud papillon, se redimensionne en %
6. Croix, se redimensionne en %
7. Étoile, se redimensionne en %
8. Triangle, se redimensionne en %
9. Zigzag, se redimensionne en %
10. Personnalisé, se redimensionne en % ou en mm selon le type de chemin.

## Points d'arrêt personnalisés

Il est possible de définir des points d'arrêt personnalisés dans le paramètre chemin personnalisé soit à l'aide d'un chemin svg avec comme unité le mm (échelle : %) soit avec des unités relatives au nombre de pas en avant ou en arrière (échelle :mm)



### Chemin svg personnalisé

Le chemin svg est toujours construit comme s'il s'agissait d'un point d'arrêt initial. S'il est positionné en fin (point d'arrêt final) il sera inversé.

A la fin du chemin svg, un nœud supplémentaire indique l'angle de connexion du chemin avec le point d'arrêt.

Par exemple le Triangle est défini par le chemin M -0.26,0.33 H 0.55 L 0,0.84 V 0 L 0.34,0.82 (ceci est la valeur de l'attribut d du chemin). Sur l'image suivante c'est le chemin en noir.

![Triangle lock stitch](/assets/images/docs/triangle_lock.png)

Les deux chemins rouges et bleus ont été paramétrés avec un triangle comme point d'arrêt initial. 

Le chemin personnalisé est tourné de telle sorte que son dernier segment (le segment en vert) soit dans l'axe du début des chemins bleu et rouge. Ce dernier segment vert ne fait pas partie du point d'arrêt initial et ne sera pas brodé.


### Chemin personnalisé en mm

Les valeurs personnalisées (positives ou négatives) en mm sont séparées par un espace. Par exemple un point d'arrêt personnalisé avec comme valeur de chemin
1 1 -1 -1 , une échelle définie à 0.7 mm fera deux points de 0.7 mm en avant puis deux points de 0.7mm en arrière.
Il est possible d'utiliser des valeurs non entières, (par exemple 0.5 2.2 -0.5 -2.2), si l'utilisateur le souhaite.

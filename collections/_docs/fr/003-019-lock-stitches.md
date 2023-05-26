---
title: "Points de sureté"
permalink: /fr/docs/stitches/lock-stitches/
excerpt: ""
last_modified_at: 2023-04-15
toc: true
---
Les points de sureté sont des petits points au début (point d'ancrage) ou à la fin (point d'arrêt)  d'une couleur ou d'un saut de fil ou d'une commande de coupe.


Ink/Stitch offre divers types pour les points de sureté et vous permet même de définir le votre.

## Points de sureté prédéfinis

![Variantes de points de sureté](/assets/images/docs/lock-stitches.png)
{: .img-half }

1. Demi-point. Ceci est le point par défaut, et le seul style disponible dans les versions précédentes d'Ink/Stitch. Il n'a pas d'option de redimensionnement, mais sa taille est relative à la longeur du point : deux demi points en arrière et deux demi points en avant.
2. Flèche, se redimensionne  en %
3. Arrière puis avant, se redimensionne  en mm
5. Noeud papillon, se redimensionne  en %
6. Croix, se redimensionne  en %
7. Étoile, se redimensionne  en %
8. Triangle, se redimensionne  en %
9. Zigzag, se redimensionne  en %
10. Personnalisé, se redimensionne  en % ou en mm selon le type de chemin.

## Points de sureté personnalisés

Il est possible de définir des points de sureté personnalisés  dans le paramètre chemin personnalisé soit à l'aide d'un chemin svg avec comme unité le mm (échelle : %) soit avec des unités relatives au nombre de pas en avant ou en arrière (échelle :mm)



### Chemin svg personnalisé

Le chemin svg est toujours construit comme s'il s'agissait d'un point d'ancrage (début de la broderie). S'il est positionné en fin (point d'arrêt) il sera inversé.

A la fin du chemin svg, un noeud supplémentaire indique l'angle de connection du chemin avec le point de sureté. Il sera supprimé quand l'angle sera traité.



### Chemin personnalisé en mm

Les valeurs personnalisées en mm sont séparées par un espace. Par exemple un point de sureté personnalisé avec comme valeur de chemin
1 1 -1 -1 , une echelle définie à 0.7 mm  fera deux points de 0.7 mm en avant puis deux points de 0.7mm en arrière.
Il est possible d'utiliser des valeurs non entières, (par exemple 0.5 2.2 -0.5 -2.2), si l'utilisateur le souhaite.

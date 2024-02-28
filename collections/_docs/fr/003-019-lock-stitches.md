---
title: "Points de sureté"
permalink: /fr/docs/stitches/lock-stitches/
last_modified_at: 2024-02-26
toc: true
---
Les points de sureté sont des petits points au début (point d'ancrage) ou à la fin (point d'arrêt)  d'une couleur ou d'un saut de fil ou d'une commande de coupe.

Ink/Stitch permet d'ajouter des commandes de coupe:

* soit sous forme de commande visuelle en utilisant Extension < Ink/Stitch < Commandes < Attacher des commandes à des objets selectionnés
* soit en cochant la case "couper après" dans le dialogue de paramètrage.
  
Le fichier de broderie est composé de multiples objets brodés consécutivement.

Lorsque la distance entre la fin de la broderie d'un objet et le début du suivant est supérieure à la "distance minimum de saut" telle que définie dans Extension > Ink/Stitch > Préférences, alors il y a un saut entre les deux objets, et un point d'arrêt est normalement fait à la fin du premier objet et un point d'ancrage au début du second, sauf si l'un ou l'autre a été interdit dans le paramètrage en modifiant la valeur par défaut (au début et à la fin) du paramètre "autoriser les points d'arrêt".

Si cette distance est inférieure à la "distance minimum de saut", alors le déplacement entre les deux objets est traité commme un point de broderie, sans ajout de points de sureté, quelque soit l'option choisie pour le paramètre "autoriser les points d'arrêt". 

Il est toutefois possible de forcer les points de sureté de chaque coté d'un de ces mini sauts, en cochant la case "forcer les points d'arrêt" lors du paramètrage de l'objet situé avant le saut. Dans ce cas la valeur du paramètre "autoriser les points d'arrêt" est ignorée pour les deux objets de chaque choté du saut. Attention si vous cochez aussi ce paramètre pour l'objet situé après le saut, alors en plus de son point d'ancrage, vous forcez un point d'arrêt sur le deuxième  objet, et de plus un point d'ancrage sur l'objet suivant, quelque soit la distance entre les deux.

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

A la fin du chemin svg, un noeud supplémentaire indique l'angle de connection du chemin avec le point de sureté. 

Par exemple le Triangle est défini par le chemin M -0.26,0.33 H 0.55 L 0,0.84 V 0 L 0.34,0.82 (ceci est la valeur de l'attribut d du chemin). Sur l'image suivante c'est le chemin en noir.

![Triangle lock stitch](/assets/images/docs/triangle_lock.png)

Les deux chemins rouges et bleus ont été paramétrés avec un triangle comme point d'ancrage. 
Le chemin personnnalisé est tourné de telle sorte que son dernier segment (le segment en vert) soit dans l'axe du début des chemins bleu et rouge. Ce dernier segment vert ne fait pas partie du point d'ancrage et ne sera pas brodé.


### Chemin personnalisé en mm

Les valeurs personnalisées (positives ou négatives) en mm sont séparées par un espace. Par exemple un point de sureté personnalisé avec comme valeur de chemin
1 1 -1 -1 , une echelle définie à 0.7 mm  fera deux points de 0.7 mm en avant puis deux points de 0.7mm en arrière.
Il est possible d'utiliser des valeurs non entières, (par exemple 0.5 2.2 -0.5 -2.2), si l'utilisateur le souhaite.

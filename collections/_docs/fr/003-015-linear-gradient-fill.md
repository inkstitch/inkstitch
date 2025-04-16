---
title: "Remplissage dégradé linéaire"
permalink: /fr/docs/stitches/linear-gradient-fill/
last_modified_at: 2025-04-12
toc: true
---
## Qu'est ce que c'est 

[![Linear Gradient Fill Sample](/assets/images/docs/linear-gradient.jpg){: width="200x"}](/assets/images/docs/linear-gradient.svg){: title="Download SVG File" .align-left download="linear-gradient.svg" }

Le remplissage en dégradé linéaire utilise la couleur du dégradé linéaire d'Inkscapes pour créer des dégradés homogènes avec un positionnement de point cohérent.

## Comment le créer

* Créez un **chemin fermé avec une couleur de remplissage**. La forme peut avoir des trous.
* Dans la boîte de dialogue « Remplissage et contour », sélectionnez un dégradé linéaire comme remplissage et ajustez les couleurs. Sur le canevas, ajustez l'angle du dégradé. L'angle du point aura un angle de 90 degrés par rapport à la direction du dégradé.
  ![dégradé linéaire](/assets/images/docs/en/linear-gradient.png)
* Ouvrez la boîte de dialogue des paramètres (`Extensions > Ink/Stitch > Paramètres`) et sélectionnez `Remplissage dégradé linéaire` comme méthode de remplissage
* Définissez les paramètres comme vous le souhaitez et appliquez

## Définir le point de début et de fin

Définissez les points de début et de fin du  remplissage avec les [Commandes visuelles](/fr/docs/commands/).

## Paramètres

Exécutez « Extensions > Ink/Stitch > Paramètres » pour ajuster les paramètres selon vos besoins.


|Paramètres||Description|
|---|---|---|
|Auto-remplissage avec des points de broderie| ☑ |Doit être activé pour que ces paramètres prennent effet.|
|Méthode de remplissage|Remplissage dégradé linéaire| Doit être sur Remplissage dégradé linéaire.|
|Élargir|![Expand example](/assets/images/docs/params-fill-expand.png) |Etend la forme avant le point de remplissage pour compenser les écarts entre les formes en raison de l'étirement du tissu.|
|Longueur maximale du point de remplissage|![Exemple de longueur de point](/assets/images/docs/params-fill-stitch_length.png) |La longueur de chaque point dans une rangée. "Max", c'est parce qu'un point plus court peut être utilisé au début ou à la fin d'une ligne.|
|Espacement entre les rangées|![Exemple d'espacement](/assets/images/docs/params-fill-spacing_between_rows.png) |Espacement entre les rangées de points.|
|Décaler les rangées autant de fois avant de répéter|![Décalage exemple](/assets/images/docs/params-fill-stagger.png) |Les points sont décalés de manière à ce que les rangées de points voisines ne tombent pas toutes dans la même colonne (ce qui créerait un effet de vallée). Ce paramètre détermine la longueur du cycle de décalage des rangées. Les fractions sont autorisées et peuvent produire des diagonales moins visibles que les valeurs entières.|
|Sauter le dernier point de chaque rangée|![Exemple sans dernier point](/assets/images/docs/params-fill-skip_stitches.png) |Le dernier point de chaque rangée est assez proche du premier point de la rangée suivante. Le sauter diminue le nombre de points et la densité.|
|Terminer à la position de fin | ☑ |Si cette option est déselectionnée, la position de fin ne sera utiisée que pour déterminer la direction générale de la broderie. Si sélectionné, la dernière section terminera au point désigné.|
|Longueur du point droit  ||Pour les chemins de dessous|
|Tolérance du point droit || Les points ne peuvent pas être éloignés du chemin de plus que cette distance. Une tolerance basse peut impliquer des points plus courts. Une tolerance haute entraine un arrondissement des angles aigus.|
|Rendre aléatoire la longueur du point ||Rendre la longueur du point aléatoire plutôt que de découper ou décaler régulièrement. Ceci est recommandé lorsque le remplissage est dense pour éviter les effets de moiré.
|Mouvement aléatoire de la longueur du point ||Pourcentage maximum de variation de la longueur du point appliqué si la longueur est rendue aléatoire.
|Graine aléatoire         ||UUtiliser cette graine aléatoire pour le calcul des attributs. Si vide, utilise l'identificateur de l'élément.
|Longueur minimum de point||Est prioritaire par rapport à la valeur de la longueur minimum de point définie dans les préférences. Les points plus courts seront supprimés.|
|Longueur minimum de saut ||Est prioritaire par rapport à la valeur de la longueur minimum de saut définie dans les préférences. Si la distance à l'objet suivant est inférieure, il n'y aura pas de points d'arrêt, sauf si les points d'arrêts sont forcés.|
|Autoriser les points d'arrêts | ☑|Ajoute un point d'arrêt à la ou les positions choisies.|
|Forcer les points d'arrêts |☑|Force un point d'arrêt après l'objet indépendament de la valeur de "Saut de fil" dans les Préférences d'Ink/Stitch.|
|Point d'arrêt initial    ||Sélectionnez le type du  [point d'arrêt initial](/fr/docs/stitches/lock-stitches).|
|Point d'arrêt final      ||Sélectionnez le type du [point d'arrêt terminal](/fr/docs/stitches/lock-stitches).|
|Arrêter après            |☑ |Faire faire une pause à la machine après avoir brodé cet objet. Si une position d'arrêt a été définie, elle est rejointe par un saut avant la pause. |
|Couper après             |☑ |Couper le fil après avoir brodé cet objet.|

{: .params-table}



## Sous-Couche

La sous-couche du Remplissage dégradé linéaire est la même que celle du remplissage automatique et utilise l'angle défini les 
 [paramètres de la sous-couche](/fr/docs/stitches/fill-stitch#underlay).

## Samples Files Including Linear Gradient Fill Stitches

{% include tutorials/tutorial_list key="stitch-type" value="Linear Gradient Fill" %}

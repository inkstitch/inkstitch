---
title: "Remplissage guidé"
permalink: /fr/docs/stitches/guided-fill/
excerpt: ""
last_modified_at: 2023-04-20
toc: true
---
## De quoi s'agit-il ?



![Fill stitch detail](/assets/images/docs/guided-fill-detail.jpg)
Tout comme le remplissage usuel, le remplissage guidé est composé de rangées décalées plus ou moins parallèles, mais au lieu de suivre des lignes droites,  les rangées peuvent être courbées par une ligne-guide. La ligne guide peut déborder de la forme, mais seule la partie qui intersecte la forme a de l'importance.

## Comment le créer

* Créez une **forme fermée avec une couleur de remplissage**. Cette forme  peut comporter des trous.
* Créez une ligne-guide pour définir la forme des rangées de points :
    * Dessinez un trait (chemin avec une couleur de contour et sans couleur de remplissage)
    * Selectionnez ce trait
    * Lancez `Extensions > Ink/Stitch > Edition > Selection vers ligne-guide`
* Sélectionnez les deux et groupez les ensemble (`Ctrl + G`).
* Ouvrez le dialogue de paramètrage (`Extensions > Ink/Stitch > Paramètres`) et sélectionnez `Remplissage guidé` comme méthode de remplissage



Il est possible d'avoir dans un même groupe plusieurs formes de remplissage et une seule ligne guide. Chaque forme de remplissage est guidée par la portion de la ligne guide qui l'intersecte. Si la ligne-guide n'intersecte pas une des formes du groupe, cette forme est remplie en remplissage normal.

![Guided fill group](/assets/images/docs/guided-fill-group.svg)

Si un groupe comporte plusieurs lignes-guides, une seule d'entre elle est effective, les autres sont ignorées. De même si la ligne-guide est un chemin composite, un seul des sous chemin est effectif. 
Toutefois, il est possible d'utiliser une ligne guide qui traverse plusieurs fois la frontière de la forme pour simuler l'effet de plusieurs lignes-guides:

![Guided fill group](/assets/images/docs/guided-fill-complex.svg)

L'utilisation de ligne guide très sinueuse ne donne pas toujours le résultat auquel on s'attend, il convient de tester les deux stratégies de remplissage et des modifications de la ligne guide jusqu'a obtenir l'effet souhaité.

## Stratégies de remplissage
Deux stratégies sont possible pour le remplissage guidé.

### Copier
La stratégie "Copier", remplit la forme avec des copies non déformées de l'intersection de la ligne-guide et de la forme. Parfois, en particulier si la ligne guide a des angles aigus, le remplissage est très irrégulier.

### Décalage parallèle

La stratégie "Décalage parallèle", remplit la forme avec des copies déformées de l'intersection de la ligne guide et de la forme, en s'assurant que chaque copie reste à distance constante de sa voisine. Cette stratégie peut introduire des angles même si la ligne guide n'en  contient pas.

## Définir le point de départ et d'arrivée
Définir le point de départ et d'arrivée pour les remplissages avec les [commandes visuelles](/fr/docs/commands/).

## Paramètres

Lancez `Extensions > Ink/Stitch  > Paramètres`. Choisir "Remplissage guidé" dans la méthode de remplissage et ajustez les réglages selon vos besoins

|Paramètres||Description|
|---|---|---|
|Autoremplissage avec des points de broderie| ☑ |Doit être activé pour que ces paramètres prennent effet.|
|Méthode de remplissage |Remplissage guidé| Remplissage guidé doit être selectionné.|
|Stratégie pour le remplissage guidé|![Stratégies de remplissage](/assets/images/docs/guidedfillstrategies.svg)| Copier(valeur par défaut), en haut sur le dessin, remplit la forme avec des copies translatées de la ligne guide. Décalage parallèle, en bas sur le dessin, remplit avec des lignes qui sont calculées à partir de la ligne guide pour que chaque ligne soit a distance constante de la ligne précédente. Cette stratégie peut introduire des angles aigus.|
|Compensation d'étirement - élargir|![Expand example](/assets/images/docs/params-fill-expand.png) |dilate la forme avant le point de remplissage pour compenser les écarts entre les formes en raison de l'étirement du tissu.|
|Longueur maximale du point de remplissage|![Exemple de longueur de point](/assets/images/docs/params-fill-stitch_length.png) |La longueur de chaque point dans une rangée. "Max", c'est parce qu'un point plus court peut être utilisé au début ou à la fin d'une ligne.|
|Espacement entre les rangées|![Exemple d'espacement](/assets/images/docs/params-fill-spacing_between_rows.png) |Distance entre les rangées de points.|
|Longueur de point droit|![Exemple de Longueur de point droit](/assets/images/docs/params-fill-running_stitch_length.png) |Longueur des points utilisés pour passer d'une section à l'autre.|
|Tolérance du point droit|![Exemple de tolérance](/assets/images/docs/contourfilltolerance.svg) |Tous les points doivent rester au plus à cette distance du chemin. Une tolérance plus faible (en haut sur le dessin) signifie que les points seront plus rapprochés. Une tolérance plus élevée (en bas) signifie que les angles vifs peuvent être arrondis.|
|Sauter le dernier point de chaque rangée|![Exemple sans dernier point](/assets/images/docs/params-fill-skip_stitches.png) |Le dernier point de chaque rangée est assez proche du premier point de la rangée suivante. Le sauter diminue le nombre de points et la densité.|
|Décaler autant de fois avant de répéter|![Décalage exemple](/assets/images/docs/params-fill-stagger.png) |Les points sont décalés de manière à ce que les rangées de points voisines ne tombent pas toutes dans la même colonne (ce qui créerait un effet de vallée). Ce paramètre détermine combien de lignes les points seront décalées avant de tomber dans la même position en colonne.|
|Chemin de dessous|![exemple de chemin de dessous](/assets/images/docs/params-fill-underpathing.png)|Doit être activé pour permettre aux points droits de se placer à l'intérieur de la forme plutôt que de suivre la bordure lors du déplacement d'une section à l'autre.|
|Forcer les points d'arrêts |☑|Force un point d'arrêt après l'objet indépendament de la valeur de "Saut de fil" dans les Préférences d'Ink/Stitch.
|Autoriser les points d'arrêts | ☑|Ajoute un point d'arrêt à la ou les positions choisies.|
|Point d'ancrage                  |Choisir le  [style désiré](/fr/docs/stitches/lock-stitches/)|
|Point d'arrêt                    |Choisir le  [style désiré](/fr/docs/stitches/lock-stitches/)|
|Couper après          |☑ | Coupe le fil après avoir brodé cet objet.|
|Arrêter après           |☑ |Fait faire une pause à la machine après avoir brodé cet objet. Si une position d'arrêt a été définie, elle est rejointe par un saut avant la pause. |

## Sous couche

La sous-couche du remplissage guidé  n'utilise pas la ligne-guide, mais tout comme pour le remplissage standard, elle utilise l'angle de remplissage qui peut être défini dans les [paramètres de la sous-couche](/fr/docs/stitches/fill-stitch/#sous-couche) .
##  Exemple de fichiers qui utilisent le remplissage guidé
{% include tutorials/tutorial_list key="stitch-type" value="Guided Fill" %}

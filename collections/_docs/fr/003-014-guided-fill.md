---
title: "Remplissage guidé"
permalink: /fr/docs/stitches/guided-fill/
last_modified_at: 2024-05-07
toc: true
---
## Description


Tout comme le remplissage usuel, le remplissage guidé est composé de rangées décalées plus ou moins parallèles, mais au lieu de suivre des lignes droites,  les rangées peuvent être courbées par une ligne-guide. La ligne guide peut déborder de la forme, mais seule la partie qui intersecte la forme a de l'importance.

{% include folder-galleries path="butterfly-fill-project/guided/" captions="1:Remplissage guidé avec fil multicolore;2: Superposition de zones en remplissage guidés pour un effet d'aquarelle;3:remplissage guidé avec la méthode Buffer" %}

## Création

* Créez une **forme fermée avec une couleur de remplissage**. Cette forme  peut comporter des trous.
* Créez une ligne-guide pour définir la forme des rangées de points :
    * Dessinez un trait (chemin avec une couleur de contour et sans couleur de remplissage)
    * Sélectionnez ce trait
    * Lancez `Extensions > Ink/Stitch > Édition > Sélection vers ligne-guide`
* Sélectionnez les deux et groupez les (`Ctrl + G`).
* Ouvrez le dialogue de paramétrage (`Extensions > Ink/Stitch > Paramètres`) et sélectionnez `Remplissage guidé` comme méthode de remplissage

Il est possible d'avoir dans un même groupe plusieurs formes de remplissage et une seule ligne guide. Chaque forme de remplissage est guidée par la portion de la ligne guide qui l'intersecte. Si la ligne-guide n'intersecte pas une des formes du groupe, cette forme est remplie en remplissage normal.

![Guided fill group](/assets/images/docs/guided-fill-group.svg)

Si un groupe comporte plusieurs lignes-guides, une seule d'entre elle est effective, les autres sont ignorées. De même si la ligne-guide est un chemin composite, un seul des sous chemin est effectif. 
Toutefois, il est possible d'utiliser une ligne guide qui traverse plusieurs fois la frontière de la forme pour simuler l'effet de plusieurs lignes-guides:

![Guided fill group](/assets/images/docs/guided-fill-complex.svg)

L'utilisation de ligne guide très sinueuse ne donne pas toujours le résultat auquel on s'attend, il convient de tester les deux stratégies de remplissage et des modifications de la ligne guide jusqu'a obtenir l'effet souhaité.

## Stratégies de remplissage

Trois  stratégies sont possible pour le remplissage guidé.

### Copier

La stratégie "Copier", remplit la forme avec des copies non déformées de l'intersection de la ligne-guide et de la forme. Parfois, en particulier si la ligne guide a des angles aigus, le remplissage est très irrégulier.

### Décalage parallèle

La stratégie "Décalage parallèle", remplit la forme avec des copies déformées de l'intersection de la ligne guide et de la forme, en s'assurant que chaque copie reste à distance constante de sa voisine. Cette stratégie peut introduire des angles même si la ligne guide n'en  contient pas.

### Buffer

{% include upcoming_release.html %}

La méthode Buffer utilise des décalages autour de la ligne guide et contrairement aux autres méthodes permet  à une ligne guide d'être composée de plusieurs sous-chemins.

## Définir le point de départ et d'arrivée

Définir le point de départ et d'arrivée pour les remplissages avec les [commandes visuelles](/fr/docs/commands/).

## Paramètres

Lancez `Extensions > Ink/Stitch  > Paramètres`. Choisir "Remplissage guidé" dans la méthode de remplissage et ajustez les réglages selon vos besoins

{% include params.html stitch_type='guided_fill'%}

## Sous couche

La sous-couche du remplissage guidé  n'utilise pas la ligne-guide, mais tout comme pour le remplissage standard, elle utilise l'angle de remplissage qui peut être défini dans les [paramètres de la sous-couche](/fr/docs/stitches/fill-stitch/#sous-couche) .
##  Exemple de fichiers qui utilisent le remplissage guidé
{% include tutorials/tutorial_list key="stitch-type" value="Guided Fill" %}

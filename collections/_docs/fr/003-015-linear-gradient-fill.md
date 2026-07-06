---
title: "Remplissage dégradé linéaire"
permalink: /fr/docs/stitches/linear-gradient-fill/
last_modified_at: 2025-04-12
toc: true
---
## Description

Le remplissage en dégradé linéaire utilise la couleur du dégradé linéaire d'Inkscape pour créer des dégradés homogènes avec un positionnement de point cohérent.

{% include folder-galleries path="butterfly-fill-project/linear_gradient/" captions="1: Dégradé Bleu PourpreB;2:Dégradé Rouge Jaune" %}

[<i class="fa fa-download"></i> Download sample files](/assets/images/stitch-type-butterflies/linear_gradient_fill.zip)

## Creation

* Créez un **chemin fermé avec une couleur de remplissage**. La forme peut avoir des trous.
* Dans la boîte de dialogue « Remplissage et contour », sélectionnez un dégradé linéaire comme remplissage et ajustez les couleurs. Sur le canevas, ajustez l'angle du dégradé. L'angle du point aura un angle de 90 degrés par rapport à la direction du dégradé.
  ![dégradé linéaire](/assets/images/docs/en/linear-gradient.png)
* Ouvrez la boîte de dialogue des paramètres (`Extensions > Ink/Stitch > Paramètres`) et sélectionnez `Remplissage dégradé linéaire` comme méthode de remplissage
* Définissez les paramètres comme vous le souhaitez et appliquez

## Définir le point de début et de fin

Définissez les points de début et de fin du  remplissage avec les [Commandes visuelles](/fr/docs/commands/).

## Paramètres

Exécutez « Extensions > Ink/Stitch > Paramètres » pour ajuster les paramètres selon vos besoins.

{% include params.html stitch_type='linear_gradient_fill'%}

## Sous-Couche

La sous-couche du Remplissage dégradé linéaire est la même que celle du remplissage automatique et utilise l'angle défini les 
 [paramètres de la sous-couche](/fr/docs/stitches/fill-stitch#underlay).

## Fichiers d'exemple incluant des remplissages en dégradé linéaire 

{% include tutorials/tutorial_list key="stitch-type" value="Linear Gradient Fill" %}

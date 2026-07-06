---
title: "Remplissage circulaire"
permalink: /fr/docs/stitches/circular-fill/
last_modified_at: 2025-04-17
toc: true
---
## Description

Le remplissage circulaire remplit une forme avec une spirale. Le centre de la spirale est positionné au centre de la forme. Il et possible de personnaliser la position du centre de la spirale à l'aide d'une cible.

{% include folder-galleries path="butterfly-fill-project/circular/" captions="1:Plusieurs couches de remplissage circulaire;2:Remplissages circulaires avec effet de dégradé circulaire" %}

[<i class="fa fa-download"></i> Download sample files](/assets/images/stitch-type-butterflies/circular_fill.zip)

## Création

* Créez **un chemin fermé avec une couleur de remplissage**. Cette forme peut avoir des trous.
* Ouvrir le dialogue de paramètrage (`Extensions > Ink/Stitch > Paramètres`) et sélectionner `Remplissage circulaire` comme méthode de remplissage.
* Choisissez vos paramètres et cliquez sur Appliquer.
 
## Définir le centre de la spirale

Par défaut, le centre de la spirale est le centre géométrique de la forme.

Notez que ce n'est pas le centre de la boite englobante.

Pour modifier le comportement par défaut, sélectionnez la forme et attachez lui la commande d'objet "Position de la cible".

Le centre du symbole de commande sera le nouveau centre de la spirale.

Lire [comment attacher des commandes aux objets](/fr/docs/commands/).

## Définir les positions de début et de fin de la broderie.

Utilisez les commandes "Position de début du remplissage" et "Position de fin du remplissage". Voir  [Commandes Visuelles](/fr/docs/commands/).

## Paramètres

Lancez `Extensions > Ink/Stitch  > Paramètres` pour choisir vos réglages.

### Couche supérieure

{% include params.html stitch_type='circular_fill'%}

## Sous-couche

La sous-couche de remplissage circulaire se comporte comme celle du remplissage automatique et utilise l'angle de remplissage qui peut être défini dans les 
[paramètres](/fr/docs/stitches/fill-stitch/#sous-couche) de la sous-couche.


## Exemples de fichier incluant des remplissage circulaire
{% include tutorials/tutorial_list key="stitch-type" value="Circular Fill" %}

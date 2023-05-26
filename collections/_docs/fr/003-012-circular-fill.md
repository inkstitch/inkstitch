---
title: "Remplissage circulaire"
permalink: /fr/docs/stitches/circular-fill/
excerpt: ""
last_modified_at: 2023-05-01
toc: true
---
## De quoi s'agit-il ?

Le remplissage circulaire remplit une forme avec une spirale. Le centre de la spirale est positionné au centre de la forme. Il et possible de personnaliser la position du centre de la spirale à l'aide d'une cible.

![Détail de point circulaire](/assets/images/docs/circular-fill-detail.png)

## Comment le créer

* Créez **un chemin fermé avec une couleur de remplissage**. Cette forme peut avoir des trous.
* Ouvrir le dialogue de paramètrage (`Extensions > Ink/Stitch > Paramètres`) et sélectionner `Remplissage circulaire` comme méthode de remplissage.
* Choisissez vos paramètres et cliquez sur Appliquer.
 
## Définir le centre de la spirale

* Selectionnez la forme et attachez lui la commande d'objet "Position de la cible". Lire
 [comment attacher des commandes aux objets](/fr/docs/commands/).

## Définir les positions de début et de fin de la broderie.

Utilisez les commandes "Position de début du remplissage" et "Position de fin du remplissage". Voir  [Commandes Visuelles](/fr/docs/commands/).

## Paramètres

Lancez `Extensions > Ink/Stitch  > Paramètres` pour choisir vos réglages.



|Paramètres||Description|
|---|---|---|
|Autoremplissage avec des points de broderie| ☑ |Doit être activé pour que ces paramètres prennent effet.|
|Méthode de remplissage |Remplissage circulaire| Remplissage circulaire  doit être selectionné.|
|Etirer|![Expand example](/assets/images/docs/params-fill-expand.png) |Etend la forme avant le point de remplissage pour compenser les écarts entre les formes dues à l'étirement du tissu.|
|Longueur maximale du point de remplissage|![Exemple de longueur de point](/assets/images/docs/params-fill-stitch_length.png) |Pour le remplissage circulaire il s'agit de longueur du point droit résultant.|
|Tolérance du point droit|![Exemple de tolerance](/assets/images/docs/contourfilltolerance.svg) |Tous les points doivent rester au plus à cette distance du chemin. Une tolérance plus faible (en haut sur le dessin) signifie que les points seront plus rapprochés. Une tolérance plus élevée (en bas) signifie que les angles vifs peuvent être arrondis.|
|Chemin de dessous           |![Example de chemin de dessous](/assets/images/docs/params-fill-underpathing.png)| Doit être autorisé pour permettre aux points de voyager dans la forme et non le long de la frontière pour passer de section en section.|
|Forcer les points d'arrêts |☑|Force un point d'arrêt après l'objet indépendament de la valeur de "Saut de fil" dans les Préférences d'Ink/Stitch.|
|Autoriser les points d'arrêts | ☑|Ajoute un point d'arrêt à la ou les positions choisies.|
|Point d'ancrage        ||Selectionnez le type du  [point d'ancrage](/fr/docs/stitches/lock-stitches).|
|Point d'arrêt        ||Selectionnez le type du [point d'arrêt](/fr/docs/stitches/lock-stitches).|
|Couper après                 |☑|Couper le fil après avoir brodé cet objet.|
|Arrêter après                |☑|Faire faire une pause à la machine après avoir brodé  cet objet. Si une position d'arrêt est définie, elle est rejointe  par un saut avant la pause de la machine.|

## Sous-couche

La sous-couche de remplissage circulaire se comporte comme celle du remplissage automatique et utilise l'angle de remplissage qui peut être défini dans les 
[paramètres](/fr/docs/stitches/fill-stitch/#sous-couche) de la sous-couche.


## Examples de fichier incluant des remplissage circulaire
{% include tutorials/tutorial_list key="stitch-type" value="Circular Fill" %}

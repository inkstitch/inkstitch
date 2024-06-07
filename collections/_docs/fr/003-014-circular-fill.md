---
title: "Remplissage circulaire"
permalink: /fr/docs/stitches/circular-fill/
last_modified_at: 2024-05-07
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

By default the center of the spiral is the geometrical center of the shape.
Note that this is not equal to the center of the bounding box.

To change default behavior selectionnez la forme et attachez lui la commande d'objet "Position de la cible".
The center of the command symbol will be the new spiral center.

Lire [comment attacher des commandes aux objets](/fr/docs/commands/).

## Définir les positions de début et de fin de la broderie.

Utilisez les commandes "Position de début du remplissage" et "Position de fin du remplissage". Voir  [Commandes Visuelles](/fr/docs/commands/).

## Paramètres

Lancez `Extensions > Ink/Stitch  > Paramètres` pour choisir vos réglages.

|Paramètres||Description|
|---|---|---|
|Autoremplissage avec des points de broderie| ☑ |Doit être activé pour que ces paramètres prennent effet.|
|Méthode de remplissage |Remplissage circulaire| Remplissage circulaire  doit être selectionné.|
|Compensation d'étirement - Élargir|![Expand example](/assets/images/docs/params-fill-expand.png) |Etend la forme avant le point de remplissage pour compenser les écarts entre les formes dues à l'étirement du tissu.|
|Espacement entre les rangées|![Exemple d'espacement](/assets/images/docs/params-fill-spacing_between_rows.png) |Espacement entre les rangées de points.|
|Espacement final entre les rangées|![Exemple d'espacement](/assets/images/docs/params-fill-end_row_spacing.png) |Si une valeur est saisie, l'espacement entre les rangées augmente ou diminue au fur et à mesure jusqu'à atteindre la valeur finale.|
|Chemin de dessous           |![Example de chemin de dessous](/assets/images/docs/params-fill-underpathing.png)| Doit être autorisé pour permettre aux points de voyager dans la forme et non le long de la frontière pour passer de section en section.|
|Longueur du point droit|![Exemple de longueur de point](/assets/images/docs/params-fill-stitch_length.png) |Pour le remplissage circulaire il s'agit de longueur du point droit résultant.|
|Tolérance du point droit|![Exemple de tolerance](/assets/images/docs/contourfilltolerance.svg) |Tous les points doivent rester au plus à cette distance du chemin. Une tolérance plus faible (en haut sur le dessin) signifie que les points seront plus rapprochés. Une tolérance plus élevée (en bas) signifie que les angles vifs peuvent être arrondis. Stitches below the value for minimum stitch length (global or object based setting, see below) will be removed.
|Longueur minimum du point||Est prioritaire par rapport à la valeur de la longueur minimum de point définie dans les [préférences](/fr/docs/preferences/#longueur-minimum-de-points-mm). Les points plus courts seront supprimés.|
|Longueur minimum de saut||Est prioritaire par rapport à la valeur de la longueur minimum de saut définie dans les [préférences](/fr/docs/preferences/#sauts-de-fil-mm). Si la distance à l'objet suivant est inférieure, il n'y aura pas de points d'arrêt, sauf si les points d'arrêts sont forcés.|
|Rendre aléatoire                      |☑ |Rendre la longueur du point aléatoire plutôt que de découper ou décaler régulièrement. Ceci est recommandé lorsque le remplissage est dense pour éviter les effets de moiré.|
|Mouvement aléatoire de la longueur du point                    ||Pourcentage maximum de variation de la longueur du point appliqué si la longueur est rendue aléatoire.|
|Graine Aléatoire                   ||Rouler le dé ou entrer une valeur modifie les points aléatoires|
|Autoriser les points d'arrêts | ☑|Ajoute un point d'arrêt à la ou les positions choisies.|
|Forcer les points d'arrêts |☑|Force un point d'arrêt après l'objet indépendament de la valeur de "Saut de fil" dans les Préférences d'Ink/Stitch.|
|Point d'arrêt initial       ||Sélectionnez le type du  [point d'ancrage](/fr/docs/stitches/lock-stitches).|
|Point d'arrêt final       ||Sélectionnez le type du [point d'arrêt](/fr/docs/stitches/lock-stitches).|
|Arrêter après                       |☑ |Faire faire une pause à la machine après avoir brodé cet objet. Si une position d'arrêt a été définie, elle est rejointe par un saut avant la pause. |
|Couper après                        |☑ |Couper le fil après avoir brodé cet objet.

{: .params-table}

## Sous-couche

La sous-couche de remplissage circulaire se comporte comme celle du remplissage automatique et utilise l'angle de remplissage qui peut être défini dans les 
[paramètres](/fr/docs/stitches/fill-stitch/#sous-couche) de la sous-couche.


## Examples de fichier incluant des remplissage circulaire
{% include tutorials/tutorial_list key="stitch-type" value="Circular Fill" %}

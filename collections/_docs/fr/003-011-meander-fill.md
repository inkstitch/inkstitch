---
title: "Remplissage en méandres"
permalink: /fr/docs/stitches/meander-fill/
excerpt: ""
last_modified_at: 2023-05-01
toc: true
---
{% include upcoming_release.html %}

## De quoi s'agit-il?

Le remplissage en méandres est originaire des techniques de quilting. Il produit un beau résultat en broderie machine. De grandes zones peuvent être remplies avec relativement peu de points.


![Meander stitch detail](/assets/images/docs/meander-fill.png)

## Comment le créer

* Créez un **chemin fermé avec une couleur de remplssager**.  Cette forme peut contenir des trous.
* Ouvrez le dialogue des paramètres (`Extensions > Ink/Stitch > Paramètres`)  et sélectionnez "Remplissage en méandres" comme méthode de remplissage.

  Vous pouvez maintenant choisir parmi un grand nombre de motif de méandres. Vous pouvez jouer sur les valeurs de  taille, régularité, longueur de point et tolérance pour modifier l'aspect.
  
## Définir le point de départ et d'arrivée

Définir le point de départ et d’arrivée pour les remplissages automatiques avec les commandes [commandes visuelles](/docs/commands/).

## Paramètres

Lancez `Extensions > Ink/Stitch > Paramètres`. Choisir “Remplissage en méandres” dans la méthode de remplissage et ajustez les réglages selon vos besoins

|Paramètres||Description|
|---|---|---|
|Autoremplissage avec des points de broderie| ☑ |Doit être activé pour que ces paramètres prennent effet.|
|Méthode de remplissage                     |Remplissage en méandres| Remplissage en méandres  doit être selectionné.|
|Motif de méandre                           || Divers motifs au choix|
|Echelle du motif                           ||Mise à l'echelle du motif ( en %)|
|Etirer                                     |![Expand example](/assets/images/docs/params-fill-expand.png) |Etend la forme avant le point de remplissage pour compenser les écarts entre les formes dues à l'étirement du tissu.|
|Lissage                                    ||Lisse la broderie. Le lissage détermine la mesure dans laquelle le chemin lissé peut s'éloigner du chemin originel. Essayez de petites valeurs comme 0.2. Attention, il est possible qu'il faille aussi modifier la tolérance du point droit.|
|Clip path                                  ||Constrain stitching to the shape.  Useful when smoothing and expand are used.
|Longueur maximale du point de remplissage  |![Exemple de longueur de point](/assets/images/docs/params-fill-stitch_length.png) |Pour le remplissage en méandres il s'agit de longueur du point droit résultant.|
|Tolérance du point droit                   |![Exemple de tolerance](/assets/images/docs/contourfilltolerance.svg) |Tous les points doivent rester au plus à cette distance du chemin. Une tolérance plus faible (en haut sur le dessin) signifie que les points seront plus rapprochés. Une tolérance plus élevée (en bas) signifie que les angles vifs peuvent être arrondis.|
|Répétitions           ||Combien de fois aller et revenir le long du chemin<br />◦ par défaut: 1 (aller une fois du début à la fin du chemin)<br />◦ Nombre impair: les points se termineront à la fin du chemin<br />◦ Nombre pair: la broderie va revenir au début du chemin|
|Nombre de répétitions pour le point triple (bean stitch)              |Active le [Mode point triple](/fr/docs/stitches/bean-stitch/)<br />|Une valeur de 1 triplera chaque point (avant, arrière, avant).<br />◦ Une valeur de 2 permettra de quintupler chaque point, etc..<br />◦ Il est possible de définir un motif de répétitions en entrant plusieurs valeurs séparées par un espace|
|Forcer les points d'arrêts                 |☑|Force un point d'arrêt après l'objet indépendament de la valeur de "Saut de fil" dans les Préférences d'Ink/Stitch.|
|Autoriser les points d'arrêts              | ☑|Ajoute un point d'arrêt à la ou les positions choisies.|
|Point d'ancrage                            ||Selectionnez le type du  [point d'ancrage](/fr/docs/stitches/lock-stitches).|
|Point d'arrêt                              ||Selectionnez le type du [point d'arrêt](/fr/docs/stitches/lock-stitches).|
|Couper après                               |☑|Couper le fil après avoir brodé cet objet.|
|Arrêter après                              |☑|Faire faire une pause à la machine après avoir brodé  cet objet. Si une position d'arrêt est définie, elle est rejointe  par un saut avant la pause de la machine.|

## Sous-couche

La sous-couche de remplissage en méandres se comporte comme celle du remplissage automatique et utilise l'angle de remplissage qui peut être défini dans les 
[paramètres](/fr/docs/stitches/fill-stitch/#sous-couche) de la sous-couche.



## Examples de fichiers incluant le remplissage en méandres
{% include tutorials/tutorial_list key="stitch-type" value="Meander Fill" %}

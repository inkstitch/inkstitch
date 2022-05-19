---
title: "Remplissage guidé par un chemin"
permalink: /fr/docs/stitches/guided-fill/
excerpt: ""
last_modified_at: 2022-05-20
toc: true
---
{% include upcoming_release.html %}

## De quoi s'agit-il ?



![Fill stitch detail](/assets/images/docs/guided-fill-detail.jpg)

Le remplissage guidé par un chemin remplit les objets parallèlement au chemin de guidage.

## Comment le créer

* Créez une **forme fermée avec une couleur de remplissage**

* Créez un chemin de guidage pour définir la direction des points :
    * dessiner un chemin avec une couleur de contour et sans couleur de remplissage
    * selectionner ce chemin
    * Lancez `Extensions > Ink/Stitch > Edition > Selection vers chemin de guidage`
* Sélectionnez les deux et groupez les ensemble (`Ctrl + G`).
  Chaque groupe peut contenir plusieurs objets de remplissage, mais un seul chemin de guidage.
  Les chemins de guidages surnuméraires seront ignorés.
* Ouvrir le dialogue de paramètrage (`Extensions > Ink/Stitch > Paramètres`) et sélectionner `Remplissage guidé par un chemin` comme méthode de remplissage.

## Définir le point de départ et d'arrivée
Définir le point de départ et d'arrivée pour les remplissages automatiques avec les [commandes visuelles](/fr/docs/commands/).

## Paramètres

Lancez `Extensions > Ink/Stitch  > Paramètres`. Choisir "Remplissage selon le contour" dans la méthode de remplissage et ajustez les réglages selon vos besoins

Lisez les informations détaillées dans la section  [Guided Fill Params](/docs/params/#guided-fill-params).

## Underlay

La sous-couche de remplissage guidé par un chemin n'est pas guidé par le chemin, mais utilise l'angle de remplissage qui peut être défini dans les 
[paramètres](/docs/params/#fill-underlay) de la sous-couche.
##  Exemple de fichiers qui utilisent le remplissage guidé par un chemin
{% include tutorials/tutorial_list key="stitch-type" value="Guided Fill" %}

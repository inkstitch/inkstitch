---
title: "Remplissage selon le contour"
permalink: /fr/docs/stitches/contour-fill/
last_modified_at: 2025-04-12
toc: true
---
## Description

Le remplissage selon le contour remplit les objets en suivant leur contour.

{% include folder-galleries path="butterfly-fill-project/contour/" captions="1:Remplissage selon contour appliqué à toute la forme;2:Remplissage selon contour appliqué par sections" %}


## Création

Créez une **forme fermée avec une couleur de remplissage**



## Définir le point de départ et d'arrivée
Seul le point de départ peut être défini avec les [commandes visuelles](/fr/docs/commands/). La commande point d'arrivée est sans effet sur les remplissages selon contour.

## Paramètres

Lancez `Extensions > Ink/Stitch  > Paramètres`. Choisir "Remplissage selon le contour" dans la méthode de remplissage et ajustez les réglages selon vos besoins

{% include params.html stitch_type='contour_fill'%}

## Sous-couche

La sous-couche de remplissage selon le contour ne suit pas le contour, mais utilise l'angle de remplissage qui peut être défini dans les 
[paramètres](/fr/docs/stitches/fill-stitch/#sous-couche) de la sous-couche.

## Exemples de fichier qui utilisent le remplissage suivant le contour
{% include tutorials/tutorial_list key="stitch-type" value="Contour Fill" %}

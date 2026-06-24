---
title: "Point manuel"
permalink: /fr/docs/stitches/manual-stitch/
last_modified_at: 2026-01-06
toc: true
---
## Description

En mode point manuel Ink / Stitch utilise chaque nœud d’un chemin comme point de pénétration de l’aiguille, exactement comme vous les avez placés, ni plus, ni moins.
{% include folder-galleries path="butterfly-fill-project/manual/" captions="1:Chemin manuel - chaque noeud représente un point." %}

Si vous ouvrez un fichier de broderie machine, vous y trouverez des points manuels.  Lorsque vous concevrez un fichier de broderie en svg, vous utiliserez très rarement les points manuels.

## Création

1. Créer un chemin. Le style de trait ou la largeur ne sont pas pertinents.
2. Ouvrer `Extensions > Ink/Stitch  > Paramètres`.
3. Choisir le type `Point manuel` comme méthode.

Les nœuds du chemin sont les points de pénétration de l'aiguille. 

![Manual Stitch Placement](/assets/images/docs/manual-stitch-placement.png)

Même si le chemin a des courbes (par exemple s'il s'agit d'un cercle ou d'une courbe de Bézier) la broderie ira directement (en ligne droite) d'un point à un autre.

Si nécessaire, une représentation de votre chemin de point manuel conforme à la broderie peut être obtenue comme suit:

1. Sélectionner tous les noeuds (`F2` puis `Ctrl`+`A`)
2. Cliquer sur ![Rendre durs les noeuds sélectionnés](/assets/images/docs/tool-controls-corner.jpg){: title="Make selected nodes corner" } dans la barre de contrôle des outils.

## Paramétres

Ouvrir `Extensions > Ink/Stitch  > Paramétres` pour paramétrer selon vos besoins.

{% include params.html stitch_type='manual-stitch'%}

## Fichier exemple avec point manuel

{% include tutorials/tutorial_list key="stitch-type" value="Manual Stitch" %}


---
title: "Broderie Ondulée"
permalink: /fr/docs/stitches/ripple-stitch/
last_modified_at: 2025-12-29
toc: true
---
## Description

La broderie ondulée tient à la fois du point droit et du remplissage : elle se comporte comme un point droit (on peut l'exécuter en point triple par exemple), elle est définie à partir d'un trait, mais elle produit à l'arrivée une broderie qui s'étend sur une surface. Utilisée de manière lâche, le résultat ressemble à des ondes, d'où son nom. 

{% include folder-galleries path="butterfly-fill-project/ripple/" captions="1:Ondulation à partir d'une forme fermée ;2:Ondulation guidée par un satin" %}

Regardez cette video de présentation:

{% include video id="cyvby3KJM10" provider="youtube" %}

Si le chemin initial est fermé, la forme sera remplie par une spirale (ondulations circulaires). S'il est ouvert, la broderie se fera en va et vient (ondulations linéaires)

## Création

### Ondulations circulaires 

* Créer **un chemin fermé simple avec une couleur de contour et sans couleur de remplissage** (pas une combinaison de sous-chemins)
* Créer [une cible ou des guides](#guider-les-ondulations) (optionnel)
* Sélectionner ce chemin
* Ouvrir le dialogue de paramétrage (`Extensions > Ink/Stitch > Paramètres`) et sélectionner `Broderie ondulée` comme méthode.
* Définir les [paramètres](#comment-la-paramètrer) à votre convenance et Appliquer

![Exemples d'ondulations circulaires](/assets/images/docs/circular-ripple.svg)

[Télécharger les exemples](/assets/images/docs/circular-ripple.svg){: download="circular-ripples.svg" }

### Ondulations linéaires

* Créer **une forme ouverte** (un chemin simple, deux chemins combinés ou même une colonne satin) **avec une couleur de contour et sans couleur de remplissage** 
* Créer [une cible ou des guides](#guider-les-ondulations) (optionnel)
* Sélectionner ce chemin
* Ouvrir le dialogue de paramétrage (`Extensions > Ink/Stitch > Paramètres`) et sélectionner `Broderie ondulée` comme méthode.
* Définir les [paramètres](#comment-la-paramètrer) à votre convenance et Appliquer

![Exemples d'ondulations linéaires](/assets/images/docs/linear-ripple.svg)

[Télécharger les exemples](/assets/images/docs/en/linear-ripple.svg){: download="linear-ripple.svg" }

## Ondulations avec boucles

Les boucles sont autorisées et bienvenues pour toutes les ondulations.
Utilisez les pour toutes sortes d'effets spéciaux....

![Ondulations avec boucles](/assets/images/docs/ripple-loops.svg)

[Télécharger les exemples](/assets/images/docs/ripple-loops.svg){: download="ripple-loops.svg" }

## Guider les ondulations

Les ondulations construites à partir d'un chemin simple (une forme fermée ou une courbe de bézier simple) peuvent être guidées en utilisant l'une quelconque de ces trois méthodes.

### Guidage par cible

Il est possible de définir le point cible de l'ondulation grâce aux [commandes visuelles](/fr/docs/commands/).

* Ouvrir `Extensions > Ink/Stitch > Commandes > Attacher des commandes à des objets sélectionnés ...`
* Sélectionner `Position de la cible` et appliquer.
* Sélectionner le symbole et déplacer le marqueur à la position souhaitée (peut importe la position du connecteur)

En l'absence de toute information de guidage, c'est le centre de l'ondulation initiale qui tient lieu de point cible.

### Guidage selon un chemin

* Directement dans le même groupe que la broderie ondulée (pas dans un sous-groupe), utilisez l'outil courbe de Béziers pour créer un chemin qui commence proche de l'ondulation puis s'en éloigne. 
* Sélectionner cette courbe et exécuter `Extensions > Ink/Stitch > Édition > Sélection vers guide`.
* Sélectionner la broderie ondulée.
* Ouvrir le dialogue de paramétrage (`Extensions > Ink/Stitch > Paramètres`) et sélectionner `Broderie ondulée` comme méthode.
* Définir les [paramètres](#params) à votre convenance et Appliquer.

La position des centres des ondulations est alors déterminée par le guide.

### Guidage Satin 

Avec le guidage satin, vous pouvez guider précisément les ondulations en utilisant une colonne satin pour guider au lieu d'un simple chemin. La largeur de la colonne satin a un effet sur la largeur des ondulations. 

* Directement dans le même groupe que la broderie ondulée (pas dans un sous-groupe), créez un objet similaire à une [colonne satin](/fr/docs/stitches/satin-column/) avec rails et traverses.
* Sélectionner ce nouvel objet et exécutez `Extensions > Ink/Stitch > Édition > Sélection vers guide`.
* Sélectionner la broderie ondulée.
* Ouvrir le dialogue de paramétrage (`Extensions > Ink/Stitch > Paramètres`) et sélectionner `Broderie ondulée` comme méthode.
* Définir les [paramètres](#params) à votre convenance et Appliquer.


Avec un guidage satin, il est aussi possible d'ajuster la direction des ondulations à l'aide d'une ligne de guidage.

* Dessiner un trait de haut en bas sur le motif à répliquer. Ce trait sera aligné sur les traverses
* Sélectionner la ligne et la marquer comme une ligne de guidage via `Extensions > Ink/Stitch > Édition > Sélection en ligne de guidage`.

![ondulation en guidage satin](/assets/images/docs/ripple_satin_guide.svg)

[Télécharger](/assets/images/docs/ripple_satin_guide.svg){: download="satin_guided_ripples.svg" }

## Découpes

{% include upcoming_release.html %}
La broderie ondulée peut être limitée à une zone donnée en utilisant une découpe.

* Créez la broderie ondulée.
* Créez la forme de découpage (elle doit se trouver au-dessus de la broderie ondulée).
* Sélectionnez les deux et exécutez `Objet > Découper > Définir une découpe`.

## Paramétrage

Ouvrir `Extensions > Ink/Stitch  > Paramétres` pour paramétrer selon vos besoins.

{% include upcoming_release_params.html %}

{% include params.html stitch_type='ripple-stitch'%}

## Exemples de fichiers qui utilisent la broderie ondulée 

{% include tutorials/tutorial_list key="stitch-type" value="Ripple Stitch" %}

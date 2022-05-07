---
title: "Outil lettrage"
permalink: /fr/docs/lettering/
excerpt: ""
last_modified_at: 2022-01-15
toc: true
---
L'outil de lettrage génère un texte multiligne sous la forme de colonnes satin et génère de manière dynamique les points, divisant éventuellement les points satins et ajoutant du point droit.

![Lettrage Extensions](/assets/images/docs/lettering.jpg)

## Usage

* Faire `Extensions > Ink/Stitch  > Lettrage
* Entrez votre texte (multi-ligne possible)
* Définir la police et l'échelle
* Cliquer sur `Appliquer et Quitter`

## Options

* **Broder les lignes de texte en aller retour**<br>
 Lorsque cette option est activée, la première ligne sera brodée de gauche à droite et la seconde de droite à gauche, etc.
   Cela donnera à votre machine des déplacements plus courts.

* **Ajouter des coupes**<br>
  Si cette option est activée, Ink/Stitch ajoutera des commandes de coupe pour chaque lettre.

## Préconfigurations

Vous pouvez enregistrer et rouvrir vos paramètres de police préférés.

## Bibliothèque de polices

Un aperçu de toutes les polices disponibles se trouve dans la [bibliothèque de polices](/fr/fonts/font-library/).

## Tri des couleurs
Si vous utilisez plusieurs lettres d'une police multicolore, vous pouvez trier les couleurs afin d'éviter de multiples changements de fil. Ce tri ne doit toutefois pas modifier l'ordre des couleurs de broderie d'une lettre. 

Lorsqu'à l'interieur d'une seule lettre les couleurs ne sont utilisées que sur des chemins consecutifs (ce qui est le cas des polices multicolores actuellement présente dans Ink/Stitch) voici une manière rapide de procéder si votre fichier ne contient que le lettrage :

Dans la fenêtre objet , choisir une lettre  peut importe laquelle:
* Selectionner le chemin qui sera brodé en premier (le dernier de la lettre dans cette fenêtre donc...)
* Edition/Selectionner Même/Couleur de contour (ceci va selectionner tout ce qui est de cette couleur dans toutes les lettres, il y a probablement beaucoup de chemins par lettre)
* Grouper, ce groupe va se trouver dans ce qui etait la dernière lettre, eventuellement donner à ce groupe le nom de la couleur
* Faites monter ce groupe le plus haut possible 

et recommencer jusqu'a qu'il n'y ait plus que des groupes de couleurs.

## Créer de nouvelle polices pour Ink/Stitch
Lire le [tutoriel de création de police](/fr/tutorials/font-creation/).

Contactez nous  sur  [GitHub](https://github.com/inkstitch/inkstitch/issues) si vous souhaitez publier votre police dans l'outil de lettrage d'Ink/Stitch.

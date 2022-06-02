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
Si vous utilisez plusieurs lettres d'une police multicolore, vous pouvez trier les couleurs afin d'éviter de multiples changements de fil. Ce tri ne doit toutefois pas modifier l'ordre des couleurs d'une lettre pour ne pas modifier la broderie. 

Lorsqu'à l'interieur d'une seule lettre les couleurs ne sont utilisées que sur des chemins consécutifs et toujours dans le même ordre (ce qui est le cas des polices multicolores actuellement présentes dans Ink/Stitch, sauf peut-être *Infinipicto*) voici une manière rapide de trier si votre fichier ne contient que le lettrage :

Dans la fenêtre objet, choisir une lettre (peu importe laquelle) :
* Sélectionner le chemin qui sera brodé en premier (le dernier de la lettre dans cette fenêtre donc...)
* Edition/Sélectionner même/Couleur de contour (ceci va sélectionner tout ce qui est de cette couleur dans toutes les lettres, il y a probablement beaucoup de chemins par lettre)
* Grouper : ce groupe va se trouver dans ce qui etait la dernière lettre à broder, éventuellement donner à ce groupe le nom de la couleur
* Faites monter ce groupe le plus haut possible dans cette dernière lettre
et recommencer jusqu'a qu'il n'y ait plus que des groupes de couleurs, en partant à chaque fois du dernier chemin d'une lettre

## Créer de nouvelle polices pour Ink/Stitch
Lire le [tutoriel de création de police](/fr/tutorials/font-creation/).

Contactez nous  sur  [GitHub](https://github.com/inkstitch/inkstitch/issues) si vous souhaitez publier votre police dans l'outil de lettrage d'Ink/Stitch.

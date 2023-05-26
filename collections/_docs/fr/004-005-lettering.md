---
title: "Outil lettrage"
permalink: /fr/docs/lettering/
excerpt: ""
last_modified_at: 2023-01-04
toc: true
---
L'outil de lettrage génère un texte multilignes sous la forme de colonnes satin et génère de manière dynamique les points, divisant éventuellement les points satins et ajoutant du point droit.

![Lettrage Extensions](/assets/images/docs/lettering.jpg)

## Usage

* Faire `Extensions > Ink/Stitch  > Lettrage`
* Entrez votre texte (multi-ligne possible)
* Définir la police et l'échelle
* Cliquer sur `Appliquer et Quitter`

## Options

* **Filtrage par taille**
  Les fontes sont conçues pour être  brodées dans  un intervalle de tailles donné. Le filtrage par taille vous aide en réduisant la liste des fontes à uniquement les fontes qui peuvent être brodées dans les dimensions choisies.
  Un filtre actif (pas à 0) déterminera  automatiquement la bonne échelle pour que la fonte sélectionnée soit dans la dimension souhaitée.

* **Broder les lignes de texte en aller retour**
 Lorsque cette option est activée, la première ligne sera brodée de gauche à droite et la seconde de droite à gauche, etc.
   Cela donnera à votre machine des déplacements plus courts.

* **Ajouter des commandes de coupes**
  Si cette option est activée, Ink/Stitch ajoutera des commandes de coupe  au choix pour chaque lettre, ou après chaque mot ou après chaque ligne.

## Préconfigurations

Vous pouvez enregistrer et rouvrir vos paramètres de police préférés.

## Lettrage le long d'un chemin

Les lettres d'ink/stitch ont été soigneusement dessinées pour une broderie optimale. Si vous essayez de les modifier avec les outils usuels d'inkscape, il se peut que cela ne fonctionne pas comme vous le souhaitez. Placez les lettres le long  d'un chemin est un gros travail. Cet outil va vous aider à le faire.

### Usage

* Sélectionnez un chemin et un groupe de lettrage 
* Exécutez `Extensions > Ink/Stitch > Lettrage le long d'un chemin ...`
* Si `Etendre` est coché Ink/Stitch va étendre les espaces entre les lettres pour que le texte utilise tout le chemin. Sinon il gardera les distances du texte original. 
* Cliquez sur 'Appliquer'



## Bibliothèque de polices

Un aperçu de toutes les polices disponibles se trouve dans la [bibliothèque de polices](/fr/fonts/font-library/).

## Tri des couleurs
Si vous utilisez plusieurs lettres d'une police multicolore, vous pouvez trier les couleurs afin d'éviter de multiples changements de fil. Ce tri ne doit toutefois pas modifier l'ordre des couleurs d'une lettre pour ne pas modifier la broderie. 

Lorsqu'à l'intérieur de chaque lettre les couleurs ne sont utilisées que sur des chemins consécutifs et toujours dans le même ordre (ce qui est le cas des polices multicolores actuellement présentes dans Ink/Stitch, sauf *Abril en Fleur* et peut-être *Infinipicto*), et que toutes les lettres utilisent toutes les couleurs  voici une manière rapide de trier si votre fichier ne contient que le lettrage :

Dans la fenêtre objet, choisir une lettre (peu importe laquelle) :
* Sélectionner le chemin qui sera brodé en premier (le dernier de la lettre dans cette fenêtre donc...)
* Edition/Sélectionner même/Couleur de contour (ceci va sélectionner tout ce qui est de cette couleur dans toutes les lettres, il y a probablement beaucoup de chemins par lettre)
* Grouper : ce groupe va se trouver dans ce qui était la dernière lettre à broder, éventuellement donner à ce groupe le nom de la couleur
* Faites monter ce groupe le plus haut possible dans cette dernière lettre
et recommencer jusqu'a qu'il n'y ait plus que des groupes de couleurs, en partant à chaque fois du dernier chemin d'une lettre

## Créer de nouvelle polices pour Ink/Stitch
Lire le [tutoriel de création de police](/fr/tutorials/font-creation/).

Contactez nous  sur  [GitHub](https://github.com/inkstitch/inkstitch/issues) si vous souhaitez publier votre police dans l'outil de lettrage d'Ink/Stitch.

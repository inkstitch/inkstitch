---
title: "Gestion des couleurs de fil"
permalink: /fr/docs/thread-color/
last_modified_at: 2025-04-17
toc: true
---

Inkscape prend en charge l'utilisation de palettes de couleurs. Les palettes de couleurs aident Ink/Stitch à définir les noms de couleurs et à enregistrer des informations supplémentaires telles que le nom du fabricant de fil et le numéro de catalogue de fil dans le fichier de broderie exporté.

En fonction des capacités de votre machine à broder, vous pourrez lire les noms des couleurs sur l'écran. Veuillez noter que certains formats de broderie (par exemple DST) ne stockent pas d'informations sur les couleurs. D'autres formats de fichiers utilisent un système de fichiers multiples pour stocker les informations de couleur. Pour les fichiers EXP, par exemple, il est courant d'enregistrer le format de couleur INF avec le fichier EXP pour transmettre les informations de couleur à votre machine.

Les définitions des couleurs sont affichées dans la [sortie pdf](/fr/docs/print-pdf/). Il est également possible d'[exporter les informations de la liste de fils](/fr/docs/threadlist/) dans un simple fichier texte.

Avant de pouvoir utiliser les fonctionnalités de couleur de fil, vous devez installer des palettes de couleurs. Vous pouvez soit [définir votre ou vos propres palettes personnalisées](/fr/docs/thread-color/#install-custom-palette) soit [installer celles livrées avec Ink/Stitch](/fr/docs/thread-color/#apply-threadlist). Quelle que soit la méthode que vous choisissez, redémarrez Inkscape après avoir installé les palettes de couleurs.

## Installer des palettes

### Installer des Palettes de couleurs de fils à broder pour Inkscape

Ink/Stitch est fourni avec de nombreuses palettes de fils de fabricants qui peuvent être installées dans Inkscape. Ceci permet de construire des broderies avec les bonnes couleurs à l'esprit.
Les couleurs apparaîtront dans la sortie pdf et seront aussi incluses dans votre fichier de broderie si son format le permet.

* `Extensions > Ink/Stitch > Installer des compléments pour Inkscape`
* Cochez l'option `Installer les palettes de couleur de fil`
* Cliquez sur  `Appliquer`
* Redémarrez Inkscape

### Installer une Palette personnalisée {#install-custom-palette}

Si vous disposez d'un fichier `.gpl` qui contient la liste des fils que vous utilisez, vous pouvez la rendre disponible dans Ink/Stitch via cette extension: `Extensions > Ink/Stitch > Gestion des couleurs de fil > Installer une palette personnalisée...`. Vous devrez ensuite redémarrer Inkscape.

Les fichiers `.gpl` de palettes peuvent être générés par GIMP.

## Générer et éditer des Palettes personnalisées  

### Générer une palette {#generate-color-palette}

Inkscape permet de générer des fichiers `.gpl`  de palette de couleurs. Mais il ne permet pas d'ordonner correctement les échantillons de couleur.

Cette extension exportera les couleurs d'éléments textuels tout en utilisant le texte pour les noms et numéros des couleurs.

1. Importez une image avec les couleurs de fils que vous voulez utiliser pour la palette de couleurs. 
2. Activez l'outil texte et copier/coller les noms de couleurs (si vous les avez) ou saisissez les.
   Utilisez une ligne par couleur.
   Si un nom de couleur se termine par un nombre, ce nombre sera utilisé pour cette couleur dans le catalogue.
3. Utilisez `Extensions > Ink/Stitch > Gestion des couleurs de fil > Générer  palette  > Séparer le texte` pour séparer un bloc de texte avec plusieurs lignes en plusieurs éléments textuels séparés. 
4. Activez l'outil pipette (D) et colorez les éléments textuels, en utilisant les tabulation pour passer de l'un à l'autre.
5. Sélectionnez les éléments textuels et  `Extensions > Ink/Stitch > Gestion des couleurs de fil > Générer palette  > Générer  palette de couleurs...`
6. Spécifiez le nom de votre palette de couleurs et cliquez sur Appliquer

{% include video id="4bcRVoKvzAw" provider="youtube" %}

### Palette vers texte

Ink/Stitch peut éditer des palettes existantes comme du texte.

- Importer les couleurs et les noms de couleurs avec `Extensions > Ink/Stitch > Gestion des couleurs de fil > Palette vers Texte`
- Changer les couleurs, mettre à jour les noms de couleurs ou les numéros de couleurs ou ajouter des couleurs
- Exporter votre palette avec  `Extensions > Ink/Stitch >  Gestion des couleurs de fil > Générer palette > Générer une palette de couleurs...`
- Redémarrer Inkscape

## Travailler avec des palettes

###  Usage Général

Une fois installées, les palettes Inkscape se trouvent dans la partie inférieure droite des nuanciers.

![Inkscape Color Palettes](/assets/images/docs/palettes-location.png)

Cliquez sur la petite flèche pour ouvrir une liste des palettes installées et choisissez la palette de couleurs du fabricant en fonction du fil que vous souhaitez utiliser.

Pour appliquer une couleur à un élément, sélectionner l'élément et cliquer sur l'échantillon de couleur en bas de la fenêtre. Utiliser un  simple clic pour une couleur de remplissage et un Majuscule clic pour une couleur de contour. Utiliser le X à gauche pour supprimer contour ou remplissage.

### Appliquer une palette {#apply-palette}

Cette extension applique aux éléments d'un document les couleurs les plus proches parmi celles de la palette choisie.

Ces changement seront pris en compte dans l'export pdf d'Ink/Stitcht.

Exécutez `Extensions > Ink/Stitch  > Gestion des couleurs de fil > Appliquer une palette` 

## Travailler avec des listes de fil

### Exportation

Les listes de fils ne peuvent être exportées qu'en enregistrant une copie du fichier au format "Ink/Stitch: ZIP exporter plusieurs formats (.zip)" , puis après avoir cliqué sur "Enregistrer" sélectionnez le format ".TXT: liste de fils".

### Appliquer une liste de fil {#apply-threadlist}

Ink/Stitch peut appliquer des listes de fil personnalisées à une broderie. Ceci est particulièrement utile si vous souhaitez utiliser un fichier de broderie qui ne comporte pas d'information de couleur (par exemple DST).

Ce peut être aussi utile si vous souhaitez essayer différents réglages de couleurs. Vous pouvez exporter et importer ces listes de fils à votre convenance, mais faites attention à ne changer ni le nombre ni l'ordre des couleurs. Si vous souhaitez les changer, faites le dans une copie du fichier svg.

* Lancez `Extensions > Ink/Stitch > Gestion des couleurs de fil > Appliquer la liste de fils`
* Choisir un fichier qui contient les information de couleur de fils qui correspondent aux éléments du document courant
* Choisir si ce fichier a été généré par Ink/Stitch ou pas.
 Si pas: sélectionner la palette de couleur Ink/Stitch avec laquelle établir la correspondance de couleurs.
* Cliquez sur Appliquer

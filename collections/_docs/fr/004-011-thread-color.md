---
title: "Gestion des couleurs de fil"
permalink: /fr/docs/thread-color/
last_modified_at: 2024-04-29
toc: true
---
Inkscape supports the usage of color palettes. Color palettes help Ink/Stitch to define color names and save additional information such as thread manufacturer name and the thread catalog number into the exported embroidery file.

Depending on the capabilities of your embroidery machine you will be able to read color names from the display. Please note, that some embroidery formats (for example DST) do not store color information. Other file formats use a mutliple file system to store color information. For EXP files for example it is common to save the color format INF along with the EXP file to transmit the color information to your machine.

Color definitions are shown in the [pdf output](/fr/docs/print-pdf/). It is also possible to [export threadlist information](/fr/docs/threadlist/) into a simple textfile.

Before you can use thread color features you need to install color palettes. You can either [define your own custom palette(s)](/docs/thread-color/#install-custom-palette) or [install the ones delivered with Ink/Stitch](/docs/thread-color/#install-thread-color-palettes-for-inkscape). Whichever method you choose, restart Inkscape after installing color palettes.

## Installer des palettes

### Installer des Palettes de couleurs de fils à broder pour Inkscape

Ink/Stitch est fourni avec de nombreuses palettes de fils de fabricants qui peuvent être installées dans Inkscape. Ceci permet de construire des broderies avec les bonnes couleurs à l'esprit.
Les couleurs apparaîtront dans la sortie pdf et seront aussi incluses dans votre fichier de broderie si son format le permet.

* Allez à `Extensions > Ink/Stitch  > Gestion des couleurs de fil > Installer des palettes de couleurs de fils à broder pour Inkscape`
* Cliquez sur `Installer`
* Redémarrez Inkscape

### Installer une Palette personnalisée {#install-custom-palette}

Si vous disposez d'un fichier `.gpl` qui contient la liste des fils que vous utilisez, vous pouvez la rendre disponible dans Ink/Stitch via cette extension: `Extensions > Ink/Stitch > Gestion des couleurs de fil > Installer une palette personnalisée...`. Vous devrez ensuite redémarrer Inkscape.

Les fichiers `.gpl` de palettes peuvent être générés par GIMP.

## Generate And Edit Custom Color Palettes

### Générer une palette {#generate-color-palette}

Inkscape permet de générer des fichiers `.gpl`  de palette de couleurs. Mais il ne permet pas d'ordonner correctement les échantillons de couleur.

Cette extension exportera les couleurs d'éléments textuels tout en utilisant le texte pour les noms et numéros des couleurs.

1. Importez une image avec les couleurs de fils que vous voulez utiliser pour la palette de couleurs. 
2. Activez l'outil texte et copier/coller les noms de couleurs (si vous les avez) ou saisissez les.
   Utilisez une ligne par couleur.
   Si un nom de couleur se termine par un nombre, ce nombre sera utilisé pour cette couleur dans le catalogue.
3. Utilisez `Extensions > Ink/Stitch > Gestion des couleurs de fil > Generer  palette  > Séparer le texte` pour séparer un bloc de texte avec plusieurs lignes en plusieurs éléments textuels séparés. 
4. Activez l'outil pipette (D) et colorez les éléments textuels, en utilisant les tabulation pour passer de l'un à l'autre.
5. Selectionnez les éléments textuels et  `Extensions > Ink/Stitch > Gestion des couleurs de fil > Generer palette  > Generer  palette de couleurs...`
6. Specifiez le nom de votre palette de couleurs et cliquez sur Appliquer

{% include video id="4bcRVoKvzAw" provider="youtube" %}

### Palette vers texte

Ink/Stitch peut éditer des palettes existantes comme du texte.

- Importer les couleurs et les noms de couleurs avec `Extensions > Ink/Stitch > Gestion des couleurs de fil > Palette vers Texte`
- Changer les couleurs, mettre à jour les noms de couleurs ou les numeros de couleus ou ajouter des couleurs
- Exporter votre pallette avec  `Extensions > Ink/Stitch >  Gestion des couleurs de fil > Generer palette > Generate palette de couleurs...`
- Redémarrer Inkscape

## Working With Palettes

### General Usage

Une fois installées, les palettes Inkscape se trouvent dans la partie inférieure droite des nuanciers.

![Inkscape Color Palettes](/assets/images/docs/palettes-location.png)

Cliquez sur la petite flèche pour ouvrir une liste des palettes installées et choisissez la palette de couleurs du fabricant en fonction du fil que vous souhaitez utiliser.

To apply a color to an element, select the element and click on the color swatches at the bottom. Use `left click` for a fill color and `shift + left click` for a stroke color. Use the X on the left side to remove colors.

### Appliquer une palette {#apply-palette}

Cette extension applique aux éléments d'un document les couleurs les plus proches parmi celles de la palette choisie.

Ces changement seront pris en compte dans l'export pdf d'Ink/Stitcht.

Exécutez `Extensions > Ink/Stitch  > Gestion des couleurs de fil > Appliquer une palette` 

## Working with Threadlists

### Exportation

Les listes de fils ne peuvent être exportées qu'en enregistrant une copie du fichier au format "Ink/Stitch: ZIP exporter plusieurs formats (.zip)" , puis après avoir cliqué sur "Enregistrer" selectionnez le format ".TXT: liste de fils".

### Appliquer une liste de fil {#apply-threadlist}

Ink/Stitch peut appliquer des listes de fil personnalisées à une broderie. Ceci est particulièrement utile si vous souhaitez utiliser un fichier de broderie qui ne comporte pas d'information de couleur (par exemple DST).

Ce peut être aussi utile si vous souhaitez essayer différents réglages de couleurs. Vous pouvez exporter et importer ces listes de fils à votre convenance, mais faites attention à ne changer ni le nombre ni l'ordre des couleurs. Si vous souhaitez les changer, faites le dans une copie du fichier svg.

* Run `Extensions > Ink/Stitch > Thread Color Management > Apply Threadlist`
* Choose a file with the thread color information to match the elements in the current document
* Define wether the color infomration file has been generated with Ink/Stitch or otherwise.
  If otherwise: Select the Ink/Stitch color palette to match colors to.
* Click on Apply

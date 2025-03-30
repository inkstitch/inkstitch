---
title: "Outil lettrage"
permalink: /fr/docs/lettering/
last_modified_at: 2025-03-14
toc: true
---
## Lettrage

Le module de lettrage crée du texte sur plusieurs lignes. Choisissez la bonne police pour votre projet dans une grande variété de polices déjà digitalisées.

![Lettrage Extensions](/assets/images/docs/fr/lettering.png)

### Usage

* Faire `Extensions > Ink/Stitch > Lettrage > Lettrage`
* Entrez votre texte (multi-ligne possible)
* Définir la police et l'échelle
    **⚠ Attention**: Pour des résultats optimaux, tenir compte des limites de redimensionement mentionnées dans le descriptif des fontes.
* Cliquer sur `Appliquer et Quitter`

### Filtres de fonte

* **Filtrage par taille**
  Les fontes sont conçues pour être  brodées dans  un intervalle de tailles donné.
  Le filtrage par taille vous aide en réduisant la liste des fontes à uniquement les fontes qui peuvent être brodées dans les dimensions choisies.
  Un filtre actif (pas à 0) déterminera  automatiquement la bonne échelle pour que la fonte sélectionnée soit dans la dimension souhaitée.

* **Glyphs**

  Si l'option est cochée, seules les fontes contenant tous les glyphes de votre texte apparaissent dans le menu déroulant des fontes

* **Famille de fonte**

  Filtre les fontes par famille, par exemple les fontes d'appliqué ou les fontes d'écriture manuelle.

### Options

* **Scale**

  Defines the output size of the font compared to the original font size (%).
  It is recommended to use the scale option, rather than resizing the font on canvas.
  This way you can make sure, that you stay within the parameters the font has been designed for.

* **Color sort**

 {% include upcoming_release.html %}
  Sort colors of multicolor fonts to avoid a huge amount of color changes.

* **Broder les lignes de texte en aller retour**

  Lorsque cette option est activée, la première ligne sera brodée de gauche à droite et la seconde de droite à gauche, etc.
  Cela donnera à votre machine des déplacements plus courts.

* **Align Text**

  Align multiline text: left, center, right, block (default), block (letterspacing)

* **Ajouter des commandes de coupes**

  Si cette option est activée, Ink/Stitch ajoutera des commandes de coupe  au choix pour chaque lettre, ou après chaque mot ou après chaque ligne.

* **Use command symbols**

  When adding trims, use command symbols. Uses the trim param setting otherwise.

### Préconfigurations

Vous pouvez enregistrer et rouvrir vos paramètres de police préférés.

## Lettrage le long d'un chemin  {#lettering-along-path}

Les lettres d'ink/stitch ont été soigneusement dessinées pour une broderie optimale. Si vous essayez de les modifier avec les outils usuels d'inkscape, il se peut que cela ne fonctionne pas comme vous le souhaitez. Placez les lettres le long  d'un chemin est un gros travail. Cet outil va vous aider à le faire.

![A text aligned along a path while using the various options](/assets/images/docs/text_along_path_alignment.png)

### Usage

* Sélectionnez un chemin et un groupe de lettrage 
* Exécutez `Extensions > Ink/Stitch > Lettrage > Lettrage le long d'un chemin ...`
* Si `Etendre` est coché Ink/Stitch va étendre les espaces entre les lettres pour que le texte utilise tout le chemin. Sinon il gardera les distances du texte original. 
* Cliquez sur 'Appliquer'

Lettering will follow the path direction. Reverse the path if needed (`Path > Reverse`).
{: .notice--info}

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

## Batch Lettering

{% include upcoming_release.html %}

Batch lettering allows to easily create multiple text files.

![A patch with four different names](/assets/images/docs/batch-lettering.png)

* Prepare a design file.
  If the file contains a path with the label `batch lettering` it will be used for the text position.
  It will work the same say as [Lettering Along Path](/docs/lettering/#lettering-along-path).
* Go to `File > Save a copy...` and click on the little arrow on the file format selection field to open a list of available file formats.
* Choose `Ink/Stitch: batch lettering (.zip)`
* Navigate to your desired output folder and click on Save

### Options

* **Text:** Enter the text, by default each new line will be placed in it's own file
* **Custom Separator:** Defaults to new lines. Specify an other separator if you wish that your text file has multiline text.
  The text will be split and placed into a new file with every occurence of the custom separator.

* **Font name:** The name of the font you wish to use. Have a look at the [font library](/fonts/font-library/) to find a list of available fonts
* **Scale (%):** Scale value to resize a font. The value will be clamped to the available scale range of the specific font.
* **Color sort:** Wether multicolor fonts should be color sorted or not
* **Add trims:** Wether trims should be added or not (never, after each line, word or letter)
* **Use command symbols:** Wether the trims should be added as command symbols or as a param option (only relevant for svg output)
* **Align Multiline Text:** Define how multiline text should be aligned
* **Lettering along path: text position:** The text position on the `batch lettering` path
* **File formats:** Enter a comma separated list of [file formats](/docs/file-formats/#writing)

### Command line usage

Here is a minimal example for command line usage of the batch lettering extension

```
./inkstitch --extension=batch_lettering --text="Hello\nworld" --font="Abecedaire" --file-formats="svg,dst" input_file.svg > output_file.zip
```

#### Options

Option             |Input Type|Values
---------- --------|----------|------
`--text`           |string    |cannot be empty
`--separator`      |string    |default: '\n'
`--font`           |string    |must be a valid font name
`--scale`          |integer   |default: 100
`--color-sort`     |string    |off, all, line, word<br>default: off
`--trim`           |string    |off, line, word, glyph<br>default: off 
`--command_symbols`|bool      |default: False
`--text-align`     |string    |left, center, right, block, letterspacing<br>default: left
`--file-formats`   |string    |must be at least one valid output format

## Créer de nouvelle polices pour Ink/Stitch
Lire le [tutoriel de création de police](/fr/tutorials/font-creation/).

Contactez nous  sur  [GitHub](https://github.com/inkstitch/inkstitch/issues) si vous souhaitez publier votre police dans l'outil de lettrage d'Ink/Stitch.

## Fichiers example concernant  le lettrage

{% include tutorials/tutorial_list key="techniques" value="Lettering" %}

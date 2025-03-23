---
title: "Import et Export de Fichiers"
permalink: /fr/docs/import-export/
last_modified_at: 2025-01-04
toc: true
---
## Importation de fichiers de broderie

Ouvrez un fichier de broderie comme vous ouvririez n’importe quel fichier SVG dans Inkscape: `Fichier > Ouvrir...` > choisissez votre fichier et cliquez `Ouvrir`.

Il ouvrira votre fichier dans le [Mode Point manuel](/fr/docs/stitches/manual-stitch/). Vous pouvez modifier des points individuels et affiner votre conception. Une fois que vous êtes satisfait, enregistrez le fichier comme décrit ci-dessous.

## Exportation de fichiers de broderie


Exportez des fichiers directement via Inkscape `Fichier > Enregistrer une copie...` (`Ctrl + Maj + Alt + S`) 
Sélectionnez un format de fichier que votre machine à broder peut lire et `Enregistrer` le fichier dans votre répertoire de sortie souhaité.

![Formats de fichiers](/assets/images/docs/en/export-selection-field.jpg)

Pour les modifications ultérieures, veillez à conserver également une version SVG de votre motif.

## Exportation par lot

Aller à `Fichier > Enregistrer une copie...` et cliquez sur la petite flèche dans le champ de sélection du format de fichier pour ouvrir une liste des formats de fichier disponibles.

Choisissez le format de fichier ZIP Ink/Stitch. Cliquez sur `Enregistrer`. On vous demandera ensuite quels formats de fichier vous souhaitez inclure.

![Export par lot](/assets/images/docs/en/export-batch.jpg)

Si vous souhaitez que les fichiers de l'archive ZIP aient un nom différent du fichier svg originel, insérez le nouveau nom dans le champs ` Nom de fichier personnalisé`.

![Options d'export par lot](/assets/images/docs/fr/zip-export1.png)

L'export en format ZIP inkstitch offre aussi des options de panelisation pour broder plusieurs copies d'un petit motif dans un grand cadre.   Si l'une des options de  répétitions est supérieure à 1, Ink/Stitch va créer  plusieurs copies du plan de broderie et les placer à la distance  choisie dans les options. Les distances sont mesurées depuis le coin haut gauche du dessin originel. Les blocs de couleur sont réordonnés pour réduire les changement de couleurs.

## Batch Lettering

{% include upcoming_release.html %}

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

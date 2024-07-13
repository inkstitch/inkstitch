---
title: "Import et Export de Fichiers"
permalink: /fr/docs/import-export/
last_modified_at: 2021-04-11
toc: true
---
## Import de fichiers de broderie

Ouvrez un fichier de broderie comme vous ouvririez n’importe quel fichier SVG dans Inkscape: `Fichier > Ouvrir...` > choisissez votre fichier et cliquez `Ouvrir`.

Il ouvrira votre dossier dans le [Mode Point manuel](/fr/docs/stitches/manual-stitch/). Vous pouvez modifier des points individuels et affiner votre conception. Une fois que vous êtes satisfait, enregistrez le fichier comme décrit ci-dessous.

## Export de fichiers de broderie

Ink/Stitch version 1.10.0 introduit la possibilité d’exporter des fichiers directement via Inkscapes `Fichier > Enregistrer une copie...` (`Ctrl + Maj + Alt + S`) 
Sélectionnez un format de fichier que votre machine à broder peut lire et `Enregistrer` le fichier dans votre répertoire de sortie souhaité.

![Formats de fichiers](/assets/images/docs/en/export-selection-field.jpg)

Pour les modifications ultérieures, veillez à conserver également une version SVG de votre motif.

## Export par lot

Aller à `Fichier > Enregistrer Enregistrer une copie...` et cliquez sur la petite flèche dans le champ de sélection du format de fichier pour ouvrir une liste des formats de fichier disponibles.

Naviguez jusqu'au dossier de sortie souhaité et choisissez le format de fichier ZIP Ink/Stitch. Cliquez sur `Enregistrer`. On vous demandera ensuite quels formats de fichier vous souhaitez inclure.

![Export par lot](/assets/images/docs/en/export-batch.jpg)

If you wish for the files within the zip-archive to have an other name than the previously saved original svg(!) file, insert the file name into the `custom file name` field.

![Batch export options](/assets/images/docs/fr/zip-export1.png)

The zip-export also offers panelization options. If repeat values are higher than one Ink/Stitch will create copies of the stitchplan and place them in defined distances.
The distances are measured from the top left position of the original design. Colorblocks will be ordered to reduce color changes.

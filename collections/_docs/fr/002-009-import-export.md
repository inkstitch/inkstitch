---
title: "Import et Export de Fichiers"
permalink: /fr/docs/import-export/
excerpt: ""
last_modified_at: 2019-10-25
toc: true
---

Ink/Stitch prend en charge de nombreux formats de broderie. Il peut importer et exporter des fichiers aux formats énumérés ci-dessous.
## Formats de fichiers pris en charge (A - Z):

### Ecriture
CSV, **DST**, **EXP**, **JEF**, PEC, **PES**, SVG, TXT (G-CODE), U01, **VP3**

### Lecture
100, 10o, BRO, DAT, DSB, **DST**, DSZ, EMD, **EXP**, EXY, FXY, GT, INB, **JEF**, JPX, KSM, MAX, MIT, NEW, PCD, PCM, PCQ, PCS, PEC, **PES**, PHB, PHC, SEW, SHV, STC, STX, TAP, TBF, TXT (G-CODE), U01, **VP3**, XXX, ZXY

**Info:** Des informations détaillées sur les formats de fichier de broderie sont disponibles dans le [EduTechWiki](http://edutechwiki.unige.ch/en/Embroidery_format).
{: .notice--info }

## Import de fichiers de broderie

Ouvrez un fichier de broderie comme vous ouvririez n’importe quel fichier SVG dans Inkscape: `Fichier > Ouvrir...` > choisissez votre fichier et cliquez `Ouvrir`.

Il ouvrira votre dossier dans le [Mode Point manuel](/fr/docs/stitches/manual-stitch/). Vous pouvez modifier des points individuels et affiner votre conception. Une fois que vous êtes satisfait, enregistrez le fichier comme décrit ci-dessous.
## Export de fichiers de broderie

### Methode 1

Ink/Stitch version 1.10.0 introduit la possibilité d’exporter des fichiers directement via Inkscapes `Fichier > Enregistrer sous...` (`Ctrl + Shift + S`) 
Sélectionnez un format de fichier que votre machine à broder peut lire et `Enregistrer` le fichier dans votre répertoire de sortie souhaité.

![Formats de fichiers](/assets/images/docs/en/export-selection-field.jpg)

Pour les modifications ultérieures, veillez à conserver également une version SVG de votre motif.

### Methode 2 (Affichage du plan de broderie)
Pour exporter vos dessins, lancez `Extensions > Ink/Stitch  > Broder...`.

![Broder...](/assets/images/docs/en/embroider.jpg){: width="450" }

Paramètres|Description
---|---
Réduire la longueur (mm)|0.0 - 10.0
Masquer les autres calques|Masquer ou pas vos calques de conception d'origine lors de la présentation du plan de points nouvellement généré
Format de fichier de sortie|Choisissez un format de fichier lisible par votre machine à broder
Dossier|Tapez votre chemin du répertoire, où vous souhaitez enregistrer votre fichier. Par défaut, le répertoire utilisé est l'emplacement où vous avez installé les fichiers Python de l'extension.

**Info:** Pour la conversion de format de fichier Ink/Stitch utilise [*pyembroidery*](https://github.com/inkstitch/pyembroidery).
{: .notice--info }

Ink/Stich va créer un fichier nommé `something.___`, où `something` est le nom de votre fichier svg(e.g. `something.svg`) et `___` est l'extension appropriée pour le format de sortie sélectionné. Si `something.___` existe déjà, il sera renommé en `something.___.1`, et `something.___.1`sera renommé en `something.___.2`, etc, jusqu'à 5 copies de sauvegarde.

   <span style="color: #3f51b5;">↳ something.___</span><br />
   <span style="color: #ff9800;">↳ something.___</span>, <span style="color: #3f51b5;">something.___.1</span><br />
   <span style="color: #f44336;">↳ something.___</span>, <span style="color: #ff9800;">something.___.1</span>, <span style="color: #3f51b5;">something.___.2</span>

**Info:** Dans les futures versions, cette extension sera renommée *`Show Stitch Plan`* et ne sauvegardera plus un fichier de broderie.
{: .notice--info}

## Export par lot

**Info:** Depuis Ink/Stitch version 1.10.0, il est possible d’exporter simultanément vers plusieurs formats de fichiers..
{: .notice--info }

Aller à `Fichier > Enregistrer sous...` et cliquez sur la petite flèche dans le champ de sélection du format de fichier pour ouvrir une liste des formats de fichier disponibles.

Naviguez jusqu'au dossier de sortie souhaité et choisissez le format de fichier ZIP Ink/Stitch. Cliquez sur `Enregistrer`. On vous demandera ensuite quels formats de fichier vous souhaitez inclure.
![Export par lot](/assets/images/docs/en/export-batch.jpg)


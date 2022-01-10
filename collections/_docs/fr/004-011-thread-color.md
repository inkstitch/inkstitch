---
title: "Thread Color Manager"
permalink: /fr/docs/thread-color/
excerpt: ""
last_modified_at: 2021-09-27
toc: true
---
## Import Threadlist

Ink/Stitch can apply custom threadlists to an embroidery design. This is especially useful, if you want to work on existing embroidery files which do not support color information (e.g. DST).

It could also be helpful, if you are wanting to test different color settings. You can export and import them as you like. But be careful not to change the amount and order of colors. In case you are planing to change these, you'd prefer to save the entire SVG instead.

## Import
Run `Extensions > Ink/Stitch > Import Threadlist ...` to apply a threadlist exported by Ink/Stitch.

If you want to import any other threadlist from a txt-file, choose the option "Import other threadlist" and pick a threadlist from the dropdown menu before clicking on apply.

**Tipp:** Install Add-Ons for Ink/Stitch to have more threadlists available.
{: .notice--info }

## Export

Threadlists can only be exported through a zip-file ([batch export](/fr/docs/import-export/#export-par-lot)).

[Read more about this function](/fr/docs/threadlist/)

## Install Custom Palette

In case you own a `.gpl` color list of the threads you are actually using. Make it available in Inkscape with this extension: `Extensions > Ink/Stitch > Thread Color Management > Install custom palette...`. You will need to restart Inkscape after this process.

The .gpl color palettes can be generated with GIMP.

## Install Thread Color Palettes for Inkscape

Ink/Stitch comes with a lot of thread manufacturer color palettes which can be installed into Inkscape. This allows to build the designs with the correct colors in mind.
Colors will appear in the PDF-Output and will also be included into your embroidery file, if your file format supports it. 

**Installer**
* Aller à `Extensions > Ink/Stitch  > Installer add-ons pour Inkscape`
* Cliquer sur `Install`
* Redémarrer Inkscape

## Palettes de couleurs du fabricant de fil

Les palettes Inkscape se trouvent dans la partie inférieure droite des nuanciers.

![Inkscape Color Palettes](/assets/images/docs/palettes-location.png)

Cliquez sur la petite flèche pour ouvrir une liste des palettes installées et choisissez la palette de couleurs du fabricant en fonction du fil que vous souhaitez utiliser.

Le choix s'appliquera également aux noms de fil à afficher dans l'aperçu avant impression.

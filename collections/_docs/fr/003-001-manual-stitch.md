---
title: "Point manuel"
permalink: /fr/docs/stitches/manual-stitch/
excerpt: ""
last_modified_at: 2023-01-20
toc: true
---
## Qu'est-ce que c'est
[![Fleurs en point manuel](/assets/images/docs/manual-stitch.jpg){: width="200x"}](/assets/images/docs/manual-stitch.svg){: title="Download SVG File" .align-left download="manual-stitch.svg" }
En mode point manuel Ink / Stitch utilisera chaque nœud d’un chemin comme point de pénétration de l’aiguille, exactement comme vous les avez placés.
![Detail de point manuel](/assets/images/docs/manual-stitch-detail.png)

Si vous ouvrez un fichier de broderie machine, vous y trouverez des points manuels.  Lorsque vous concevrez un fichier de broderie en svg, vous utiliserez très rarement les points manuels.
## Comment le créer

1. Créez un chemin. Le style de trait ou la largeur ne sont pas pertinents.
2. Ouvrez `Extensions > Ink/Stitch  > Paramètres`.
3. Activez `Placement manuel de points`. Les autres réglages n'auront aucun effet en mode point manuel.
   ![Params Stroke](/assets/images/docs/en/params-manual-stitch.jpg)


Chaque nœud d'un chemin représente un point de pénétration de l'aiguille. Ça ne va pas suivre les courbes.

![Manual Stitch Placement](/assets/images/docs/manual-stitch-placement.png)

Une représentation nette de votre chemin de point manuel peut être obtenue comme suit:
1. Selectionner tous les noeuds (`F2` puis `Ctrl`+`A`)
2. Cliquer sur ![Rendre durs les noeuds sélectionnés](/assets/images/docs/tool-controls-corner.jpg){: title="Make selected nodes corner" } in the `Tool Controls Bar`.

## Paramétres

Ouvrir `Extensions > Ink/Stitch  > Paramétres` pour paramétrer selon vos besoins.

Paramètre||Description
---|--|---
Points droits le long des chemins   ||Doit être activé pour que ces paramètres prennent effet.
Méthode                             ||Choisir le type "Point droit" 
Placement de points manuels         || **Activer Point Manuel**
Répéter                             ||Ce paramètre est sans effet sur les points manuels
Longueur du point droit             ||Ce paramètre est sans effet sur les points manuels
Tolérance du point droit            ||Ce paramètre est sans effet sur les points manuels
Espacement Zig-Zag (crête à crête)  ||Ce paramètre est sans effet sur les points manuels
Autoriser les points d'arrêts       ||Les points manuels ne permette pas l'ajout automatique de points d'arrêt. Vous devez le inclure manuellement dans votre chemin.
Forcer les points d'arrêts          ||Ce paramètre est sans effet sur les points manuels
Couper après                        ||Couper le fil après avoir brodé cet objet
Arrêter après                       ||Arrêter (pause machine) après avoir brodé cet objet. Avant l'arrêt, il y aura un saut vers la position d'arrêt si elle a été définie.

## Fichier exemple avec point manuel
{: style="clear: both;" }
{% include tutorials/tutorial_list key="stitch-type" value="Manual Stitch" %}


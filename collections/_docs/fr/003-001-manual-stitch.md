---
title: "Point manuel"
permalink: /fr/docs/stitches/manual-stitch/
excerpt: ""
last_modified_at: 2019-10-17
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

## Astuce

### Points d'arrêt en début et fin

Il ne sera pas ajouter automatiquement de points d'arrêt. Veillez donc à les créer dans le chemin.

### Faire des noeuds durs

Chaque nœud d'un chemin représente un point de pénétration de l'aiguille. Ça ne va pas suivre les courbes.

![Manual Stitch Placement](/assets/images/docs/manual-stitch-placement.png)

Une représentation nette de votre chemin de point manuel peut être obtenue comme suit:
1. Selectionner tous les noeuds (`F2` puis `Ctrl`+`A`)
2. Cliquer sur ![Rendre durs les noeuds sélectionnés](/assets/images/docs/tool-controls-corner.jpg){: title="Make selected nodes corner" } in the `Tool Controls Bar`.

## Fichier exemple avec point manuel
{: style="clear: both;" }
{% include tutorials/tutorial_list key="stitch-type" value="Manual Stitch" %}


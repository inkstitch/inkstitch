---
title: "Point manuel"
permalink: /fr/docs/stitches/manual-stitch/
last_modified_at: 2026-01-06
toc: true
---
## De quoi s'agit-il
[![Fleurs en point manuel](/assets/images/docs/manual-stitch.jpg){: width="200x"}](/assets/images/docs/manual-stitch.svg){: title="Download SVG File" .align-left download="manual-stitch.svg" }
En mode point manuel Ink / Stitch utilisera chaque nœud d’un chemin comme point de pénétration de l’aiguille, exactement comme vous les avez placés.
![Detail de point manuel](/assets/images/docs/manual-stitch-detail.png)

Si vous ouvrez un fichier de broderie machine, vous y trouverez des points manuels.  Lorsque vous concevrez un fichier de broderie en svg, vous utiliserez très rarement les points manuels.
## Comment le créer

1. Créez un chemin. Le style de trait ou la largeur ne sont pas pertinents.
2. Ouvrez `Extensions > Ink/Stitch  > Paramètres`.
3. Choisir le type `Point manuel` comme méthode.


Chaque nœud d'un chemin représente un point de pénétration de l'aiguille. Ça ne va pas suivre les courbes.

![Manual Stitch Placement](/assets/images/docs/manual-stitch-placement.png)

Une représentation nette de votre chemin de point manuel peut être obtenue comme suit:
1. Sélectionner tous les noeuds (`F2` puis `Ctrl`+`A`)
2. Cliquer sur ![Rendre durs les noeuds sélectionnés](/assets/images/docs/tool-controls-corner.jpg){: title="Make selected nodes corner" } in the `Tool Controls Bar`.

## Paramétres

Ouvrir `Extensions > Ink/Stitch  > Paramétres` pour paramétrer selon vos besoins.

Paramètre|Description     
---|---
Points droits le long des chemins       |Doit être activé pour que ces paramètres prennent effet.
Méthode                                 |Choisir le type "Point manuel"
Nombre de répétitions du point triple   |Active le [Mode point multiple](/fr/docs/stitches/bean-stitch/)<br />◦ Repasse sur chaque point le nombre de fois indiqué.<br />◦ Une valeur de 1 triplera chaque point (avant, arrière, avant).<br />◦ Une valeur de 2 permettra de quintupler chaque point, etc..<br />
Longueur maximum de point               |Les points plus longs  seront subdivisés. Laissez vide si vous ne souhaitez pas de subdivision.
Longueur minimum de point               |Est prioritaire par rapport à la valeur de la longueur minimum de point définie dans les préférences. Les points plus courts seront supprimés.
Longueur minimum de saut                |Est prioritaire par rapport à la valeur de la longueur minimum de saut définie dans les préférences. Si la distance à l'objet suivant est inférieure, il n'y aura pas de points d'arrêt, sauf si les points d'arrêts sont forcés.
Autoriser les points d'arrêts           |Les points manuels ne permette pas l'ajout automatique de points d'arrêt. Vous devez les inclure manuellement dans votre chemin. Mais vous pouvez les activer via "Forcer les points d'arrêts". 
Forcer les points d'arrêts              |Sur un point manuel, ajoute un point d'arrêt.
Couper après                            |Couper le fil après avoir brodé cet objet
Arrêter après                           |Arrêter (pause machine) après avoir brodé cet objet. Avant l'arrêt, il y aura un saut vers la position d'arrêt si elle a été définie.

## Fichier exemple avec point manuel
{: style="clear: both;" }

{% include tutorials/tutorial_list key="stitch-type" value="Manual Stitch" %}


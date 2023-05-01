---
permalink: /fr/tutorials/autoroute_sashiko/
title: "Sashiko "
language: fr
last_modified_at: 2022-05-28
excerpt: "Agencement automatique de points droits et extension Sashiko"
image: "/assets/images/tutorials/sashiko/sashiko.jpg"
tutorial-type:
  - Sample File
stitch-type:
  - "Bean Stitch"
tool:
  - "Stroke"
techniques:
field-of-use:
user-level: 
---


![Sample](/assets/images/tutorials/sashiko/sashiko.jpg)


[L'extension inkscape Sashiko](https://inkscape.org/~FractalLotus/%E2%98%85sashiko-stitching-patterns) associée à l'agencement automatique de points droits
permet de produire des fichiers de broderie style sashiko en point triple d'une manière si simple que cela en est presque indécent.

Il convient bien sur d'installer l'extension Sashiko. 

Une fois cette extension installée, y accèder par

`Extensions > Rendu > Sashiko' 

![ScreeShot](/assets/images/tutorials/sashiko/Sashiko1.jpg)

En cliquant sur "Aperçu en direct", vous pouvez facilement choisir  le motif,  le  nombre de lignes et le nombre de colonnes.

Votre choix fait, cliquez sur 'Appliquer".

Vous pouvez maintenant fermer la fenêtre de dialogue de l'extension.

Pour passer du dessin à une broderie en point triple
* Selectionnez tous les chemins que l'extension vient de créer (il y en a beaucoup)
  * Mettre tous les contours en pointillé
  * `Extensions > Ink/Stitch > Paramètres' 
    * Choisir la longueur du point droit (2 mm sur l'exemple brodé)
     * Choisir le nombre de répétitions de point triple (1 sur  l'exemple brodé)
  * `Extensions > Ink/Stitch > Outils:Trait > Agencement automatique de points droits` 
    *   Cocher "Ajouter des noeuds aux intersections"
    *   Décocher "Préservez l'ordre des points droits"

**et c'est tout !!!!**

 
Vous avez maintenant un groupe Agencement automatique qui contient un mélange de:
* chemins en  point triple dont les noms commencent par "Agencement automatique", qui correspondent au dessin choisi
* chemins en point droit simple dont les noms commencent par "Chemin de dessous", qui ont été ajouté pour vous permettre d'obtenir un résultat sans sauts de fils

Vous pourriez aussi essayer avec cette  [extension](https://tesselace.com/tools/inkscape-extension/)

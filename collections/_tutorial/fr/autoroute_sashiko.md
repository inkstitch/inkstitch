---
permalink: /fr/tutorials/autoroute_sashiko/
title: "Sashiko "
language: fr
last_modified_at: 2025-02-10
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

[L'extension inkscape Sashiko pour ink/stitch ](https://gitlab.com/kaalleen/sashiko-inkscape-extension) associée à l'agencement automatique de points droits ou à l'extension redwork permet de produire facilement des fichiers de broderie style sashiko .

Notez que cette extension est légérement différente de l'extension originale [Sashiko Inkscape extension](https://inkscape.org/~FractalLotus/%E2%98%85sashiko-stitching-patterns), en ce sens que le résultat produit ne contient jamais deux copies superposées du même chemin.

Il convient bien sûr d'installer l'extension Sashiko pour ink/stitch. 

Une fois cette extension installée, y accèder par

`Extensions > Rendu > Sashiko' 

![ScreeShot](/assets/images/tutorials/sashiko/Sashiko1.jpg)

En cliquant sur "Aperçu en direct", vous pouvez facilement choisir  le motif,  le  nombre de lignes et le nombre de colonnes.

Votre choix fait, cliquez sur 'Appliquer".

Vous pouvez maintenant fermer la fenêtre de dialogue de l'extension.

## Si vous avez choisi un motif qui donne un résultat non connecté (par exemple Offset Crosses)  

Utilisez maintenant  `Extensions > Ink/Stitch > Outils:Trait > Agencement automatique de points droits` 

Pour passer du dessin à une broderie en point triple
* Selectionnez tous les chemins que l'extension vient de créer (il y en a beaucoup)
  * `Extensions > Ink/Stitch > Paramètres'
    * choisir point droit comme methode
    * Choisir la longueur du point droit (2 mm sur l'exemple brodé)
     * Choisir le nombre de répétitions de point triple (1 sur  l'exemple brodé)
  * `Extensions > Ink/Stitch > Outils:Trait > Agencement automatique de points droits` 
    *   Cocher "Ajouter des noeuds aux intersections"
    *   Décocher "Préservez l'ordre des points droits"
   
      Vous avez maintenant un groupe Agencement automatique qui contient un mélange de:
* chemins en  point triple dont les noms commencent par "Agencement automatique", qui correspondent au dessin choisi
* chemins en point droit simple dont les noms commencent par "Chemin de dessous", qui ont été ajoutés pour vous permettre d'obtenir un résultat sans sauts de fils

## Si vous aves choisi un motif qui donne  un resultat connecté  (ou très peu disconnecté) (par exemple Blue Ocean Weaves) 

Utilisez maintenant `Extensions > Ink/Stitch > Outils:Trait > Redwork` 

Choisissez vos paramètres (0.5mm est un bon choix pour les deux premiers  paramètres.

Si vous choisissez l'option combiner et 0 répétition de point multiple, vous obtiendrez un unique chemin qui passe partout exactement deux fois.

Si vous choisissez l'option combiner et un point multiple, vous obtiendrez une alternance de chemin de dessous au point droit  et  de chemin en point multiple. Pour un rendu uniforme, chaque chemin sera brodé une fois en point droit simple dessous et une fois en point multiple dessus

Si vous choisissez de ne pas  combiner vous obtiendrez une multitude de chemins. Cette option n'est à utiliser que si vous souhaitez manipuler le résultat.

Vous pourriez aussi essayer avec d'autres extensions comme :

*[Tiling extension](https://inkscape.org/fr/~cwant/%E2%98%85inkscape-tiling-extension+2)

*[Bobbinlace extension](https://d-bl.github.io/inkscape-bobbinlace).

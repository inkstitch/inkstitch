---
permalink: /fr/tutorials/cookie_cutter_tiling/
title: "Pavage à l'emporte pièce"
language: fr
last_modified_at: 2023-05-04
excerpt: "Pavage"
image: "/assets/images/tutorials/tutorial-preview-images/cloth_line.jpg"
tutorial-type:
stitch-type:
  - "Running Stitch"
  - "Bean Stitch"
techniques:
field-of-use:
tool:
  - "Stroke"
  - "Fill"
  - "Circular Fill"
user-level:
toc:
  true
---

{% include upcoming_release.html %}

![Brodé](/assets/images/tutorials/tutorial-preview-images/cloth_line.jpg)

Le but de ce tutorial est de montrer comment remplir une forme en découpant  une répétition régulière de motifs obtenue  en utilisant l'effet de chemin pavage.



## Pavages
L'effet de chemin pavage répéte un dessin un nombre spécifié de fois en lignes et en colonnes, avec des options permettant de varier espacement, décalage, rotation, d'ajouter des symmétries, etc.

Ces pavages sont particulièrement intéréssant pour la broderie, que ce soit pour créer des textures sur des remplissages, ou pour créer des motifs de remplissages.
Voici quelques exemples:

 ![tiles](/assets/images/tutorials/cookie_cutter_tiling/all_png.png) 
 
Vous reconnaitrez (ou pas) parmi ces exemple les 4 pavages qui ont été utilisés pour créer la broderie de la corde la linge.
* le remplissage du T shirt à gauche provient du pavage du milieu de la première rangée
* le haut et le bas de la robe proviennent des deux derniers pavage de la dernière rangée
* la ceinture de la robe, exception de cet exemple, est un remplissage circulaire avec alternance de point simples et de points triples
* le remplissage du maillot de bain provient du dernier pavage de la rangée du milieu. Moins évident à l'oeil....

[Télécharger le fichier contenant tous ces pavages](/assets/images/tutorials/cookie_cutter_tiling/tiles_ideas.svg) 
Dans tous ces exemples, tous les chemins constituant le motif sont regroupés, et l'effet de chemin est appliqué sur le groupe. 
Ils sont assez faciles à obtenir car toute modification est réfléchie immédiatement sur le canevas d'inkscape.

Plus de détails sur l'utilisation de l'effet de chemin pavage dans un tutoriel à venir


## Préparation  des  vêtements

Les svg des trois vêtements ont été créés par Bernd Lakenbrink du [Noun Project](https://thenounproject.com/browse/collection-icon/clothes-icon-set-158916/?p=1).

Le svg du  [T Shirt](https://thenounproject.com/browse/icons/term/womans-shirt/) doit être modifié. En effet, ce type de svg parfait pour les écrans ou les machines de broderie ne convient pas tel quel pour ce type de broderie : ce qui apparait à l'oeil comme des traits est en fait constitué de remplissage. 



* Téléchargez le fichier  du T Shirt
* Sélectionnnez les chemins constituant le vêtement
* `Extensions > Ink/Stitch > Outils: Remplissage > Convertir remplissage en trait`
* L'extension a créé un groupe avec beaucoup de chemins, dont certains sont inutiles. Il est utile de les simplifier avant de reconstitué la forme que l'on souhaite remplir ainsi que les détails suplémentaires à broder.

Les quatre images ci dessous montrent successivement l'apparence du svg à l'écran, ce à quoi il ressemble  en supprimant le remplissage, et ce que l'extension de conversion permet d'obtenir, et ce que l'on utilisera finalement : une forme fermée (orange) et deux détails en rouge.

![T-Shirt](/assets/images/tutorials/cookie_cutter_tiling/Tshirt.png) 

Les vêtéments préparés, se trouvent dans le calque "clothes" de ce fichier qui contient ausi tous les pavages necessaires.

![cloth_line](/assets/images/tutorials/cookie_cutter_tiling/cloth_line.svg) 

[Télécharger le fichier](/assets/images/tutorials/cookie_cutter_tiling/cloth_line.svg)




## Recouvrir chaque surface à remplir par un pavage
L'étape suivante consiste à recouvrir chaque surface à remplir par un pavage. Voici le choix qui a été fait (et que vous pouvez retrouver dans le calque "Clothline preparing pattern fill"

![cloth_line](/assets/images/tutorials/cookie_cutter_tiling/tiled_cloths.png) 

Aucune difficulté à cette étape

## Passer au  remplissage de chaque vêtement
Le but est d'obtenir ceci
![final](/assets/images/tutorials/cookie_cutter_tiling/clothline_final.png) 

Selon le pavage choisi, le résultat est plus ou moins facile à atteindre

### Exemple d'un résultat facile : le T -Shirt 

* dupliquer la forme T-shirt

* Applatir l'effet de chemin
* Prendre l'intersection  du resultat avec une copie du T shi

* Tout sélectionner (intersection plus copie restante)
* Extensions > Ink/Stitch > Paramètres 

* Extensions > Ink/Stitch > Outils : Trait > Agencement automatique de points droits.

On constate une multitude de tous petits chemins. On pourrait les éliminer, mais le plus simple est d'aller dans les préférences, et pour ce fichier seulement augmenter la longueur minimum de point et la passer à 1mm.

A part, paramétrer les détails

### Exemple d'une suprise : le maillot de bain

### Exemple ou l'intersection n'est pas satisfaisante 

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

Plus de détails sur l'utilisation de l'effet de chemin pavage dans un tutoriel à veni


## Préparation  des  vêtements

Les svg des trois vêtements ont été créés par Bernd Lakenbrink du [Noun Project](https://thenounproject.com/browse/collection-icon/clothes-icon-set-158916/?p=1).

Le svg du  [T Shirt](https://thenounproject.com/browse/icons/term/womans-shirt/" target="_blank" title="womans shirt Icons") doit être modifié. En effet, ce type de svg parfait pour les écrans ou les machines de broderie ne convient pas tel quel pour ce type de broderie : ce qui apparait à l'oeil comme des traits est en fait constitué de remplissage. 

* Téléchargez le fichier  du T Shirt
* Selectionnnez les chemins constituant le vêtement
* `Extensions > Ink/Stitch > Outils: Remplissage > Convertir remplissage en trait`



### Étape 2: Applatir et paramètrer
* Applatir l'effet de chemin
![Flatten](/assets/images/tutorials/tiling/flatten_lazy.jpg)
* Tout sélectionner
* Extensions > Ink/Stitch > Paramètres 


### Étape 3 : Agencement automatique de points droits
* Tout sélectionner
* Extensions > Ink/Stitch > Outils : Trait > Agencement automatique de points droits.

[Télécharger le dessin final ](/assets/images/tutorials/tiling/tiling_lazy.svg)

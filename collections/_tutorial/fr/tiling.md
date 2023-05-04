---
permalink: /fr/tutorials/pavage/
title: "Pavage"
language: fr
last_modified_at: 2023-05-04
excerpt: "Pavage"
image: "/assets/images/tutorials/tutorial-preview-images/tiling_embroidered.jpg"
tutorial-type:
stitch-type:
  - "Running Stitch"
  - "Bean Stitch"
techniques:
field-of-use:
tool:
  - "Stroke"
user-level:
---

{% include upcoming_release.html %}

![Brodé](/assets/images/tutorials/tutorial-preview-images/tiling_embroidered.jpg)

Le but de ce tutorial est de montrer comment utiliser l'effet de chemin Pavage pour obtenir un pavage, puis  
les manipulations à faire pour obtenir une broderie sans sauts de fils.

## Étape 1 : Création du pavage

Le pavage final ![tiles](/assets/images/tutorials/tiling/full_tiling.png) est constitué de copies de :
![tile](/assets/images/tutorials/tiling/tile.png)

Pour pouvoir créer un cheminement minimisant les sauts de fil dans la broderie finale, ce dessin est en fait :

![Dessin initial ](/assets/images/tutorials/tiling/tile.svg)
[Télécharger le dessin initial](/assets/images/tutorials/tiling/tile.svg)

Le dessin est constitué de 6 chemins :
  * Bleu , Jaune , Orange et Noir ont leur deux extrémités alignées sur une verticale
  * Vert et Rouge, ont leur deux extrémités alignées sur une horizontale
  
De plus il y a beaucoup d'extrémités en commun:
  * Bleu et Noir ont les mêmes extrémités
  * Jaune et Orange ont les mêmes extrémités
  * Vert et Rouge, dans le pavage obtenu ont quasiment les mêmes extrémités sauf sur les bords
  
  Il est préférable de faire une première fois le tutorial [en téléchargeant ce  dessin initial](/assets/images/tutorials/tiling/tile.svg)
  
* Sélectionnez le groupe qui contient les 6 chemins et appliquez l'effet de chemin Pavage avec ce paramètrage :
* ![LPE](/assets/images/tutorials/tiling/colored_tiling.jpg)


## Étape 2 : Applatir d'effet de chemin 
 ![Flaten](/assets/images/tutorials/tiling/flatten.jpg)

## Étape 3 : Dégrouper
Le groupe autour des chemins n'est plus utile, vous pouvez dégrouper

## Étape 4 : Couleur par couleur joindre les noeuds

 ![Join a color](/assets/images/tutorials/tiling/join-a-color.jpg)
 A faire 6 fois, une fois par chemin (un chemin = une couleur) :
 * Masquez les 5 autres couleurs
 * Sélectionnez le chemin visible
 * En mode Noeud, sélectionnez **les noeuds intérieurs seulement**, et cliquez sur "Joindre les noeuds selectionnés" (entouré d'un rectangle rouge)


## Étape 5 : Joindre les couleurs deux par deux

 ![Jointwo colors](/assets/images/tutorials/tiling/join_two_colors.jpg)
 
 Remarque : Il arrive qu'à cette étape des chemins soient recombinés.
 
* Masquez  Rouge, Vert, Jaune et Orange
* Sélectionnnez Bleu et Noir
* En mode Noeud, **sélectionnez tous les noeuds en haut**, et cliquez sur "Joindre les noeuds selectionnés" 
* Groupez le ou les chemin résultant

Pour Jaune et Orange, sélectionnez tous les noeuds en bas et cliquez sur "Joindre les noeuds selectionnés" 
Pour Vert et Rouge, sélectionnez les  noeuds  **superposés** à gauche et cliquez sur "Joindre les noeuds selectionnés" 

Voici un résultat possible: 

 ![Two colors joined](/assets/images/tutorials/tiling/two_colors_joined.jpg)
 
 














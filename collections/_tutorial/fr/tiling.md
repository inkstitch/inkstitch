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
les manipulations à faire pour obtenir une broderie sans sauts de fils. Deux techniques sont présentées:
Une technique paresseuse très simple, mais va créer beaucoup de chemins de dessous. Ce n'est pas grave si l'on veut une broderie en point triple qui les camoufler  bien, mais si l'on veut utiliser une alternance de point simple et de point triple pour évoquer un point à la main, la deuxième technique qui ne générera pas de chemins de dessous est préférable

## Technique paresseuse


## Technique sans chemins de dessous

### Étape 1 : Création du pavage

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


### Étape 2 : Applatir d'effet de chemin 
 ![Flaten](/assets/images/tutorials/tiling/flatten.jpg)

### Étape 3 : Dégrouper
Le groupe autour des chemins n'est plus utile, vous pouvez dégrouper

### Étape 4 : Couleur par couleur joindre les noeuds

 ![Join a color](/assets/images/tutorials/tiling/join-a-color.jpg)
 A faire 6 fois, une fois par chemin (un chemin = une couleur) :
 * Masquez les 5 autres couleurs
 * Sélectionnez le chemin visible
 * En mode Noeud, sélectionnez **les noeuds intérieurs seulement**, et cliquez sur "Joindre les noeuds selectionnés" (entouré d'un rectangle rouge)


### Étape 5 : Joindre les couleurs deux par deux

 ![Jointwo colors](/assets/images/tutorials/tiling/join_two_colors.jpg)
 
 Remarque : Il arrive qu'à cette étape des chemins soient recombinés.
 
* Masquez  Rouge, Vert, Jaune et Orange
* Sélectionnnez Bleu et Noir
* En mode Noeud, **sélectionnez tous les noeuds en haut**, et cliquez sur "Joindre les noeuds selectionnés" 
* Groupez le ou les chemin résultant

Pour Jaune et Orange, sélectionnez tous les noeuds en bas et cliquez sur "Joindre les noeuds selectionnés" 
Pour Vert et Rouge, sélectionnez les  noeuds  **superposés** à gauche et cliquez sur "Joindre les noeuds selectionnés" 

Voici un résultat possible: 

 ![Two colors joined](/assets/images/tutorials/tiling/joined_two_colors.jpg)
 
 
### Étape 6: Séparer les chemins

* Sélectionnez tous les chemins
* Chemin > Séparer

### Étape 7: Ordonner les groupes et ordonner dans les groupes 

Pour limiter au maximum les sauts de chemins, ici le bon  choix c'est de broder dans l'ordre:

* les chemins bleus de la gauche vers la droite (on part en bas à gauche, on arrive en bas à droite
* les chemins rouge-vert de bas en haut (on part en bas à droite, on arrive en haut à droite)
* les chemins jaunes de la droite vers la gauche (on part en haut à droite,  on a arrive en haut à  gauche

L'usage de Extensions > Inkstitch > Editer >Réordonner dans l'ordre de la sélection simplifie la tâche.


### Étape 8: Tout mettre de la même couleur et appliquer les paramètres de broderie

* Tout sélectionner et donner à tous les chemins la même couleur
* Extensions > Inkstitch> Paramètres

 ![Two colors joined](/assets/images/tutorials/tiling/parameters.jpg)
 Ici on a choisit un point alternativement simple et quintuple
 
 Observer la simulation et vérifier que tout se passe bien dans l'ordre pévu.
 
 ### Étape 9: Convertir les sauts de fil en chemin
 
 * Tout sélectionner
 * Extensions > InkStitch > Outils: Trait > Convertir sauts de fil en trait
 * Choisir la longueur du points pour ces  chemins de liaison


### Étape 10: Compléter le carré extérieur
  * Ajouter à la fin un chemin à gauche de bas en haut
  * Modifier les chemins (ex sauts) aux deux coins à droite pour couvrir les manques
  
 * Extensions > InkStitch > Visualiser et Exporter > Simulation
 pour admirer le travail



 [Télécharger le fichier complet](/assets/images/tutorials/tiling/tiling.svg)



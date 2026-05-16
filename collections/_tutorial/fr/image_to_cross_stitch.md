---
permalink: /fr/tutorials/image_to_cross_stitch/
title: "D'une image aux points de croix"
language: fr
last_modified_at: 2026-05-15
excerpt: "Utilisation de l'assistant point de croix pour passer d'une image à un remplissage en points de croix"
image: "/assets/images/tutorials/tutorial-preview-images/cross_stitch_cat.jpg"
tutorial-type:
stitch-type:
 - Cross Stitch
tool:
 - Fill
techniques:
field-of-use:
user-level: 
---

L'assistant point de croix permet la transformation d'une image en remplissage en Point de Croix

Le résultat des différentes étapes de ce tutorial se trouvent dans ce fichier:

![SVG](/assets/images/tutorials/image_to_cross_stitch/pawpedia.svg)

[Télécharger ](/assets/images/tutorials/image_to_cross_stitch/pawpedia.svg){: download="pawpedia.svg" }





## Image de départ

Le processus sera d'autant plus simple et efficace que l'image sera simple, avec peu de couleurs, et des zones de couleurs bien démarquées. 
L'image de départ (en haut à gauche) est proposée par Pawpedia sur [Pixabay](https://pixabay.com/de/illustrations/image-10216974), sous licence pixabay, permettant la création d'œuvre dérivée. 

Il faut décider de deux dimensions :

- la taille souhaitée pour la broderie (180 mm dans l'exemple), et réduire l'image à cette taille
- la taille des croix (2 mm dans l'exemple)


## Utilisation de l'assistant point de croix pour générer des remplissages
Sélectionner l'image et Ink/Stitch > Outils: Remplissage > Assistant point de croix

- Dans l'onglet paramètres :
   - Rétablir les valeurs par défaut
   - Choisir l'espacement horizontal de la grille
- Puis dans l'onglet Paramètres de l'image matricielle, jouer avec les divers paramètres pour obtenir un résultat satisfaisant
![chat](/assets/images/tutorials/image_to_cross_stitch/cat_settings.jpg)

Pour que les zones soient mieux reconnues, j'ai beaucoup augmenté la saturation, modifiant ce faisant les couleurs originelles.

Si votre ordinateur le supporte cocher la case Aperçu svg est utile, mais déjà la simple prévisualisation de l'image permet de choisir les paramètres.

Sur cet exemple, il n'a pas été possible de l'éliminer totalement l'arrière-plan multicolore.

Notez que le nombre de couleurs comprend la couleur de l'arrière fond, qu'il soit supprimé ou non. Ce nombre de couleurs est aussi un maximum, et non une valeur qu'Ink/Stitch atteindra à tout prix.

Le résultat (calque "first result") est une base de travail que l'on peut améliorer. 

## Amélioration des formes et de la broderie
- supprimer les parties de l'arrièrre-plan qui ont été conservées.
- rajout des moustaches et autres poils. Les poils blancs de l'image de départ sont fins et n'ont pas été assez conservés par l'assistant point de croix.
 Il suffit de les dessiner **au-dessus** de l'image obtenue, sans se soucier de produire une forme pixelisée. J'ai donc dessiné avec l'outil courbe de beziers des lignes blanches là où je voulais des poils, j'ai donné une épaisseur de 3 mm a ces lignes, j'ai converti leur contour en chemin (Inkscape > Chemin > Contour en chemin) pour obtenir des surfaces étroites.
 Je sélectionne alors le groupe de Point de Croix et les poils ajoutés, et je relance l'assistant point de croix (j'aime bien dégrouper avant pour un résultat plus ordonné).

 Le fait de relancer l'assistant point de croix (avec les options pixeliser et supprimer les superpositions cochées), permet de recalculer de nouvelles formes pixelisées et de  bien voir où l'on en est.
 Au cours du processus d'amélioration, on peut être amené à utiliser l'assistant plusieurs fois.

Avec une telle image de départ, il est inévitable d'obtenir beaucoup de toutes petites zones (avec seulement une ou deux croix) et beaucoup de formes déconnectées, donc à l'arrivée énormément de sauts ou de coupes de fil.

- pour les toutes petites zones, je modifie leur couleur pour leur donner la couleur d'une zone adjacente : pour cela sélectionner la petite zone, puis sélectionner l'outil pipette et cliquer dans une zone adjacente.
- j'essaye de fusionner des zones de couleurs identiques quasi adjacentes. Notez qu'il suffit que deux zones de même couleur se touchent par un coin pour qu'elles puissent être fusionnées. Cela peut se faire soit par déformation des formes existantes soit simplement en dessinant au-dessus les formes existantes.

Après avoir un résultat visuellement satisfaisant, ne pas oublier de tout sélectionner et relancer l'assistant point de croix afin que les zones adjacentes de même couleur soient fusionnées.

Il faut trouver un compromis entre le respect de l'image initiale, et la simplification de la broderie.

Le résultat se trouve dans le calque "tweaking the shapes"

## Choisir les couleurs de la broderie
Avant de broder, on peut si on le souhaite choisir des couleurs plus proches de celles de l'image d'origine, tout en se limitant aux couleurs de sa palette de fil préférée.
Le résultat final est dans le calque "changing_colors"






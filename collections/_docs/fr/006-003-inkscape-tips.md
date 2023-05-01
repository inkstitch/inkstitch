---
title: "Astuces Inkscape"
permalink: /fr/docs/inkscape-tips/
excerpt: ""
last_modified_at: 2023-05-01
toc: true
---
Beaucoup des outils présentés ici ne créent pas de chemins. Pour les utiliser avec Ink/Stitch, vous devrez  convertir les objets créés en chemin (`Majuscule + Ctrl + C`) et éventuellement les modifier encore plus.

Ink/Stitch peut être utilisé avec Inkscape 0.92 ou Inkscape 1. La plupart des tutoriels listés sur cette page utilisent Inkscape 0.92.

## Inkscape : Tutoriels Basiques

Plusieurs tutoriaux interactifs sont disponibles dans Inkscape même en sélectionnant `Aide> Didacticiels` dans le menu, dont le tutoriel basique ci-dessous:

 * [Tutoriel basique sur inkscape.org](https://inkscape.org/fr/doc/basic/tutorial-basic.fr.html)
 * [Bases sur tavmjong.free.fr](http://tavmjong.free.fr/INKSCAPE/MANUAL_v14/html_fr/Basics.html)
 * [tutoriel sur les formes sur inkscape.org](https://inkscape.org/fr/doc/tutorials/shapes/tutorial-shapes.html)
 * [Chemins sur tavmjong.free.fr](http://tavmjong.free.fr/INKSCAPE/MANUAL_v14/html_fr/Paths-Combining.html)

### Vecteurs

Les éléments de votre fichier Inkscape sont des _images vectorielles_, qui utilisent des fonctions mathématiques pour définir des formes.  Ils utilisent des points appelés  _noeuds_,  et des _segments_  qui connectent les noeuds. Il est possible d'éditer des formes vectorielles en déplaçant des noeuds et en modifiant les angles des segments à l'aide de l'éditeur de noeuds ou en utilisant d'autres outils Inkscape. Quand vous utilisez d'autres outils, comme par exemple lorsque vous agrandissez une forme avec l'outil de Sélection, de nombreux noeuds sont modifiés derrière la scène par Inkscape.

Une forme vectorielle est _fermée_  quand elle fait un tour complet  (comme un cercle ou un carré) et chaque noeud est connecté à deux autres noeuds. Une forme est _ouverte_ quand elle a deux extrémités libres, (comme une spirale ou une ligne droite). La bordure de la forme est appelée le _contour_ et la surface à l'intérieur d'une forme fermée est appelée le  _fond_. 

[Lire plus sur le fonctionnement des formes vectorielles sur Sketchpad.net](http://sketchpad.net/drawing1.htm)


### Dessiner et Sélectionner

Les icônes du côté gauche de votre fenêtre montrent tous les outils pour créer et interagir avec votre dessin. 
Inkscape dispose de plusieurs outils pour créer divers types d'objets, tels que l'outil rectangle (`F4`), l'outil ellipse (`F5`), l'outil étoile (`*`), l'outil spirale (`F9`), l'outil crayon (`F6`), et l'outil texte (`F8`).  
La plupart de ces outils s'utilisent en glissant sur le canevas pour placer les coins de votre forme. Chaque outil de dessin a ses propres options (montrées dans la barre d'outils Contrôles au dessus du canevas) que vous pouvez utiliser pour obtenir différents résultats. En savoir plus sur la création de [Formes](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Shapes.html), de [Chemins](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Paths.html), ou de [Texte](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Text.html).

La première icône en haut du panneau Outils est l'outil de Sélection. que vous pouvez aussi activer en tapant `F1`. 
Cliquez sur un objet avec l'outil de sélection pour le déplacer sur le canevas et pour faire apparaître des poignées qui permettent de le transformer. Cliquer une fois sur un objet fait apparaître les poignées de redimensionnement, cliquer une deuxième fois les remplace par des poignées de rotation. Garder la touche Majuscule enfoncée pour sélectionner plusieurs objets en même temps. Vous pouvez aussi sélectionner plusieurs objets simultanément en glissant l'outil de sélection autour d'eux. 
[En savoir plus sur les transformations d'objets.](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Transforms.html)

Les objets peuvent aussi être sélectionnés en ouvrant le panneau Calques et Objets (` Objet > Calques et Objets...` dans le menu) et en cliquant sur un des noms de la liste. Vous pouvez sélectionner des objets de cette manière quelque soit l'outil actif.

Pour utiliser une commande de menu sur un objet (par exemple pour le convertir en chemin) vous devez préalablement le sélectionner.


### Objets et Chemins
Un _objet_  est un élément de votre fichier qui peut être manipulé individuellement. Vous pouvez voir la liste de tous les objets de votre fichiers en exécutant `Objet > Objets...`  dans le menu. Savoir comment vos objets sont définis est très important pour vos fichiers de broderie, c'est donc une bonne idée de garder ce panneau ouvert quand vous travaillez avec Ink/Stitch.

Il y a de nombreux types d'objets dans Inkscape, tels que chemins, rectangles, cercles, polygones, spirales et textes. Des outils différents créent des objets de type différents, chaque type ayant ses propres règles d'usage.

Un _chemin_ est la représentation la plus basique d'une forme vectorielle : il s'agit juste d'une série de noeuds et de segments qui décrivent une forme. Une fois un chemin créé, seuls les outils de base permettent de l'éditer, et ces outils fonctionnent de la même manière quelque soit l'apparence du chemin.  D'autres objets mémorisent l'information sur leur forme de manière plus spécifique ce qui permet de les modifier facilement. Par exemple, après avoir dessiné un polygone avec l'outil étoile, vous pouvez utiliser les contrôles de l'outil pour changer rapidement le nombre de sommets de la forme. Si vous aviez dessiné la même forme comme un chemin, vous devriez déplacer chaque sommet manuellement pour en ajouter d'autres. Toutefois, vous pouvez modifier un chemin pour obtenir n'importe quelle forme, tandis que les autres types d'objets ont des contraintes sur leur forme.

Ink/stitchh peut maintenant travailler avec presque tous les objets sans qu'il ne soit nécessaire de les transformer en chemins.  L'exception restant l'objet texte qu'Ink/Stitch ne connait pas et qui donc necessite une convertion en chemin.


Tout objet peut être converti en chemin en le sélectionnant  (soit en cliquant avec l'outil Sélection, soit en cliquant son nom dans le panneau Objets) puis en tapant `Majuscule+ Ctrl + C` ou en exécutant  `Chemin > Objet en Chemin` dans le menu.  Une fois l'objet converti en chemin, vous pouvez utiliser l'outil d'édition de  Noeuds pour faire des changements précis sur les noeuds et les segments.

Attention, lorsque vous convertissez des objets en chemins, car on ne peut pas reconvertir ces chemins en objets. Pour cette raison, vous pouvez préférer dupliquer d'abord votre objet avant de convertir la copie en chemin, tout en gardant la forme originale pour le cas où vous souhaiteriez l'éditer ultérieurement.


Ces objets particuliers sont adaptés pour:
 * du texte ou des formes géométriques simples
 * modifier la géométrie d'une forme en son entier
 * comme point de départ d'un nouveau dessin

Les chemins sont adaptés pour:
 * Faire des changements précis sur une petite section d'une forme
 * Dessiner des formes à main levée
 * Préparer votre dessin terminé pour la broderie
 
Vous pouvez vérifier le type d'un objet dans la description qui apparait dans la barre de statut en bas de l'écran lorsque l'objet est sélectionné. Notez que vous ne _pouvez pas_ dire si un objet est un chemin rien qu'en regardant son nom dans le panneau Objets car Inkscape donne des noms comme "path1234" à des cercles ou des spirales aussi bien qu'à de véritables chemins.

### Fond et Contour
Faites apparaître le panneau "Fond et Contour" en tapant `Majuscule+Ctrl+F` ou en sélectionnant `Objet > Fond et Contour...`  à partir du menu pour contrôler la couleur et le style du fond et du contour du chemin.
La couleur exacte et le style de votre chemin n'ont globalement rien à voir avec votre fichier de broderie, mais vous devez savoir comment les éditer car Ink/Stitch utilise le style du contour pour décider du type de point de broderie à utiliser, et insère  ou non des changements de fils selon si les chemins sont ou non de la même couleur.

Ce panneau est assez simple. Pour des chemins qu'Ink/Stitch transformera en point de remplissage, l'onglet Fond doit choisir Aplat (le deuxième choix) ou dégradé linéaire (troisième choix) et l'onglet Contour doit avoir la croix X sélectionnée (premier choix). Pour tous les autres points, sélectionnez le X dans l'onglet Fond et Aplat dans l'onglet Contour. Utilisez l'onglet "Style de contour" pour choisir soit une ligne pleine soit un pointillé selon le style de point désiré.

Le dégradé linéaire ne peut s'utiliser que sur un remplissage automatique et nécessitera l'usage ultérieur de [Convertir en bloc de dégradés]

Les couleurs peuvent aussi être choisies en utilisant la palette en bas de la fenêtre : cliquez sur une couleur pour l'utiliser comme une couleur de fond, et faites un clic majuscule pour l'utiliser pour le contour.


### Travailler avec des chemins
Utilisez le second outil à partir du haut , l'outil noeud (aussi activé par  `F2`), pour éditer directement les noeuds et les segments d'un chemin.
Sélectionnez un chemin avec l'éditeur de noeuds cause l'apparition de marqueurs sur tous les noeuds. Ces marqueurs peuvent être déplacés à la souris, il est possible aussi d'ajouter des noeuds, d'en supprimer et autre. Vous verrez aussi des poignées sur les noeuds, que vous pouvez déplacer pour ajuster l'angle des segments. 
Cet outil ne fonctionne qu'avec des objet _chemin_ comme expliqué ci-dessous -- si vous ne voyez pas de points gris apparaître au long de l'objet quand vous le sélectionner avec l'éditeur de noeuds, c'est qu'il ne s'agit pas d'un chemin.
[En savoir plus sur l'éditeur de noeuds.](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Paths-Editing.html)

Deux commandes sont importantes pour préparer les chemins pour  Ink/Stitch:  Combiner (`Ctrl+K` or `Chemin > Combiner`)  et Séparer  (`Majuscule+Ctrl+K` ou `Chemin > Séparer`).  Par exemple, pour créer des colonnes satin dans  Ink/Stitch  il faut combiner deux lignes en un seul chemin. Ces commandes ne font aucune modification sur la forme ou les noeuds d'un chemin, elles ne font que modifier la manière dont Inkscape classifie le chemin.

La commande  _Combiner_  prend tous les chemins sélectionnés et les fusionne en un seul objet chemin. Inkscape traite alors ces chemins comme une seule unité pour la sélection et la transformation. On peut voir dans le panneau objets que la liste est plus courte après un Combiner. Le résultat de combiner est un _chemin composite_, qui comporte plus qu'une ligne.

La commande _Séparer_ , appliquée à un chemin composite , isole chaque ligne continue dans un objet séparé. Elle sépare le chemin composite en autant de chemins que possible sans perdre de segment. Après son utilisation, la liste des objets sera plus longue.

il y a d'autres commandes pour combiner ou diviser au niveau des noeuds d'un chemin, d'une manière qui change la forme elle même, et pas seulement la manière dont Inkscape la gère.
[lire plus sur les opérations de chemin.](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Paths-Combining.html)

### Calques
Dans Inkscape, tous les objets sont empilés dans un ordre spécifique. Ink/Stitch utilise cet ordre pour déterminer l'ordre dans lequel ces objets seront brodés.
Vous pouvez voir cet ordre dans le panneau Objets (`Objet > Objets...` dans le menu). 
L'ordre des objets peut être modifié en faisant glisser les noms dans le panneau Objets, ou en tapant  `Page Haut` et `Page Bas`.  

Il est possible de renommer un objet en double cliquant sur son nom, ce qui peut vous aider à organiser votre empilement. Vous verrez aussi trois icônes à la gauche de chaque nom d'objet dans ce panneau. Cliquez sur l'icône oeil pour cacher un objet, et cliquez sur l'icône verrou pour empêcher un objet d'être éditer.


Les _Groupes_ et les  _Calques_  rendent plus facile la gestion de vos objets et de leur ordre.
Une fois un groupe formé, cliquer sur un objet du groupe sélectionne le groupe tout entier, vous permettant de modifier tous les éléments d'un groupe en une seule opération.
Pour grouper des objets, sélectionnez les tous avec `Majuscule+clic`, puis tapez `Ctrl+G` ou exécutez `Objet > Grouper` dans le menu.
Le groupe apparait aussi comme un élément repliable dans la liste d'Objets, et les objets peuvent être déplacés dans et en dehors d'un groupe en les faisant glisser dans le panneau Objets. Toutefois, il est plus sûr d'utiliser `Edition > Couper` pour enlever un objet d'un groupe, puis  `Edition > Coller` dans un autre groupe. Vous devez sélectionner un objet dans le groupe de destination pour que l'objet collé aille bien dans ce groupe. 
Un groupe peut contenir d'autres groupes. 

Les calques fonctionnent de manière similaire aux groupes, mais leur principale raison d'être est de permettre de contrôler plus facilement l'ordre des objets.
Un nouveau calque est créé avec le bouton + sous la liste d'objets ou en tapant `Majuscule+Ctrl+N`. 
Les objets peuvent être déplacés d'un calque à l'autre en les faisant glisser dans la liste d'objets , exactement comme les groupes, mais ils peuvent aussi être rapidement déplacés un calque au dessus ou en dessous en tapant 
 `Ctrl+Page Haut` or `Ctrl+Page Bas`. 

[En savoir plus sur les calques dans le tutoriel de Roy Torley.](https://roy-torley.github.io/Inkscape_Tutorial/Tutorial06/Tutorial06.html)

## Tutoriels généraux sur  Inkscape 
 * [Tutoriel sur les formes sur inkscape.org](https://inkscape.org/doc/tutorials/shapes/tutorial-shapes.html) - Comment dessiner et modifier des objets selon des formes géométriques. 
 * [Tutoriel avancé suroninkscape.org](https://inkscape.org/doc/tutorials/advanced/tutorial-advanced.html) - Dessiner et modifier chemins et textes
 * [Index des guides Inkscape sur tavmjong.free.fr](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/index.html) - Guide en profondeur sur tous les aspects d'Inkscape
 * [Tutoriel inkscape par TJ Free sur Youtube](https://www.youtube.com/playlist?list=PLqazFFzUAPc5lOQwDoZ4Dw2YSXtO7lWNv) -Série de tutoriels video couvrant un large usage 

## Tutoriels sur des outils spécifiques

### Digitaliser une Image
Vous pouvez convertir une image bitmap (telle que JPEG ou PNG) en une image vectorielle en important l'image, puis en utilisant  `Chemin > Vectoriser un objet matriciel...`. C'est un processus fastidieux qui demande généralement beaucoup d'essais et d'erreurs. Cela marche mieux sur des images aux traits prononcés ayant peu de couleur
 * [Tutoriel sur la digitalisation sur inkscape.org](https://inkscape.org/doc/tutorials/tracing/tutorial-tracing.html)
 * [Tutoriel video par TJ Free sur Youtube](https://www.youtube.com/watch?v=E7HwLTQu2FI)


## Pavage

Créer des pavages `Edition > Cloner > Créer un pavage de clones ...`.

Lire plus sur les [pavages sur tavmjong.free.fr](http://tavmjong.free.fr/INKSCAPE/MANUAL_v14/html_fr/Tiles.html). Cliquez sur la `Table des matières`, où vous trouverez des informations détaillées sur toutes les parties de la boîte de dialogue de pavage.

## Outils de modification des chemins

### Outil noeud
  * [Outil noeud (tavmjong.free.fr)](http://tavmjong.free.fr/INKSCAPE/MANUAL_v14/html_fr/Paths-Editing.html)

#### Influencer le style de ligne

##### Ornements avec Spiro

 * [Comment faire des volutes et ornements avec Inkscape - Youtube](https://www.youtube.com/watch?v=YHddGNae3-c)

##### Formes lignes

  * [Ellipse - Youtube](https://www.youtube.com/watch?v=TDI2ViYw4KY)
  * [Personnaliser - Youtube](https://www.youtube.com/watch?v=wiqUrzzHszI)

### Outil Ajuster

  * [Outil Ajuster (tavmjong.free.fr)](http://tavmjong.free.fr/INKSCAPE/MANUAL_v14/html_fr/Tweak.html)

### Outil Pulvériser

  * [Outil pulvériser (tavmjong.free.fr)](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Spray.html)

### Effacer

  * [Gomme (tavmjong.free.fr)](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Eraser.html)

## Effets de chemin en temps réel

* [Effets de chemin en temps réel (tavmjong.free.fr)](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Paths-LivePathEffects.html)
  * [Courber (tavmjong.free.fr)](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Paths-LivePathEffects-BendTool.html)
  * [Déformation par enveloppe (tavmjong.free.fr)](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Paths-LivePathEffects-EnvelopeDeformation.html)<br>
    [Youtube Example](https://www.youtube.com/watch?v=8XbIsw48vTk)
  * [Interpoler les sous-chemins (tavmjong.free.fr)](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Paths-LivePathEffects-InterpolateSubPaths.html)
  * [Motif suivant un chemin (tavmjong.free.fr)](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Paths-LivePathEffects-PatternAlongPath.html)<br>
    [Youtube Example](https://www.youtube.com/watch?v=3Bhg727wYMc)
  * [Croquis (tavmjong.free.fr)](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Paths-LivePathEffects-Sketch.html)
  * [Relier les sous-chemins (tavmjong.free.fr)](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Paths-LivePathEffects-StitchSubPaths.html)
  * [Agitation (Youtube)](https://www.youtube.com/watch?v=130Dbt0juvY)





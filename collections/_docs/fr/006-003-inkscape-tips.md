---
title: "Astuces Inkscape"
permalink: /fr/docs/inkscape-tips/
excerpt: ""
last_modified_at: 2019-10-23
toc: true
---
Beaucoup de ces outils ne créent pas de chemins. Pour les utiliser avec Ink/Stitch, vous devez les convertir en chemin (`Shift + Ctrl + C`) et éventuellement les modifier encore plus.

Inkstitch peut ête utilisé avec Inkscape 0.92 ou Inkscape 1. La plupart des tutoriels listés sur cette page utilisent Inkscape 0.92.

## Inkscape : Tutoriels Basiques

Plusieurs tutoriaux interactifs sont disponibles dans Inkscape lui même en sélectionnant `Aide> Didacticiels` dans le menu dont le tutoriel basique ci-dessous:

 * [Tutoriel basique sur inkscape.org](https://inkscape.org/fr/doc/basic/tutorial-basic.fr.html)
 * [Bases at tavmjong.free.fr](http://tavmjong.free.fr/INKSCAPE/MANUAL_v14/html_fr/Basics.html)
 * [tutoriel sur les formes sur inkscape.org](https://inkscape.org/fr/doc/tutorials/shapes/tutorial-shapes.html)
 * [Chemins sur tavmjong.free.fr](http://tavmjong.free.fr/INKSCAPE/MANUAL_v14/html_fr/Paths-Combining.html)

### Vecteurs

Les éléments de votre fichier Inkscape sont des _images vectorielles_, qui utilisent des fonctions mathématiques pour définir des formes.  Ils utilisent des points appellés  _noeuds_,  et des _segments_  qui connectent les noeuds. Il est possible d'éditer des formes vectorielles en déplaçant des noeuds et en modifiant les angles des segments à l'aide de l'éditeur de noeuds ou en utilisant d'autres outils Inkscape. Quand vous utilisez d'autres outils, comme par exemple en agrandissant une forme avec l'outil de Sélection, de nombreux noeuds sont modifiés derrière la scène par Inkscape.

Une forme vectoriell est _fermée_  quand elle fait un tour complet  (comme un cercle ou un carré) et chaque noeud est connecté à deux autres noeuds. Une forme est _ouverte_ quand elle a deux extrémités libres, (une spirale ou une ligne droitee). La bordure de la forme est appelée le _contour_ et la surface à l'intérieur d'une forme fermée est appellée le  _fond_. 

[Lire plus sur le fonctinonnement des formes vectorielles à Sketchpad.net](http://sketchpad.net/drawing1.htm)


### Dessiner et Sélectionner

Les icônes du côté gauche de votre fenêtre montrent tous les outils pour créer et interagir avec votre dessin. 
Inkscape dispose de plusieurs outils pour créer divers types d'objets, tels que l'outil rectangle (`F4`), l'outil elipse (`F5`), l'outil étoile (`*`), l'outil spirale (`F9`), l'outil crayon (`F6`), et l'outil texte (`F8`).  
La plupart de ces outils s'utilisent en glissant sur le canevas pour placer les coins de votre forme. Chaque outil de dessin a ses propres options (montrées dans la barre d'outils Contrôles au dessus du canevas) que vous pouvez utiliser pour obtenir différnts résultats. En savoir plus sur la création de  [Formes](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Shapes.html), [Cheminss](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Paths.html), ou [Texte](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Text.html).

La première icône en haut du panneau Outils est l'outil de Sélection. que vous pouvez aussi activer en tappant `F1`. 
Cliquez sur un objet avec l'outil de sélection pour le déplacer sur le canevs et pour faire apparaître des poignées qui permettent de le transformer. Cliquer une fois sur un objet fait apparaître les poignées de redimensionnement, cliquer une deuxième fois les remplace par des poignées de rotation. Garder la touche Majuscule enfoncée pour sélectionner plusieurs objets en même temps. Vous pouvez aussi sélectionner plusieurs objets simultanément en glissant l'outil autour d'eux. [En savoir plus sur les transformations d'objets.](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Transforms.html)

Les objets peuvent aussi être sélectionnés en ouvrant le panneau Objets (`Objet > Objets...` dans le menu) et en cliquant sur un des noms de la liste. Vous pouvez selectionner des objets de cette manière quelque soit l'outil actif.

Pour utiliser une commande de menu sur un objet (par exemple pour le convertir en chemin) vous devez préalablement le sélectionner.


### Objets et Chemins
Un _objet_  est un élément de votre fichier qui peut être manipulé individuellement. Vous pouvez voir la liste de tous les objets de votre fichiers en exécutant `Objet > Objets...`  dans le menu. Savoir comment vos objets sont définis est très important pour vos fihiers de broderie, c'est donc une bonne idée de garder ce panneau ouvert quand vous travaillez avec Ink/Stitch.

Il y a de nombreux types d'objets dans Inkscape, tels que chemins, rectanbles, cercles, polygones, spirales et textes. Des outils différents créent des objets de type différents, chaque type ayant ses propres règles d'usage.

Un _chemin_ est la représentation la plus basique d'une forme vectorielle : il s'agit juste d'une série de noeuds et de segments qui décrivent une forme. Une fois un chemin créé, seuls les outils de base permettent de l'éditer, et ces outils fonctionnent de la même manière quelque soit l'apparance du chemin.  D'autres objets mémorisent l'informtion sur leur forme de manière plus spécifique ce qui permet de les modifier facilement. Par eemple, après avoir dessiné un polygone avec l'outil étoile, vous pouvez utiliser les contrôles de l'outil pour changer rapidement le nombre de sommets de la forme. Si vous aviez dessiné la même forme comme un chemin, vous devriiez déplacer chaque sommet manuellement pour en ajouter d'autres. Toutefois, vous pouvez modifier un chemin pour obtenir n'importe quelle forme, tandis que les autres types d'objets ont des contraintes sur leur forme.

Le chemin est le type d'objet le plus important pour Ink/Stitch. Votre dessin  **doit être sous forme de chemin** pour qu'Ink/Stitch puisse l'utiliser.

Tout objet peut être converti en chemin en le selection (soit en cliquant avec l'outil Sélection, soit en cliquant son nom dans le panneau Objets) puis en tappant `Shift + Ctrl + C` ou en exécutant  `Chemin > Objet en Chemin` dans le menu.  Une fois l'objet converti en chemin, vous pouvez utiliser l'outils Noeuds pour faire des changements précis sur les noeuds et les segments.

Attention, lorsque vous convertissez des objets en chemins, car on ne peut pas inverserment reconvertir ces chemins en objets. Pour cette raison, vous pouvez préferrer dupliquer d'abord votre objet avant de convertir la copie en chemin, tout en gardant la forme originale pour le cas où vous souhaiteriez l'éditer ultérIeurement.


Ces objets particuliers sont adaptés pour:
 * du texte ou des formes géométriques simples
 * modifier la géométrie d'une forme en son entier
 * comme point de départ d'un nouveau dessin

Les chemins sont adaptés pour:
 * Faire des changements précis sur une petite section d'une forme
 * Dessiner des formes à main levée
 * Préparer votre dessin terminé pour la broderie
 
Vous pouvez verifier le type d'un objet dans la description qui apparait dans la barre de statut en bas de l'écran lorsque l'objet est selectionné. Notez que vous ne _pouvez pas_ dire si un objet est un chemin rien qu'en regardant son nom dans le panneau Objets car Inkscape donne des noms commee "path1234" à des cercles ou des spirales aussi bien qu'à de véritables chemins.

### Fond et Contour
Faites apparaître le panneau "Fond et Contour" en tappant `Shift+Ctrl+F` ou en sélectionnant `Objet > Fond et COBTOUR...`  à partir du menu pour contrôler la couleur et le style du fond et du contour du chemin.
La couleur exacte et le style de votre chemin n'ont globalement rien à voir avec votre fichier de broderie, mais vous devez savoir comment les éditer car Ink/Stitch utilise le style du contour pour décider du type de point de broderie à utiliser, et insérre ou non des changements de fils selon si les chemins sont ou non de la même couleur.

Ce panneau est assez simple. Pour des chemins qu'Ik/Stitch transformera en point de remplissage, l'onglet Fond doit choisir Aplat (le deuxième choix), et l'onglet Cntour doit avoir la croix X sélectionnée (premier choix). Pour tous les autres points, sélectionnez le X dans l'onglet Fond et Aplat dans l'onglet COntour. Utilisez l'onglet "Style de contour" pour choisir soit une ligne pleine soit un pointillé selon le style de point désiré.

Les couleurs peuvent aussi être choisies en utilisant la palette en bas de l'ecra, : cliquez sur une couleur pour l'utiliser comme une couleur de font, et faites un clic majuscue pour l'utiliser pour le contour.


### Travailler avec des chemins
Use the second tool from the top, the Node Tool (also activated with `F2`), to directly edit the points and lines in a path. Select a path with the Node Tool to display markers on all of its nodes. These node markers can then be dragged around with the cursor, added, removed, and more. You will also see handles coming off each node, which you can drag to adjust the angles of the line segments. This tool only works on _path_ objects, explained below--if you do not see gray points appear along the object after you select it, then it is not a path. [Learn more about the Node Tool here.](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Paths-Editing.html)

Two important commands when preparing paths for Ink/Stitch are Combine (`Ctrl+K` or `Path > Combine`) and Break Apart (`Shift+Ctrl+K` or `Path > Break Apart`). For example, creating satin columns in Ink/Stitch requires two lines that are combined into one path. These commands don't make any changes to the actual shape or to the nodes within a path; instead, they alter the way that Inkscape classifies it. 

The _Combine_ command takes all the paths currently selected and merges them into a single path object. Inkscape will now treat those paths as one unit for selecting and transforming. You can see in the Objects panel that the list contains fewer objects after a Combine. The result of combining is a _compound path_, which contains more than one line.

The _Break Apart_ command takes a compound path and isolates each continuous line into a separate object. It splits up the compound path into as many separate paths as possible without deleting any segments. After using Break Apart, the Objects list will be longer. 

There are other commands for combining or dividing the actual nodes in a path, in a way that changes the shape itself instead of just the way Inkscape manages it. [Read about path operations here.](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Paths-Combining.html)

### Layering
All objects in Inkscape are stacked on top of each other in a specific order. Ink/Stitch will use this order to determine what should be stitched first. You can view the order in the Objects panel (`Object > Objects...` in the menu). Ink/Stitch makes the path at the bottom of the list into the first instruction, and proceeds upward through the list. You can change the order by dragging around the names inside the Objects panel, or pressing `Page Up` and `Page Down`.  

You can double click an object name to rename it, which may help you keep track of your layering. You will also see three icons to the left of each object name in this panel. Click the eye icon to hide something from view, and click the lock icon to prevent it from being edited. 

_Groups_ and _layers_ can make it easier to manage your objects and their order. Once a group is formed, clicking one item in the group selects the entire group, allowing you to alter all elements of the group at once. To group objects together, select all of them with `Shift+click`, then press `Ctrl+G` or click `Object > Group` in the menu. The group also appears as a collapsible item in the Objects list, and objects can be moved in and out of the group (or from one group to another) by dragging them around the Objects panel. A group can contain other groups. However the safest way seems to be to `Edit > Cut` an object out of one group and then `Edit > Paste` it into another. You have to select an object in the destination group so that the pasted object goes into that group.

Layers function similarly to groups, but their main purpose is to more easily control how your objects are ordered. A new layer is created with the + button below the Objects list, or by pressing `Shift+Ctrl+N`. Objects can be moved from one layer to another by dragging in the Objects list, just like groups, but they can also be quickly moved to the layer above or below by pressing `Ctrl+Page Up` or `Ctrl+Page Down`. 

[Read more about layers in Roy Torley's tutorial here.](https://roy-torley.github.io/Inkscape_Tutorial/Tutorial06/Tutorial06.html)

## General Inkscape Tutorials
 * [Shapes Tutorial on inkscape.org](https://inkscape.org/doc/tutorials/shapes/tutorial-shapes.html) - How to draw and modify geometric shape objects
 * [Advanced Tutorial on inkscape.org](https://inkscape.org/doc/tutorials/advanced/tutorial-advanced.html) - Drawing and editing paths and text
 * [Inkscape Guide Index on tavmjong.free.fr](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/index.html) - In-depth guide to all aspects of Inkscape
 * [Inkscape Tutorial by TJ Free on Youtube](https://www.youtube.com/playlist?list=PLqazFFzUAPc5lOQwDoZ4Dw2YSXtO7lWNv) - Video tutorial series covering a wide range of uses

## Specific Tool Tutorials

### Tracing an Image
You can convert a raster image (such as a JPEG or PNG) into a path by importing/pasting an image, then using `Path > Trace Bitmap...`. This is a finicky process that usually requires a lot of trial and error. It works best on images with hard edges and few colors.
 * [Tracing Tutorial on inkscape.org](https://inkscape.org/doc/tutorials/tracing/tutorial-tracing.html)
 * [Video tutorial by TJ Free on Youtube](https://www.youtube.com/watch?v=E7HwLTQu2FI)


## Pavage

Créer des pavages `Edition > Cloner > Créer un pavage de clones ...`.

Lire plus sur les [pavages sur tavmjong.free.fr](http://tavmjong.free.fr/INKSCAPE/MANUAL_v14/html_fr/Tiles.html). Cliquez sur la `Table des matères`, où vous trouverez des informations détaillées sur toutes les parties de la boîte de dialogue de pavage.

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

  * [Spray Tool (tavmjong.free.fr)](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Spray.html)

### Effacer

  * [Eraser (tavmjong.free.fr)](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Eraser.html)

## Effets de chemin en temps réel

* [Effets de chemin en temps réel (tavmjong.free.fr)](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Paths-LivePathEffects.html)
  * [Bend Tool (tavmjong.free.fr)](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Paths-LivePathEffects-BendTool.html)
  * [Envelope Deformation (tavmjong.free.fr)](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Paths-LivePathEffects-EnvelopeDeformation.html)<br>
    [Youtube Example](https://www.youtube.com/watch?v=8XbIsw48vTk)
  * [Interpolate Sub Paths (tavmjong.free.fr)](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Paths-LivePathEffects-InterpolateSubPaths.html)
  * [PatternAlongPath (tavmjong.free.fr)](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Paths-LivePathEffects-PatternAlongPath.html)<br>
    [Youtube Example](https://www.youtube.com/watch?v=3Bhg727wYMc)
  * [Sketch (tavmjong.free.fr)](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Paths-LivePathEffects-Sketch.html)
  * [StitchSubPaths (tavmjong.free.fr)](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Paths-LivePathEffects-StitchSubPaths.html)
  * [Roughen (Youtube)](https://www.youtube.com/watch?v=130Dbt0juvY)





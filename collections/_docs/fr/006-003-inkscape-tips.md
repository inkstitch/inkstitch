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

Une forme vectoriell est _fermée_  quand elle fait un tour complet  (comme un cercle ou un carré) et chaque noeud est connecté à deux autres noeuds. Une forme est _ouverte_ quand elle a deux extrémités libres, (comme (une spirale ou une ligne droitee). La bordure de la forme est appelée le _trait_ et la surface à l'intérieur d'une forme fermée est appellée le  _remplissage_. 

[Lire plus sur le fonctinonnement des formes vectorielles à Sketchpad.net](http://sketchpad.net/drawing1.htm)


### Dessiner et Sélectionner

Les icônes du côté gauhe de votre fenêtre montrent tous les outils pour créer et interragir avec votre dessin. 
Inkscape dispose de plusieurs outils pour créer divers types d'objets, tels que l'outil rectangle (`F4`), l'outil elipse (`F5`), l'outil étoile (`*`), l'outil spirale (`F9`), l'outil crayon (`F6`), et l'outil texte (`F8`).  
Most of them are used by dragging across the canvas where you want to place the corners of your shape. Each drawing tool has unique options (shown in the Tool Controls bar above the canvas) that you can play around with to get different results. Learn more about creating [Shapes](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Shapes.html), [Paths](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Paths.html), or [Text](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Text.html) at these links.

The top icon in the Toolbox panel is the Select Tool, which you can also activate by pressing `F1`. Click an object with the Select tool to drag it around the canvas and to display handles for transforming it. Clicking the object once shows handles for resizing it, and clicking it a second time switches to handles for rotating it. Hold down `Shift` to select multiple objects at once. You can also select many objects at once by dragging around them. [Learn more about transforming objects here.](http://tavmjong.free.fr/INKSCAPE/MANUAL/html/Transforms.html)

Another way to select objects is to open the Objects panel (`Object > Objects...` in the menu) and click on a name in the list. You can select objects this way no matter what tool is active.

In order to use a menu command on an object (e.g. to convert it to a path), you must select the object first.

### Objects and Paths
An _object_ is any piece of your file that you can manipulate individually. You can see a list of all the objects in your file by selecting `Object > Objects...` in the menu. Knowing how your objects are defined is very important to your embroidery files, so it's a good idea to keep this window open when working with Ink/Stitch.

There are many types of objects in Inkscape, such as paths, rectangles, circles, polygons, spirals, and, text. Different tools create different types of objects, which each have different rules about how to work with them. 

A _path_ is the most basic representation of a vector shape: it is just a series of nodes and segments that describes the shape. Once a path has been made, you can only use basic tools to edit it, and it works the same way no matter what the path looks like. Other object types store the information about the shape in more specific way that allows you to change it easily. For example, after drawing a polygon object with the Star Tool, you can use the tool controls to quickly change the number of corners on the shape. If you drew the same shape as a path instead, you would need to manually move each point in order to add more corners. However, paths can be altered into any shape you like, whereas other types of objects have constraints on their shape.

Paths are the most important type of object for Ink/Stitch. Your design **must be formatted as a path** for Ink/Stitch to work on it.

You can convert any object to a path by selecting that object (either by clicking on it with the Select Tool or clicking its name in the Objects panel) and then pressing `Shift + Ctrl + C` or selecting `Path > Object to Path` in the menu. Once it becomes a path, you can use the Node Tool to make precise changes to the points and curves. 

Be careful when you convert objects to paths, because there is no way to convert paths back to objects. For this reason, you may want to duplicate your object first and convert the copy into a path, saving the original shape in case you decide that you want to edit it later.

Special objects are good for:
 * Text or simple geometric shapes
 * Changing the geometry of a whole shape
 * Starting point for a new design

Paths are good for:
 * Making precise changes to a small section of a shape
 * Drawing unique freehand shapes
 * Preparing your finished design for embroidery

You can check an object's type in the description that appears in the status bar at the bottom of the screen when it's selected. Note that you _cannot_ tell whether something is a path by looking at its name in the Objects panel, because Inkscape gives names like "path1234" to circles and spirals as well as to actual paths.

### Stroke and Fill
Bring up the Fill and Stroke panel by pressing `Shift+Ctrl+F` or selecting `Object > Fill and Stroke...` from the menu to control the color and style of a path's fill and stroke. The exact color and style of your path are mostly irrelevant to the embroidery file, but you do need to know how to edit them because Ink/Stitch uses stroke style to determine what kind of stitch to use and inserts thread change prompts based on whether paths are the same color.

This panel is rather straightforward. For paths that Ink/Stitch will make into fill stitch areas, the Fill tab should be set to "flat color" (second square) and the Stroke Paint tab should have the X selected (first square). For all other kinds of stitch, select the X on the Fill tab and select "flat color" on the Stroke Paint tab. Use the Stroke Style tab to choose a solid or dashed stroke, depending on what kind of stitch you want. 

Color can also be set using the palette at the bottom of the screen; click a color to use it for the fill or shift click to use it for the stroke.

### Working with Paths
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





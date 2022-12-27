---
title: "Outils: Trait"
permalink: /fr/docs/stroke-tools/
excerpt: ""
last_modified_at: 2022-05-23
toc: true
---
## Agencement automatique de points droits

Cet  outil **remplace** un ensemble de chemins paramétrés en points droits par un nouvel ensemble de chemins paramétrés en points droits  empilés dans un ordre logique de broderie qui évite autant que faire se peut les sauts de fil. Lorsque nécessaire des chemins (chemins de dessous) sont ajoutés, sous les chemins existants pour assurer les connexions . Les points droits résultants conservent tous les  paramètres des points droits originaux tels que la longueur de point droit, le  nombre de répétitions, le nombre de répétitions pour le point triple.  Les chemins de dessous ne conservent que la longueur du point, le nombre de répétitions est remis à un et et le nombre de répétitions de point triple à zéro.

Cette extension cherche à minimiser la longueur des sauts de fil inévitables.

### Usage
- Sélectionnez tous les chemins paramétrés en points droits que vous souhaitez organiser
- Excutez `Extensions > Ink/Stitch > Outils : Trait > Agencement automatique  de points droits`
- Choisir les options désirées et cliquer sur "Appliquer et quitter"
  
Par défaut, l'extension choisira de commencer par le noeud le plus à gauche et de terminer par le noeud le plus à droite même si ces noeuds ne sont pas des noeuds terminaux. Vous pouvez attacher les commandes " Début/Fin d'agencement automatique de point droit" pour forcer les positions de début et de fin.

### Options

- Cocher **Ajouter des noeuds aux intersections** donnera un meilleur résultat de routage, avec des chemins de dessous qui auront leurs extrémités aux intersections ou aux noeuds terminaux. Ne décocher cette option que si vous avez manuellement ajouté des noeuds là où vous souhaitez les coupures de chemin.
- Cocher **Préserver l'ordre des points droits** si vous souhaitez préserver l'ordre initial des chemins paramétrés en points droits.
- Cocher **Couper les sauts de fil**  pour  utiliser des commandes de coupe plutôt que des sauts de fil. Les commandes de coupe sont ajoutées au svg, vous pouvez donc ensuite les modifier/supprimer à votre guise.

## Convert Satin to Stroke

Satin to stroke will convert a satin column to it's centerline. This can be useful, when you decide later in the designing process to turn a satin column into a running stitch. You can also use it to alter the thickness of your satin column, when pull compensation isn't satisfying. In that case use this function to convert your satin column into a running stitch, set stroke width in the fill and stroke panel and run the ["Connvert line to to satin"](#convert-line-to-satin) function. 

This works best on evenly spaced satin columns.

![Satin to Stroke example](/assets/images/docs/en/satin_to_stroke.png)

### Usage

1. Select the satin column(s) you want to convert into a running stitch
2. Run `Extensions > Ink/Stitch > Satin Tools > Convert satin to stroke...`
3. Choose wether you want to keep selected satin column(s) or if you want to replace them
4. Click apply


## Fill to Stroke

{% include upcoming_release.html %}

Fill outlines never look nice when embroidered - but it is a lot of work to convert a fill outline to a satin column or a running stitch. This tool helps you with this operation.

It is comparable to the Inkscape functionality of `Path > Trace bitmap > Centerline tracing` (- and has similar issues.) But instead of converting raster graphics, it will find the centerline of vector based objects with a fill.

You can refine the result by defining cut lines.

### Usage

*  (Optional) Draw cut lines at the intersections/joints. They are simple stroke objects. This is especially useful, when you aim for satin columns. Please note, that each stroke element has to cut the fill element in which that each side of the fill is entirely disconnected.
* Select one or more fill objects which you want to convert to a centerline along with the cut lines if you have defined them ealier.</label>
* Run `Extensions > Ink/Stitch > Tools: Stroke > Fill to Stroke`
* Set options and apply
* Use the node tool to perform corrections if necessary

### Options

* Keep original: enable this option, if you want to keep the original object(s). Otherwise it will be removed.
* Threshold for dead ends (px): This will remove small lines. In most cases the best value is the approximate line width of the original shape in pixels.
* Dashed line: Set to true if you aim for a running stitch outline.
* Line width (px): If you want to convert this directly into a satin column, set this to the satin column width. In most cases you would want to keep this value low, so it will be easier to check and correct the outlines before the conversion.

## Jump to Stroke

{% include upcoming_release.html %}

This will create a running stitch from the end position of the first element to the start position of the second element. Place this running stitch under following top stitches and avoid jump stitches.

### Usage

* Select two or more objects
* Run `Extensions > Ink/Stitch > Tools: Stroke > Jump Stitch to Stroke`

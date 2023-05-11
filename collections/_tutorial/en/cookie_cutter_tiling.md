---
permalink: /tutorials/cookie_cutter_tiling/
title: "Cookie Cutter Tiling"
language: en
last_modified_at: 2023-05-07
excerpt: "Using Tiling LPE, clipping path and autorouting to achieve Pattern Fill"
image: "/assets/images/tutorials/tutorial-preview-images/cookie_cutter_tiling.jpg"
tutorial-type:
stitch-type:
  - "Running Stitch"
  - "Bean Stitch"
  - "Circular Fill"
techniques:
field-of-use:
tool:
  - "Stroke"
  - "Fill"
  
user-level:
toc:
  true
---

{% include upcoming_release.html %}

![Brodé](/assets/images/tutorials/tutorial-preview-images/cookie_cutter_tiling.jpg)
This tutorial explains how to fill a shape with pattern repetitions using the Tiling Live Path Effect , Clipping and Autorouting.

##  Tiling
Tiling Live Path Effect repeats a tile (a path or a group of paths) in rows and colomns, with many options to modify spacing, create offset, rotate, and add all kind of mirroring effects.

Tilings are really interesting for embroidery purpose, be it to create patterned fills or to loosely fill with repetitions of patterns.

Here are some  samples
 ![tiles](/assets/images/tutorials/cookie_cutter_tiling/all_png.png) 
 
You may recognize them in the clothline embroidery:
* T-shirt : first row, middle tiling
* Dress top: last row, last tiling
* Dress Bottom last row,  second last tiling
* Swiming Suit, middle row, last tiling

The Belt fill is a circular fill, with bean stitch repeat 0 2, that is alternating simple and quituple stitches.

[Download tilings file](/assets/images/tutorials/cookie_cutter_tiling/tiles_idea.svg){: download="tiles_idea.svg" }

All designs in this file are created  applying Tiling LPE to a group, it makes it much easier to use than trying to apply the LPE individually on each path of a tile.

They are easy to modify:  you may modify a path in the group or add a path and see immediatly the result on the canvas. From the LPE dialog you may change the number of 
rows and columns, again seeing immediatly the result. 

You may use these tilings or create your tilings, it is really fun and easy to do.

To create the clothline design, besides tilings, we need cloth shapes.

## Cloths Preparation

Instead of drawing cloths why not download them? 

I used three svgs created by 
Bernd Lakenbrink of  the [Noun Project](https://thenounproject.com/browse/collection-icon/clothes-icon-set-158916/?p=1).

However, we need to modify these svgs to serve our purpose. 

Let's adapt the   [T Shirt](https://thenounproject.com/browse/icons/term/womans-shirt/).

This kind of svg is perfect for screen, or for cutting machine, but must be  modified for embroidery, as what appears like a stroke is actually a fill. Using
`Extensions > Ink/Stitch > Tools: Fill> Fill to Stroke`, this is easily solved.

The four images below are from left to right:
* screen look
* what it looks like if  we remove the fill and add a stroke
* what `Fill to Stroke` returns
* what we really need : a closed shape (orange fill)   and two additional details (red  paths)

![T-Shirt](/assets/images/tutorials/cookie_cutter_tiling/Tshirt.png) 

So  after   [downloading ](https://thenounproject.com/browse/icons/term/womans-shirt/) the T-Shirt
* Select all T-Shirt  paths 
* `Extensions > Ink/Stitch > Tools: Fill> Fill to Stroke`
* This create a "Centerline" group: in there, pick up  paths and construct the shape (outline) of the T Shirt (joining nodes or breaking paths). Keep some additional
details if you wish.

The cloth_line.svg file contains all prepared cloths in the "Cloths Preparation" layer and the same tilings again in the "Tilings" layer. 

It also contains what you should obtain  at all  steps of the process, up to the final embroidery.

![cloth_line](/assets/images/tutorials/cookie_cutter_tiling/cloth_line.svg) 

[download cloth_line.svg](/assets/images/tutorials/cookie_cutter_tiling/cloth_line.svg){: download="cloth_line.svg" }




## Covering each shape with a tiling

Next step is simply chose a tiling per shape to cover.

Working on the canvas, you may rotate or resize the tiling, from the LPE dialog you may change the number of rows and columns. 

Do your best to entirely cover each shape to be filled, without having too many unuseful repetitions of patterns.

This is what was chosen (this is layer "Clothline preparing pattern fill" in the cloth_line.svg file )

![cloth_line](/assets/images/tutorials/cookie_cutter_tiling/tiled_cloths.png) 

## Pattern filling
This is our goal
![final](/assets/images/tutorials/cookie_cutter_tiling/clothline_final.png) 

This is easy to achieve: just follow the following steps, respecting the ordering of the steps.

For each future pattern filled shape we have a group containing :
 * shape: a close path that outlines the T-shirt
 * Details: a group containing stuff to be embroidered over the filled shape. We want to embroider that after patterned fill is stitched.
 * Tiling: the tiling group that contains all the paths of the tiling
 
 ###  Tiling LPE overview
 Let's have a look at the Tiling LPE  applied on the Tiling group of the T Shirt


![starting_point](/assets/images/tutorials/cookie_cutter_tiling/T-shirt-1.jpg)
The eye in the red rectangle hides/shows the LPE.

Later on you will need to flatten the effect, see the menu to the right of the eye.

In another red rectangle is the ![symbole](/assets/images/tutorials/cookie_cutter_tiling/tiling_moulin.jpg) symbol that dictates the mirrors effect of the tiling.

For a better  understanding, let's turn  the tiling  back  to horizontal and set it to two rows and two columns:
![starting_point](/assets/images/tutorials/cookie_cutter_tiling/tiling_moulin2x2.jpg)

The pink shape of the symbol is the tile and the three other shapes shows the mirroring effects applied to rows and columns.

Click on another symbol and you will get another tiling. Try and  chose your favorite.

![mirroring](/assets/images/tutorials/cookie_cutter_tiling/mirroring.jpg)

Once you are happy with your modification flatten the LPE using the menu at top right of the LPE dialog.

After that, path8 is no more a triangle, but a composite path containing plenty of copies of the triangle.

Once the LPE is flatten, you can't use the LPE dialog anymore.

In node edition mode, this is what you get when selectiong  all path8 nodes :

![flattened](/assets/images/tutorials/cookie_cutter_tiling/flatened.jpg)

Breaking  apart this path would create  plenty of triangles. Don't.

### Combine  paths in Tiling groups  and flatten  effect 
For each Tiling:
* If there are more than a single path in a Tiling group, combine all paths together.
* Flatten the Effet

If you look at the canvas, nothing is different.

### Duplicate shape, and use it to Clip Tiling
For each Tiling:
* Duplicate shape
* Select the single path in the Tiling group and a  copy  of shape (this copy must be above the Tiling  group in the Layers and Objects pannel
* `Object  > Clip > Set Clip` 

You should get :
![clipepd](/assets/images/tutorials/cookie_cutter_tiling/after_clip.jpg)

### Prepare for Embroidery Parameters
For each Tiling:
* Set the remaining shape path to stroke only. 
* Make sure that Tiling path and shape color is identical
* Choose if you also want the Details to be same color (i did, to have less color changes)

![strole_shape](/assets/images/tutorials/cookie_cutter_tiling/stroke_shape.jpg)

### Chose Embroidery Parameters
* Select shape ,Tiling and  Details 
* Run `Extensions > Ink/Stitch > Params `

For nice triple stitches: 
  *  Choose  Runninng Stitch/ Bean Stitch as Method
  *  Set Running Stitch Length to 2 mm
  *  Set Bean Stitch Number of Eepeats to 1

One Cloth at a time :
  *  Select the whole group
  *  Run `Extensions > Ink/Stitch > Visualise and Export > Stitch Plan Preview`


You should get :
![Before_Autoroute](/assets/images/tutorials/cookie_cutter_tiling/before_autoroute.jpg)

If render jumps is checked, you see that some path  ordering is required, this is next step.
However, you may disable it and check that the embroidery seems fine.

### Autoroute

For each Tiling:
  * Select the path in the Tiling group
  * Select the shape
  *  Run `Extensions > Ink/Stitch > Tools : Stroke> Autoroute Running Stitch`

One Cloth at a time :
  *  Select the whole group
  *  Run `Extensions > Ink/Stitch > Visualise and Export > Stitch Plan Preview`


and  you will see that the jumps stitches are almost all gone. 

If you look at the results in the Auto-Route groups you may notice some unuseful very short paths . You  could get  rid of them,  but the easy way is
* `Extensions > Ink/Stitch > Preference`
*  Set  *minimum stitch length* to at least 0.5 mm locally only 

### Final steps

* remove all empty groups

If Details have a different color, the only jumps left are inside the Details group. Otherwise, there is also a jump from the last path of Autoroute to the first detail.
You may either : 
  - Left the jumps as they are, and either  your embroidery machine will turn them into trims,  or you will have to trim  later.
  - Add a trim command 
  - Or convert jumps to paths 
  
  You may use `Extensions > Ink/Stitch > Tools : Stroke >  Jump Stitch to Stroke` to help you : if you chose two consecutive paths with a jump in between and run this extension, it will create a straight  path from 
the end of the first  path to the begining of the second. No need to guess where the fill is ending.... But it is up to you to camouflage it (see example in the T Shirt shape)
 




<!--

### Swimming Suit
Same  process, but because the tile contains 3 open paths, intersecting is a little surprising.

Follow the same first steps as for the T Shirt and let's try to intersect tiling and shape.


#### First trial
Follow the same road as for the T shirt, that is flatten the LPE and then intersect the paths of the tiling group with the swimming suit shape.

![intersection_1](/assets/images/tutorials/cookie_cutter_tiling/ss_intersection_1.jpg )

The result is quite logical, after flattening the effect, the group contains 3 paths, so we are in fact intersecting 4 paths.

Not ugly but not so good for embroidery, that would yield too many jumps.


#### Second trial
In oder to intersect only two paths,let's combine the three paths of the tiling  before flattening. Then intersect the single resulting path with
the swiming suit shape.

![intersection_2](/assets/images/tutorials/cookie_cutter_tiling/ss_intersection_2.jpg)

Still not exactly what was planned, but i liked the result, so i kept it for the final embroidery.

Why is the result not a subpart of the tiling ? this is because  if we do have a single  path in the  tiling,  it is not  a closed  paths combination.
Intersection, considers what's *inside* both intersecting shape, and is intended to intersect fills rather than strokes.

In that   case,  the way to go is to use 'Path >  Cut  Path', but because it is more tedious to  use, before that, let's  try another easy path operation
`Path  >  Division`


Intersection is a symmetric  operation, Division and Cut Path are not, and the order in the object  stack of the layer  and object pannel matters.
* Have a copy of the swimming suit shape bellow the tiling group in the Layers and Object pannel
* Select the tiling path and the bellow  copy of the swimming suit
* `Path > Division`


![idivision](/assets/images/tutorials/cookie_cutter_tiling/division.jpg)

Not bad, but still some jumps to expect...

Both intersection and  division  are easy to use as they get rid of everything outside the shape to be  filled.

But if the tiling  is not a combination of closed path, the result is  probably not  what you wish.



### 'Path Cut' to the rescue

Again you need to combine and flatten the effect to get a single path.

This time have a copy of the swimming suit shape above the tiling path.

* Select the tiling path and the copy of the swimming suit above it
* `Path > Cut Path`


Imagine that you are using a swiming suit shaped cookie cutter, and cut a single cookie from the tiling path. The path get broken in plenty of pieces
but nothing is gone.

This is the real disadvantage of Cut Path, you need to tidy and get rid of all that is outside the shape and it is somewhat tedious.

![cut_path](/assets/images/tutorials/cookie_cutter_tiling/cut_path.jpg)

My favorite way to tidy up is
* Lock whatever you are sure you want to keep (in that case the leftover swimsuit shape and the decolleté detail)
* Holding down ALT and MAJ keys, with your mouse, draw a path that intersects as many superfluous paths as you safely may (meaning don't touch what you want to keep). 
You will see a red path on the screen, and this will select all the intersected paths. Delete them.
* Repeat  or use any other selecting process to finish the process.



![cut_path](/assets/images/tutorials/cookie_cutter_tiling/ss.jpg)

After that, same steps as for the T Shirt.
-->








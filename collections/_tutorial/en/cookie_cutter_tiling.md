---
permalink: /tutorials/cookie_cutter_tiling/
title: "Cookie Cutter Tiling"
language: en
last_modified_at: 2023-05-07
excerpt: "Tiling"
image: "/assets/images/tutorials/tutorial-preview-images/cloth_line.jpg"
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

![Brodé](/assets/images/tutorials/tutorial-preview-images/cloth_line.jpg)
This tutorial explains how to fill a shape with pattern repetitions using the Tiling Live Path Effect.

## Tiling
Tiling Live Path Effect repeats a tile (a path or a group of paths) in rows and colomns, with many options to modify spacing, create offset, rotate, and add all kind of mirroring effects.

Tilings are really interesting for embroidery purpose, be it to create patterned fills or to loosely fill with repetitions of patterns.

Here are some  samples
 ![tiles](/assets/images/tutorials/cookie_cutter_tiling/all_png.png) 
 
You may (or not) be able to recognize them in the clothline embroidery:
* T-shirt : first row, middle tiling
* Dress top: last row, last tiling
* Dress Bottom last row,  second last tiling
* Swiming Suit, middle row, last tiling

The Belt fill is a circular fill, with bean stitch repeat 0 1, that is alternating simple and triple stitches.

[Download tilings file](/assets/images/tutorials/cookie_cutter_tiling/tiles_ideas.svg) 

All designs in this file are created  applying Tiling LPE to a group, it makes it much easier to use than trying to apply the LPE individually on each path of a tile.

They are easy to modify:  you may modify a path in the group or add a path and see immediatly the result on the canvas. From the LPE dialog you may change the number of 
rows and columns, again seeing immediatly the result. 

You may use these tilings or create your tilings, it is really fun and easy to do.

To create the clothline design, besides tilings, we need cloth shapes.

## Cloths preparation

Instead of drawing cloths why not download them? 

I used three svgs created by 
Bernd Lakenbrink of [Noun Project](https://thenounproject.com/browse/collection-icon/clothes-icon-set-158916/?p=1).

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
* This create a "Centerline" group. In there, pick up  paths and construct the outline of the T Shirt (joining nodes or breaking paths). Keep some additional
details if you wish.

The cloth_line.svg file contains all prepared cloths in the "Clothes" layer and the same tilings again in the "Tilings" layer. 

It also contains what you should obtain  at all  steps of the process, up to the final embroidery.

![cloth_line](/assets/images/tutorials/cookie_cutter_tiling/cloth_line.svg) 

[download cloth_line.svg](/assets/images/tutorials/cookie_cutter_tiling/cloth_line.svg)


## Covering each shape with a tiling

Next step is simply chose a tiling per shape to cover.

Working on the canvas, you may rotate or resize the tiling, from the LPE dialog you may change the number of rows and columns. 

Do your best to entirely cover each shape to be filled, without having too many unuseful repetitions of patterns.

This is what was chosen (this is layer "Clothline preparing pattern fill" in the cloth_line.svg file )

![cloth_line](/assets/images/tutorials/cookie_cutter_tiling/tiled_cloths.png) 

## Pattern filling
This is our goal
![final](/assets/images/tutorials/cookie_cutter_tiling/clothline_final.png) 

Some tilings make the job easy, other implies more work. Let's start with an  easy one.

### T -Shirt 

We start with:
 * shape: a close path that outlines the T-shirt
 * details: a group containing stuff to be embroidered over the filled T-Shirt
 * Moulins: the tiling group that contains a single path (path8, a small triangle) 
 
 
 Let's have a look at the Tiling LPE  applied on Moulins group;


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

* Duplicate shape, the T-shirt outline
* Select path8  and a single copy  of shape
* `Path > Intersection `

and  you get
![flattened](/assets/images/tutorials/cookie_cutter_tiling/after_intersection.jpg)

The reason this tiling is easy to use, is that the group contains a single closed path. In that case intersection does the  intersecting work quick and well.

* Select the result of the intersection and the remaining shape copy
*  Remove fill if any, add stroke if necessary
* `Extensions > Ink/Stitch > Params `

and chose your embroidery parameters. In the sample, bean stitches were chosen.


With the same two elements selected

* `Extensions > Ink/Stitch > Tools : Stroke > Autoroute Running Stitch`

and let the extension to the ordering job.

If you look at the results in the Auto-Route group you may notice some unuseful very short paths . You  could get  rid of them,  but the easy way is
* `Extensions > Ink/Stitch > Preference`
*  Set  *minimum stitch length* to 1mm locally only 

Now you only need to parameter the T-Shirt details.

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








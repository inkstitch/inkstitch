---
title: Using distort path effects
permalink: /tutorials/distort/
last_modified_at: 2024-05-23
language: en
excerpt: "Using distort paths effects"
image: "/assets/images/galleries/fonts/multiple/multifont3.jpg"

tutorial-type:
  - Sample File
stitch-type: 
  - Running Stitch
  - Fill Stitch
  - Satin Stitch
techniques:
   -Lettering
field-of-use:
user-level: 
---
{% include upcoming_release.html %}

![Distort effect](/assets/images/galleries/fonts/multiple/multifont3.jpg)

Using inkscape live distort paths effects with embroidery is fun. You may try any  of these live path effects: 

* Bend
* Envelope Deformation
* Lattice Deformation
* Perspective/Envelope

To  get the best results :
* simplify the paths as much as possible
* avoid very small shapes

Satin column  are tricky : because there is nothing  in the svg file that distinguish rails from rungs 
in the compound path, inkstitch need to pinpoint the two rails among all the subpaths of a satin column. 

To help  inkstitch chose the same subpaths as rails after  distortion:

- avoid  superposed  rails end points
- rungs should not end  up on the rails,  but cross both rails with flair
- do not  use satin with no rung or with exactly two rungs.


If you follow these rules, there is a good chance that  your satin will still be recognized 
as the same satin after distortion. 

Most Ink/Stitch lettering font do well with gentle distortion. 
However if  the distortotion is too extreme, the result will probably not stitch well.


## Bend Effect
Bend effect is very easy to apply to a lettering :
* Select the lettering group
* Add a  bend path effect to the group
* Click the "edit on canvas" button and  distort the green path that appears

  As it is a live path effect you can change  the green  path again whenever you like 

assets/images/tutorials/


![Bend Example](/assets/images/tutorials/distort/peace_dove.svg)

[Download](/assets/images/tutorials/distort/peace_dove.svg){: download="peace_dove.svg" }




1. Digitize placement and tackdown stitches as different colors, in order to force a stop on your machine.
2. May or may not have to digitize the zig zag tackdown stitch as a different color, depends on the design.
3. Complete the rest of the design as normal.
4. Start sewing like normal, after machine does Placement Stitch, stop machine.
5. Place material over Placement stitch, totally covering the stitch.  Use a light adhesive spray to hold material.
6. Start sewing 1st Tackdown stitch.  Stop Machine after.
7. Completely cut away excess material from the tack down stitch.  Best to use applique scissors if available.
8. Start machine again and let it finish stitching the rest of the design.  Applique portion is finished at this point.

## Applique Color Change (by Evan West)

![Applique Color Change](/assets/images/tutorials/samples/Applique Color Change.svg)

[Download](/assets/images/tutorials/samples/Applique Color Change.svg){: download="Applique-Color-Change.svg" }

## Applique Stop (by Evan West)

![Applique Stop](/assets/images/tutorials/samples/Applique Stop.svg)

[Download](/assets/images/tutorials/samples/Applique Stop.svg){: download="Applique-Stop.svg" }

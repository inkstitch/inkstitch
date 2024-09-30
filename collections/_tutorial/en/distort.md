---
title: Using distort path effects
permalink: /tutorials/distort/
last_modified_at: 2024-05-24
language: en
excerpt: "Using distort paths effects"
image: "/assets/images/galleries/fonts/multiple/multifont3.jpg"

tutorial-type:
  - Sample File
stitch-type: 
  - Satin Stitch
techniques:
   - Lettering
field-of-use:
user-level: 
---
![Distort effect](/assets/images/galleries/fonts/multiple/multifont3.jpg)

Using inkscape live distort paths effects with embroidery is fun. You may try any  of these live path effects: 

* Bend
* Envelope Deformation
* Perspective/Envelope
* Lattice Deformation

To  get the best results :
* simplify the paths as much as possible
* avoid very small shapes

Satin column  are tricky : because there is nothing  in the svg file that distinguish rails from rungs 
in the compound path, Ink/Stitch  needs to pinpoint the two rails among all the subpaths of a satin column. 

To help  Ink/Stitch chose the same subpaths as rails before and after  distortion:

- avoid  superposed  rails end points
- rungs should not end  up on the rails,  but cross both rails with flair
- do not  use satin with no rung or with exactly two rungs.


If you follow these rules, there is a good chance that  your satin will still be recognized 
as the same satin after distortion. 

Most Ink/Stitch lettering fonts do well with gentle distortion. 
However if  the distortotion is too extreme, the result will probably not stitch well.


## Bend Effect
Bend effect is very easy to apply to a lettering :
* Select the lettering group
* Add a  bend path effect to the group
* In the path effects dialog, click the "edit on canvas" button and  distort the green path that appears

  As it is a live path effect you can change  the green  path again whenever you like 

If your text is multiline, you may prefer to apply the effect independantly on each line.

![Lettering Bend Example](/assets/images/tutorials/distort/peace_dove.svg)

[Download](/assets/images/tutorials/distort/peace_dove.svg){: download="peace_dove.svg" }

Of course this is not limited to fonts, you can use this effect to pretend you have a whole school of Mantas even if you draw a single one.

![Mantas Bend Example](/assets/images/tutorials/distort/Mantas.svg)

[Download](/assets/images/tutorials/distort/Mantas.svg){: download="Mantas.svg" }

## Envelope deformation
It works basically the same way, except that this time you have four paths to control the distortion. Edit on canvas any or all of the four paths.

![Manger Enveloppe deformation example](/assets/images/tutorials/distort/manger.svg)

[Download](/assets/images/tutorials/distort/manger.svg){: download="manger.svg" }

Here the enveloppe deformation is used independantly on each  line of text.

## Perspective/Envelope
This path effect  is very  handy  to apply....a perspective effect.

![perspective example](/assets/images/tutorials/distort/perspective.svg)

[Download](/assets/images/tutorials/distort/manger.svg){: download="perspective.svg" }

After adding the effect, activate the node  tool and move the four corners.

You can use it to sort of turn  a font  into its italic version :

![italique](/assets/images/tutorials/distort/italic.png)

## Grid deformation

After  applying the grid deformation effect and activating the node tool, you cann move 25 control nodes  to distort your  embroidery:


![grid](/assets/images/tutorials/distort/grid.png)

Use it to transform  your still  fonts  into dancing ones....

![italique](/assets/images/tutorials/distort/hello.png)




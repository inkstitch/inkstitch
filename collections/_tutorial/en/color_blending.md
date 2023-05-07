---
title: Color Blending
permalink: /tutorials/color-blending/
last_modified_at: 2023-05-05
language: en
excerpt: "Color Blending Methods"
image: "/assets/images/tutorials/tutorial-preview-images/blend.png"

tutorial-type:
  - Sample File
stitch-type: 
  - Fill Stitch
techniques:
field-of-use:
tool:
  -Fill Stitch
user-level:
---

Automatic fills colors don't have to be flat, gradient fills are welcome !

The easiest way is to use

## ["Convert to Gradient Block" Ink/Stitch extension](docs/fill-tools/#convert-to-gradient-blocks)
* Create a shape with an inkscape gradient fill
* Choose the automatic fill method and choose the rest of the parameters.
* Select the shape
* `Extensions > Ink/Stitch > Tools : fill > Convert to gradient blocks`



{% include folder-galleries path="color-blending/" captions="1:Inkscape gradient, n+1 colors;2:Result of extension ;3:Split view;" caption="<i>How the extension works</i>" %}



![Download Sample File](/assets/images/tutorials/samples/inkstitch_gradient_extension.svg)

[Download Sample File](/assets/images/tutorials/samples/inkstitch_gradient_extension.svg).

On each subshape, while first color row spacing decreases,  second color row spacing increases, yielding a gradient fill from first color to second color. 


The gradient direction dictates the fill *angle*. 




## How is varying row spacing achieved ?

Setting *End row spacing* parameter allows for a varying row spacing fill. 
Looking perpendicularly to the fill angle, the  row spacing starts at *spacing between rows* value  and ends up at *end row spacing* value, varying linearly in between.

The two gradient blocks the `Convert to gradient blocks` stacks on each subshape have same *spacing between rows* and *end row spacing* but opposite fill angles, therefore achieving the gradient effect. The actual values of these parameters depends on the initial parameters of the shape, aiming to respect the overall row spacing.


## Tweaking the result

Using the extension instead of manually creating the subshapes and the gradient blocks is a huge time saver. 
You may carefully change the values of *spacing between rows* and *end row spacing* to achieve a different blending effect, but be aware of possible density issue, as you are filling each subshape twice.

Remember that density is the inverse of *spacing between rows*. If you aim to a given overall *spacing between rows* **sbr** (both colors included), then the sum of the inverse of the  *spacing between rows* of the two gradient blocs must be equal to **1/sbr**, as well as the sum of the inverse of their 
*end row spacing*.



These is part of a file containing 100 rectangles each covered by a red varying spacing fill and a blue varying spacing fill, for different values of the parameters

![Download Sample File](/assets/images/tutorials/samples/end_row_spacing_2_colors_blending.svg)

[Dowload the sample  ](/assets/images/tutorials/samples/end_row_spacing_2_colors_blending.svg) 



## Manual blending
If you wish to go the manual way and have total control
### Faux Fill Blend

1. A faux blend has a regular fill layer on bottom and each subsequent layer has variable density settings
2. Make sure that all of the layers have the same stitch angle, this allows for blending to happen
3. When doing more than 2 layers, each blending layer uses less density then the previous layer
4. Make sure to follow the same start and end points for each layer.  For instance, if the base layer starts at top left and ends at bottom right, follow that same sequence for each layer.
5. Underlay is typically not needed, but it does depend on the individual project.
6. Typically, it is best to work from light to dark colors, but again it does depend on the design and the desired end look.
7. While this is not a true blend, in most instances, this type of blend is good enough to achieve the desired end look.
8. The density values in this example are not set in stone, but just to illustrate the concept.  True settings will depend on the design, fabric it's going on and the size of design.

[Download Sample File](/assets/images/tutorials/samples/Faux_Fill_Blend.svg){: download="Faux_Fill_Blend.svg" }

### True Blend


1. Many of the conditions of faux blends also apply here.  Stitch angle, start/end sequencing, typically go from light to dark colors (depends on the design as well)
2. Biggest difference is math is involved and the more complicated the blend, the more complicated the math.  Just have to make sure that each layer for a given section equals 100% of the density for that section that you are wanting.
3. This can involve more layers of colors and more increments of density variation.  The biggest factor is the size/shape of the design and the specifics of the project.
4. What makes this a true blend compared to a faux blend is that each section of the layers are actually mixing with each other.

[Download Sample File](/assets/images/tutorials/samples/True_Blend.svg){: download="True_Blend.svg" }





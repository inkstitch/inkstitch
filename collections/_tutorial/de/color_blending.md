---
title: Color Blending
permalink: /de/tutorials/color-blending/
last_modified_at: 2020-10-04
language: de
excerpt: "Farbübergänge"
image: "/assets/images/tutorials/tutorial-preview-images/blend.png"
werkzeug:
  - Füllung
tutorial-typ:
  - Beispieldatei
stichart: 
  - Füllstich
techniken:
schwierigkeitsgrad:
---


Automatic fills colors don't have to be flat, gradient fills are welcome !

The easiest way is to use

## ["Convert to Gradient Block" Ink/Stitch extension](docs/fill-tools/#convert-to-gradient-blocks)
* Create a shape with an inkscape gradient fill
* Choose the automatic fill method and choose the rest of the parameters.
* Select the shape
* `Extensions > Ink/Stitch > Tools : fill > Convert to gradient blocks`



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
## Falscher Farbübgergang (Faux Fill Blend)

1. Ein falscher Farbübergang hat eine unterste Ebene mit Standard-Füllstich, jede darüberliegende Ebene variiert in ihrer Dichte
2. Jede Ebene sollte den selben Stich-Winkel haben, so kann der Farbübergang-Effekt erzielt werden
3. Solltest du mehr als 2 Ebenen nutzen, muss jede folgende Ebene eine geringere Dichte aufweisen
4. Am Besten sollte jede Ebene am selben Punkt starten und am selben Punkt enden.
5. Eine Unterlage ist nicht unbedingt nötig. Das hängt jedoch immer von dem individuellen Projekt ab.
6. Normalerweise macht es Sinn mit den helleren Farben zu beginnen. Auch das hängt natürlich von dem jeweiligen Projekt ab.
7. Obwohl dies kein echter Farbübergang ist, reicht diese Methode in den meisten Fällen vollkommen aus, um den gewünschten Effekt zu erzielen.
8. Die Werte für die Dichte in diesem Beispiel sind nicht in Stein gemeißelt, es soll nur das Konzept demonstrieren. Die Werten hängen von verschiedenen Faktoren, wie z.B. Stoffart und Designgröße, ab.

[Download Sample File](/assets/images/tutorials/samples/Faux_Fill_Blend.svg){: download="Faux_Fill_Blend.svg" }

## Echter Farbübergang (True Blend)

1. Viele Konditionen des falschen Farbübergangs sind auch auf den echten übertragbar.  Stichwinkel, Start- und Endpunkte, sowie Farbreihenfolge hängen vom individuellen Design ab.
2. Der größte Unterschied ist, dass gerechnet werden muss: die Gesamtdichte für jeden Bereich sollte bei 100% liegen.
3. Das kann bedeuten, dass mehr Farb-Ebenen und Dichte-Variationen erforderlich sind. Der größte Faktor ist die Größe und Form des Designs, sowie die Besonderheiten des einzelnen Projekts.
4. Was diese Methode zu einem echten Farbbergang macht, ist, dass sich die Farben tatsächlich miteinander "vermischen".

[Download Sample File](/assets/images/tutorials/samples/True_Blend.svg){: download="True_Blend.svg" }



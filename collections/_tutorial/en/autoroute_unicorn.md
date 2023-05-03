---
permalink: /en/tutorials/autoroute_unicorn/
title: "Licorne obtenue en arrangement automatique de points droits"
language: en
last_modified_at: 2022-06-04
excerpt: "Auto-route running stitch Unicorn"
image: "/assets/images/tutorials/tutorial-preview-images/autoroute_unicorn.jpg"
tutorial-type:
  - Sample File
tool:
  - "Stroke" 
stitch-type:
  - "Bean Stitch"
  - "Running Stitch"
techniques:
field-of-use:
user-level:
---
## Running stitch Unicorn

We start with this image , downloaded as a png from https://freesvg.org/1539642047 :
<a title="Public Domain" href="https://freesvg.org/1539642047"><img width="512" alt="Unicorn" src="https://freesvg.org/img/1539642047.png"></a>

This is the result :

![Brodée](/assets/images/tutorials/tutorial-preview-images/autoroute_unicorn.jpg)

with very few effort....

The svg file contains all the steps

- Image Layer: starting image

- Step 1 Layer :Vectorize with `Path/ Trace bitmap` 

These parameters were applied

![Paramètres](/assets/images/tutorials/autoroute/autoroute_unicorn_parameters_en.jpg)

Very important: chose **"centerline tracing"** as **detection mode**

- Step 2  Layer : improving the path
  - `Path/ Split Path` 
  -   `Extensions > Ink/Stitch  > Troubleshoot > Cleanup document` to remove the very short paths ( 20px was chosen)

- Step 3 Layer: Embroidery parameters
  - Select all paths,and set stroke style to any dashed
  -  `Extensions > Ink/Stitch  > Params`. 

Chose running stitch length, and bean stitch number of  repeats.

You will see a lot of thread jumps.

![Jumps](/assets/images/tutorials/autoroute/autoroute_unicorn_embroidery_params_en.jpg)

- Step 4 Layer
  
  `Extensions > Ink/Stitch  > Tools: Stroke > Auto-route Running Stitch` enabling only *"Add nodes at intersection"*.
  
  Underpaths are added and now 
  
`Extensions > Ink/Stitch  > Visualise and Export> Simulator` to check that only two jumps are left between eye and body.
   
   ![No Jump](/assets/images/tutorials/autoroute/autoroute_unicorn_embroidery_preview.jpg)
 
Remark: The starting image is very high quality. When it is not as good, before using the Auto-Route extension, you may wish to use these  Ellenn Wasbo's 
extensions  (https://inkscape.org/cs/~EllenWasbo/resources/)
- remove duplicate nodes
- remove duplicate lines

that are even more useful that their name suggest.

You may also benefit from simpliflying the paths.


![SVG](/assets/images/tutorials/samples/autoroute_unicorn.svg)

[Télécharger](/assets/images/tutorials/samples/autoroute_unicorn.svg){: download="autoroute_unicorn.svg" }

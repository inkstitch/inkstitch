---
permalink: /fr/tutorials/autoroute_unicorn/
title: "Licorne obtenue en arrangement automatique de points droits"
language: fr
last_modified_at: 2022-06-05
excerpt: "fichier exemple licorne en points droits"
image: "/assets/images/tutorials/tutorial-preview-images/autoroute_unicorn.jpg"
tutorial-type:
  - Sample File
stitch-type:
  - "Bean Stitch"
  - "Running Stitch"
techniques:
field-of-use:
user-level:
---

## Licorne en point droit
Au départ cette image , téléchargée en png  depuis https://freesvg.org/1539642047 :
<a title="Public Domain" href="https://freesvg.org/1539642047"><img width="512" alt="Unicorn" src="https://freesvg.org/img/1539642047.png"></a>

Une fois brodée :

![Brodée](/assets/images/tutorials/tutorial-preview-images/autoroute_unicorn.jpg)

Le tout avec un minimum d'effort....

Dans le svg, vous trouverez toutes les étapes:


- Calque Image : image de départ


- Calque Step 1 :Vectorisation de l'image avec `Chemin/ Vectoriser un objet matriciel` 


Ici  on a appliqué ces  paramètres :

![Paramètres](/assets/images/tutorials/autoroute/autoroute_unicorn_parameters.jpg)

Le plus important est de choisir **"traçage centerline"** comme **mode de détection**

- Calque Step 2 : amélioration du chemin en vue de la broderie
  - `Chemin/ Séparer` 
  - puis  `Extensions > Ink/Stitch  > Résolution de problèmes > Nettoyer le document` pour supprimer les tous petits chemins (cette fois ci en réglant sur 20px)

 
- Calque Step 3 : Paramètrages de broderie 
  - Mettre tout en pointillé
  - Appliquer des paramètres de broderie   avec  `Extensions > Ink/Stitch  > Paramètres`. 
C'est le moment de choisir la longueur du point et si l'on souhaite ou non du point triple



On observe beaucoup de saut de fils.

![Sauts de fil](/assets/images/tutorials/autoroute/autoroute_unicorn_embroidery_params.jpg)


- Calque Step 4
  Application  de  l'arrangement  automatique de points droits après avoir sélectionnés tous les chemins
  `Extensions > Ink/Stitch  > Outils: Trait > Agencement automatique de points droits` en cochant "Ajouter des noeuds aux intersections".
  
  Des chemins de dessous sont ajoutés, et maintenant 
  
`Extensions > Ink/Stitch  > Visualiser et Exporter > Simulateur` pour constater qu'il n'y plus que deux sauts de fil, entre l'oeil et le corps.
   
   ![Plus de sauts de fil](/assets/images/tutorials/autoroute/autoroute_unicorn_embroidery_preview.jpg)
 

Remarque : Ici l'image de départ est de très bonne qualité, si elle est moins bonne , vous pouvez, avant d'appliquer  l'arrangement automatique
utiliser  ces extensions d'Ellen Wasbo (https://inkscape.org/cs/~EllenWasbo/resources/)
- remove duplicate nodes
- remove duplicate lines


qui peuvent être encore plus utiles que ce que leur nom suggère pour améliorer l'image.

Une simplification des chemins, peut aussi être une bonne idée.


![SVG](/assets/images/tutorials/samples/autoroute_unicorn.svg)




[Télécharger](/assets/images/tutorials/samples/autoroute_unicorn.svg){: download="autoroute_unicorn.svg" }

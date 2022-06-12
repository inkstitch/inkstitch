---
permalink: /fr/tutorials/autoroute_life_flower/
title: "Fleur de vie "
language: fr
last_modified_at: 2022-06-12
excerpt: "Agencement automatique de points droits"
image: "/assets/images/tutorials/life_flower/flower-of-life-two-digitalisation.svg"
tutorial-type:
  - 
stitch-type:
  - Bean Stitch
  - Running Stitch
techniques:
field-of-use:
user-level: 
---

L'agencement automatique de points droits permet de passer facilement de certaines images à une broderie de type redwork.

Partons par exemple du png de cette fleur de vie trouvée sur wikipedia: 

<a title="Credit to the author, CC BY-SA 3.0 &lt;https://creativecommons.org/licenses/by-sa/3.0&gt;, via Wikimedia Commons" href="https://commons.wikimedia.org/wiki/File:Flower-of-Life-small.svg"><img width="512" alt="Flower-of-Life-small" src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Flower-of-Life-small.svg/512px-Flower-of-Life-small.svg.png"></a>


Inkscape permet de numériser cette image de plusieurs manières. 

Ce fichier contient deux numérisations obtenues sous inkscape en utilisant Chemin/Vectoriser une image vectorielle puis  pour celle de gauche la méthode de detection " seuil de luminosité " et pour celle de droite "Traçage centerline".

![Sample](/assets/images/tutorials/life_flower/flower-of-life-two-digitalisation.svg)
[Download](/assets/images/tutorials/life_flower/flower-of-life-two-digitalisation.svg){: download="life_flower.svg" }

Dans les deux cas,  on peut selectionner tous les chemins, leur donner les paramètres de broderie souhaités puis  appliquer l'agencement automatique des  points droits, qui va permettre d'obtenir une broderie sans sauts de fil. 

Voici le résultat de la broderie

![Sample](/assets/images/tutorials/life_flower/twolifeflower.jpg)

La numérisation "seuil de luminosité" a été brodée en point droit simple, la numérisation centerline en  point  triple. 

La numérisation  "centerline" permet d'éviter de doubler tous les contours (les autre numérisations utilisent des remplissages, celle  ci n'utilise que des contours)


  

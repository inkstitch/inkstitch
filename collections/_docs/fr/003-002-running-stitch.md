---
title: "Point droit"
permalink: /fr/docs/stitches/running-stitch/
last_modified_at: 2023-04-23
toc: true
---
## De quoi s'agit-il

[![Papillon au point droit](/assets/images/docs/running-stitch.jpg){: width="200x"}](/assets/images/docs/running-stitch.svg){: title="Download SVG File" .align-left download="running-stitch.svg" }

Le point droit produit une série de petits points suivant une ligne ou une courbe.

![Point droit Détail](/assets/images/docs/running-stitch-detail.jpg)

## Comment le créer
Un point droit est créé à l'aide d'un chemin muni d'une couleur de contour.

Le sens de la broderie est influencé par [la direction du chemin](/fr/docs/customize/#activation-de-la-direction-des-chemins). Si vous souhaitez échanger le départ et l'arrivée de votre point droit, exécutez `Chemin > Inverser`.

Si un objet est constitué de plusieurs chemins, ils seront brodés l'un après l'autre, avec un saut entre chaque.



## Paramétres

Ouvrir `Extensions > Ink/Stitch  > Paramètres` pour paramétrer selon vos besoins.

Paramètres|Description
---|---
Points droits le long des chemins |Doit être activé pour que ces paramètres prennent effet
Méthode                           |Choisir `Point droit / Point multiple`
Répéter                           |Définir combien de fois aller et revenir le long du chemin<br />◦ par défaut: 1 (aller une fois du début à la fin du chemin)<br />◦ Nombre impair: les points se termineront à la fin du chemin<br />◦ Nombre pair: la broderie va revenir au début du chemin
Nombre de répétitions du point triple |Active le [Mode point triple](/fr/docs/stitches/bean-stitch/)<br />◦ Repasse sur chaque point le nombre de fois indiqué.<br />◦ Une valeur de 1 triplera chaque point (avant, arrière, avant).<br />◦ Une valeur de 2 permettra de quintupler chaque point, etc..<br />
Longueur du point droit           |Longueur des points 
Tolerance du point droit          |Les points ne peuvent pas être éloignés du chemin de plus que cette distance. Une tolerance basse peut impliquer des points plus courts. Une tolerance haute entraine un arrondissement des angles aigus.
Autoriser les points d'arrêts     |Ajoute un point d'arrêt à la ou les positions choisies
Forcer les points d'arrêts        |Force un point d'arrêt après l'objet indépendament de la valeur de "Saut de fil" dans les Préférences d'Ink/Stitch.
Point d'arrêt initial                   |Choisir le  [style désiré](/fr/docs/stitches/lock-stitches/)
Point d'arrêt final                 |Choisir le  [style désiré](/fr/docs/stitches/lock-stitches/)
Couper après                      |Couper le fil après avoir brodé cet objet
Arrêter après                     |Arrêter (pause machine) après avoir brodé cet objet. Avant l'arrêt, il y aura un saut vers la position d'arrêt si elle a été définie


## Routage (agencement automatique)

Pour un meilleur ordonnancement des points, essayez l'extension `Agencement automatique de points droits ` dans  [Outils: Traits](/fr/docs/stroke-tools/).

## Motif sur point droit

Lire le [tutoriel](/fr/tutorials/patterned-unning-stitch/) pour créer facilement un motif sur point droit

![patterned running stitch](/assets/images/tutorials/pattern-along-path/copy-paste.png)

## Fichiers exemple avec point droit
{% include tutorials/tutorial_list key="stitch-type" value="Running Stitch" %}

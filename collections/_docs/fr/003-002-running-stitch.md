---
title: "Point droit"
permalink: /fr/docs/stitches/running-stitch/
excerpt: ""
last_modified_at: 2022-01-14
toc: true
---
## Qu'est-ce que c'est

[![Papillon au point droit](/assets/images/docs/running-stitch.jpg){: width="200x"}](/assets/images/docs/running-stitch.svg){: title="Download SVG File" .align-left download="running-stitch.svg" }

Le point droit produit une série de petits points suivant une ligne ou une courbe.

![Point droit Détail](/assets/images/docs/running-stitch-detail.jpg)

## Comment le créer
Le point droit est créé en définissant un trait en pointillé sur un chemin. Tout type de tiret fera l'affaire et la largeur du trait n'est pas pertinente.
![Pointillé pour point droit](/assets/images/docs/running-stitch-dashes.jpg){: .align-left style="padding: 5px"}
Sélectionnez le trait et allez à `Objet > Fond et contour...` et choisissez l’une des lignes pointillées de l’onglet `Style du contour`.


Ouvrir [`Extensions > Ink/Stitch  > Paramètres`](/fr/docs/params/#stroke-params) pour modifier les paramètres selon vos besoins.

Le sens de la broderie est influencé par la direction du chemin. Si vous souhaitez échanger le départ et l'arrivée de votre point droit, exécutez `Chemin > Inverser`.

**Info:** Afin d'éviter les angles arrondis, un point supplémentaire sera ajouté à la pointe des coins pointus.
{: .notice--info style="clear: both;" }

## Fichiers exemple avec point droit
{% include tutorials/tutorial_list key="stitch-type" value="Running Stitch" %}

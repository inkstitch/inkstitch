---
title: "## Caractéristiques notables"
permalink: /fr/features/
excerpt: "Ink/Stitch features"
last_modified_at: 2022-06-12
sidebar:
  nav: pages
toc: true
---
Ink/Stitch: digitaliser des broderies machines en utilisant Inkscape (SVG)

## Accessibilité

* Multiplateforme (Linux, Windows, macOS)
* Interface utilisateur traduite en plusieurs langues ([aide à la traduction appréciée](https://translate.inkstitch.org))

## Types de points

* Divers [types de points](/docs/stitch-library/) : point de remplissage, colonne satin, points de type trait
* Les [motifs](/docs/stitches/patterns/) personnalisés peuvent être appliqués à tous les types de points disponibles.

### Point de remplissage

* [remplir](/docs/stitches/fill-stitch/) automatiquement des formes arbitraires avec des points
* Ajustez la longueur du point, l'espacement des rangées et l'angle des rangées
* Sous-couche
* [Remplissage contour](/docs/stitches/contour-fill/)
* [Remplissage guidé](/docs/stitches/guided-fill/)

### Colonne Satin
* Concevez votre [colonne de satin](/docs/stitches/satin-column/) avec une largeur variable
* Mélangez et assortissez 3 types de sous-couche (sous-couche centrale, sous-couche de contour, sous-couche en zig-zag)
* [E-point](/docs/points/e-point/)
* Split: découpe un point en plusieurs pour respecter une longueur de point maximale
* [Routage automatique](/docs/satin-tools/) (avec  ajout de sous-chemin en point droit si nécessaire)

### Points de type trait

* [Point droit](/docs/stitches/running-stitch/)
* [Point triple](/docs/stitches/bean-stitch/)
* [Point manuel](/docs/stitches/manual-stitch/) (chaque point exactement où vous le voulez)
* [Richelieu](/docs/cutwork/)
* [Routage automatique](/docs/stroke-tools/) pour éviter les sauts de points

## Texte

* [Module lettrage](/docs/lettering/) avec de nombreuses [polices](/fonts/font-library/) prête à l'usage.

## Prévisualisation de la broderie
* Aperçu animé de la broderie (y compris aperçu en direct lorsque vous ajustez les paramètres tels que la sous-couche , l'espacement des lignes, etc.)
* [Simulateur et aperçu du plan de broderie](/docs/visualize/)
* [Imprimer au format PDF](/docs/print-pdf/)
   * rendu réaliste ou  pas
   * Mise en page pour l'opérateur de la machine à broder avec blocs de couleur, noms de fils, nombre de points et notes personnalisées
   * mise en page orientée client conçue pour que vous puissiez l'envoyer à votre client
   * hautement personnalisable

## Gestion des fils

Ink/Stitch a une section [Gestion des fils](/docs/thread-color/) dans le menu.

* Palettes de fabricants de fils (plus de 60 fabricants inclus)
   * installation automatisée des palettes Inkscape à utiliser dans vos conceptions
   * noms de fils et numéros de catalogue inclus dans les impressions PDF
* Outils pour créer facilement vos propres palettes de fils


## Import et Export

[Import et Export](/docs/import-export/) beaucoup de format machine (inclant l'export en lot)

### Ecriture
CSV, **DST**, **EXP**, **JEF**, PEC, **PES**, SVG, TXT (G-CODE), U01, **VP3**

### Lecture
100, 10o, BRO, DAT, DSB, **DST**, DSZ, EMD, **EXP**, EXY, FXY, GT, INB, **JEF**, JPX, KSM, MAX, MIT, NEW, PCD, PCM, PCQ, PCS, PEC, **PES**, PHB, PHC, SEW, SHV, STC, STX, TAP, TBF, TXT (G-CODE), U01, **VP3**, XXX, ZXY

###  Commandes Machine

* Ajouter des commandes de [Coupe et Arrêt](/docs/commands/)
* Définir un  [point origine personnalité](/docs/commands/) comme (0, 0) dans le fichier de broderie.

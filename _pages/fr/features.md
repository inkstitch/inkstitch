---
title: "Fonctionnalités d'Ink/Stitch"
permalink: /fr/features/
excerpt: "Ink/Stitch features"
last_modified_at: 2019-10-24
sidebar:
  nav: pages
toc: true
---
## Caractéristiques notables
* Numérisez des motifs de broderie à la machine avec Inkscape (SVG)
* Cross Platform
  * toutes les bibliothèques de code intégrées, pas besoin d'installer autre chose!
* Interface utilisateur traduite en plusieurs langues (aide appréciée de la traduction](https://crowdin.com/project/inkstitch)!)
* Importer et exporter de nombreux formats de broderie à la machine populaires
  * y compris l'exportation par lots
* Ajoute des commande de coupe et de Stop
* Modifier l'ordre des points
* Définir le point d'origine personnalisé comme (0, 0) dans le fichier de dessin
* Aperçu de broderie animée
  * y compris la prévisualisation en direct lorsque vous ajustez les paramètres tels que la sous-couche d'espacement des lignes, etc.
* Imprimer en PDF
  * rendu réaliste
    * mode tracé disponible également
  * Le mode de dessin au trait est également disponible ainsi que le schéma de broderie avec les blocs de couleur, les noms de fil, le nombre de points et les notes personnalisées
  * mise en page orientée client conçue pour que vous puissiez l'envoyer à votre client
  * hautement personnalisable via votre navigateur web
* Palettes de fil (plus de 60 fabricants inclus)
  * installation automatisée des palettes Inkscape à utiliser dans vos motifs
  * noms de fil et numéros de catalogue inclus dans les impressions PDF
* Lettrage

## Types de points pris en charge

### Point de remplissage
* remplir automatiquement des formes arbitraires avec des points
* ajuster la longueur de point, l'espacement des rangées et l'angle des rangées
* sous-couche

### Point Satin
* personnaliser votre colonne satin avec une largeur variable
* routage automatique (avec sous-chemi en point droit si nécessaire)
* mélanger et assortir 3 types de sous-couches
   * centrée
   * contour
   * zig-zag
Point E
### Type de points en ligne 
* point droit
* point triple
* point manuel
  * chaque point exactement où vous le voulez

## Formats de fichiers pris en charge

### Ecriture
CSV, **DST**, **EXP**, **JEF**, PEC, **PES**, SVG, TXT (G-CODE), U01, **VP3**

### Lecture
100, 10o, BRO, DAT, DSB, **DST**, DSZ, EMD, **EXP**, EXY, FXY, GT, INB, **JEF**, JPX, KSM, MAX, MIT, NEW, PCD, PCM, PCQ, PCS, PEC, **PES**, PHB, PHC, SEW, SHV, STC, STX, TAP, TBF, TXT (G-CODE), U01, **VP3**, XXX, ZXY

## Feuille de route

Voici les fonctionnalités que nous espérons ajouter, mais pas nécessairement dans cet ordre:

* Remplissage avec dégradé (déjà réalisé en tant que [fonction cachée](https://github.com/inkstitch/inkstitch/pull/108#issuecomment-369444197))
* Point programmable [#33](https://github.com/inkstitch/inkstitch/issues/33)
* Multi-Decoration Support [#371](https://github.com/inkstitch/inkstitch/issues/371)
* Fractionnement automatique des dessins pour petites machines [#182](https://github.com/inkstitch/inkstitch/issues/182)
* Sous-couches multiples pour le remplissage [#110](https://github.com/inkstitch/inkstitch/issues/110)
* Fractionnement satins [#77](https://github.com/inkstitch/inkstitch/issues/77)
* Gestion automatique des points droits [#373](https://github.com/inkstitch/inkstitch/issues/373)
* 32-bit Linux support (build engineers needed!)


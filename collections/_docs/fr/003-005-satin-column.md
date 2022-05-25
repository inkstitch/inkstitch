---
title: "Colonne Satin"
permalink: /fr/docs/stitches/satin-column/
excerpt: ""
last_modified_at: 2021-10-23
toc: true
---
## Qu’est-ce que c’est

Le point satin est principalement utilisé pour les bordures, les lettres ou les petites zones de remplissage.

![Stitch Types - Satin Column](/assets/images/docs/stitch-type-satincolumn.jpg)

## Création à partir d'un trait

* Choisir un trait (un objet avec une couleur de contour, mais pas de couleur de remplissage)
* Définissez l'épaisseur du contour à la taille souhaitée pour la largeur de votre point satin.
* Lancer `Extensions > Ink/Stitch > Outils : Satin > Convertir ligne en satin`

Vous obtenez un chemin composite composé de 
  - deux rails qui correspondent aux bords longs de votre trait 
  - des traverses perpendiculaires aux rails qui indiquent la direction des  points de broderie


* Utilisez tel quel ou modifier les traverses ou les rails en déplaçant leur noeuds.


* En option lancer `Extensions > Ink/stitch > Outils : Satin > Agencement automatique de colonnes satin...` après avoir sélectionné une ou plusieurs colonnes satins


## Création manuelle  de colonne Satin

* Commencez par définir les rails de votre colonne satin : dessinez  **deux traits presque parallèles**. La future colonne satin se brodera en zigzag entre les deux rails, vous pouvez faire varier l'épaisseur de la colonne à votre guise, en faisant varier la distance entre les deux rails.

* Combinez ces deux traits avec `Chemin > Combiner` ou taper `Ctrl+K`.

* [Vérifier les directions de chemin](/fr/docs/customize/#activation-de-la-direction-des-chemins). Pour que la colonne satin fonctionne comme attendu, les deux rails doivent avoir la même direction.

Si ce n'est pas le cas Sélectionnez avec l' *Outil Editer les noeuds* (`N`) un noeud d'un des deux rails et faites `Chemin > Inverser`. Cela n'inversera que le rail sélectionné.
 
* Ink/Stitch va dessiner des zig-zags entre les deux lignes : pour régler la direction des points de broderie, utilisez la méthode des noeuds ou la méthodes des traverses décrites ci-dessous.


* Ensuite, sélectionnez votre colonne satin et lancez les paramètres avec `Extensions > Ink/Stitch  > Paramètres` ou un  [raccourci clavier personnalisé](/fr/docs/customize/).

### Méthode des noeuds

[![Bateau en colonne satin](/assets/images/docs/satin-column.jpg){: width="200x"}](/assets/images/docs/satin-column.svg){: title="Télécharger le fichier SVG" .align-left download="satin-column.svg" }
Selon la complexité de votre conception, cette méthode peut prendre beaucoup de temps, car les deux rails doivent avoir exactement le **même nombre de noeuds** (Cela signifie que chaque rail sera composé d'un nombre égal de courbes de Bézier). 

Chaque paire de noeuds (une paire de noeud est constituée d'un noeud sur chaque rail, en commençant par la paire des  noeuds initiaux des deux rails, puis la paire des deuxième noeuds de chaque rail, etc....) agit comme un "point de contrôle": Ink/Stitch garantira qu'un "zag" finisse par aller d'un noeud  de chaque paire à l'autre noeud de la paire.

### Méthode des traverses

[![Chapeau du chef en colonne satin](/assets/images/docs/satin-column-rungs-example.jpg){: width="200x"}](/assets/images/docs/satin-column-rungs.svg){: title="Télécharger le fichier SVG" .align-left download="satin-column-rungs.svg" }

La méthode des traverses vous donnera plus de contrôle sur le rendu de la colonne satin. Un bon positionnement des points sur chacun des deux rails aide à bien orienter les points. 

Cependant, il existe des situations dans lesquelles vous devez ajouter manuellement des lignes de direction ("traverses") pour les colonnes satin:
* Quelques angles difficiles
* Dessins complexes où les déplacements de points sont à la fois difficiles et longs
* Situations spéciales dans lesquelles vous souhaitez que les instructions de point soient particulières
{: style="clear: both;" }

**Ajout manuel de traverses**

* Assurez-vous que le chemin de la colonne satin existant (avec les deux rails comme sous-chemins) est sélectionné avec l'outil Editer les noeuds.
* Appuyez sur `P` ou sélectionnez l'outil Crayon.
* Maintenir la touche `Maj`enfoncée.
* Cliquez une fois là où vous souhaitez le début de la traverse.
* Cliquez une seconde fois à la fin de la traverse.
  [![Traverse en Action](https://edutechwiki.unige.ch/mediawiki/images/thumb/6/68/InkStitch-round-bird-2.png/300px-InkStitch-round-bird-2.png)](https://edutechwiki.unige.ch/mediawiki/images/6/68/InkStitch-round-bird-2.png)

  Dessin original de [Liv Iko](https://thenounproject.com/liv_iko/collection/birds/?i=898697) modifié par [EDUTECH Wiki](https://edutechwiki.unige.ch/en/InkStitch)
{: style="font-size: 0.5rem;"}

**Info:** Nous recommandons fortement d'utiliser au moins trois traverses. Si vous utilisez exactement deux traverses (et deux rails), il est difficile pour Ink/stitch de décider qui est qui.
{: .notice--warning }

## Paramètres

Utiliser `Extensions > Ink/Stitch  > Paramètres` vous donne la possibilité de parfaire votre colonne de satin et d’utiliser une sous-couche.
Pour des informations détaillées, lisez la section Satin Paramètres](/fr/docs/params/#paramètres-satin).
Lisez aussi [cet excellent article](https://www.mrxstitch.com/underlay/) sur les motifs en colonnes satin.

## Outils Satin

Assurez-vous de regarder [Satin Tools](/fr/docs/params/#paramètres-satin/). Cela vous facilitera grandement la vie avec les colonnes en satin.

## Fichiers exemple avec des colonnes satin
{% include tutorials/tutorial_list key="stitch-type" value="Satin Stitch" %}

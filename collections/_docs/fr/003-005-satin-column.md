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

## Comment le créer

* Ajouter un contour à un objet chemin (sans remplissage).
* Définissez la largeur du contour à la taille souhaitée pour votre point satin.
* Lancer `Extensions > Ink/Stitch > Outils de satin > Convertir ligne en satin`
* En option lancer `Extensions > Ink/stitch > Outils de satin > Remplissage automatique de colonnes satin...`
* Utilisez tel quel ou modifier les traverses ou les rails

## Colonne Satin manuelle

Vous définissez une colonne satin à l'aide d'une forme composée de **deux lignes presque parallèles**. Ink/Stitch va dessiner des zig-zags entre les deux lignes. Vous pouvez faire varier l'épaisseur de la colonne à votre guise.
* Combinez deux traits avec `Chemin > Combiner` ou taper `Ctrl+K`.
* [Vérifier les directions de chemin](/fr/docs/customize/#activation-de-la-direction-des-chemins). Pour que la colonne satin fonctionne, elles doivent être égales.<br />Si ce n'est pas le cas Sélectionnez avec l' *Outil Editer les noeuds* (`N`) un point du sous-chemin et faites `Chemin > Inverser`. Cela n'inversera que le sous-chemin sélectionné.
* Utilisez la méthode noeud ou traverse comme décrit ci-dessous.
* Ensuite, sélectionnez votre colonne satin et lancez les paramètres avec `Extensions > Ink/Stitch  > Paramètres` ou un  [raccourci clavier personnalisé](/fr/docs/customize/).

### Méthode des noeuds

[![Bateau en colonne satin](/assets/images/docs/satin-column.jpg){: width="200x"}](/assets/images/docs/satin-column.svg){: title="Télécharger le fichier SVG" .align-left download="satin-column.svg" }
Selon la complexité de votre conception, cette méthode peut prendre beaucoup de temps, car les deux chemins doivent avoir le **même nombre de points**. Cela signifie que chaque chemin sera composé d'un nombre égal de courbes de Bézier. Chaque paire de points agit comme un "point de contrôle": Ink/Stitch garantira qu'un "zag" finisse par aller d'un point à l'autre.

### Méthode des traverses

[![Chapeau du chef en colonne satin](/assets/images/docs/satin-column-rungs-example.jpg){: width="200x"}](/assets/images/docs/satin-column-rungs.svg){: title="Télécharger le fichier SVG" .align-left download="satin-column-rungs.svg" }
La méthode des traverses vous donnera plus de contrôle sur le rendu de la colonne satin. Un bon positionnement des points sur chacune des deux lignes aide à bien orienter les points. Cependant, il existe des situations dans lesquelles vous devez ajouter des lignes de direction ("traverses") pour les colonnes satin:
* Quelques angles difficiles
* Dessins complexes où les déplacements de points sont à la fois difficiles et longs
* Situations spéciales dans lesquelles vous souhaitez que les instructions de point soient particulières
{: style="clear: both;" }

**Ajout manuel de traverses**

* Assurez-vous que le chemin de la colonne satin existant (avec les deux sous-chemins) est sélectionné avec l'outil Editer les noeuds.
* Appuyez sur `P` ou sélectionnez l'outil Crayon.
* Maintenir la touche `Maj`enfoncée.
* Cliquez une fois au début de la traverse.
* Cliquez une seconde fois à la fin de la traverse.
  [![Traverse en Action](https://edutechwiki.unige.ch/mediawiki/images/thumb/6/68/InkStitch-round-bird-2.png/300px-InkStitch-round-bird-2.png)](https://edutechwiki.unige.ch/mediawiki/images/6/68/InkStitch-round-bird-2.png)

  Dessin original de [Liv Iko](https://thenounproject.com/liv_iko/collection/birds/?i=898697) modifié par [EDUTECH Wiki](https://edutechwiki.unige.ch/en/InkStitch)
{: style="font-size: 0.5rem;"}

**Info:** Nous recommandons fortement d'utiliser au moins trois traverses. Si vous utilisez exactement deux traverses (et deux rails), il est difficile pour Ink/stitch de décider qui est qui.
{: .notice--warning }

## Paramètres

Utiliser `Extensions > Ink/Stitch  > Params` vous donnera la possibilité de parfaire votre colonne de satin et d’utiliser une sous-couche.
Pour des informations détaillées, lisez [Satin Paramètres](/fr/docs/params/#paramètres-satin) section.
Lisez aussi [cet excellent article](https://www.mrxstitch.com/underlay/) sur les motifs en colonnes satin.

## Outils Satin

Assurez-vous de regarder [Satin Tools](/fr/docs/params/#paramètres-satin/). Cela vous facilitera grandement la vie avec les colonnes en satin.

## Fichiers exemple avec des colonnes satin
{% include tutorials/tutorial_list key="stitch-type" value="Satin Stitch" %}

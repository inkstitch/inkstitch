---
title: "Changements, Mises à jour et Corrections pour la prochaine  version Ink/Stitch"
permalink: /fr/upcoming/
last_modified_at: 2026-01-02
sidebar:
  nav: pages
toc: true
---

Ink/Stitch est en développement constant. Vous pouvez consulter ici toutes les modifications apportées depuis la dernière version officielle.

## [Fontes](/fr/fonts/font-library)

### Nouvelles Fontes

* [Alchemy](/fr/fonts/alchemy/)

  ![Alchemy](/assets/images/fonts/alchemy.jpg)

* [Allegria 20](/fr/fonts/allegria/)

  ![Allegria 20](/assets/images/fonts/allegria20.png)
* [Allegria 55](/fr/fonts/allegria/)

  ![Allegria 55](/assets/images/fonts/allegria55.png)
* [Apex simple small AGS](/fr/fonts/apex/)

  ![Apex simple small](/assets/images/fonts/apex_simple_small_AGS.png)
* [Apesplit](/fr/onts/apespit/)
    
  ![Apesplit](/assets/images/fonts/apesplit.jpg)
* [Braille](/fonts/braille/)

  ![Braille](/assets/images/fonts/braille.png)
* [Circular 3 letters monogram](/fr/fonts/circular-3letters-monogram/)

    ![Circular 3 letters monogram](/assets/images/fonts/circular_3letters_monogram.png)
* [Cyrillic](/fr/fonts/cyrillic/)

  ![Cyrillic](/assets/images/fonts/cyrillic.png)
 * [Handkerchief](/fonts/handkerchief/)

  ![Handkerchief](/assets/images/fonts/handkerchief.png)
* [Jacquard 12](/fonts/jacquard_12/)

  ![Jacquard 12](/assets/images/fonts/jacquard12.png)
* [Jersey 15](/fonts/jersey_15/)

  ![Jersey 15](/assets/images/fonts/jersey15.png)
* [Ladies's present](/fonts/ladies_present/)

  ![Ladies's present](/assets/images/fonts/ladies_present.png)
* [Magic Crosses](/fonts/magic_crosses/)

  ![Magic Crosses](/assets/images/fonts/magic_crosses.png)
* [Montecarlo](/fr/fonts/montecarlo/)

  ![Montecarlo](/assets/images/fonts/montecarlo.png)
* [Nautical](/fonts/nautical/)

  ![Nautical](/assets/images/fonts/nautical.png)
* [Neon](/fr/fonts/neon/)

  ![Neon](/assets/images/fonts/neon.png)
* [Neon blinking](/fr/fonts/neon/)

  ![Neon blinking](/assets/images/fonts/neon_blinking.png)
* [Priscilla](/fr/fonts/priscillaa/)

  ![Priscilla](/assets/images/fonts/priscilla.png)
* [Venezia](/fr/fonts/venezia/)

  ![Venezia](/assets/images/fonts/venezia.png)
* [Venezia small](/fr/fonts/venezia/)

  ![Venezia](/assets/images/fonts/venezia_small.png)

### Mises à jour des polices

De nombreuses mises à jour ont été apportées aux polices existantes. Merci à tous les contributeurs !

## Traductions

Un grand merci à tous les traducteurs. Nous avons reçu de nouvelles traductions en :

* Tchèque
* Néerlandais
* Français
* Allemand
* Grec
* Hongrois
* Portugais (Brésil)
* Espagnol

[Comment traduire Ink/Stitch](/developers/localize/)

## Nouveaux types de points

### Point de croix

![Grenouille au point de croix](/assets/images/upcoming/3.3.0/cross_stitch.jpg){: width="600px" }

[En savoir plus sur le point de croix](/fr/docs/stitches/cross-stitch)

## Mises à jour relatives aux types de points

### Remplissage Legacy

#### Elargir une forme

* Ajout de l'option élargir [#3988](https://github.com/inkstitch/inkstitch/pull/3988)

![Expansion](/assets/images/docs/params-fill-expand.png)

[En savoir plus sur le remplissage legacy](/fr/docs/stitches/fill-stitch/#legacy-fill)

### Broderie Ondulée

#### Largeur adaptative

* Rendu amélioré pour l'option de largeur adaptative [#4079](https://github.com/inkstitch/inkstitch/pull/4079)

![Largeur adaptative](/assets/images/docs/ripple_adaptive_distance.jpg){: width="600px"}

#### Découpe

* Les points ondulés peuvent être utilisées avec une découpe [#4082](https://github.com/inkstitch/inkstitch/pull/4082)

![Ondulation ondnulée avec découpe](/assets/images/docs/ripple_clipped.jpg){: width="600px"}

#### Inverser et permuter les rails de guidage satin

* Ajout d'options de paramètres pour inverser et permuter les rails de guidage satin [#4083](https://github.com/inkstitch/inkstitch/pull/4083)

Ceci affectera le motif et/ou la direction du point.

![Inverser et inverser les rails](/assets/images/docs/ripple_swap_reverse_rails.jpg){: width="600px"}

[En savoir plus sur la broderie ondulée](/fr/docs/stitches/ripple-stitch/)

### Point droit

#### Séquence de longueurs de point

* Il est devenu possible d'entrer une séquence de valeurs séparées par des espaces pour la longueur du point [#4034](https://github.com/inkstitch/inkstitch/pull/4034).

Cette séquence peut également être appliquée aux points ondulés.

![Séquence de longueur de point](/assets/images/docs/running_stitch_length_sequence.jpg)

_Image ci-dessus : point ondulé avec une longueur de point de `1 1 5`_

[En savoir plus sur les points de droits](/fr/docs/stitches/running-stitch/)

### Colonnes Satin

#### Conversion implicite des traits en satin 

Les traits simples peuvent être utilisés directement comme colonnes satin [#3874](https://github.com/inkstitch/inkstitch/pull/3874).

* La largeur du trait doit être supérieure à 0,3 mm.

* La position des nœuds peut influencer le rendu du satin :

![Trait vers satin. Même chemin avec différentes configurations de nœuds](/assets/images/upcoming/3.3.0/stroke-to-satin-nodes.png){: width="600px"}

#### Niveaux d'insertion des points courts

L'insertion des points courts peut désormais prendre plusieurs valeurs séparées par un espace.

Lorsque plusieurs valeurs sont définies, la colonne satin les utilise alternativement pour niveler les points courts consécutifs [#3987](https://github.com/inkstitch/inkstitch/pull/3987).

![Satin avec deux niveaux d'inserts de points courts](/assets/images/docs/satin_multiple_short_stitch_inset_values.jpg){: width="600px"}

[En savoir plus sur les colonnes de satin](/fr/docs/stitches/satin-column/)

### Point zigzag (trait)

* Ajout de l'option de paramètre répétition de point multiple  [#4127](https://github.com/inkstitch/inkstitch/pull/4127)

## Nouvelles extensions

### Appliquer un attribut

`Édition > Appliquer un attribut` [#3983](https://github.com/inkstitch/inkstitch/pull/3983)

Extension destinée aux utilisateurs expérimentés. Applique un attribut donné à tous les éléments sélectionnés.

![Interface graphique d'application d'attribut](/assets/images/upcoming/3.3.0/apply_attribute.jpg)

[En savoir plus](/fr/docs/edit/#apply-attributes)

### Organiser les glyphes

`Gestion des polices > Organiser les glyphes` [#3870](https://github.com/inkstitch/inkstitch/pull/3870)

Aide les  numérisateurs de polices à organiser leur travail par étapes afin de pouvoir réutiliser des lettres déjà numérisées.

[En savoir plus](/fr/docs/font-tools/#organize-glyphs)

### Assistant Point de Croix

Cette extension facilite la création de points de croix dans Ink/Stitch. Elle permet de :

* Calculer la longueur des points en fonction de l'espacement de la grille.
* Appliquer les paramètres du point de croix aux éléments de remplissage sélectionnés.
* Pixelliser les contours des éléments de remplissage sélectionnés.
* Appliquer des valeurs d'espacement à la grille de la page.

[En savoir plus](/fr/docs/fill-tools/#cross-stitch-helper)

## Extensions mises à jour

### Découpe du satin

Un outil pour découper le satin à des endroits précis.

* Il est désormais possible de découper un satin à plusieurs endroits simultanément. [#4015](https://github.com/inkstitch/inkstitch/pull/4015)

[En savoir plus](/fr/docs/satin-tools/#cut-satin-column)

### Briser des objets de remplissage

Un outil pour réparer et décomposer les formes de remplissage simples ou complexes (y compris celles qui se chevauchent).

* Ajout d'une option de seuil [##4110](https://github.com/inkstitch/inkstitch/pull/#4110)

La fonction « Briser des objets de remplissage » supprime les éléments et les trous dont la taille est inférieure à cette valeur.

### Informations sur les éléments

Un outil pour collecter les informations de broderie.

* Ajout d'une option pour copier la liste dans le presse-papiers (accessible depuis l'onglet Aide) [#3817](https://github.com/inkstitch/inkstitch/pull/3817)

[En savoir plus](/fr/docs/troubleshoot/#element-info)

### Gestion des polices

#### Conventions de nommage des fichiers de polices

Auparavant, les noms de fichiers de polices indiquaient le sens des points par des flèches. Cela posait problème sur certains systèmes d'exploitation lors de l'installation d'Inkstitch.

Désormais, les fichiers de polices peuvent être nommés ltr.svg, rtl.svg, ttb.svg, btt.svg pour définir les variantes de la police [#4087](https://github.com/inkstitch/inkstitch/pull/4087)

#### Conversion d'une police SVG en calques de glyphes

Il s'agit d'une extension pour la numérisation de polices de broderie.

* Ajout d'une option pour le dimensionnement des polices [#3799](https://github.com/inkstitch/inkstitch/pull/3799)

* Suppression de l'option permettant d'arrêter la conversion après un certain nombre de glyphes importés [#3937](https://github.com/inkstitch/inkstitch/pull/3937)

* Ignorer les glyphes de la catégorie Unicode Z, car ils ne sont pas rendus.

* Tentative de déchiffrement des noms de glyphes provenant de la zone Unicode privée [#3883](https://github.com/inkstitch/inkstitch/pull/3883)

[En savoir plus](/fr/docs/font-tools/#convert-svg-font-to-glyph-layers)

#### Modifier le JSON

Un outil pour les numériseurs de polices. Il permet aux auteurs de polices de modifier les informations relatives aux polices et au crénage.

* Il est désormais possible de définir la valeur `0` pour `horiz_adv_x_default`. Ceci permet à Ink/Stitch d'utiliser la largeur de chaque glyphe [#3965](https://github.com/inkstitch/inkstitch/pull/3965)

* Nouveaux champs de saisie pour : la police d'origine, son URL et sa licence [#4103](https://github.com/inkstitch/inkstitch/pull/4103)

[En savoir plus](/fr/docs/font-tools/#edit-json)

#### Générer un fichier JSON

Outil destiné aux numériseurs de polices pour la création initiale du fichier JSON. Ce fichier contient toutes les informations relatives à la police.

* Nouveaux champs de saisie pour : police d'origine, URL de la police d'origine et licence de la police [#4103](https://github.com/inkstitch/inkstitch/pull/4103)

[En savoir plus](/fr/docs/font-tools/#generate-json)

#### Test de polices

Un outil permettant aux numériseurs de polices de valider le rendu.

* Affichage uniquement des glyphes déverrouillés (sensibles). Ceci permet un échantillonnage partiel lors de la création de la police [#3870](https://github.com/inkstitch/inkstitch/pull/3870)

* Enregistrement et rechargement des paramètres d'échelle [#3870](https://github.com/inkstitch/inkstitch/pull/3870)

[En savoir plus](/fr/docs/font-tools/#font-sampling)

#### Verrouillage forcé des points d'arrêt

Un outil permettant aux auteurs de polices d'activer automatiquement l'option de verrouillage forcé des points d'arrêt lorsqu'un élément répond à des critères spécifiques.

* Ajout d'une option pour appliquer des points d'arrêt forcés au dernier élément de chaque groupe sélectionné [#3875](https://github.com/inkstitch/inkstitch/pull/3875)

[En savoir plus](/fr/docs/font-tools/#force-lock-stitches)

### Conversion des sauts de point en commandes de coupe/arrêt

Convertit les sauts de point en commandes de coupe.

* Ajout d'une option pour convertir en commande de coupe ou d'arrêt [#4038](https://github.com/inkstitch/inkstitch/pull/4038)

[En savoir plus](/fr/docs/commands/#jump-stitch-to-trim-command)



### Assise de points couchants

Ajoute un remplissage sous les objets sélectionnés.

* Ajout d'une option de longueur de point [#4084](https://github.com/inkstitch/inkstitch/pull/4084)

L'espacement des rangées s'adaptera automatiquement pour s'aligner avec les points.

[En savoir plus](/fr/docs/fill-tools/#knockdown-fill)

### Lettrage

Module de texte utilisant des polices pré-numérisées.

* Ajout d'options d'espacement [#4020](https://github.com/inkstitch/inkstitch/pull/4020)

![Image montrant les options d'espacement : espacement des lettres, espacement des mots et hauteur de ligne](/assets/images/upcoming/3.3.0/letter_spacing_gui.jpg)

![Dessinez deux textes écrits librement : un avec un espacement normal et l'autre avec un espacement adapté des lettres et des mots](/assets/images/upcoming/3.3.0/letter_spacing.jpg){: width="600px" }

[En savoir plus](/fr/docs/lettering/)

### Préférences

Définit les paramètres globaux ou ceux du document SVG actuellement ouvert.

* Ajout de l'option « Rotation à l'exportation » (affecte uniquement le fichier SVG courant) [#3840](https://github.com/inkstitch/inkstitch/pull/3840)

[En savoir plus](/fr/docs/preferences/)

### Détection de probblèmes

Signale les zones problématiques (ou potentiellement problématiques) du design.

* Ajout d'options d'affichage (erreurs, avertissements, avertissements de type) [#3969](https://github.com/inkstitch/inkstitch/pull/3969)

[En savoir plus](/fr/docs/troubleshoot/#troubleshoot-objects)



## Nouvelles Palettes de couleur

* Magnifico thread palette [#4022](https://github.com/inkstitch/inkstitch/pull/4022)
* Threadart thread palette [#4022](https://github.com/inkstitch/inkstitch/pull/4022)

[Read more about color palettes](/fr/docs/thread-color/#install-palettes)

## Corrections de bugs

* Fix issue with rgba thread color definitions [#4126](https://github.com/inkstitch/inkstitch/pull/4126)
* Do not save empty embroidery files [#4125](https://github.com/inkstitch/inkstitch/pull/4125)
* Remove embroidery settings: command param along with commands for trim and stop [#4074](https://github.com/inkstitch/inkstitch/pull/4074)
* Fill to satin: process rungs within the fill shape better [#4025](https://github.com/inkstitch/inkstitch/pull/4025)
* fill to satin: fix stroke width [#4005](https://github.com/inkstitch/inkstitch/pull/4005)
* redwork: delete empty groups [#4014](https://github.com/inkstitch/inkstitch/pull/4014)
* empty-d-object: define a default color (black) [#4018](https://github.com/inkstitch/inkstitch/pull/4018)
* jump to stroke: add path label [#4011](https://github.com/inkstitch/inkstitch/pull/4011)
* params: prevent settings error [#4004](https://github.com/inkstitch/inkstitch/pull/4004)
* satin: do no error on one point zigzag underlay segment [#3996](https://github.com/inkstitch/inkstitch/pull/3996)
* fix remove kerning [#3995](https://github.com/inkstitch/inkstitch/pull/3995)
* fix redwork stroke width [#3964](https://github.com/inkstitch/inkstitch/pull/3964)
* Fix transform issues in lettering along path [#3972](https://github.com/inkstitch/inkstitch/pull/3972)
* Gradient color: fix cache key error [#3966](https://github.com/inkstitch/inkstitch/pull/4007)
* Fill to satin: do not error out when one of multiple selected fills has no matching rung [#3966](https://github.com/inkstitch/inkstitch/pull/3966)
* Satin: rely more on path length for invalid satins [#3963](https://github.com/inkstitch/inkstitch/pull/3963)
* Stroke: filter invalid paths in clipped path [#3989](https://github.com/inkstitch/inkstitch/pull/3989)
* Meander: fix clamp [#3945](https://github.com/inkstitch/inkstitch/pull/3945)
* Stroke to satin: ensure a good starting point for closed paths [#3944](https://github.com/inkstitch/inkstitch/pull/3944)
* Fill: tag last stitch in a row correctly [#3940](https://github.com/inkstitch/inkstitch/pull/3940)
* Color fixes [#3936](https://github.com/inkstitch/inkstitch/pull/3936)
* Satin: fix crash with tiny satin [#3934](https://github.com/inkstitch/inkstitch/pull/3934)
* Preset-related fixes [#3931](https://github.com/inkstitch/inkstitch/pull/3931)
* Stroke: do not overwrite stroke params with satin column values [#3927](https://github.com/inkstitch/inkstitch/pull/3927)
* Satin: skip contour underlay if there are no pairs [#3912](https://github.com/inkstitch/inkstitch/pull/3912)
* Presets: prevent that "add" overwrites existing presets [#3896](https://github.com/inkstitch/inkstitch/pull/3896)
* Satin: fix first_stitch for invalid paths [#3882](https://github.com/inkstitch/inkstitch/pull/3882)
* Satin: fix empty rail issue [#3863](https://github.com/inkstitch/inkstitch/pull/3863)
* Zigzag to Satin: fix zerodivision error [#3858](https://github.com/inkstitch/inkstitch/pull/3858)
* Switch from NFKC to NFC normalization form in the lettering tool [#3828](https://github.com/inkstitch/inkstitch/pull/3828)
* Set trims=True for pyembroidery.write [#3821](https://github.com/inkstitch/inkstitch/pull/3821)
* Fix issue with bad color names [#3816](https://github.com/inkstitch/inkstitch/pull/3816)
* Fix simulator drawing panel attribute error when no stitch is loaded [#3815](https://github.com/inkstitch/inkstitch/pull/3815)

## Builds, tests, workflows, code quality and house keeping

* Move fonts to submodule [#4061](https://github.com/inkstitch/inkstitch/pull/4061)
* debugger vscode adaption [#3981](https://github.com/inkstitch/inkstitch/pull/3981)
* README: add contact information (forum, chat) [#3979](https://github.com/inkstitch/inkstitch/pull/3979)
* removed shapely rebuild from macos builds [#3960](https://github.com/inkstitch/inkstitch/pull/3960)
* Rename pyembroidery to pystitch [#3889](https://github.com/inkstitch/inkstitch/pull/3830)
* Fix(test): fix output tests being fluky [#3859](https://github.com/inkstitch/inkstitch/pull/3859) 
* Fix type errors [#3928](https://github.com/inkstitch/inkstitch/pull/3928)
* Ci: add workflow to run tests on pull requests and pushes [#3830](https://github.com/inkstitch/inkstitch/pull/3830)
* Fix package build with Nix package manager [#3826](https://github.com/inkstitch/inkstitch/pull/3826)



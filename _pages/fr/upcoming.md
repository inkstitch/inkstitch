---
title: "Changements, Mises à jour et Corrections pour la prochaine  version Ink/Stitch"
permalink: /fr/upcoming/
last_modified_at: 2026-06-19
sidebar:
  nav: pages
toc: true
---

This page summarizes the changes included in Ink/Stitch v3.3.0.

The main feature of Ink/Stitch v3.3.0 is the new **Cross Stitch** stitch type.
It is a fill stitch type, and using the new Cross Stitch Assistant, it is easy to set up.
For more detailed guidance, see the tutorials covering various cross stitch creation workflows:
* [From hand cross stitch embroidery chart to cross stitch fills](/tutorials/cross_stitch_chart_to_cross_stitch_fills/)
* [QR Code](/tutorials/qr-code/)
* [From image to Cross Stitch ](/tutorials/image_to_cross_stitch/)
* [Cross Stitch Lettering](/tutorials/cross_stitch_lettering/)

Another major focus of this release is **lettering**.

This version includes many new and updated fonts.
Please note that some fonts have been renamed; a list of the name changes is provided below.

Some of the key lettering improvements include:

* Lettering tool: new spacing options added
* Lettering along Path / Batch lettering export:
  * automatically rotates crosses of cross stitch fonts
  * added option for vertical text positioning
* Font creation: the new Organize Glyphs extension to simplify font development

Another highlight is the simplified creation of even-width **satin columns**.
Simple strokes can now directly be used as satins without an explicit path conversion.

Guided Fill has a new strategy, named **buffer**.
With this strategy it is possible to apply a guide line with multiple subpaths, opening it up for a variety of artistic possibilities.

Explore the full list of changes below. If you find a bug, please report it on GitHub.
Let's improve Ink/Stitch together!

## [Fontes](/fr/fonts/font-library)

### Nouvelles Fontes

* [Alchemy](/fr/fonts/alchemy/)

  ![Alchemy](/assets/images/fonts/alchemy.jpg)

* [Allegria 20](/fr/fonts/allegria/)

  ![Allegria 20](/assets/images/fonts/allegria20.png)
* [Allegria 55](/fr/fonts/allegria/)

  ![Allegria 55](/assets/images/fonts/allegria55.png)
* [Animals](/fr/fonts/animals/)

  ![Animals english](/assets/images/fonts/animals.png)
  ![Animals français](/assets/images/fonts/animaux.png)
  ![Tieralphabet](/assets/images/fonts/tieralphabet.png)
  
* [Apex simple small AGS](/fr/fonts/apex/)

  ![Apex simple small](/assets/images/fonts/apex_simple_small_AGS.png)
* [Apesplit](/fr/fonts/apesplit/)
    
  ![Apesplit](/assets/images/fonts/apesplit.jpg)
* [Barstitch crosses](/fr/fonts/barstitch_bold/)

  ![Barstitch  crosses](/assets/images/fonts/barstitch_crosses.jpg)
* [Braille](/fr/fonts/braille/)

  ![Braille](/assets/images/fonts/braille.png)
* [Circular 3 letters monogram](/fr/fonts/circular-3letters-monogram/)

    ![Circular 3 letters monogram](/assets/images/fonts/circular_3letters_monogram.png)
* [Cyrillic](/fr/fonts/cyrillic/)

  ![Cyrillic](/assets/images/fonts/cyrillic.png)
* [Egyptian](/fr/fonts/egyptian/)

  ![Egyptian](/assets/images/fonts/egyptian.png)

* [Ellenika](/fr/fonts/ellenika/)

  ![Ellenika](/assets/images/fonts/ellenika.png)
* [Eloquent](/fr/fonts/eloquent/)

  ![Eloquent](/assets/images/fonts/eloquent.png)
* [Flowery Crosses](/fr/fonts/flowery_crosses/)

  ![Flowery Crosses](/assets/images/fonts/flowery_crosses.jpg)
   ![Flowery Crosses Multicolor](/assets/images/fonts/flowery_multicolor.jpg)
 * [Handkerchief](/fr/onts/handkerchief/)

  ![Handkerchief](/assets/images/fonts/handkerchief.png)
* [Heavenly](/fr/fonts/heavenly/)

  ![Heavenly](/assets/images/fonts/heavenly.png)
* [Jacquard 12](/fr/fonts/jacquard_12/)

  ![Jacquard 12](/assets/images/fonts/jacquard12.png)
* [Jacquarda Bastarda 9](/fr/fonts/jacquarda_bastarda_9/)

  ![Jacquarda Bastarda 9J](/assets/images/fonts/jacquarda_bastarda.png)
* [Jersey 15](/fr/fonts/jersey_15/)

  ![Jersey 15](/assets/images/fonts/jersey15.png)
* [Ladies's present](/fr/fonts/ladies_present/)

  ![Ladies's present](/assets/images/fonts/ladies_present.png)
* [Magic Crosses](/fr/fonts/magic_crosses/)

  ![Magic Crosses](/assets/images/fonts/magic_crosses.png)
* [Montecarlo](/fr/fonts/montecarlo/)

  ![Montecarlo](/assets/images/fonts/montecarlo.png)
* [Nautical](/fr/fonts/nautical/)

  ![Nautical](/assets/images/fonts/nautical.png)
* [Neon](/fr/fonts/neon/)

  ![Neon](/assets/images/fonts/neon.png)
* [Neon blinking](/fr/fonts/neon/)

  ![Neon blinking](/assets/images/fonts/neon_blinking.png)
* [Noble](/fr/fonts/noble/)

  ![Noble](/assets/images/fonts/noble.png)
* [Precious](/fr/fonts/precious/)

  ![Precious](/assets/images/fonts/precious.jpg)
* [Priscilla](/fr/fonts/priscilla/)

  ![Priscilla](/assets/images/fonts/priscilla.png)
* [Venezia](/fr/fonts/venezia/)

  ![Venezia](/assets/images/fonts/venezia.png)
* [Venezia small](/fr/fonts/venezia/)

  ![Venezia](/assets/images/fonts/venezia_small.png)
*[Very crossy](/fr/fonts/very_crossy/)

  ![Very Crossy](/assets/images/fonts/very_crossy.png)


### Renommage

Pour nous conformer aux noms de polices réservés dans certaines licences OFL, nous avons dû renommer certaines polices Ink/Stitch.

|Ancien Nom|Nouveau Nom|
|---|---|
|Baumans FI|Bathaus FI|
|Marcellus SC FI|Caesarus SC FI |
|Espresso|Caffeine KOR |
|Espresso tiny|Caffeine KOR tiny|
|Sortefax Initials Medium|Initials Medium|
|Sortefax Initials XL|Initial XL|
|Namskout AGS|Kum Tsoan AGS|
|Namskout Relief|Kum Tsoan Relief|
|Namskout Tartan|Kum Tsoan Tartan|
|April en Fleur|Mai en fleur|
|Kaushan Script MAM|MAM Script|
|Coronaviral|Paquerette|
|Manuskript Gothisch|Pisankris|
|Lobster AGS| Stebor AGS|

### Mises à jour des polices

De nombreuses mises à jour ont été apportées aux polices existantes. Merci à tous les contributeurs !

## Traductions

Un grand merci à tous les traducteurs. Nous avons reçu de nouvelles traductions en :

* Chinese Simplified
* Tchèque
* Néerlandais
* Français
* Allemand
* Grec
* Hongrois
* Japanese
* Polish
* Portugais (Brésil)
* Espagnol

[Comment traduire Ink/Stitch](/developers/localize/)

## Nouveaux types de points

### Point de croix

Cross stitch is a new fill stitch stitch type. It is best to use it in combination with the [cross stitch assistant](#cross-stitch-assistant).

![Grenouille au point de croix](/assets/images/upcoming/3.3.0/cross_stitch.jpg){: width="600px" }

[En savoir plus sur le point de croix](/fr/docs/stitches/cross-stitch)

## Mises à jour relatives aux types de points

### Remplissages

Changement de la valeur par défaut du paramétre "Longueur maximale du point de remplissage" de 3 à 4mm.

Les anciens fichiers seront mis à jour pour conserver leur paramétrage.

### AutoFill

* AutoFill a été **renommé**  Tatami [#4454](https://github.com/inkstitch/inkstitch/pull/4454)

[En savoir plus sur le point de remplissage](/fr/docs/stitches/fill-stitch/)

### Remplissage selon contour

* ajout des options de répétition [#4440](https://github.com/inkstitch/inkstitch/pull/4440)

[En savoir plus sur le remplissage selon contour](/fr/docs/stitches/contour-fill/)

### Remplissage guidé

* Ajout de l'option "Nombre de répétitions pour le point multiple " [#4352](https://github.com/inkstitch/inkstitch/pull/4352)
* Nouvelle méthode :  Buffer [#4392](https://github.com/inkstitch/inkstitch/pull/4392)

  Cette nouvelle méthode permet l'usage de chemins qui s'autointersectent comme ligne guide. Il est ausssi possible d'utiliser des chemins composés de plusieurs sous-chemins.

  ![A turtle and a bird using the buffer strategy](/assets/images/upcoming/3.3.0/buffer.jpg)
* Copy strategy: add angle option [#4435](https://github.com/inkstitch/inkstitch/issues/4435)

  The copy strategy allows now to manually adapt the angle in which copies of the guide line are shifted.

  ![Guided fill with strategy copy and two different angles applied](/assets/images/upcoming/3.3.0/copy_angle.jpg)

[En savoir plus sur le remplissage guidé](/fr/docs/stitches/guided-fill/)

### Remplissage Manuel (Legacy)

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

[En savoir plus sur les points droits](/fr/docs/stitches/running-stitch/)

### Colonnes Satin

[En savoir plus sur les colonnes de satin](/fr/docs/stitches/satin-column/)

#### Conversion implicite des traits en satin 

Les traits simples peuvent être utilisés directement comme colonnes satin [#3874](https://github.com/inkstitch/inkstitch/pull/3874).

Les régle suivantes s'appliquent:
* Par défaut, la largeur du trait doit être d'au moins 1mm (adaptable dans le dialogue des préférences 
* La position des nœuds peut influencer le rendu du satin :

  ![Trait vers satin. Même chemin avec différentes configurations de nœuds](/assets/images/upcoming/3.3.0/stroke-to-satin-nodes.png){: width="600px"}

#### Niveaux d'insertion des points courts

L'insertion des points courts peut désormais prendre plusieurs valeurs séparées par un espace.

Lorsque plusieurs valeurs sont définies, la colonne satin les utilise alternativement pour niveler les points courts consécutifs [#3987](https://github.com/inkstitch/inkstitch/pull/3987).

![Satin avec deux niveaux d'inserts de points courts](/assets/images/docs/satin_multiple_short_stitch_inset_values.jpg){: width="600px"}

#### Compensation d'élongation

Ink/Stitch permet depuis un certain temps de définir une compensation d'étirement. Maintenant, il permet aussi de définir une compensation d'élongation.

Elle va racourcir une colones satin aux extrémités spécifiées afin de compenser la poussée des points sur le tissu.

### Point zigzag (trait)

* Ajout de l'option de paramètre répétition de point multiple  [#4127](https://github.com/inkstitch/inkstitch/pull/4127)
* Ajout du paramètre angle [#4141](https://github.com/inkstitch/inkstitch/pull/4141)

### Textures

* Texture: ajout de l'option intervalle pour les textures en trait [#4250](https://github.com/inkstitch/inkstitch/pull/4250)

  Cette option permet de sauter des points aux intersections avec le plan de broderie (par exemple une sur deux)
 
[En savoir plus](/fr/docs/stitches/patterns/)

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
* Convertir des images en éléments de remplissage
* Supprimer les superpositions

![Pixelated mushrom](/assets/images/docs/cross_stitch_assistant.jpg)

[En savoir plus](/fr/docs/fill-tools/#cross-stitch-helper)

## Extensions mises à jour

### Découpe du satin

Un outil pour découper le satin à des endroits précis.

* Il est désormais possible de découper un satin à plusieurs endroits simultanément. [#4015](https://github.com/inkstitch/inkstitch/pull/4015)
* Enable cutting with strokes [#4350](https://github.com/inkstitch/inkstitch/pull/4350)

[En savoir plus](/fr/docs/satin-tools/#cut-satin-column)

### Briser des objets de remplissage

Un outil pour réparer et décomposer les formes de remplissage simples ou complexes (y compris celles qui se chevauchent).

* Ajout d'une option de seuil [##4110](https://github.com/inkstitch/inkstitch/pull/#4110)

La fonction « Briser des objets de remplissage » supprime les éléments et les trous dont la taille est inférieure à cette valeur.

[En savoir plus](/fr/docs/fill-tools/#break-apart-fill-objects)

### Informations sur les éléments

Un outil pour collecter les informations de broderie.

* Ajout d'une option pour copier la liste dans le presse-papiers (accessible depuis l'onglet Aide) [#3817](https://github.com/inkstitch/inkstitch/pull/3817)

[En savoir plus](/fr/docs/troubleshoot/#element-info)

### Multicolor satin

* Re-edit multicolor satin [#4475](https://github.com/inkstitch/inkstitch/pull/4475) makes it much easier to adapt the result once multicolor satin has been applied

[En savoir plus](/fr/docs/satin-tools/#multicolor-satin)

### Redwork

A tool to optimize routing over running stitches without jumps. Runs on every path exactly twice.

* Le redwork a  maintenant l'option de traiter les couleurs séparement (#4426)

[En savoir plus](/fr/docs/stroke-tools/#redwork)

### Gestion des polices

#### Conventions de nommage des fichiers de polices

Auparavant, les noms de fichiers de polices indiquaient le sens des points par des flèches. Cela posait problème sur certains systèmes d'exploitation lors de l'installation d'Inkstitch.

Désormais, les fichiers de polices peuvent être nommés ltr.svg, rtl.svg, ttb.svg, btt.svg pour définir les variantes de la police [#4087](https://github.com/inkstitch/inkstitch/pull/4087)

[En savoir plus](/fr/tutorials/font-creation/)

#### Lettres vers police

* Les glyphes sont maintenant positionnés en bas et à gauche par rapport à la page [#4332](https://github.com/inkstitch/inkstitch/pull/4332)
* La baseline est positionnée en bas de la page [#4332](https://github.com/inkstitch/inkstitch/pull/4332)
* Il est possible de définir une distance au bord gauche de la page [#4332](https://github.com/inkstitch/inkstitch/pull/4332)

[En savoir plus](/fr/docs/font-tools/#letters-to-font)

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

* Nouveaux champs de saisie pour:
  * police d'origine, URL de la police d'origine et licence de la police [#4103](https://github.com/inkstitch/inkstitch/pull/4103)
  * Echelle des points de croixc [#4281](https://github.com/inkstitch/inkstitch/pull/4281)

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

### Sauts en traits

Les etiquettes des paramètres ont été réécrites et légérement modifiées [#4239](https://github.com/inkstitch/inkstitch/pull/4239):

* Convertir les sauts plus longs que  (mm):  Une valeur de 0 permet d'utiliser la valeur de la longeur minimum de saut.
* Convertit les sauts plus courts que (mm): Une valeur de 0, signifie aucune limite

### Installer des compléments pour Inkscape

Ajout d'une nouvelle bibliiothèque de symboles pour des motifs de remplissage [#4296](https://github.com/inkstitch/inkstitch/pull/4296)

[En savoir plus](/fr/docs/install-addons/)

### Conversion des sauts de point en commandes de coupe/arrêt

Convertit les sauts de point en commandes de coupe.

* Ajout d'une option pour convertir en commande de coupe ou d'arrêt [#4038](https://github.com/inkstitch/inkstitch/pull/4038)

[En savoir plus](/fr/docs/stroke-tools/#jump-to-stroke)

### Assise de points couchants

Ajoute un remplissage sous les objets sélectionnés.

* Ajout d'une option de longueur de point [#4084](https://github.com/inkstitch/inkstitch/pull/4084)

  L'espacement des rangées s'adaptera automatiquement pour s'aligner avec les points.

*  Nouvelle option pour inclure les formes (rectangle ou cercle) sans enlever la forme du motif [#4397](https://github.com/inkstitch/inkstitch/pull/4397)

[En savoir plus](/fr/docs/fill-tools/#knockdown-fill)

### Lettrage

Module de texte utilisant des polices pré-numérisées.

* Ajout d'options d'espacement [#4020](https://github.com/inkstitch/inkstitch/pull/4020)

![Image montrant les options d'espacement : espacement des lettres, espacement des mots et hauteur de ligne](/assets/images/upcoming/3.3.0/letter_spacing_gui.jpg)

![Dessinez deux textes écrits librement : un avec un espacement normal et l'autre avec un espacement adapté des lettres et des mots](/assets/images/upcoming/3.3.0/letter_spacing.jpg){: width="600px" }

[En savoir plus](/fr/docs/lettering/)

### Lettrage le long d'un chemin

* Fonctionne aussi pour le point de croix en tournant les croix [#4277](https://github.com/inkstitch/inkstitch/pull/4277)
* Options de positionnement vertical [#4329](https://github.com/inkstitch/inkstitch/pull/4329):
  * Au dessus : le texte en entierement au dessus du chemin (y compris les lettres comme p, g, q.)
  * Baseline:  la baseline du texte est exactement sur le chemin
  * En dessous: le texte est entierement sous le chemin


Les mêmes options ont été ajoutées à l'export par lots.


[En savoir plus (lettrage le long d'un chemin)](/fr/docs/lettering/#lettering-along-path)
[En savoir plus (export par lot)](/fr/docs/lettering/#batch-lettering)

### Ajouter une commande à des objets

* Ajout d'un paramètre de position [#4169](https://github.com/inkstitch/inkstitch/pull/4169)

[En savoir plus](/fr/docs/commands/#attach-commands-to-selected-objects-)

### Paramètres

* Afficher les points droits, même lorsque les colonnes satin sont activées[#4137](https://github.com/inkstitch/inkstitch/pull/4137)
* Afficher également les infobulles lors du survol des champs de saisie (et pas seulement pour les étiquettes) [#4179](https://github.com/inkstitch/inkstitch/pull/4179)

[En savoir plus](/fr/docs/troubleshoot/#element-info)

### Préférences

Définit les paramètres globaux ou ceux du document SVG actuellement ouvert.

* Ajout de l'option « Rotation à l'exportation » (affecte uniquement le fichier SVG courant) [#3840](https://github.com/inkstitch/inkstitch/pull/3840)
* Ajout du paramètre `Seuil d'auto-conversion trait en satin`  [#4279](https://github.com/inkstitch/inkstitch/pull/4279)

La possibilité de rendre un trait comme un satin dépend de la largeur du trait et de la valeur de préférence pour le seuil d'auto-conversion trait en satin

La largeur du trait doit être supérieure à la valeur de préférence ; sinon, cet élément sera traité comme un point droit. 
Pour éviter les problèmes à la broderie, il est recommandé d'utiliser uniquement des traits satin d'une largeur supérieure à 1 mm.
 
[En savoir plus](/fr/docs/preferences/)

### Simulateur

* Options de choix pour la couleur, la taille et l'epaisseur de la croix du simulateur [#4299](https://github.com/inkstitch/inkstitch/pull/4299)

[Read more](/fr/docs/simulator/)

### Détection de problèmes

Signale les zones problématiques (ou potentiellement problématiques) du design.

* Ajout d'options d'affichage (erreurs, avertissements, avertissements de type) [#3969](https://github.com/inkstitch/inkstitch/pull/3969)

[En savoir plus](/fr/docs/troubleshoot/#troubleshoot-objects)


## Nouvelles Palettes de couleur

* Magnifico thread palette [#4022](https://github.com/inkstitch/inkstitch/pull/4022)
* Threadart thread palette [#4022](https://github.com/inkstitch/inkstitch/pull/4022)

[En savoir plus](/fr/docs/thread-color/#install-palettes)

## Mise a jour pour certains formats machine

* VP3: correction d'une erreur d'arrondi [pystitch:129](https://github.com/inkstitch/pystitch/pull/129)

## Corrections de bugs

* realistic preview image: add ignore object attribute when ignore layer was selected (to avoid a object type warning in troubleshoot) [#4477](https://github.com/inkstitch/inkstitch/pull/4477)
* meander with zigzag spacing and clamping: fix stitch length [#4451](https://github.com/inkstitch/inkstitch/pull/4451)
* Cleanup: use mm [#4445](https://github.com/inkstitch/inkstitch/pull/4445)
* redwork: fix element style when moved out of original grouping [#4427](https://github.com/inkstitch/inkstitch/pull/4427)
* satin column: use running stitch length for connecting lines [#4446](https://github.com/inkstitch/inkstitch/pull/4446)
* clone: check if grouped clone elements are embroiderable (prevent error message for example with comments) [#4444](https://github.com/inkstitch/inkstitch/pull/4444)
* edit json: do not render elements from hidden groups [#4430](https://github.com/inkstitch/inkstitch/pull/4430)
* fix glyph filter for white space characters [#4412](https://github.com/inkstitch/inkstitch/pull/4412)
* ripple stitch render at rungs: fallback when no rungs [#4405](https://github.com/inkstitch/inkstitch/pull/4405)
* fix cannot pickle pathelement [#4391](https://github.com/inkstitch/inkstitch/pull/4391)
* Fix issue for linear gradients without gradients [#4361](https://github.com/inkstitch/inkstitch/pull/4361)
* Meander: fix straight segment clipped path [#4340](https://github.com/inkstitch/inkstitch/pull/4340)
* Fix editjson sample text glyph distance between text parts [#4339](https://github.com/inkstitch/inkstitch/pull/4339)
* Manual stitch: skip (sub)paths with a single node [#4328](https://github.com/inkstitch/inkstitch/pull/4328)
* Gradient blocks: fix path output for shapes with holes [#4325](https://github.com/inkstitch/inkstitch/pull/4325)
* Apply thread palette: match tartan palette colors [#4320](https://github.com/inkstitch/inkstitch/pull/4320)
* Fill to satin: skip when there is no combinable rung [#4282](https://github.com/inkstitch/inkstitch/pull/4282)
* EditJson: specify encoding on json load - fixes the extension for Windows users [#4258](https://github.com/inkstitch/inkstitch/pull/4258)
* Fill to satin: improve warnings and error messages [#4244](https://github.com/inkstitch/inkstitch/pull/4244)
* Fix bbox for gradient blocks [#4248](https://github.com/inkstitch/inkstitch/pull/4248)
* Skip clamping when buffering the polygon returns GEOSException [#4221](https://github.com/inkstitch/inkstitch/pull/4221)
* Satin column: start at nearest: allow to connect to outline when centerline has a greater distance than min jump stitch length [#4220](https://github.com/inkstitch/inkstitch/pull/4220)
* Break apart: fix issue with area size value (can be negtative) [#4173](https://github.com/inkstitch/inkstitch/pull/4173)
* Stroke: ignore invalid shapes in first_stitch [#4178](https://github.com/inkstitch/inkstitch/pull/4178)
* Fill to satin: fix skip end segments, when there are only two rungs [#4146](https://github.com/inkstitch/inkstitch/pull/4146)
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

* CI changes to reduce package size (#4341)
* use local repo for wxpython [#4400](https://github.com/inkstitch/inkstitch/pull/4400)
* Fixed profilers when exiting early, added time profiler [#4331](https://github.com/inkstitch/inkstitch/pull/4331)
* Chore: Bumped CI action versions to get rid of deprecation warnings [#4330](https://github.com/inkstitch/inkstitch/pull/4330)
* Refactored non-drawing code out of DrawingPanel [#4305](https://github.com/inkstitch/inkstitch/pull/4305)
* Update contributing and code style documents and add pull request template [#4170](https://github.com/inkstitch/inkstitch/pull/4170)
* Fix untyped decorator errors (and downstream type errors) [#4197](https://github.com/inkstitch/inkstitch/pull/4197)
* CI: Added code style check, pinned action-gh-release version [#4192](https://github.com/inkstitch/inkstitch/pull/4192), [#4196](https://github.com/inkstitch/inkstitch/pull/4196)
* Move fonts to submodule [#4061](https://github.com/inkstitch/inkstitch/pull/4061)
* debugger vscode adaption [#3981](https://github.com/inkstitch/inkstitch/pull/3981)
* README: add contact information (forum, chat) [#3979](https://github.com/inkstitch/inkstitch/pull/3979)
* removed shapely rebuild from macos builds [#3960](https://github.com/inkstitch/inkstitch/pull/3960)
* Rename pyembroidery to pystitch [#3889](https://github.com/inkstitch/inkstitch/pull/3830)
* Fix(test): fix output tests being fluky [#3859](https://github.com/inkstitch/inkstitch/pull/3859) 
* Fix type errors [#3928](https://github.com/inkstitch/inkstitch/pull/3928)
* Ci: add workflow to run tests on pull requests and pushes [#3830](https://github.com/inkstitch/inkstitch/pull/3830)
* Fix package build with Nix package manager [#3826](https://github.com/inkstitch/inkstitch/pull/3826)



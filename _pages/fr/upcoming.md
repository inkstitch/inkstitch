---
title: "Changements, Mises à jour et Corrections pour la prochaine  version Ink/Stitch"
permalink: /fr/upcoming/
last_modified_at: 2025-04-16
sidebar:
  nav: pages
toc: true
---
Ink/Stitch est en développement constant. Vous trouverez ici toutes les modifications apportées depuis la dernière version officielle.

## [Polices](/fonts/font-library)

### Nouvelles Polices

* [Ambigüe](/fr/fonts/ambigue/)

  ![Ambigüe](/assets/images/fonts/ambigue.png)
* [Barstitch bold](/fr/fonts/barstitch_bold/)

  ![Barstitch bold](/assets/images/fonts/barstitch_bold.png)
* [Barstitch cloudy](/fr/fonts/barstitch_bold/)

  ![Barstitch cloudy](/assets/images/fonts/barstitch_cloudy.png)
* [Barstitch mandala](/fr/fonts/barstitch/bold/)

  ![Barstitch mandala](/assets/images/fonts/barstitch_mandala.png)
* [Barstitch regular](/fr/fonts/barstitch_bold)

  ![Barstitch regular](/assets/images/fonts/barstitch_regular.png)
* [Barstitch textured](/fr/fonts/barstitch_bold/)

  ![Barstitch textured](/assets/images/fonts/barstitch_textured.png)
* [Califragilistic](/fr/fonts/califragilistic/)

  ![Califragilistic](/assets/images/fonts/califragilistic.png)
* [Cogs_KOR](/fr/fonts/cogs_KOR)

  ![Cogs_KOR](/assets/images/fonts/cogs_KOR.png)
* [Computer](/fr/fonts/computer/)

  ![Cpmputer](/assets/images/fonts/computer.png)
* [Decadent Flower Monogram](/fr/fonts/decadent_flowers_monogram/)

  ![Decadent flower monogram](/assets/images/fonts/decadent_flowers_monogram.png)
* [גופן בינוני](/fr/fonts/hebrew_font/)

  ![גופן בינוני](/assets/images/fonts/hebrew_font_medium.png)
  ![גופן בינוני](/assets/images/fonts/hebrew_font_large.png)
* [פשוט מעוגל](/fr/fonts/hebrew_font/)

  ![פשוט מעוגל](/assets/images/fonts/hebrew_simple_rounded.png)
* [Ink/Stitch Masego](/fr/fonts/inkstitch-masego/)

  ![Ink/Stitch Masego](/assets/images/fonts/inkstitch_masego.png)
* [Magnolia tamed](/fr/fonts/magnolia-script/)

  ![Magnolia tamed preview](/assets/images/fonts/magnolia_tamed.png)
* [Malika](/fr/fonts/malika/)

  ![Malika](/assets/images/fonts/malika.png)
* [Mimosa](/fr/fonts/mimosa/)

  ![Mimosa medium](/assets/images/fonts/mimosa_medium.png)

  ![Mimosa large](/assets/images/fonts/mimosa_large.png)
* [Pixel 10](/fr/fonts/pixel10/)

  ![Pixel 10](/assets/images/fonts/pixel_10.png)
* [Sunset](/fr/fonts/sunset/)

  ![Sunset](/assets/images/fonts/sunset.png)
* [Western light](/fr/fonts/western_light/)

  ![Western light](/assets/images/fonts/western_light.png)

### Mises à jour des polices

De nombreuses mises à jour des polices existantes ont été effectuées. Merci à tous !

## Nouvelles extensions
### Éditer le fichier JSON

`Gestion des polices > Editer le fichier JSON` [#3371](https://github.com/inkstitch/inkstitch/pull/3371)

`Editer le fichier JSON` fait partie de la gestion des polices et permet aux auteurs de polices de corriger facilement les données du fichier JSON. Cette fonctionnalité est particulièrement utile pour les corrections de crénage, car elle simule un texte personnalisé lors de la mise à jour du crénage.![Edition du Crénage (distance entre les lettres](/assets/images/upcoming/3.2.0/edit_json.png)

[En savoir plus](/fr/docs/font-tools/#edit-json)

### Remplissage en Satin

`Outils: Satin > Remplissage en Satin...` [#3406](https://github.com/inkstitch/inkstitch/pull/3406)

Convertit un remplissage  en  satin. Nécessite un positionnement manuel des traverses

![Remplissage en satin](/assets/images/docs/fill_to_satin_bridge.png)

[En savoir plus](/fr/docs/satin-tools/#fill-to-satin)

### Installer des modules complémentaires pour Inkscape

Installer des modules complémentaires pour Inkscape [#3606](https://github.com/inkstitch/inkstitch/pull/3606)

Installe des palettes de couleurs ou une bibliothèque de symboles pour les points de motif dans Inkscape. Veuillez redémarrer Inkscape après l'installation.

![Points de motif](/assets/images/upcoming/3.2.0/motif-stitches.png)

Remplace « Installer des palettes de couleurs de fil pour Inkscape ».

[En savoir plus](/fr/docs/install-addons/)

### Supprimer les points dupliqués

`Édition > Supprimer les points dupliqués` [#3117](https://github.com/inkstitch/inkstitch/pull/3117)

Permet, par exemple, de supprimer les répétitions des plans de broderie des points multiples et de les transformer en lignes simples.

![Supprimer les points dupliqués](/assets/images/upcoming/3.2.0/remove_duplicated_points.png)

[En savoir plus](/fr/docs/edit/#remove-duplicated-points)

### Sélection en remplissage en points couchants (Knockdown)

`Outils : Remplissage > Sélection en remplissage en points couchants` [#3526](https://github.com/inkstitch/inkstitch/pull/3526)

Méthode permettant de générer une zone de remplissage en point couchants sous tous les éléments sélectionnés, avec un décalage optionnel. Ceci peut s'avérer très utile pour les tissus à poils longs.

![Une figure entourée d'un point couchant](/assets/images/docs/knockdown.png)

[En savoir plus](/fr/docs/fill-tools/#knockdown-fill)

### Définir l'index de tri des couleurs

`Gestion des polices > Définir l'index de tri des couleurs` [#3242](https://github.com/inkstitch/inkstitch/pull/3242)

Un outil pour les créateurs de polices qui définit un index de tri des couleurs sur les éléments sélectionnés afin de contrôler leur regroupement lorsque l'option de tri des couleurs est activée dans l'outil de lettrage.

![Index de tri des couleurs](/assets/images/upcoming/3.2.0/color_sort_index.png)

[En savoir plus](/fr/docs/font-tools/#set-color-index)

### Transformation

`Édition > Transformation...` [#3657](https://github.com/inkstitch/inkstitch/pull/3657)

Applique des transformations aux éléments (rotation/retournement) tout en adaptant l'angle de remplissage.

![Élément de remplissage transformé à 45 degrés, angle de remplissage adapté](/assets/images/docs/transform.png)

## Mises à jour des extensions

### Général

* Demander l'autorisation de mettre à jour les anciens fichiers SVG si l'attribut de version SVG d'Ink/Stitch n'est pas spécifié dans le fichier. [#3228](https://github.com/inkstitch/inkstitch/pull/3228)

Cela empêche la mise à jour erronée du contenu copié-collé dans un nouveau fichier.
* Les extensions Ink/Stitch sont désormais affichées avec des icônes et des descriptions dans la galerie d'extensions pour un accès facile [#3287](https://github.com/inkstitch/inkstitch/pull/3287)

  ![Extension gallery](/assets/images/upcoming/3.2.0/extension_gallery.png)

### Agencement automatique de colonnes satin

`Outils: Satin > Agencement automatique de colonnes satin`

* Ajout d'une option pour conserver les chemins  originels [#3332](https://github.com/inkstitch/inkstitch/pull/3332)
  
* Transfert de la valeur de longueur minimal de saut basée sur l'objet (si présente) depuis les satins sur les traits centraux générés automatiquement [#3154](https://github.com/inkstitch/inkstitch/pull/3154)

[En savoir plus](/fr/docs/satin-tools/#auto-route-satin-columns)

### Attacher des commandes aux objets sélectionnés

* Nous avons reçu de nombreuses plaintes concernant la difficulté de positionnement des symboles de commande.  Les commandes visuelles sont désormais dirigées par la position du centre du symbole, plutôt que par le point de contact du connecteur de commande [#3542](https://github.com/inkstitch/inkstitch/pull/3542).

Cela signifie que lorsque vous positionnez un symbole de départ, le point de départ de l'élément sera directement au centre du symbole. Les anciens fichiers seront automatiquement mis à jour.

![Commande de connecteur masquée](/assets/images/upcoming/3.2.0/hidden_connector_commands.png)

* Commandes de démarrage et d'arrêt unifiées pour différents types de points. Les anciens fichiers seront automatiquement mis à jour.

[En savoir plus](/fr/docs/commands/)

### Conversion en blocs de dégradé

* Insère des blocs de couleur dans un groupe et ignore les petits éléments [#3584](https://github.com/inkstitch/inkstitch/pull/3584)

[En savoir plus](/fr/docs/fill-tools/#convert-to-gradient-blocks)

### Mise à l'échelle des symboles de commande

`Commandes > Affichage > Mise à l'échelle des symboles de commande`

* Définit simultanément une taille unique pour toutes les commandes [#3329](https://github.com/inkstitch/inkstitch/pull/3329)

Veuillez noter que les transformations manuelles sur des groupes contenants des commandes peuvent influencer la taille réelle des symboles de commandes.

[En savoir plus](/fr/docs/commands/#scale-command-symbols)

### Test de polices 

`Gestion des polices > Test de police`

* Ajout d'une option  de tri des couleurs pour les polices multicolores [#3242](https://github.com/inkstitch/inkstitch/pull/3242).  Uniquement si la police prend en charge le tri des couleurs.

[En savoir plus](/fr/docs/font-tools/#font-sampling)

### Forcer des points d'arrêt

`Gestion des polices > Forcer des points d'arrêts`

* Ajout d'une option pour désactiver l'insertion de points d'arrêt en fonction de la distance (par exemple, pour ajouter des points d'arrêt uniquement après le dernier élément du glyphe) [#3559](https://github.com/inkstitch/inkstitch/pull/3559)

[En savoir plus](/fr/docs/font-tools/#force-lock-stitches)

### Lettrage

`Lettrage> Lettrage`

* Charge la dernière police sélectionnée et mémorise d'autres paramètres [#3498](https://github.com/inkstitch/inkstitch/pull/3498) [#3504](https://github.com/inkstitch/inkstitch/pull/3504)
* Prise en charge de plus de langues (écriture de droite à gauche) [#3432](https://github.com/inkstitch/inkstitch/pull/3358) [#3466](https://github.com/inkstitch/inkstitch/pull/3466)
* Simulateur du lettrage : affichage précis des points de départ et d'arrivée [#3358](https://github.com/inkstitch/inkstitch/pull/3358)
* Informations de taille uniformes (% et mm) [#3346](https://github.com/inkstitch/inkstitch/pull/3346)
* Ajout d'une option de tri par couleur pour les polices multicolores [#3242](https://github.com/inkstitch/inkstitch/pull/3242), [#3381](https://github.com/inkstitch/inkstitch/pull/3381). La police doit prendre en charge le tri par couleur.
* Options d'alignement du texte [#3382](https://github.com/inkstitch/inkstitch/pull/3382)

![Lettrage: plus d' options](/assets/images/upcoming/3.2.0/lettering.png)

[En savoir plus](/fr/docs/lettering/)

### Lettrage le long d'un chemin

`Lettrage > Lettrage le long d'un chemin`

Ajout d'une option pour le positionnement du texte le long du tracé (gauche, centre, droite, étirer)

![Texte aligné le long d'un tracé avec différentes options](/assets/images/docs/text_along_path_alignment.png)

[En savoir plus](/fr/docs/lettering/#lettering-along-path)

### Satin Multicolore

* Option d'ajustement des sous-couches [#3152](https://github.com/inkstitch/inkstitch/pull/3152)

[En savoir plus](/fr/docs/satin-tools/#multicolor-satin)

### Redwork

* Ajout d'une  option `Combiner` [#3407](https://github.com/inkstitch/inkstitch/pull/3407)
* Ajout d'une option `Garder les chemins originels` [#3407](https://github.com/inkstitch/inkstitch/pull/3407)

[En savoir plus](/fr/docs/stroke-tools/#redwork)

### Simulateur

* Ajout d'un bouton pour montrer la position de l'aiguille [#3616](https://github.com/inkstitch/inkstitch/pull/3616)
* Ajout d'une option permettant d'enregistrer la vitesse et de réouvrir ultérieurement le simulateur avec cette même vitesse  (facultatif) [#3420](https://github.com/inkstitch/inkstitch/pull/3420)
* Enregistre et recharge certains paramètres du simulateur (état des boutons : saut, coupe, changement de couleur, arrêt, point de pénétration de l'aiguille, bordure de page) [#3323](https://github.com/inkstitch/inkstitch/pull/3323)
* Afficher la page dans le simulateur [#3120](https://github.com/inkstitch/inkstitch/pull/3120)

[En savoir plus](/fr/docs/visualize/#simulator)

### Prévisualisation du plan de broderie

* Amélioration du filtre réaliste [#3222](https://github.com/inkstitch/inkstitch/pull/3222)

[En savoir plus](/fr/docs/visualize/#stitch-plan-preview)

### Trait en Effet de chemin satin 

* Prend en compte les transformation  (seulement pour les effets de chemin satin avec chemin spécifique) [#3500](https://github.com/inkstitch/inkstitch/pull/3500)

[En savoir plus](/fr/docs/satin-tools/#stroke-to-live-path-effect-satin)

### Résolution de problèmes

* Le regroupement en groupes  permet d'afficher/désafficher des types d'erreur  ou d'avertissement [#3486](https://github.com/inkstitch/inkstitch/pull/3486)
* Ajout d'un fond au texte de résolution des problèmes [#3357](https://github.com/inkstitch/inkstitch/pull/3357)

[En savoir plus](/fr/docs/troubleshoot/#troubleshoot-objects)

### Délier les clones

* Ajout d'une option pour grouper ou nous les éléments déliés [#3624](https://github.com/inkstitch/inkstitch/pull/3624)

[En savoir plus](/fr/docs/edit/#unlink-clone)

## Extensions supprimées

### Mise à jour de la liste des glyphes

A  été remplacé par l'extension bien plus puissante
[Editer le fichier  JSON ](/docs/font-tools/#edit-json)  [#3380](https://github.com/inkstitch/inkstitch/pull/3380)

### Installer des palettes de couleur de fil (pour Inkscape)

Déplacé vers  `Installer des modules complémentaires pour Inkscape`

[En savoir plus](/fr/docs/install-addons/)

## Mises a jour relatives aux types de points de broderie

### Point de départ et d'arrivée automatiques

Les remplissages et les colonnes satin commencent désormais automatiquement au point le plus proche de l'élément précédent et se terminent au point le plus proche de l'élément suivant [#3370](https://github.com/inkstitch/inkstitch/pull/3370).

Le comportement est adaptable et, bien sûr, les commandes de début et de fin fonctionnent toujours.

![Deux satins se rejoignant en un point, rendu sans saut](/assets/images/upcoming/3.2.0/start_at_nearest_point.png)

### Découpes

Les découpes sont désormais facilement accessibles dans Ink/Stitch sous toutes leurs formes. Elles sont particulièrement utiles en combinaison avec l'outil Redwork.

* **Groupes :** Ink/Stitch peut désormais analyser les découpes appliqués aux groupes [#3261](https://github.com/inkstitch/inkstitch/pull/3261).

![Groupes avec découpe](/assets/images/tutorials/mandala/lettremandala.svg)

* **Découpes d'effet** permettent d'utiliser une découpe inversée ([#3364](https://github.com/inkstitch/inkstitch/pull/3364)).

  ![découpes inversées](/assets/images/galleries/fonts/decadent_flowers_monogram/IMG_5211.jpg)

### Clones

* Les clones clonent désormais également les commandes attachées à l'élément et à ses enfants [#3086](https://github.com/inkstitch/inkstitch/pull/3086)

[En savoir plus](/fr/docs/stitches/clone/)

### Remplissage par contour

* Ajout d'une option Élargir [#3462](https://github.com/inkstitch/inkstitch/pull/3462)

[En savoir plus](/fr/docs/stitches/contour-fill/)

### Remplissage en dégradé  linéaaire

* Ajout d'une  option de randomisation au remplissage en dégradé linéaire[#3311](https://github.com/inkstitch/inkstitch/pull/3311)

[En savoir plus](/fr/docs/stitches/linear-gradient-fill/)

### Point manuel

* Ajout d'une option de répétitions au point manuel [#3312](https://github.com/inkstitch/inkstitch/pull/3312)

[En savoir plus](/fr/docs/stitches/manual-stitch/)

### Broderie ondulée

* Option de placement manuel des points pour les réplications [#3256](https://github.com/inkstitch/inkstitch/pull/3256)
* Ajout  d'une option pour broder la grille en premier [#3436](https://github.com/inkstitch/inkstitch/pull/3436)
* Ondulations guidées par un satin

  ![Ondulations guidées par un satin](/assets/images/docs/ripple_satin_guide.svg)

  * Option pour choisir ou non d'inverser une réplication sur deux 
  * Ajout possible de lignes d'ancrage pour aligner les réplications sur les traverses du satin de guidage [#3436](https://github.com/inkstitch/inkstitch/pull/3436)

  [En savoir plus](/fr/docs/stitches/ripple-stitch/#satin-guide)

###  Colonnes Satin

* Par défaut elles commencent et terminent au point le plus proche [#3423](https://github.com/inkstitch/inkstitch/pull/3423)

  ![Automated start and end point for satin column](/assets/images/upcoming/3.2.0/satin_start_end.png)
* Ajout des commandes de début et fin pour les satins [#3315](https://github.com/inkstitch/inkstitch/pull/3315)

  ![Start/end command for satin columns](/assets/images/upcoming/3.2.0/satin_start_end_command.png)

[En savoir plus](/fr/docs/stitches/satin-column/)

## Palettes

* Mise à jour de `InkStitch Madeira Rayon.gpl` [#3444](https://github.com/inkstitch/inkstitch/pull/3444)
* Isacord polyester: ajout de la couleur `0713 Lemon`  [#3225](https://github.com/inkstitch/inkstitch/pull/3225)

## Export / Import

Voir la [liste complète des formats pris en compte](/fr/docs/file-formats/)

### Nouveaux formats d'export

TBF

Longarm Quilting: PLT, QCC

### Nouveaux formats d'import

Longarm Quilting: PLT, QCC, IQP

### GCODE

* Valeurs RGB personnalisées [#3530](https://github.com/inkstitch/inkstitch/pull/3530)
* JUMP personnalisé

### Lettrage par lot

Ink/Stitch permet maintenant d'exporter plusieurs fichiers avec des textes différents en une seule fois. Pour un texte le long d'un tracé, il est possible d'utiliser un chemin avec un label spécifié pour définir le tracé.

![Un écusson avec 4 noms différents](/assets/images/docs/batch-lettering.png)

[En savoir plus](/fr/docs/lettering/#batch-lettering)

## Versions

* Les versions Windows sont désormais signées gratuitement ([SignPath.io](https://about.signpath.io)) grace au certificat de la [SignPath Foundation](https://signpath.org). Nous leur sommes très reconnaissants de leur soutien.
* La version Windows 32 bits a été supprimée, car elle n'est plus prise en charge.
* Versions Linux disponibles pour 64 bits et 32 ​​bits.

## Du coté des Développeurs 

* Sew Stack (premières étapes) [#3133](https://github.com/inkstitch/inkstitch/pull/3133)

"Sew Stack" remplacera à terme "Paramètres" et contiendra ses fonctionnalités. Pour l'instant, il est invisible dans nos versions.
La boîte de dialogue des paramètres actuelle souffre de toutes les options ajoutées au fil des ans. Il est désormais difficile d'y trouver un paramètre spécifique, et encore plus difficile si vous ne connaissez pas encore le programme. Sew Stack vous aidera à organiser les paramètres.

Il n'est visible que lors des installations manuelles et ne s'affichera pas, sauf si « enable_sew_stack » est activé dans le fichier de configuration de débogage.
Veuillez noter que cela modifiera les points de début et de fin des éléments et ne doit être utilisé qu'à des fins de développement.
  

* Mise à jour du processus de mises  à jour [#3652](https://github.com/inkstitch/inkstitch/pull/3652)
  * removed win32 build
  * use geos source build only for linux32
  * set python version to 3.11 for all builds
  * sign only releases for windows
  * sign windows release with release certificate [#3613](https://github.com/inkstitch/inkstitch/pull/3613)
* Mypy type correctness [#3199](https://github.com/inkstitch/inkstitch/pull/3199)
* use get_user_dir [#3549](https://github.com/inkstitch/inkstitch/pull/3549)
* Migrate from appdirs to platformdirs [#3450](https://github.com/inkstitch/inkstitch/pull/3450)
* remove scipy dependency [#3483](https://github.com/inkstitch/inkstitch/pull/3483) [#3481](https://github.com/inkstitch/inkstitch/pull/3481)
* Update translations workflow [#3435](https://github.com/inkstitch/inkstitch/pull/3435)
* Add lmde6 32bit build [#3298](https://github.com/inkstitch/inkstitch/pull/3298)
* Update macos cloud build [#3291](https://github.com/inkstitch/inkstitch/pull/3291)
* Use colormath2 instead of colormath [#3266](https://github.com/inkstitch/inkstitch/pull/3266)
* make hook actually cancel the commit [#3235](https://github.com/inkstitch/inkstitch/pull/3235)
* linux package fix [#3210](https://github.com/inkstitch/inkstitch/pull/3210)
* arm64 python update [#3201](https://github.com/inkstitch/inkstitch/pull/3201)
* only style-check staged changes [#3186](https://github.com/inkstitch/inkstitch/pull/3186)
* Additional CI Improvements [#3174](https://github.com/inkstitch/inkstitch/pull/3174)
* CI: Added pytest, some speed improvements [#3135](https://github.com/inkstitch/inkstitch/pull/3135)

## Résolution de bugs

* fix ensure even center walk underlay repeats in auto_satin when value is empty [#3651](https://github.com/inkstitch/inkstitch/pull/3651)
* Prevent unwanted simulator scale transforms [#3637](https://github.com/inkstitch/inkstitch/pull/3637)
* Always update satin param to avoid actual param/rendering mismatch [#3647](https://github.com/inkstitch/inkstitch/pull/3647)
* Lettering, custom directories: do not try to read hidden directories [#3632](https://github.com/inkstitch/inkstitch/pull/3632)
* Simulator on macOS Ventura: update background color correctly [#3621](https://github.com/inkstitch/inkstitch/pull/3621)
* ignore palette files with wrong encoding [#3620](https://github.com/inkstitch/inkstitch/pull/3620)
* fix updater [#3583](https://github.com/inkstitch/inkstitch/pull/3583)
* Element info: take pattern into account [#3581](https://github.com/inkstitch/inkstitch/pull/3581)
* Autosatin: more efforts to keep the stroke width consistant [#3563](https://github.com/inkstitch/inkstitch/pull/3563)
* display stop commands in simulator and print preview [#3545](https://github.com/inkstitch/inkstitch/pull/3545)
* auto-route: apply transforms to ensure stroke width being unchanged [#3538](https://github.com/inkstitch/inkstitch/pull/3538)
* lettering: do not add commands on top of command connectors [#3528](https://github.com/inkstitch/inkstitch/pull/3528)
* Fix jump to trim: NoneType element error [#3525](https://github.com/inkstitch/inkstitch/pull/3525)
* stroke: as_multi_line_string ignore single point paths [#3491](https://github.com/inkstitch/inkstitch/pull/3491)
* Adapt simulator slider symbols to dark theme [#3475](https://github.com/inkstitch/inkstitch/pull/3475)
* Auto-run: try harder to avoid networkx issues [#3457](https://github.com/inkstitch/inkstitch/pull/3457)
* Improve handling of symbols [#3440](https://github.com/inkstitch/inkstitch/pull/3440)
* Lettering: ignore auto-satin setting in the json file when there is no satin [#3434](https://github.com/inkstitch/inkstitch/pull/3434)
* Fix issue in preferences when value is 0.0 [#3430](https://github.com/inkstitch/inkstitch/pull/3430)
* Exclude invisible from node_to_elements directly [#3424](https://github.com/inkstitch/inkstitch/pull/3424)
* Cache: reset on operational error [#3421](https://github.com/inkstitch/inkstitch/pull/3421)
* Update README [#3405](https://github.com/inkstitch/inkstitch/pull/3405)
* Fix an other FloatingPointError [#3404](https://github.com/inkstitch/inkstitch/pull/3404)
* Minimize multi shape tartan jumps [#3386](https://github.com/inkstitch/inkstitch/pull/3386)
* Lettering: prevent duplicated output [#3365](https://github.com/inkstitch/inkstitch/pull/3365)
* Cut satin column: add more rungs when rails are intersecting [#3344](https://github.com/inkstitch/inkstitch/pull/3344)
* Fix jump to stroke transform glitch [#3306](https://github.com/inkstitch/inkstitch/pull/3306)
* Make remove commands more robust for broken commands with active selection [#3288](https://github.com/inkstitch/inkstitch/pull/3288)
* Avoid code repetition in paths detection [#3282](https://github.com/inkstitch/inkstitch/pull/3282)
* Thread catalog: fix broken path [#3281](https://github.com/inkstitch/inkstitch/pull/3281)
* Clone: do not fixup href [#3277](https://github.com/inkstitch/inkstitch/pull/3277)
* Prevent zerodivision error for zero length segments [#3268](https://github.com/inkstitch/inkstitch/pull/3268)
* Set svg version when importing an embroidery file [#3276](https://github.com/inkstitch/inkstitch/pull/3276)
* Redwork/Auto-Run: keep stroke width [#3264](https://github.com/inkstitch/inkstitch/pull/3264)
* Fix 'None'-string confusions in style [#3243](https://github.com/inkstitch/inkstitch/pull/3243)
* Print pdf: prevent rendering original paths [#3262](https://github.com/inkstitch/inkstitch/pull/3262)
* Avoid error message on info panel update [#3246](https://github.com/inkstitch/inkstitch/pull/3246)
* Satin column: ignore single point paths [#3244](https://github.com/inkstitch/inkstitch/pull/3244)
* Fix select redwork top layer [#3230](https://github.com/inkstitch/inkstitch/pull/3230)
* Fix gradient style [#3200](https://github.com/inkstitch/inkstitch/pull/3200)
* Fix clones with NoneType hrefs [#3196](https://github.com/inkstitch/inkstitch/pull/3196)
* Fixed hidden objects being stitched out when cloned (Fix #3167) [#3171](https://github.com/inkstitch/inkstitch/pull/3171)
* Fixed transforms on cloned commands [#3160](https://github.com/inkstitch/inkstitch/pull/3160)
* fill: ensure polygon in pull comp adjusted shape [#3143](https://github.com/inkstitch/inkstitch/pull/3143)
* add wxpython abort message (as alternative to stderr output) [#3145](https://github.com/inkstitch/inkstitch/pull/3145)
* fix fills without underpath and bad start-end positions [#3141](https://github.com/inkstitch/inkstitch/pull/3141)
* satin troubleshoot: do not fail on satins without rails [#3148](https://github.com/inkstitch/inkstitch/pull/3148)
* auto satin: filter zero length strokes as well [#3139](https://github.com/inkstitch/inkstitch/pull/3139)
* Disable darkmode symbols for windows (darkmode in windows doesn't work as excepted) [#3144](https://github.com/inkstitch/inkstitch/pull/3144)
* Fix simulator slider dark theme issue [#3147](https://github.com/inkstitch/inkstitch/pull/3147)
* skip empty gradient blocks [#3142](https://github.com/inkstitch/inkstitch/pull/3142)
* Simulator: toggle info and preferences dialog [#3115](https://github.com/inkstitch/inkstitch/pull/3115)

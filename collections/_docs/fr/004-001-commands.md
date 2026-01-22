---
title: "Commandes visuelles"
permalink: /fr/docs/commands/
last_modified_at: 2025-12-31
toc: true
---
Les commandes visuelles peuvent être utilisées pour spécifier des informations complémentaires sur la manière de broder. Elles peuvent par exemple être utilisées pour dire à la machine de couper le fil après avoir brodé un élément ou pour spécifier un arrêt par exemple pour ajouter le tissu d'un appliqué plus facilement.

Toutes les machines à broder ne sont pas capable de comprendre ces commandes. Si ça ne fonctionne pas bien pour vous, lisez le manuel de vos machines pour vérifier leur capacités.{: .notice--warning }

Dans `Extensions > Ink/Stitch  > Commandes` vous trouverez quatre options

* [Ajouter des commandes](#ajouter-des-commandes-)
* [Ajouter des commandes de calque](#ajouter-des-commandes-de-calque-)
* [Attacher des commandes à l'objet sélectionné](#attacher-des-commandes-aux-objets-sélectionnés-)
* [Affichage](#affichage)

**Need to duplicate objects with commands?** A common way to copy objects in Inkscape is duplicate. Before duplicating objects with commands, ensure that `Relink Duplicated Clones` in `Edit > Preferences > Behavior > Clones` is enabled.
{: .notice--info }

Pour déplacer une commande, déplacer le marqueur seulement, le connecteur suivra.
{: .notice--info }

## Ajouter des Commandes ...{#add-commands-}

Ces commandes affectent l’ensemble du motif de broderie.


### ![origine](/assets/images/docs/visual-commands-origin.jpg) Origine

Spécifie l'origine (point (0,0)) du fichier de broderie. Particulièrement utile pour les personnes qui ont accès à tout l'espace de broderie possible pour leur machine, indépendamment du cadre utilisé.

### ![stop position](/assets/images/docs/visual-commands-stop-position.jpg) Position d'arrêt

La machine à broder déplace l'aiguille jusqu'à ce point avant chaque commande d'attêt. Cela permet entre autre de déplacer le cadre de broderie vers l'utilisateur pour faciliter les étapes d'un appliqué.


## Ajouter des commandes de calque ...{/#add-layer-commands-}

Ces commandes seront ajoutées au calque sélectionné.

### ![ignore-layer](/assets/images/docs/visual-commands-ignore-layer.jpg) Ignorer le calque

Aucun objet de ce calque ne sera exporté dans les fichiers de broderie. Cette commande est couramment utilisée dans les fichiers des tutoriels lorsqu'on ne veut pas que Ink/Stitch brode les textes explicatifs.


## Attacher des commandes aux objets sélectionnés ...{#attach-commands-to-selected-objects-}

Ces commandes seront attachées aux objets actuellement sélectionnés.

Il est recommandé d’ajouter les commandes via les extensions:

* Sélectionnez un ou plusieurs objets
* Lancez `Extensions > Ink/Stitch  > Commandes > Attacher commandes ...`
* Activez les commandes souhaitées et cliquez sur appliquer
* Commandes Départ/Stop/Coupe: Le centre du symbole est le point auquel l'effet sera appliqué.

### ![starting-point-symbol](/assets/images/docs/visual-commands-start.jpg) ![ending point symbol](/assets/images/docs/visual-commands-end.jpg) Position de départ/de fin

Définit (1) le point de départ (2) le point d'arrivée d'un remplissage ou de colonnes satin.

###  ![auto-route-runing-starting-position-symbol](/assets/images/docs/visual-commands-auto-route-running-stitch-start.jpg) ![auto route  ending position symbol](/assets/images/docs/visual-commands-auto-route-running-stitch-end.jpg)  Position de départ/de fin pour l'agencement automatique

Définit le point de départ (1) ou le point final (2) de l'agencement automatique.

N'utiliser qu'un point de départ et qu'un point d'arrivée par agencement automatique.
{: .notice--warning}

Les agencements automatiques peuvent être effectués sur les satins ([Outils: Satin > Agencement automatique de Colonne Satin](/docs/satin-tools/#auto-route-satin-columns)) ou sur les traits.

Les  traits ont deux formes différentes d'agencement automatique:

* [Outils: Trait > Agencement automatique de points droits. ...](/fr/docs/stroke-tools/#autoroute-running-stitch) (un ou deux passages par  trait)
* [Outils: Trait > Redwork](/fr/docs/stroke-tools/#redwork) (exactement deux passages par trait)

Redwork n'utilise  que le  point  de départ, car  Redwork commence et termine toujours au même endroit.

### ![ripple-stitch-target-symbol](/assets/images/docs/visual-commands-ripple-target.png) Position de la cible

Définit la position cible d'une broderie ondulée ou d'un remplissage circulaire.

### ![Point de partage de colonne satin](/assets/images/docs/visual-commands-satin-cut-point.jpg) Point de partage de la colonne satin

Fractionner une colonne satin au point spécifié par cette commande. Après le placement de la commande, exécutez la commande "[Scinder une colonne satin](/fr/docs/satin-tools/#scinder-une-colonne-satin)".

### ![stop-symbol](/assets/images/docs/visual-commands-stop.jpg) Stop (pause machine) après avoir brodé cet objet

Les machines à broder commerciales qui ont plusieurs aiguilles passent normalement d’une couleur à l’autre sans pause. Parfois, vous *voulez* une pause (par exemple pour couper le tissu appliqué), donc "STOP après" ajoute un changement de couleur supplémentaire qui peut être affecté à une instruction d'arrêt spéciale à l'aide de l'interface utilisateur de la machine (par exemple C00 sur les machines Barudan). Les utilisations courantes de cette méthode sont l’application de mousse , l'appliquer du tissu appliqué et / ou même vouloir ralentir la machine à un certain endroit pour certains types de broderie sans avoir à surveiller la machine.

### ![trim-symbol](/assets/images/docs/visual-commands-trim.jpg) Couper le fil après avoir brodé cet objet

"Couper après" indique à la machine à broder de couper le fil une fois que l'objet désigné a été brodé. Toutes les machines domestiques ne prennent pas en charge la fonction de coupe dans un bloc de couleur. Principalement utilisé pour empêcher le saut de fil entre les objets de broderie et pour éviter la coupe des fils après la broderie par l'opérateur.

### ![ignore symbol](/assets/images/docs/visual-commands-ignore.jpg) Ignorer cet object (ne pas le broder)

Les objets auxquels cette commande est associée seront exclus du plan de broderie.

## Supprimer les commandes {#delete-commands}

### Supprimer une commande particulière.

Sélectionnez  le groupe de commande et supprimez le. 
### Supprimer toutes les commandes du document

*Lancez `Extensions > Ink/Stitch > Résolution des problèmes > Supprimer tous les paramètres de broderie`
* Choisissez tout ou les types de commandes spécifiques que vous souhaitez supprimer du document
* Cliquez sur  `Appliquer`


## Saut en Coupe {#jump-to-trim-commannd}

Cette extension insère des commandes de coupe à la place des sauts.
{% include upcoming_release.html %}
Vous pouvez chosir entre une commande de coupe et une commande de stop.

**Info**:Ne pas utiliser cette extension avant d'avoir optimisé le chemin de broderie: il faut éviter au maximum les coupes de fil. Vous trouverez dans 
[optimisation du chemin de broderie](/tutorials/routing/) l'ensemble des outils qu'Ink/Stitch mets à votre disposition pour vous aider dans votre tâche d'optimisation.
{: .notice--info }

## Affichage {#view}

### Afficher Masquer les commandes des objets 

Bascule la visibilité des commandes. Les commandes restent fonctionnelles même si elles sont masquées.
`Extensions > Ink/Stitch > Commandes > Affichage > Afficher/Masquer les commandes  des objets`

### Mise à l'echelle des symboles de commande {#scale-command-symbols}

Défini la taille des symboles de commande dans le document tout entier : `Extensions > Ink/Stitch > Commandes > Affichage> Mise à l'echelle des symboles de commande.`

Il est possible d'utiliser le "live preview" pour visualiser la nouvelle  taille des symboles pendant la mise à l'échelle.

---
title: "Commandes visuelles"
permalink: /fr/docs/commands/
excerpt: ""
last_modified_at: 2022-01-14
---
Les commandes visuelles peuvent être utilisées pour spécifier des informations complémentaires sur la manière de broder. Elles peuvent par exemple être utilisées pour dire à la machine de couper le fil après avoir brodé un élément ou pour spécifier un arrêt par exemple pour ajouter le tissu d'un appliqué plus facilement.

Toutes les machines à broder ne sont pas capable de comprendre ces commandes. Si ça ne fonctionne pas bien pour vous, lisez le manuel de vos machines pour vérifier leur capacités.

{: .notice--warning }

## Attachez des commandes visuelles via l'extension

Il est recommandé d’ajouter des commandes via les extensions:

* Sélectionnez un ou plusieurs objets
* Lancez `Extensions > Ink/Stitch  > Commandes > Attacher commandes ...`
* Activez les commandes souhaitées et cliquez sur appliquer
* Commandes Départ/Stop/découpage: Le noeud final du connecteur le plus proche de l'objet est le point auquel l'effet sera appliqué.

Dans `Extensions > Ink/Stitch  > Commandes` vous trouverez trois options: ajouter des commandes, ajouter des commandes de calque et attacher des commandes à l'objet sélectionné.
### Ajouter des Commandes ...

Ces commandes affectent l’ensemble du motif de broderie.

![stop position](/assets/images/docs/visual-commands-stop-position.jpg) [Position d'arrêt](#-stop-position)

La machine à broder déplace l'aiguille jusqu'à ce point avant chaque commande d'attêt. Cela permet entre autre de déplacer le cadre de broderie vers l'utilisateur pour faciliter les étapes d'un appliqué.

![origine](/assets/images/docs/visual-commands-origin.jpg) [Origine](#-origine)

Spécifie l'origine (point (0,0)) du fichier de broderie. Particulièrement utile pour les personnes qui ont accès à tout l'espace de broderie possible pour leur machine, indépendement du cadre utilisé.


### Ajouter des commandes de calque ...

Ces commandes seront ajoutées au calque sélectionné.

![ignore-layer](/assets/images/docs/visual-commands-ignore-layer.jpg) [Ignorer le calque](#-ignore-layer)

Aucun objet de ce calque ne sera exporté dans les fichiers de broderie. Cette commande est couramment utilisée dans les fichiers des tutoriels lorsqu'on ne veut pas que Ink/Stitch brode les textes explicatifs.

### Attacher des commandes aux objets sélectionnés ...

Ces commandes seront attachées aux objets actuellement sélectionnés.

![starting-point-symbol](/assets/images/docs/visual-commands-start.jpg) ![ending point symbol](/assets/images/docs/visual-commands-end.jpg)   [Position de départ/de fin pour un remplissage](#-starting-point-symbol)

Définit  (1) le point de départ  (2) le point d'arrivée d'un remplissage.


![symbole de coupe](/assets/images/docs/visual-commands-trim.jpg) [Coupe](#-coupe-le-fil) le fil après avoir brodé l'objet

"Couper après" indique à la machine à broder de couper le fil une fois que l'objet désigné a été brodé. Toutes les machines domestiques ne prennent pas en charge la fonction de coupe dans un bloc de couleur. Principalement utilisé pour empêcher le saut de fil entre les objets de broderie et pour éviter la coupe des fils après la broderie par l'opérateur.

![symbole de stop ](/assets/images/docs/visual-commands-stop.jpg) [Stop](#-stop) (pause) la machine après avoir brodé cet objet (pour les appliqués, etc)

Les machines à broder commerciales qui ont plusieurs aiguilles passent normalement d’une couleur à l’autre sans pause entre elles. Parfois, vous * voulez * une pause (par exemple pour couper le tissu appliqué), donc "STOP après" ajoute un changement de couleur supplémentaire qui peut être affecté à une instruction d'arrêt spéciale à l'aide de l'interface utilisateur de la machine (par exemple C00 sur les machines Barudan). Les utilisations courantes de cette méthode sont l’application de mousse feuilletée après une broderie régulière. Appliquer du tissu appliqué et / ou même vouloir ralentir la machine à un certain endroit pour certains types de broderie sans avoir à surveiller la machine.

![ignore](/assets/images/docs/visual-commands-ignore.jpg) [Ignorer l'objet](#-ignore)

Les objets auxquels cette commande est associée seront exclus du plan de broderie.

![Point de partage de colonne satin](/assets/images/docs/visual-commands-satin-cut-point.jpg) [Point de partage de la colonne satin](#-point-de-partage-de-colonne-satin)

Fractionner une colonne satin au point spécifié par cette commande. Après le placement de la commande, exécutez la commande "[Scinder une colonne satin] (/fr/docs/satin-tools/#scinder-une-colonne-satin)".

![auto-route-satin-stitch-start](/assets/images/docs/visual-commands-auto-route-satin-stitch-start.jpg) ![auto-route-satin-stitch-end](/assets/images/docs/visual-commands-auto-route-satin-stitch-end.jpg)   [Position de départ/de fin pour auto route colonne satin](#-auto-route-satin-stitch-start)

Définit le point de départ (1) ou le point final (2) de la colonne auto route satin. Exécutez ensuite "[Remplissage automatique de Colonne Satin. ...](/fr/docs/satin-tools/#auto-route-satin-columns)".

[Télécharger le fichier exemple](/assets/images/docs/visual-commands-fill-stitch.svg){: download="visual-commands-fill-stitch.svg" title="Télécharger le fichier exemple"}

## Afficher Masquer les commandes des objets 
{% include upcoming_release.html %}

Bascule la visibilité des commandes. Les commandes restent fonctionnelles même si elles sont masquées.
`Extensions > Ink/Stitch > Commandes > Vue > Afficher/Masquer les commandes  des objets`

## Mise à l'echelle des symboles de commande
{% include upcoming_release.html %}

Défini la taille des symboles de commande dans le document tout entier

Set the size of command symbols in the entire document: `Extensions > Ink/Stitch > Commandes > Vue > Mise à l'echelle des symboles de commande.`

Il est possible d'utiliser le "live preview" pour visualiser la nouvelle  taille des symboles pendant la mise à l'echelle.

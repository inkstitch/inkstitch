---
title: "Commandes visuelles"
permalink: /fr/docs/commands/
excerpt: ""
last_modified_at: 2019-10-20
toc: true
---
## Installation

[Installer les Commandes](/docs/addons/) avant usage.

## Attachez des commandes visuelles via l'extension

Il est recommandé d’ajouter des commandes via les extensions:

* Sélectionnez un ou plusieurs objets
* Lancer `Extensions > Ink/Stitch  > Commandes > Attacher commandes ...`
* Activer les commandes souhaitées et appliquer
* Commandes Départ/Stop/découpage: Le noeud final du connecteur le plus proche de l'objet est le point auquel l'effet sera effectué.

Dans `Extensions > Ink/Stitch  > Commandes` vous trouverez trois options: ajouter des commandes, ajouter des commandes de calque et attacher des commandes à l'objet sélectionné.
### Ajouter des Commandes ...

Ces commandes affectent l’ensemble du motif de broderie.

![stop position](/assets/images/docs/visual-commands-stop-position.jpg) [Stop Position](#-stop-position)

![origine](/assets/images/docs/visual-commands-origin.jpg) [Origine](#-origin)

#### Ajouter des commandes de calque ...

Ces commandes seront ajoutées au calque sélectionné.

![symbole ignorer le calque ](/assets/images/docs/visual-commands-ignore-layer.jpg) Ignorer le calque

#### Attacher des commandes aux objets sélectionnés ...

Ces commandes seront attachées aux objets actuellement sélectionnés.

![symbole de point de départ](/assets/images/docs/visual-commands-start.jpg) Point de départ du remplissage

![symbole de point de fin](/assets/images/docs/visual-commands-end.jpg) Point de fin du remplissage

![symbole de coupe](/assets/images/docs/visual-commands-trim.jpg) [Coupe](#-trim) le fil après avoir brodé l'objet

![symbole de stop ](/assets/images/docs/visual-commands-stop.jpg) [Stop](#-stop) (pause) la machine parès avoir brodé cet objet (pour les appliqués, etc)

![symbole ignorer ](/assets/images/docs/visual-commands-ignore.jpg) Ignore l'objet

![symbole de découpage de point satin](/assets/images/docs/visual-commands-satin-cut-point.jpg) [Point de partage de la colonne satin](/docs/commands/#-satin-cut-point) (utiliser avec "Cut Satin Column")

![symbole de départ de auto route satin ](/assets/images/docs/visual-commands-auto-route-satin-stitch-start.jpg) Mode Auto-route satin  [position de départ](#--startingending-position-for-auto-route-satin)

![symbole de position de fin de auto route satin](/assets/images/docs/visual-commands-auto-route-satin-stitch-end.jpg) Auto-route satin  [position de fin](#--startingending-position-for-auto-route-satin)

### Attacher des commandes visuelles à la main
* Aller à `Objet > Symboles` oo taper `Shift+Ctrl+Y` pour accéder aux marqueurs via la boîte de dialogue des symboles.
* Selectionner "Ink/Stitch Commands" comme jeu de symboles.
![Jeux de symboles](/assets/images/docs/en/visual-commands-symbol-set.jpg)
* Faites glisser un marqueur sur votre canevas (peu importe où).
* Utiliser l'outil Créer des connecteurs (`Ctrl+F2`) pour dessiner une connexion entre le marqueur et l'objet de remplissage auquel il s'appliquera. Cela va ajouter un chemin de connecteur.
* Déplacer le marqueur va changer la position du connecteur pour correspondre au point choisi. Vous pouvez également déplacer manuellement les extrémités du connecteur. Le noeud final du connecteur le plus proche de l'objet de remplissage est le point de début ou de fin de la broderie.
  <div style="position: relative; padding-bottom: 50%; height: 0;">
    <iframe src="/assets/video/docs/visual-commands.m4v" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
  </div>
  
  [Télécharger le fichier exemple](/assets/images/docs/visual-commands-fill-stitch.svg){: download="visual-commands-fill-stitch.svg" title="Télécharger le fichier exemple"}

## Référence des commandes visuelles

### ![symbole de coupe](/assets/images/docs/visual-commands-trim.jpg) Coupe le fil

"Couper après" indique à la machine à broder de couper le fil une fois que l'objet désigné a été brodé. Toutes les machines domestiques ne prennent pas en charge la fonction de coupe dans un bloc de couleur. Principalement utilisé pour empêcher le saut de fil entre les objets de broderie et pour éviter la coupe des fils après la broderie par l'opérateur.
### ![ symbole stop](/assets/images/docs/visual-commands-stop.jpg) Stop
Les machines à broder commerciales qui ont plusieurs aiguilles passent normalement d’une couleur à l’autre sans pause entre elles. Parfois, vous * voulez * une pause (par exemple pour couper le tissu appliqué), donc "STOP après" ajoute un changement de couleur supplémentaire qui peut être affecté à une instruction d'arrêt spéciale à l'aide de l'interface utilisateur de la machine (par exemple C00 sur les machines Barudan). Les utilisations courantes de cette méthode sont l’application de mousse feuilletée après une broderie régulière. Appliquer du tissu appliqué et / ou même vouloir ralentir la machine à un certain endroit pour certains types de broderie sans avoir à surveiller la machine.

### ![position de stop](/assets/images/docs/visual-commands-stop-position.jpg) Stop position

La machine à broder va à ce point avant chaque commande d'arrêt. Cela permet de pousser le cadre de broderie vers l'utilisateur pour faciliter les étapes pour un appliqué.
### ![origine](/assets/images/docs/visual-commands-origin.jpg) Origine

Spécifie le point d'origine (0,0) pour les fichiers de broderie. La configuration des origines est particulièrement utile pour les personnes ayant un accès complet à l’ensemble du champ de couture dont leur machine est capable, quel que soit le cadre qu’elles utilisent.

### ![starting point symbol](/assets/images/docs/visual-commands-start.jpg) ![ending point symbol](/assets/images/docs/visual-commands-end.jpg)Position de départ/de fin pour un remplissage 

Defines the (1) starting or (2) ending point of an fill stitch area.

###  ![symbole de position de départ de auto route satin](/assets/images/docs/visual-commands-auto-route-satin-stitch-start.jpg) ![symbole de position de fin de auto route satin](/assets/images/docs/visual-commands-auto-route-satin-stitch-end.jpg) symbole de position de départ/de fin de auto route satin

Définit le point de départ (1) ou le point final (2) de la colonne auto route satin. Exécutez ensuite "[Colonne satin de routage automatique ...](/docs/satin-tools/#auto-route-satin-columns)".

### ![symbole de point de partagede colonne satin](/assets/images/docs/visual-commands-satin-cut-point.jpg) Point de partage de colonne satin

Fractionner une colonne satin au point spécifié par cette commande. Après le placement de la commande, exécutez la commande "[Cut Satin Column] (/ docs / satin-tools / # cut-satin-column)".

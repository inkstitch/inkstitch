---
title: "Colonne Satin"
permalink: /fr/docs/stitches/satin-column/
excerpt: ""
last_modified_at: 2023-04-28
toc: true
---
## Qu’est-ce que c’est

Le point satin est principalement utilisé pour les bordures, les lettres ou les petites zones de remplissage.

![Stitch Types - Satin Column](/assets/images/docs/stitch-type-satincolumn.jpg)

## Méthodes de création

Ink/Stitch offre plusieurs options pour créer des colonnes satin. Les trois premières méthodes permettent une conversion vers une colonne satin standard qui pourra ensuite être modifiée manuellement.

![Méthodes](/assets/images/docs/satin_methods.svg)

1. [Convertir ligne en satin](#1-convertir-ligne-en-satin): pour créer des colonnes satin de largeur constante
2. [Convertir ligne en Effet de Chemin satin](#2-convertir-ligne-en-effet-de-chemin-satin): colonne satin facilement modifiable avec un motif de contour optionnel
3. [Convertir "ligne en zigzag" en Satin](#3-convertir-ligne-en-zigzag-en-satin): une manière simple de créer les colonnes satin particulièrement bien adaptée aux tablettes graphiques et aux écrans tactiles.
4. [Création manuelle de Colonne Satin ](#4-création-manuelle-de-colonne-satin): prendre tout le contrôle sur la colonne satin

### 1. Convertir Ligne en Satin

* Choisir un trait (un objet avec une couleur de contour, mais pas de couleur de remplissage)
* Définissez l'épaisseur du contour à  la largeursouhaitée pour votre colonne satin.
* Lancer `Extensions > Ink/Stitch > Outils : Satin > Convertir Ligne en Satin`

Vous obtenez un chemin composite composé de 
  - deux rails qui correspondent aux bords longs de votre trait 
  - des traverses perpendiculaires aux rails qui indiquent la direction des points de broderie

* Utilisez tel quel ou modifiez les traverses ou les rails en déplaçant leur noeuds

* En option lancer `Extensions > Ink/stitch > Outils : Satin > Agencement automatique de colonnes satin...` après avoir sélectionné une ou plusieurs colonnes satins
Plus d'informations sur [Convertir ligne en satin](/fr/docs/satin-tools/#convertir-ligne-en-satin)

### 2. Convertir Ligne en Effet de Chemin Satin

Ceci peut être utilisé pour créer une colonne satin possédant  un motif sur son coutour ou dont la largeur est plus adaptable. Attention, si vous utilisez l'agencement automatique sur ce type de satin, l'effet de chemin sera appliqué et le chemin ne pourra plus être modifié que manuellement.


Utilisez `Chemin > Objet en chemin` pour convertir en colonne satin standard (colonne satin manuelle).
Notez que la largeur de la ligne n'a pas d'influence.
Pour plus d'information sur l'[effet de chemin satin ](/fr/docs/satin-tools/#convertir-ligne-en-effet-de-chemin-satin)

### 3. Convertir "Ligne en zigzag" en Satin

Cette méthode est particulierement adaptée aux écrans tactiles et aux tablettes graphiques

Plus d'information  sur [Convertir "ligne en zigzag" en satin](/fr/docs/satin-tools/#zigzag-line-to-satin)

### 4. Création manuelle de Colonne Satin

* Commencez par définir les rails de votre colonne satin : dessinez  **deux traits presque parallèles**. La future colonne satin se brodera en zigzag entre les deux rails, vous pouvez faire varier l'épaisseur de la colonne à votre guise, en faisant varier la distance entre les deux rails.

* Combinez ces deux traits avec `Chemin > Combiner` ou taper `Ctrl+K`.

* [Vérifier les directions de chemin](/fr/docs/customize/#activation-de-la-direction-des-chemins). Pour que la colonne satin fonctionne comme attendu, les deux rails doivent avoir la même direction.

Si ce n'est pas le cas Sélectionnez avec l' *Outil Editer les noeuds* (`N`) un noeud d'un des deux rails et faites `Chemin > Inverser`. Cela n'inversera que le rail sélectionné. Vous pouvez aussi agir sur la direction des rails dans le paramètrage.
 
* Ink/Stitch va dessiner des zig-zags entre les deux lignes : pour régler la direction des points de broderie, utilisez la méthode des noeuds ou la méthodes des traverses décrites ci-dessous.

* Ensuite, sélectionnez votre colonne satin et lancez les paramètres avec `Extensions > Ink/Stitch  > Paramètres` ou un  [raccourci clavier personnalisé](/fr/docs/customize/).

#### Méthode des noeuds

[![Bateau en colonne satin](/assets/images/docs/satin-column.jpg){: width="200x"}](/assets/images/docs/satin-column.svg){: title="Télécharger le fichier SVG" .align-left download="satin-column.svg" }
Selon la complexité de votre conception, cette méthode peut prendre beaucoup de temps, car les deux rails doivent avoir exactement le **même nombre de noeuds** (Cela signifie que chaque rail sera composé d'un nombre égal de courbes de Bézier). 

Chaque paire de noeuds (une paire de noeud est constituée d'un noeud sur chaque rail, en commençant par la paire des  noeuds initiaux des deux rails, puis la paire des deuxième noeuds de chaque rail, etc....) agit comme un "point de contrôle": Ink/Stitch garantira qu'un "zag" finisse par aller d'un noeud  de chaque paire à l'autre noeud de la paire.

#### Méthode des traverses

[![Chapeau du chef en colonne satin](/assets/images/docs/satin-column-rungs-example.jpg){: width="200x"}](/assets/images/docs/satin-column-rungs.svg){: title="Télécharger le fichier SVG" .align-left download="satin-column-rungs.svg" }

La méthode des traverses vous donnera plus de contrôle sur le rendu de la colonne satin. Un bon positionnement des points sur chacun des deux rails aide à bien orienter les points. 

Cependant, il existe des situations dans lesquelles vous devez ajouter manuellement des lignes de direction ("traverses") pour les colonnes satin:
* Quelques angles difficiles
* Dessins complexes où les déplacements de points sont à la fois difficiles et longs
* Situations spéciales dans lesquelles vous souhaitez que les instructions de point soient particulières
{: style="clear: both;" }

**Ajout manuel de traverses**

* Assurez-vous que le chemin de la colonne satin existant (avec les deux rails comme sous-chemins) est sélectionné avec l'outil Éditer les noeuds.
* Appuyez sur `P` ou sélectionnez l'outil Crayon.
* Maintenir la touche `Maj`enfoncée.
* Cliquez une fois là où vous souhaitez le début de la traverse.
* Cliquez une seconde fois à la fin de la traverse.
  [![Traverse en Action](https://edutechwiki.unige.ch/mediawiki/images/thumb/6/68/InkStitch-round-bird-2.png/300px-InkStitch-round-bird-2.png)](https://edutechwiki.unige.ch/mediawiki/images/6/68/InkStitch-round-bird-2.png)

  Dessin original de [Liv Iko](https://thenounproject.com/liv_iko/collection/birds/?i=898697) modifié par [EDUTECH Wiki](https://edutechwiki.unige.ch/en/InkStitch)
{: style="font-size: 0.5rem;"}

**Info:** Nous recommandons fortement d'utiliser au moins trois traverses. Si vous utilisez exactement deux traverses (et deux rails), il est difficile pour Ink/stitch de décider qui est qui.
{: .notice--warning }

**Info:** Ink/Stitch examine chaque tronçon de rail, c'est à dire chaque paire de courbes de Bézier individuellement . Il choisit la plus longue des deux et détermine combien de zig-zags seront nécessaires pour satisfaire le réglage *espacement de zig-zag*. De sorte que le rail le plus long n'aura jamais des points clairsemés comme dans un zig-zag simple.<br /><br />Toutefois, cela signifie aussi que le rail le plus court aura une densité de points supérieure à celle spécifiée. Soyez prudent lorsque vous concevez des courbes prononcées, parce que *broder à une densité trop élevée peut faire un trou dans le tissu*!. Le paramètrage des points courts peut aider.
{: .notice--info }

## Paramètres

`Extensions > Ink/Stitch  > Paramètres` vous donne la possibilité de parfaire votre colonne de satin et d’utiliser une sous-couche.

Les colonnes satin permettent trois types de sous-couche différents que vous pouvez utilisez ensemble ou séparement.

Lisez aussi [cet excellent article](https://www.mrxstitch.com/underlay/) sur les motifs en colonnes satin.

Certains de ces paramètres ne font pas partie de la version récente.
{: .notice--info}

### Couche supérieure du satin

|Paramètres||Description|
|---|---|--|
|Colonne satin personnalisée   | ☑ |Doit être activé pour que ces paramètres prennent effet|
|Méthode                       | | Choisir `Colonne Satin`|
|Longueur maximale du point    | ![Maximum stitch length](/assets/images/docs/params-satin-maximum_stitch_length.png) | Les points plus longs seront découpés en plusieurs points.
|Décalage des points courts    | ![Short Stitch example](/assets/images/docs/params-satin-short_stitch_inset.png) |Les points dans les zones à forte densité seront raccourcis de ce pourcentage.|
|Distance des points courts    | ![Short Stitch example](/assets/images/docs/params-satin-short_stitch_distance.png) |Faire des points courts si la distance entre les crêtes est inférieure à cette valeur.|
|Espacement de Zig-zag         |![exemple d'espacement de zig-zag](/assets/images/docs/params-satin-zig-zag-spacing.png)|la distance de crête à crête entre les zig-zag|
|Pourcentage de compensation d'étirement |![Pull compensation example](/assets/images/docs/params-satin-pull_compensation.png)|Compensation d'étirement proportionelle à la largeur du point satin. Deux valeurs séparées par un espace peuvent être utilisées pour un effet asymétrique.|
|Compensation d'étirement      |![exemple de compensation d'étirement](/assets/images/docs/params-satin-pull_compensation.png)|Les points Satin [resserrent le tissu](/fr/tutorials/push-pull-compensation/),   il en résulte une colonne plus étroite que votre dessin dans Inkscape. Ce paramètre étend chaque paire de pénétrations d’aiguilles vers l’extérieur de la colonne satin. Vous devrez expérimentalement déterminer le montant de la compensation en tenant compte de votre tissu, de votre fil et de votre stabilisateur.<br /> Deux valeurs séparées par un espace peuvent être utilisées pour un effet asymétrique.<br /> Une valeur négative contracte.|
Inverser la direction des rails    |![Reverse Rung](/assets/images/docs/satin-reverse-rung.png) |Ceci peut aider si le rendu de votre satin est étrange. <br />Options:<br /> ◦ Automatique, valeur par défaut, cherche à détecter et corriger le cas des rails ayant des directions opposées.  <br />◦ Ne pas inverser désactive la détection automatique <br />◦ Inverser la direction du premier rail <br />◦ Inverser la direction du second rail <br />◦ Inverser la direction des deux rails
|Échanger les rails            |☑ |Échange les deux rails de la colonne satin, ce qui affecte le côté de fin de broderie ainsi que tous les paramètres asymétriques|
|Autoriser les points d'arrêts | ☑|Ajoute un point d'arrêt à la ou les positions choisies.|
|Forcer les points d'arrêts    | ☑ | Force un point d'arrêt après l'objet indépendament de la valeur de "Saut de fil" dans les Préférences d'Ink/Stitch|
|Point d'ancrage               | |Choisir le [style désiré](/fr/docs/stitches/lock-stitches/).|
|Point d'arrêt                 | |Choisir le [style désiré](/fr/docs/stitches/lock-stitches/).|
|Couper après                  |☑ | Coupe le fil après avoir brodé cet objet|
|Arrêter après                 |☑ |Fait faire une pause à la machine après avoir brodé cet objet. Si une position d'arrêt a été définie, elle est rejointe par un saut avant la pause. |
|Pourcentage maximum d'augmentation aléatoire de la largeur du satin |![Random width increase](/assets/images/docs/params-satin-random-width-increase.png)| Élargir le satin d'au plus ce pourcentage. Deux valeurs séparées par un espace peuvent être utilisées pour un effet asymétrique.|
|Pourcentage maximum  de diminution aléatoire de la largeur du satin |![Random width decrease](/assets/images/docs/params-satin-random-width-decrease.png)| Réduire la largeur du satin d'au plus ce pourcentage. Deux valeurs séparées par un espace peuvent être utilisées pour un effet asymétrique.|
|Pourcentage aléatoire pour l'espacement zigzag               |![Random zigzag spacing](/assets/images/docs/params-satin-random-zigzag-spacing.png)|Pourcentage maximum d'augmentation à appliquer à  l'espacement zigzag.|
|Déplacement aléatoire pour le découpage des points           |![Random split stitch jitter](/assets/images/docs/params-satin-random-split-stitch-jitter.png)| Si le découpage totalement aléatoire des points est activé, ce paramètre rend la longueur du point aléatoire, sinon, le déplacement aléatoire du découpage se fait autour de sa position normale (sans appliquer d'aléatoire)|
|Découpage totalement aléatoire des points                     | ☑ |Si activé, le découpage des points est totalement  aléatoire (ce qui risque de modifier le nombre de points par zig (ou par zag)), sinon, le nombre de points par zig est conservé, mais leur position sur le zig peut varier du déplacement aléatoire paramétré.|
|Longueur minimum du point si découpage totalement aléatoire   |  | Par défaut, prend la valeur de la longueur maximum du point. Une valeur inférieure permet une meilleure transition entre les points découpés et les points non découpés.|
|Graine Aléatoire              | | Utiliser cette graine aléatoire pour le calcul du plan de broderie. Si vide, utilise l'identificateur de l'élément. Relancer le dé si vous n'êtes pas satisfait du résultat.|
{: .params-table }

### Sous-couche centrale

C'est une rangée aller-retour de points droits au centre de la colonne. C'est peut-être tout ce dont vous avez besoin pour de fines colonnes de satin. Vous pouvez également l'utiliser comme base pour une sous-couche plus élaborée.
![Exemple de paramètres de sous-couche centrée](/assets/images/docs/params-center-walk-underlay-example.jpg)

![Paramètres de sous-couche centrée](/assets/images/docs/fr/params-satincolumn-underlay-centerwalk.jpg)

|Paramètre      |Description|
|---|---|
|Longueur de point |Longueur de point (en mm)|
|Répéter | Un nombre impair renverse la direction de broderie de la colonne satin, la broderie commencera et terminera au même endroit.|
|Position      |Position de la sous-couche entre les rails. 0% est le long du premier rail, 50% est centré, 100% est le long du second  rail.|
{: .table-full-width }

#### Sous-couche de contour

Il s’agit d’une rangée de points droits d’un bout de la colonne à l’autre. Les lignes sont placées à la distance du bord de la colonne que vous spécifiez. Pour les colonnes de petite ou moyenne largeur, cela peut suffire.

![Exemple de sous-couche contour](/assets/images/docs/params-contour-underlay-example.jpg)

![Paramètres de sous-couche contour](/assets/images/docs/fr/params-satincolumn-underlay-contour.jpg)

|Paramètres      |Description|
|---|---|
|Longueur de point           |Longueur de point (en mm)|
|Décalage de sous-couche contour (fixe) |décale d'une valeur fixe pour couvrir la sous-couche entièrement par la couche supérieure. Les valeurs négatives sont possibles.|
|Décalage de sous-couche contour (proportionel) |décale proportionellement à la largeur du satin pour couvrir la sous-couche entièrement par la couche supérieure. Les valeurs négatives sont possibles.|
{: .table-full-width }

#### Sous-couche zig-zag

Il s’agit essentiellement d’un aller-retour en point satin de faible densité. Ajouté à la sous-couche de contour, vous obtenez la "sous-couche allemande" mentionnée dans [cet article](https://www.mrxstitch.com/underlay/). Pour les colonnes larges ou les tissus difficiles, vous pouvez utiliser les trois types de sous-couches ensemble.

![Exemple de paramètres de sous-couche zig-zag](/assets/images/docs/params-zigzag-underlay-example.jpg)

![Paramètres sous-couche zig-zag](/assets/images/docs/fr/params-satincolumn-underlay-zigzag.jpg)

|Paramètres              |Description|
|---|---|
|Décalage(proportionel)       |Décalage en pourcentage de la largeur pour couvrir la sous-couche entièrement par la couche supérieure. Valeurs négatives possibles. Par défaut la moitié de la valeur est appliquée de chaque coté. Il est possible d'entrer deux valeurs séparées par un espace pour un effet asymétrique.|
|Décalage(fixe)        |Décalage pour couvrir la sous-couche entièrement par la couche supérieure. Valeurs négatives possibles. Par défaut la moitié de la valeur est appliquée de chaque coté. Il est possible d'entrer deux valeurs séparées par un espace pour un effet asymétrique.|
|Longueur maximum du point  | ![Longueur maximum du point](/assets/images/docs/params-satin-maximum_stitch_length.png) | Les points plus longs seront découpés en plusieurs points|
|Espacement Zig-Zag      |La distance crête à crête entre zig-zags.|
{: .table-full-width }

## Outils Satin

Assurez-vous de lire [Outils: Satin](/fr/docs/params/satin-tools/);
Cela vous facilitera grandement la vie avec les colonnes en satin.

## Fichiers exemple avec des colonnes satin

{% include tutorials/tutorial_list key="stitch-type" value="Satin Stitch" %}

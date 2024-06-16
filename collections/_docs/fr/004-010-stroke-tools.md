---
title: "Outils: Trait"
permalink: /fr/docs/stroke-tools/
last_modified_at: 2024-06-16

toc: true
---
## Agencement automatique de points droits {#autoroute-running-stitch}

Cet  outil **remplace** un ensemble de chemins paramétrés en points droits par un nouvel ensemble de chemins paramétrés en points droits  empilés dans un ordre logique de broderie qui évite autant que faire se peut les sauts de fil. Lorsque nécessaire des chemins (chemins de dessous) sont ajoutés, sous les chemins existants pour assurer les connexions . Les points droits résultants conservent tous les  paramètres des points droits originaux tels que la longueur de point droit, la tolérance, le  nombre de répétitions, le nombre de répétitions pour le point triple.  Les chemins de dessous ne conservent que la longueur du point, le nombre de répétitions est remis à un et et le nombre de répétitions de point triple à zéro.

Cette extension cherche à minimiser la longueur des sauts de fil inévitables.

### Usage

- Sélectionnez tous les chemins paramétrés en points droits que vous souhaitez organiser
- Exécutez `Extensions > Ink/Stitch > Outils : Trait > Agencement automatique  de points droits`
- Choisir les options désirées et cliquer sur "Appliquer et quitter"
  
Par défaut, l'extension choisira de commencer par le noeud le plus à gauche et de terminer par le noeud le plus à droite même si ces noeuds ne sont pas des noeuds terminaux. Vous pouvez attacher les commandes " Début/Fin d'agencement automatique de point droit" pour forcer les positions de début et de fin.
{: .notice--info }

### Options

- Cocher **Ajouter des noeuds aux intersections** donnera un meilleur résultat de routage, avec des chemins de dessous qui auront leurs extrémités aux intersections ou aux noeuds terminaux. Ne décocher cette option que si vous avez manuellement ajouté des noeuds là où vous souhaitez les coupures de chemin.
- Cocher **Préserver l'ordre des points droits** si vous souhaitez préserver l'ordre initial des chemins paramétrés en points droits.
- Cocher **Couper les sauts de fil**  pour  utiliser des commandes de coupe plutôt que des sauts de fil. Les commandes de coupe sont ajoutées au svg, vous pouvez donc ensuite les modifier/supprimer à votre guise.


## Satin en Trait {#convert-satin-to-stroke}

Convertir le satin en trait converti une colonne satin en un trait qui correspond à sa ligne centrale. Ceci peut être utile si vous décider tardivement dans le processus  de transformer une colonne satin en point droit. Vous pouvez aussi l'utiliser pour modifier la largeur d'une colonne satin lorsque la compensation d'étirement ne convient pas bien. Dans ce cas, utilisez cette fonction pour convertir votre colonne satin en point droit, puis modifier l'épaisseur du trait dans le panneau Fond et Contour puis lancez l'extension "Outils Satin > convertir ligne en satin".
Ceci fonctionne d'autant mieux que la largeur de la colonne satin initiale est constante.

![Satin to Stroke example](/assets/images/docs/en/satin_to_stroke.png)

### Usage

1. Sélectionez la ou les colonnes satin que vous souhaitez convertir en point droits.
2. Exécutez  `Extensions > Ink/Stitch > Outils: Trait > Satin en Trait...`
3. Choisissez si vous vous souhaitez ou non conserver les colonnes satins sélectionnées.
4. Cliquez sur Appliquer


## Remplissage en Trait {#fill-to-stroke}

Des contours paramétrés en remplissage ne donnent jamais rien de bon en broderie, mais convertir un tel contour en colonne satin ou en point droit nécessite beaucoup de travail. Cet outil aide à accomplir cette opération.

Il est comparable à la fonctionalité d'Inkscape `Chemin > Vectoriser un objet matriciel > Traçage Centerline`  ( -et cause le même genre de prolème...). Mais au lieu de convertir un bitmap en lignes, il détermine une ligne centrale pour des objets de type remplissage.

Vous pouvez améliorer le résultat en définissant des lignes de découpage.
![Remplissage en trait](/assets/images/docs/en/fill_to_stroke.png)

### Usage

* (Optionnel). Dessiner des lignes de découpage aux intersections/jointures. Ce sont des simples traits. Ceci est particulièrement utile si vous voulez définir des colonnes satin.  
Merci de noter que chaque trait doit découper le remplissage en deux. 
* Sélectionnez un ou plusieurs objets remplissage que vous souhaitez convertir en trait, ainsi que les lignes de découpages correspondantes si vous en avez définies.
* Exécutez  `Extensions > Ink/Stitch > Outils: trait > Remplissage en Trait`
* Choisissez les options et cliquez sur Appliquer
* Utilisez l'outil noeuds pour les éventuelles corrections

### Options

* *Garder l'original* : utilisez cette option si vous voulez garder les objets de départ, sinon ils seront supprimés.
* *Seuil de cul de sac(px)* : ceci supprimera les petits traits. Dans la plus part des cas, la meilleure valeur  est à peu près la largeur de la forme de départ en pixel.
* *Pointillé* : Mettre à vrai si vous souhaitez un point droit.
* *Largeur (px)* : Si vous souhaitez directement convertir en colonne satin, donner ici la valeur de la largeur de la colonne satin. Dans la plupart des cas, vous voudrez une valeur faible pour pouvoir facilement inspecter et modifier avant conversion.
* *Lignes de découpage : fermer les écarts* :  Les lignes de découpage créent des écarts entre les chemins générés. Ces écarts peuvent être supprimés en activant cette option. Cette option est utile si vous ne pensez pas convertir vos chemins en colonnes satin.


## Saut en Trait {#jump-to-stroke}

Ceci crééra un point droit direct entre la fin du premier élément et le début du second. Il ne vous reste plus qu'à le positionner là où il sera recouvert par des broderies ultérieures pour éviter un saut de fil. 

### Usage

* Sélectionnez au moins deux objets
* Exécutez  `Extensions > Ink/Stitch > Outils: Trait > Saut en Trait`

### Options

* {% include upcoming_release.html %}

* Convertir les sauts de longueur au moins 
* Convertir les sauts de longueur au plus 
* Connecter seulement au sein des groupes ou des calques 
* Ne pas connecger après une coupe, un stop ou des points d'arrêt forcés.

#### Options de sortie
* Fusionner les nouveaux points droits avec le précédent ou le suivant si de même type.
* Connectez les sous-chemins et fusionner

et pour les connexions non fusionnées:
* Longueur minimum du point droit
* Tolerance


## Redwork

{% include upcoming_release.html %}
Redwork  est une technique de broderie qui assure que chaque point est brodé exactement deux fois.

Cet outil va **remplacer** votre ensemble de points droits par un nouveau ensemble de points  droits en ordre logique de broderie. 

La différence principale avec  "l'agencement automatique" est qu'il assure que les chemins sont brodés exactement deux fois. De plus, le nombre de sauts est optimisé  (chaque partie connexe est brodée entièrement avant de  passer à la suivante), mais pas leur longueur. 

Cet outil est à utiliser de préférence avec un dessin connexe ou avec peu de morceaux disjoints.


### Usage

* Sélectionnez les chemins que vous désirez organiser
* Lancez `Extensions > Ink/Stitch > Outils : Trait > Redwork...`
* Paramétrez les options et  cliquez sur "Appliquer"

### Options

* Connectez les traits distants de  moins de (mm)
  
L'extension redwork peut travailler avec des groupes disconnectés de points droits.  Par contre certains de vos traits peuvent de ne pas s'enchainer les uns les autres ce qui laisse de petits espaces.
Avec cette option, vous pouvez définir jusqu'à quelle distance ces espaces doivent être supprimés.

Les  traits dont la distance est supérieure à cette valeur seront considérés comme non connectés.

L'extension brode  successivement chaque groupe connecté, avec un unique saut entre deux groupes connectés.


* Longueur minimale du chemin (mm)

Supprime du résultat les chemins plus court  que cette valeur

Le résultat peut contenir des petits chemins (par exemple en cas de traits pas tout a fait jointif mais avec une  petite superposition). 
Des chemins plus court que  la [longeur minimum  de saut](/docs/preferences/#minimum-jump-stitch-length-mm) peuvent généralement être supprimés, mais s'ils sont consecutifs, il vaudra mieux diminuer cettte valeur.

  
* Longueur du point Redwork  (mm)
  
Détermine la longueur du point pour tous les chemins du résultat.
  
* Nombre de répétitions du point multiple (bean stitch)
  
Détermine [le nombre de répétitions du point multiple (bean stitch)](/docs/stitches/bean-stitch/) pour les chemins brodés au deuxime passage uniquement.

### Position de début et de fin
Le redwork commence et termine toujours au même endroit. Vous pouvez  définir cet endroit à l'aide de la commande [Position de départ pour l'agencement automatique de point droit](/docs/commands/#--startingending-position-for-auto-route-of-running-stitch).


## Contour {#outline}
{% include upcoming_release.html %}

![Fill to outline](/assets/images/docs/outline.png)

Cette extensionn aide à reconstruire l'objet original à partir du fichier de points lorsqu'on ne dispose plus du fichier svg de départ. Sélectionner un ou plusieurs chemins de points (en general un remplissage) et cette extension va essayer de trouver leur contour.

### Usage

- Sélectioner  les éléments que vous souhaitez convertir
- Exécutez `Extensions > Ink/Stitch > Outils: Trait > Contour...`
- Cochez  "live preview" to see the actual result
- Adjust settings until you are happy with the outcome
- Cliquez "Appliquer"

## Tutoriaux utilisant Outils: Trait

{% include tutorials/tutorial_list key="tool" value="Stroke" %}

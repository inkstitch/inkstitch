---
title: "Outils: Trait"
permalink: /fr/docs/stroke-tools/
last_modified_at: 2024-03-1é
toc: true
---
## Agencement automatique de points droits

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

## Contour {#outline}
{% include upcoming_release.html %}

![Fill to outline](/assets/images/docs/outline.png)

Cette extensionn aide à reconstruire l'objet original à partir du fichier de points lorsqu'on ne dispose plus du fichier svg de départ. Sélectionner un ou plusieurs chemins de points (en general un remplissage) et cette extension va essayer de trouver leur contour.
### Usage

- Sélectioner  les éléments que vous souhaitez convertir
- Exécutez `Extensions > Ink/Stitch > Outils: Trait > Contour...`
- Cochez  "live preview"  et utilises la scroll bar pour modifier le ratio et trouver la meilleure valeur pour le chemin choisi.
- Cliquez "Appliquer"

## Satin en Trait

Convertir le satin en trait converti une colonne satin en un trait qui correspond à sa ligne centrale. Ceci peut être utile si vous décider tardivement dans le processus  de transformer une colonne satin en point droit. Vous pouvez aussi l'utiliser pour modifier la largeur d'une colonne satin lorsque la compensation d'étirement ne convient pas bien. Dans ce cas, utilisez cette fonction pour convertir votre colonne satin en point droit, puis modifier l'épaisseur du trait dans le panneau Fond et Contour puis lancez l'extension "Outils Satin > convertir ligne en satin".
Ceci fonctionne d'autant mieux que la largeur de la colonne satin initiale est constante.

![Satin to Stroke example](/assets/images/docs/en/satin_to_stroke.png)

### Usage

1. Sélectionez la ou les colonnes satin que vous souhaitez convertir en point droits.
2. Exécutez  `Extensions > Ink/Stitch > Outils: Trait > Satin en Trait...`
3. Choisissez si vous vous souhaitez ou non conserver les colonnes satins sélectionnées.
4. Cliquez sur Appliquer

## Remplissage en Trait

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


## Saut en Trait

Ceci crééra un point droit direct entre la fin du premier élément et le début du second. Il ne vous reste plus qu'à le positionner là où il sera recouvert par des broderies ultérieures pour éviter un saut de fil. 

### Usage

* Sélectionnez au moins deux objets
* Exécutez  `Extensions > Ink/Stitch > Outils: Trait > Saut en Trait`

* {% include upcoming_release.html %}
### Options

* Convertir les sauts de longueur au moins 
* Convertir les sauts de longueur au plus 
* Connecter seulement au sein des groupes ou des calques 
* Ne pas connecger après une coupe, un stop ou des points d'arrêt forcés.

#### Options de sortie
* Fusionner les nouveaux points droits avec le précédent ou le suivant si de même type.Merge new strokes with previous/next stroke if same type
* Connectez les sous-chemins et fusionner

et pour les connexions non fusionnées:
* Longueur minimum du point droit
* Tolerance


## Tutoriaux utilisant Outils: Trait

{% include tutorials/tutorial_list key="tool" value="Stroke" %}

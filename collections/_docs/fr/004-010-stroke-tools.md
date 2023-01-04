---
title: "Outils: Trait"
permalink: /fr/docs/stroke-tools/
excerpt: ""
last_modified_at: 2023-01-04
toc: true
---
## Agencement automatique de points droits

Cet  outil **remplace** un ensemble de chemins paramétrés en points droits par un nouvel ensemble de chemins paramétrés en points droits  empilés dans un ordre logique de broderie qui évite autant que faire se peut les sauts de fil. Lorsque nécessaire des chemins (chemins de dessous) sont ajoutés, sous les chemins existants pour assurer les connexions . Les points droits résultants conservent tous les  paramètres des points droits originaux tels que la longueur de point droit, le  nombre de répétitions, le nombre de répétitions pour le point triple.  Les chemins de dessous ne conservent que la longueur du point, le nombre de répétitions est remis à un et et le nombre de répétitions de point triple à zéro.

Cette extension cherche à minimiser la longueur des sauts de fil inévitables.

### Usage
- Sélectionnez tous les chemins paramétrés en points droits que vous souhaitez organiser
- Exécutez `Extensions > Ink/Stitch > Outils : Trait > Agencement automatique  de points droits`
- Choisir les options désirées et cliquer sur "Appliquer et quitter"
  
Par défaut, l'extension choisira de commencer par le noeud le plus à gauche et de terminer par le noeud le plus à droite même si ces noeuds ne sont pas des noeuds terminaux. Vous pouvez attacher les commandes " Début/Fin d'agencement automatique de point droit" pour forcer les positions de début et de fin.

### Options

- Cocher **Ajouter des noeuds aux intersections** donnera un meilleur résultat de routage, avec des chemins de dessous qui auront leurs extrémités aux intersections ou aux noeuds terminaux. Ne décocher cette option que si vous avez manuellement ajouté des noeuds là où vous souhaitez les coupures de chemin.
- Cocher **Préserver l'ordre des points droits** si vous souhaitez préserver l'ordre initial des chemins paramétrés en points droits.
- Cocher **Couper les sauts de fil**  pour  utiliser des commandes de coupe plutôt que des sauts de fil. Les commandes de coupe sont ajoutées au svg, vous pouvez donc ensuite les modifier/supprimer à votre guise.

## Convertir le Satin en trait

Convertir le satin en trait converti une colonne satin en un trait qui correspond à sa ligne centrale. Ceci peut être utile si vous décider tardivement dans le processus  de transformer une colonne satin en point droit. Vous pouvez aussi l'utiliser pour modifier la largeur d'une colonne satin lorsque la compensation d'étirement ne convient pas bien. Dans ce cas, utilisez cette fonction pour convertir votre colonne satin en point droit, puis modifier l'épaisseur du trait dans le panneau Fond et Contour puis lancez l'extension "Outils Satin > convertir ligne en satin".
Ceci fonctionne d'autant mieux que la largeur de la colonne satin initiale est constante.

![Satin to Stroke example](/assets/images/docs/en/satin_to_stroke.png)

### Utilisation

1. Sélectionez la ou les colonnes satin que vous souhaitez convertir en point droits.
2. Exécutez  `Extensions > Ink/Stitch > Outils Trait > Convertir  le satin en trait...`
3. Choisissez si vous vous souhaitez ou non conserver les colonnes satins sélectionnées.
4. Cliquez sur Appliquer


## Remplissage en trait

{% include upcoming_release.html %}

Des contours paramétrés en remplissage ne donnent jamais rien de bon en broderie, mais convertir un tel contour en colonne satin ou en point droit nécessite beaucoup de travail. Cet outil aide à accomplir cette opération.

Il est comparable à la fonctionalité d'Inkscape 'Chemin > Vectoriser un objet matriciel > Traçage Centerline'  ( -et cause le même genre de prolème...). Mais au lieu de convertir un bitmap en lignes, il détermine une ligne centrale pour des objets de type remplissage.

Vous pouvez améliorer le résultat en définissant des lignes de découpage.



### Utilisation
* (Optionnel). Dessiner des lignes de découpage aux intersections/jointures. Ce sont des simples traits. Ceci est particulièrement utile si vous voulez définir des colonnes satin.  
Merci de noter que chaque trait doit découper le remplissage en deux. 
* Sélectionnez un ou plusieurs objets remplissage que vous souhaitez convertir en trait, ainsi que les lignes de découpages correspondantes si vous en avez définies.
* Exécutez  `Extensions > Ink/Stitch > Outils: trait > Remplissage en trait`
* Choisissez les options et cliquez sur Appliquer
* Utilisez l'outil noeuds pour les éventuelles corrections

### Options

* Garder l'original : utilisez cette option si vous voulez garder les objets de départ, sinon ils seront supprimés.
* Seuil de cul de sac(px) : ceci supprimera les petits traits. Dans la plus part des cas, la meilleure valeur  est à peu près la largeur de la forme de départ en pixel.
* Pointillé : Mettre à vrai si vous souhaitez un point droit.
* Largeur (px) : Si vous souhaitez directement convertir en colonne satin, donner ici la valeur de la largeur de la colonne satin. Dans la plupart des cas, vous voudrez une valeur faible pour pouvoir facilement inspecter et modifier avant conversion.


## Saut en Trait

{% include upcoming_release.html %}

Ceci crééra un point droit entre la fin du premier élément et le début du second. Il ne vous reste plus qu'à le positionner là où il sera recouvert par des broderies ultérieures pour éviter un saut de fil.



### Utilisation

* Sélectionnez au moins deux objets
* Exécutez  `Extensions > Ink/Stitch > Outils: trait > Saut en Trait`

---
title: "Outils Satin"
permalink: /fr/docs/satin-tools/
excerpt: ""
last_modified_at: 2023-04-18
toc: true
---
`Extensions > Ink/Stitch  > Outils de satin` inclut un certain nombre d’aides utiles, facilitant le travail avec [les colonnes satin](/fr/docs/stitches/satin-column/).

**Exemple:**
* Créer un chemin à l'aide de l'outil courbes de Bézier (`B`)
* Faire [Convertir les lignes Satin](#convertir-des-lignes-en-satin)
* Utiliser le [Dialogue de Paramètres ](/fr/docs/params/#paramètres-satin) pour choisir une sous-couche
* Lancer [Agencement automatique des colonnes satin](#auto-route-satin-colonnes) pour obtenir des colonnes de satin bien organisées

[![Convertir Ligne en Satin](/assets/images/docs/en/satin-tools.svg)](/assets/images/docs/en/satin-tools.svg){: title="Télécharger le fichier SVG" download="satin-tools.svg" }

**Astuce** Pour un accès plus rapide [activer les raccourcis](/fr/docs/customize/) des outils satin spécifiques.
{: .notice--info}

## Agencement automatique de Colonnes Satin...

Cet outil remplacera vos colonnes satin par un nouvel ensemble de colonnes satin dans un ordre d'assemblage logique. Des sous-chemins et les sauts de points seront ajoutés si nécessaire et les colonnes seront scindées pour faciliter les sauts. Les points satins résultants conserveront tous les paramètres que vous avez définis sur les points satins originaux, y compris la sous-couche, l’espacement en zigzag, etc.

### Usage

1. Sélectionnez les colonnes satin (préparées avec sous-couche, etc.)
2. Lancer `Extensions > Ink/Stitch  > Outils de Satin > Agencement automatique de Colonnes Satin...`
3. Activer les options souhaitées et cliquez sur Appliquer

**Astuce:** Par défaut, le point à l'extrême gauche sera choisi comme départ et celui à l'extrême droite comme fin (même s'ils se trouvent à mi-chemin dans un satin, tel que le bord gauche de la lettre "o"). Vous pouvez le remplacer en activant les [commandes de "Position de départ/fin pour points satin autogénérés"](/fr/docs/commands/).
{: .notice--info }

### Options

* Activer **Couper les sauts de fil** pour couper les fils au lieu de créer des sauts de fil. Tout saut de fil au-dessus de 1mm est coupé. Les commandes de coupe sont ajoutées au SVG, vous pouvez donc les modifier / supprimer à votre guise.

* Si vous préférez conserver votre ordre initial (ce qui pourrait être le cas si vous avez superposé des satins), activez l'option ** **Préserver l'ordre des colonnes satin**.

## Convertir des Lignes en Satin

Cette extension convertira un trait en une colonne satin avec une largeur spécifiée. Après la conversion, vous verrez les deux rails et (éventuellement) de nombreuses traverses de direction, en fonction de la forme de votre ligne.

### Usage

1. Tracer une courbe de Bézier (`B`)
2. Définir une largeur de trait
2. Lancer `Extensions > Ink/Stitch  > Satin Tools > Convert Line to Satin`

## Convertir le satin en trait

Satin en trait converti une colonne satin en sa ligne centrale. Cette fonction peut être utile si vous décidez, tardivement dans le processus, de remplacer une colonne satin par un point droit. Vous pouvez aussi l'utiliser pour modifier l'épaisseur de votre colonne satin lorsqu'un étirement n'est pas satisfaisant.  

Dans ce cas, convertissez votre colonne satin en point droit, modifiez la largeur du trait dans le panneau `Fond et Contour` puis exécutez  ["Convertir des lignes en Satin"](#convertir-des-Lignes-en-atin) function. Ce processus fonctionne bien si les colonnes satin ont une épaisseur constante.

![Satin to Stroke example](/assets/images/docs/en/satin_to_stroke.png)

### Usage

1. Sélectionner la ou les colonne(s) satin que vous souhaitez convertir en point droit.
2. Exécutez  `Extensions > Ink/Stitch > Outils de satin > Convertir satin en trait...`
3. Choisissez si vous souhaitez conserver les colonnes satin selectionnées ou les remplacer.
4. Cliquez sur `Appliquer`

## Scinder une colonne Satin

Scinder une colonne Satin à un point précis. La coupure a lieu à la limite d'un point pour que les deux satins résultants soient cousus exactement comme l'original. Tous les paramètres définis sur le satin d'origine restent sur les deux nouveaux satins et toutes les traverses sont conservées. Si l'un des satins n'a plus de traverse, de nouvelles sont ajoutées.

### Usage

1. Sélectionnez une colonne satin (le satin simple ne fonctionne pas)
2. Ajouter la commande "Point de partage..." avec `Extensions > Ink/Stitch  > Commandes > Attacher des Commandes à un objet sélectionné`.
3. Déplacez le symbole (ou simplement l'extrémité de la ligne de connexion) pour pointer sur l'endroit exact où vous souhaitez diviser le satin.
4. Sélectionnez à nouveau la colonne satin.
5. Faire `Extensions > Ink/Stitch  > Outils de Satin > Scinder colonne Satin`.
6. La commande de point de partage et la ligne de connexion disparaissent et il ne semble plus rien s'être passé. Sélectionnez votre satin et vous verrez qu'il a été divisé.
7. 
## Intervertir les rails des colonnes satin

C'est un petit outil pour vous aider à planifier votre chemin de points avec précision: par exemple, retourner les colonnes satin pour raccourcir les connexions entre deux sections.

Une colonne satin qui commence à l'origine sur le rail de gauche et se termine à droite commence sur le rail de droite et se termine à gauche.
![Retourner la colonne satin](/assets/images/docs/en/flip-satin-column.jpg)

### Usage

* Sélectionnez une ou plusieurs colonnes satin
* Lancez `Extensions > Ink/Stitch  > Outils Satin > Intervertir les rails satin`

## Converti Ligne en Effet de Chemin Satin 

{% include upcoming_release.html %}

Converti une ligne en colonne satin, en utilisant un Effet de Chemin. Cela rend le satin plus adaptable en forme et en largeur qu'une conversion en colonne satin normale.



### Usage

1. Sélectionner une ligne 
2. Lancez `Extensions > Ink/Stitch > Outils: Satin > Ligne vers Effet de Chemin Satin...`
3. Choisir les paramètres qui vous conviennent
4. Cliquez sur Appliquer


### Appliquer l'effet de chemin

Utilisez `Chemin > Objet en chemin` pour convertir en colonne satin standard.

### Modifier ou changer le motif

Vous pouvez changer le motif de plusieurs manières :

* Modifier le chemin comme n'importe quel chemin à l'aide de l'outil noeud.
* Modifier le motif en ouvrant le dialogue de l'effet de chemin (via `Chemin > Effets de Chemin`):
  * Modifier la largeur du satin via le réglage "Largeur"
  * Modifier le motif en cliquant sur `Modifier sur la zone de travail` dans `source du motif`.
    
    ![Modifier sur la zone de travail](/assets/images/tutorials/pattern-along-path/edit.png)
* Changer de motif en relançant à nouveau cet outil.
* Convertir en chemin normal  (`Shift + Ctrl + C`)  et rafiner manuellement le chemin (ceci perdra la fonctionnalité Effet de Chemin)


## Convertir Ligne en Zigzag en Satin

{% include upcoming_release.html %}

Quand vous tracez manuellement une colonne satin, cet outil vous aidera à le faire en une seule étape : au lieu de dessiner d'abord deux rails puis des traverses, cet outil vous permet de dessiner une ligne en zigzag ( ou en dents de scie, ou en carrés) qui pourra ensuite être converti en colonne satin normale.



### Usage

* Dessinez votre forme avec votre style de zigzag préféré.
* Sélectionnez la forme et lancez  `Extensions > Ink/Stitch > Outis: Satin > Ligne en Zigzag vers Colonne Satin`
  * Selectionnez votre style de zigzag 
  * Choisissez  si votre chemin doit être adouci ou constitué de segments de droites
  * Choisissez si les traverses doivent être inserrées ou non. Les colonnes satin crées auront toujours autant de noeuds sur les deux rails.

### Style de zigzag

* Toutes les lignes de zigzag commencent et terminent par une traverse.
* Pour **Carré (1)** et **dents de scie (2)** dessinez les traverses les unes après les autres.
*  **zigzag (3)** crée des traverses de chaque pic d'un rail vers le milieu d'un pic sur l'autre rail.
![Styles de zigzags](/assets/images/docs/zigzag-line-to-satin.png)

Si vous voyez quelque chose comme le dessin ci-dessous, vous avez probablement choisi le mauvais style de zigzag pour votre dessin.
![Mauvais choix de style de zigzag](/assets/images/docs/zigzag-line-to-satin-wrong-pattern.png)

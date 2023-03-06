---
title: "Outils Satin"
permalink: /fr/docs/satin-tools/
excerpt: ""
last_modified_at: 2022-01-16
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

## Stroke to Live Path Effect Satin

{% include upcoming_release.html %}

Converts a stroke into a satin using a live path effect. This makes it more adaptable in width and shape as a normal satin column.

### Usage

1. Select a Stroke
2. Run `Extensions > Ink/Stitch > Tools: Satin > Stroke to Live Path Effect Satin...`
3. Set the approximate sizes that you wish your satin to be
4. Click on apply

### Update and change the pattern

Now you can change the pattern in the following ways.

* Update the path as every other path in inkscape with the node tool
* Change pattern by opening the path effects dialog (`Path > Path Effects`).
  * Make the satin wider or thinner by manipulating the `width` setting.
  * Change the pattern element, by clicking `Edit on-canvas` in the `pattern source` setting.
    
    ![edit on canvas](/assets/images/tutorials/pattern-along-path/edit.png)
* Change the pattern by running this tool again
* Convert it to a normal path (`Shift + Ctrl + C`) and refine the path manually (it will then lose the path effect functionality)

---
title: "Outils Satin"
permalink: /fr/docs/satin-tools/
last_modified_at: 2025-12-29
toc: true
---
`Extensions > Ink/Stitch > Outils : Satin` inclut un certain nombre d’aides utiles, facilitant le travail avec [les colonnes satin](/fr/docs/stitches/satin-column/).

**Exemple:**
* Créer un chemin à l'aide de l'outil courbes de Bézier (`B`)
* Faire [Ligne en Satin](#ligne-en-satin)
* Utiliser le [Dialogue de Paramétrage](/fr/docs/params/#paramètres-satin) pour choisir une sous-couche
* Lancer [Agencement automatique des colonnes satin](#agencement-automatique-de-colonnes-satin) pour obtenir des colonnes de satin bien organisées

[![Convertir Ligne en Satin](/assets/images/docs/en/satin-tools.svg)](/assets/images/docs/en/satin-tools.svg){: title="Télécharger le fichier SVG" download="satin-tools.svg" }

**Astuce** Pour un accès plus rapide [activer les raccourcis](/fr/docs/customize/) des outils satin spécifiques.
{: .notice--info}


## Agencement automatique de Colonnes Satin {#auto-route-satin-columns}

Cet outil remplacera vos colonnes satin par un nouvel ensemble de colonnes satin dans un ordre d'assemblage logique. Des sous-chemins et les sauts de points seront ajoutés si nécessaire et les colonnes seront scindées pour faciliter les sauts. Les points satins résultants conserveront tous les paramètres que vous avez définis sur les points satins originaux, y compris la sous-couche, l’espacement en zigzag, etc.

### Usage

1. Sélectionnez les colonnes satin (préparées avec sous-couche, etc.)
2. Lancer `Extensions > Ink/Stitch > Outils de Satin > Agencement automatique de Colonnes Satin...`
3. Activer les options souhaitées et cliquez sur Appliquer

**Astuce:** Par défaut, le point à l'extrême gauche sera choisi comme départ et celui à l'extrême droite comme fin (même s'ils se trouvent à mi-chemin dans un satin, tel que le bord gauche de la lettre "o"). Vous pouvez le remplacer en activant les [commandes de "Position de départ/fin pour l'agencement automatique de colonnes satin "](/fr/docs/commands/).
{: .notice--info }

### Options

* Activer **Couper les sauts de fil** pour couper les fils au lieu de créer des sauts de fil. Tout saut de fil au-dessus de 1mm est coupé. Les commandes de coupe sont ajoutées au SVG, vous pouvez donc les modifier / supprimer à votre guise.

* Si vous préférez conserver votre ordre initial (ce qui pourrait être le cas si vous avez superposé des satins), activez l'option ** **Préserver l'ordre des colonnes satin**.

* **Garder les chemins originels** indique si les éléments originels doivent être gardés ou pas.

## Trait en Satin

Cette extension convertira un trait en une (ou plusieurs) colonne satin avec une largeur spécifiée. Après la conversion, vous verrez les deux rails et (éventuellement) de nombreuses traverses de direction, en fonction de la forme de votre ligne.

### Usage

1. Tracer une courbe de Bézier (`B`)
2. Définir une largeur de trait
2. Lancer `Extensions > Ink/Stitch > Outils: Satin > Trait en Satin`

## Scinder une colonne Satin

Scinder une colonne Satin à un point précis. La coupure a lieu à la limite d'un point pour que les deux satins résultants soient cousus exactement comme l'original. Tous les paramètres définis sur le satin d'origine restent sur les deux nouveaux satins et toutes les traverses sont conservées. Si l'un des satins n'a plus de traverse, de nouvelles sont ajoutées.

### Usage

1. Sélectionnez une colonne satin (le satin simple ne fonctionne pas)
2. Ajouter la commande "Point de partage..." avec `Extensions > Ink/Stitch > Commandes > Attacher des Commandes à un objet sélectionné`.
3. Déplacez le symbole (ou simplement l'extrémité de la ligne de connexion) pour pointer sur l'endroit exact où vous souhaitez diviser le satin.
4. Sélectionnez à nouveau la colonne satin.
5. Faire `Extensions > Ink/Stitch > Outils de Satin > Scinder colonne Satin`.
6. La commande de point de partage et la ligne de connexion disparaissent et il semble que rien ne s'être passé. Sélectionnez votre satin et vous verrez qu'il a été divisé.
{% include upcoming_release.html %}
Vous pouvez utiliser plusieurs commandes sur la même colonne de satin pour la diviser en plusieurs morceaux en une seule action.

## Remplissage en Satin {#fill-to-satin}

Remplissage en satin peut être utilisé pour convertir un remplissage en satin. C'est une fonction semi-automatique qui nécessite un peu de travail manuel.

Le [Fichier d'exemple](#sample-file) vous aidera à comprendre le fonctionnement.

### Utilisation

* Préparez vos objets de remplissage. Il peut être nécessaire de diviser votre remplissage en formes plus simples avec l'outil de création de formes ou avec d'autres outils d'édition de chemins dans Inkscape.
* Assurez-vous que le remplissage n'a qu'une couleur de remplissage et pas de couleur de contour.
* Dans un objet à part, créez des traverses avec une couleur de contour (et aucune couleur de remplissage). Les traverses aident à définir comment la forme de remplissage va être convertie.

Assurez-vous d'ajouter un nombre suffisant de traverses, en particulier lorsque vous souhaitez activer l'option `début/fin à la traverse` qui supprime une partie des extrémités ouvertes.
{: .notice--warning }
* Sélectionnez le remplissage et les traverses
* Exécutez `Extensions > Ink/Stitch > Outils: Satin > Remplissage en Satin...`
* Activez les options souhaitées
* Cliquez sur `Appliquer`

### Options

Option        | Description
---------------------|-------------
Début / fin à la traverse | Lorsque cette option est activée, les sections d'extrémité ouvertes seront supprimées du satin. Attention à définir un nombre suffisant de traverses faute de quoi il manquera des parties. Cette option est utile, car dans la plupart des cas, vous ne voudrez pas que votre satin se termine trop étroitement car il pousse vers les extrémités lorsque vous le brodez.
Sous-couche de passage central | Ajoute une sous-couche centrale par défaut au(x) satin(s)
Sous-couche de contour | Ajoute une sous-couche de contour par défaut au(x) satin(s)
Sous-couche en zigzag | Ajoute une sous-couche zigzag par défaut au(x) satin(s)
Conserver les chemins originels | Conserver ou supprimer les chemins sélectionnés

### Intersections

Utilisez des ponts aux intersections pour expliquer à Ink/Stitch la manière de connecter les colonnes satins.

En l'absence de pont, il reste un espace vide aux intersections.

Les ponts doivent être **entièrement contenus** dans le remplissage et **ne peuvent pas traverser sa frontière.**
{: .notice--info}

![Conversion en satin avec et sans pont](/assets/images/docs/fill_to_satin_bridge.png)

### Fichier d'exemple {#sample-file}

[Téléchargez le fichier d'exemple](/assets/images/docs/fill_to_satin_playground.svg){: title="Download SVG File" download="fill_to_satin_playground.svg" }

## Intervertir les rails des colonnes satin

C'est un petit outil pour vous aider à planifier votre chemin de points avec précision: par exemple, retourner les colonnes satin pour raccourcir les connexions entre deux sections.

Une colonne satin qui commence à l'origine sur le rail de gauche et se termine à droite commence sur le rail de droite et se termine à gauche.
![Retourner la colonne satin](/assets/images/docs/en/flip-satin-column.jpg)

Il est aussi possible de faire la même opération à partir du paramètrage.

### Usage

* Sélectionnez une ou plusieurs colonnes satin
* Lancez `Extensions > Ink/Stitch > Outils Satin > Intervertir les rails satin`

## Satin Multicolore {#multicolor-satin}

Cette extension crée des copies des satins sélectionnés pour imiter une colonne satin multicolore.
![Multicolor Satin](/assets/images/tutorials/multicolor_satin/solution.png)

Vous pouvez lire [ceci](/fr/tutorials/multicolor_satin), si vous souhaitez comprendre comment cette extension fonctionne.

### Usage

* Sélectionnez une ou plusieurs colonnes satin
* `Extensions > Ink/Stitch > Outils: Satin > Satin Multicolore`
* Choisir les options dans l'onglet `Colorer`
* Cliquer sur `Appliquer`

### Options

#### Réglages généraux

* Choisir si les couleurs sont équidistantes ou si elles ont des largeurs différentes.
 * Si cette option est cochée, la largeur des couleurs et des marges sont définies pour toutes les couleurs par la valeur de `Largeur de la zone monochrome` .
 * Si la case est décochée il devient possible de choisir individuellement la largeur de chaque couleur **ET** d'ajouter une zone où deux couleurs se mélangent.
* Ajouter un dépassement à gauche (%): Ajoute un bord irrégulier sur le côté gauche du satin
* Ajouter un dépassement à droite (%): Ajoute un bord irrégulier sur le côté droit du satin
* Compensation d'étirement (mm): Élargit les colonnes satin et superpose les couleurs pour éviter les trous.
* Graine aléatoire: Changez la valeur pour changer l'apparence des paramètres aléatoires 
* Garder le satin originel : choisir de garder ou de supprimer le satin originel
* Ajuster la sous-couche par couleur: ne s'applique que si le satin originel a une ou des sous-couches
 * Si coché, les sous-couches seront appliquées individuellement à chaque couleur en évitant les zones multicolores
 * Sinon, seule la première couleur aura une sous-couche, couvrant toute la surface
#### Couleurs

Les valeurs des largeurs sont données en pourcentage. Faites attention que la somme des valeurs soit bien égale à 100%.

Notez que le premier champ des définitions des couleurs définie la largeur de la zone monochrome, le second champ défini la marge avec la couleur suivante. Ceci est la largeur qui sera partagée par les deux couleurs. Lorsque `Couleurs équidistantes` est coché, réduire la valeur de la 'Largeur de la zone monochrome' augmentera la taille des zones bicolores.
{: .notice--info}

![Multicolor satin ui](/assets/images/docs/en/multicolor_satin_ui_01.png)

![Multicolor satin ui](/assets/images/docs/en/multicolor_satin_ui_02.png)

## Trait en Effet de Chemin Satin {#stroke-to-live-path-effect-satin}

Converti une ligne en colonne satin, en utilisant un Effet de Chemin. Cela rend le satin plus adaptable en forme et en largeur qu'une conversion en colonne satin normale. La ligne reste une ligne, mais un effet de chemin lui est appliqué. Si vous utilisez l'éditeur de nœud, vous pourrez agir sur les nœuds de la ligne, même après application de l'effet.

** Évitez les angles aigus.** Comme pour les satins standards, il est préférable de découper le chemin aux angles aigus. Dans certains cas il pourra être nécessaire de tirer sur les poignées des nœuds ou d'ajouter des nœuds pour obtenir une largeur convenable. 
{: .notice--warning }

### Usage

1. Sélectionner un trait ou un trait avec déjà un Effet de Chemin Satin
2. Lancez `Extensions > Ink/Stitch > Outils: Satin > Trait en Effet de Chemin Satin...`
3. Choisir les paramètres qui vous conviennent
5. Cliquez sur Appliquer

### Options

--|--|--
Motif         | ![LPE-Patterns](/assets/images/docs/lpe_patterns.png) | Choix du motif à appliquer répétitivement à la colonne satin
Largeur minimum (mm)  | ![Min width](/assets/images/docs/lpe_min_width.png)  | Largeur du motif là où il est le plus étroit
Largeur maximum (mm)  | ![Max width](/assets/images/docs/lpe_max_width.png)  | Largeur du motif là où il est le plus large
Longueur du motif (mm) | ![Length](/assets/images/docs/lpe_length.png)     | Longueur du motif à répéter
Étiré         | ![Stretched](/assets/images/docs/lpe_stretched.png)  | Si coché le motif sera étiré pour que ses répétitions de motif occupent exactement la longueur de la ligne, sinon, il pourra rester un vide en fin de ligne
Ajouter des traverses | ![Rungs](/assets/images/docs/lpe_rungs.png)      | Les motifs ayant tous le même nombre de nœuds sur les deux rails, les traverses sont facultatives. Choisissez d'en ajouter ou non
Chemin privé      |                            | ● Si coché, la colonne satin dispose de son propre motif. Une modification du modif n'influence que cette colonne. Des transformations peuvent être appliquées au motif.<br>● Sinon, le motif est commun à toutes les colonnes satin utilisant cet effet et ce motif. Modifier le motif pour l'une d'elle le modifie pour toutes. Des transformations du motif peuvent conduire à des largeurs de colonne inattendues.

### Appliquer l'effet de chemin

Utilisez `Chemin > Objet en chemin` pour convertir en colonne satin standard. 

### Modifier ou changer le motif

Vous pouvez changer le motif de plusieurs manières :

* Modifier le chemin comme n'importe quel chemin à l'aide de l'outil nœud.
* Modifier le motif en ouvrant le dialogue de l'effet de chemin (via `Chemin > Effets de Chemin`):
 * Modifier la largeur du satin via le réglage "Largeur"
 * Modifier le motif en cliquant sur `Modifier sur la zone de travail` dans `Source du motif`.
  
  ![Modifier sur la zone de travail](/assets/images/tutorials/pattern-along-path/edit_french.png)
* Changer de motif en relançant à nouveau `Convertir Ligne en Effet de Chemin Satin`.
* Convertir en chemin normal (`Shift + Ctrl + C`) et raffiner manuellement le chemin (ceci perdra la fonctionnalité Effet de Chemin)

## "Ligne Zigzag" en Satin {#zigzag-line-to-satin}

Quand vous tracez manuellement une colonne satin, cet outil vous aidera à le faire en une seule étape : au lieu de dessiner d'abord deux rails puis des traverses, cet outil vous permet de dessiner une ligne en zigzag ( ou en dents de scie, ou en carrés) qui pourra ensuite être convertie en colonne satin normale.

### Usage

* Dessinez votre forme avec votre style de zigzag préféré.
* Sélectionnez la forme et lancez `Extensions > Ink/Stitch > Outils: Satin > "Ligne Zigzag" en Satin`
 * Sélectionnez votre style de zigzag 
 * Choisissez si votre chemin doit être adouci ou constitué de segments de droites
 * Choisissez si les traverses doivent être insérées ou non. Les colonnes satin créées auront toujours autant de nœuds sur les deux rails.

### Style de zigzag

* Toutes les lignes de zigzag commencent et se terminent par une traverse.
* Pour **Carré (1)** et **dents de scie (2)** dessinez les traverses les unes après les autres.
* **zigzag (3)** crée des traverses de chaque pic d'un rail vers le milieu d'un pic sur l'autre rail.
![Styles de zigzags](/assets/images/docs/zigzag-line-to-satin.png)

Si vous voyez quelque chose comme le dessin ci-dessous, vous avez probablement choisi le mauvais style de zigzag pour votre dessin.
![Mauvais choix de style de zigzag](/assets/images/docs/zigzag-line-to-satin-wrong-pattern.png)

## Tutoriels utilisant Outils: Satin

{% include tutorials/tutorial_list key="tool" value="Satin" %}

---
title: "Outil lettrage"
permalink: /fr/docs/lettering/
last_modified_at: 2026-10-20
toc: true
---
## Lettrage

Le module de lettrage crée du texte sur plusieurs lignes. Choisissez la bonne police pour votre projet dans une grande variété de polices déjà digitalisées.

![Lettrage Extensions](/assets/images/docs/fr/lettering.png)

### Usage

* Faire `Extensions > Ink/Stitch > Lettrage > Lettrage`
* Entrez votre texte (multi-ligne possible)
* Définir la police et l'échelle
    **⚠ Attention**: Pour des résultats optimaux, tenir compte des limites de redimensionnement mentionnées dans le descriptif des fontes.
* Cliquer sur `Appliquer et Quitter`

### Filtres de fonte

* **Filtrage par taille**
  Les fontes sont conçues pour être  brodées dans  un intervalle de tailles donné.
  Le filtrage par taille vous aide en réduisant la liste des fontes à uniquement les fontes qui peuvent être brodées dans les dimensions choisies.
  Un filtre actif (pas à 0) déterminera  automatiquement la bonne échelle pour que la fonte sélectionnée soit dans la dimension souhaitée.

* **Glyphes**

  Si l'option est cochée, seules les fontes contenant tous les glyphes de votre texte apparaissent dans le menu déroulant des fontes

* **Famille de fonte**

  Filtre les fontes par famille, par exemple les fontes d'appliqué ou les fontes d'écriture manuelle.

### Options

* **Échelle**

  Définit la taille de sortie de la police par rapport à la taille de police d'origine (%).
  Il est recommandé d'utiliser l'option d'échelle plutôt que de redimensionner la police sur le canevas.
  De cette façon, vous pouvez vous assurer que vous respectez les paramètres pour lesquels la police a été conçue.

* **Alignement du Texte**

  Alignement du texte sur plusieurs lignes: gauche, centre, droit, justifié (mots)- modifie uniquement les espaces entre les mots, justifié (lettres) - modifie aussi l'espacement inter lettres.

* **Espacememnt des lettres**

  Ajoute cette largeur (en mm) entre les lettres

* **Espacement des mots**

  Ajoute cette largeur (en mm) entre les mots

* **Hauteur de ligne**

  Augmente d'autant l'espace entre les lignes
  
* **Tri des couleurs**

  Option de tri des couleurs pour certaines fontes multicolores afin d'éviter de nombreux changement de couleur de fils. Attention toutefois au risque de décalage si le tri se fait sur un texte trop long. Il est possible de  trier tout le texte ou de trier ligne par ligne ou mot par  mot

  
* **Broder les lignes de texte en aller retour**

  Lorsque cette option est activée, la première ligne sera brodée de gauche à droite et la seconde de droite à gauche, etc.
  Cela donnera à votre machine des déplacements plus courts.

* **Alignement du Texte**

  Alignement du texte sur plusieurs lignes: gauche, centre, droit, justifié (mots)- modifie uniquement les espaces entre les mots, justifié (lettres) - modifie aussi l'espacement inter lettres.

* **Ajouter des commandes de coupes**

  Si cette option est activée, Ink/Stitch ajoutera des commandes de coupe  au choix pour chaque lettre, ou après chaque mot ou après chaque ligne.

* **Utiliser des symboles de commandes**

  Si cette option est cochée, les coupes sont ajoutées sous  forme de symboles de commandes, si non coché, elles sont ajoutées dans le paramétrage des objets concernés.

### Préconfigurations

Vous pouvez enregistrer et rouvrir vos paramètres de police préférés.

## Polices

Un aperçu de toutes les polices disponibles se trouve dans la [bibliothèque de polices](/fr/fonts/font-library/).

### Créer de nouvelle polices

Lire le [tutoriel de création de police](/fr/tutorials/font-creation/).

Contactez nous  sur  [GitHub](https://github.com/inkstitch/inkstitch/issues) si vous souhaitez publier votre police dans l'outil de lettrage d'Ink/Stitch.

## Lettrage le long d'un chemin  {#lettering-along-path}

Les lettres d'Ink/Stitch ont été soigneusement dessinées pour une broderie optimale. Si vous essayez de les modifier avec les outils usuels d'inkscape, il se peut que cela ne fonctionne pas comme vous le souhaitez. Placez les lettres le long  d'un chemin est un gros travail. Cet outil va vous aider à le faire.

![curvy text](/assets/images/docs/text_along_path.jpg)

### Usage

* Sélectionnez un chemin et un groupe de lettrage

La longueur du tracé doit être adaptée à la longueur du texte. Il est important de redimensionner le texte à l'aide de l'outil Lettrage plutôt que par transformation manuelle.

L'outil Lettrage offre également la possibilité d'augmenter ou de diminuer l'espacement entre les caractères ; cette fonction est particulièrement utile lorsque le texte est incurvé vers l'intérieur.
  {: .notice--info}
* Exécutez `Extensions > Ink/Stitch > Lettrage > Lettrage le long d'un chemin ...`
* Ajustez les options selon vos préférences (voir ci-dessous).
* Cliquez sur 'Appliquer'

Besoin de modifier le tracé ou d'ajuster vos options? Vous pouvez les affiner à tout moment, même après la transformation du texte, en réappliquant simplement la fonction.
{: .notice--info}

Dans la version actuelle d'Ink/Stitch (3.3.0), une erreur de positionnement se produit si le document a été mis à l'échelle via les paramètres du document (`Fichier > Propriétés du document > Échelle`). Veuillez vous assurer que cette valeur est bien définie sur 1.
{: .notice--warning}

### Options

#### Position du texte

Ink/Stitch propose plusieurs options de positionnement du texte pour aligner vos lettres le long d'un tracé :

* **Gauche :** Place le texte au tout début du tracé.
* **Centre :** Centre le texte au milieu du tracé.
* **Droite :** Aligne le texte à la fin du tracé.
* **Étirer :** Augmente l'espacement entre les caractères pour occuper toute la longueur du tracé.
Ink/Stitch offers several text positioning options to align your lettering along a path:

L'alignement précis dépend de deux facteurs essentiels : le **point de départ** du tracé et sa **direction**.

![Texte aligné le long d'un tracé à l'aide de différentes options](/assets/images/docs/text_along_path_alignment.png)

**Exemple : Lettrage sur un cercle**

Un cas d'utilisation courant consiste à placer du texte le long d'un cercle ou d'un ovale. Par défaut, dans Inkscape, un objet circulaire fermé commence en haut et se déploie dans le sens antihoraire.

L'exécution du simulateur révèle que le tracé de broderie suit exactement ce comportement. Ce n'est généralement pas le réglage approprié pour le positionnement de votre texte.

Pour ajuster le cercle, vous devez d'abord convertir l'objet en tracé :

* Allez dans **Chemin > Objet en chemin** (ou appuyez sur `Ctrl + Maj + C`).
* Cette action modifie à la fois la direction et le point de départ du tracé.
* Vérifiez-le dans le simulateur ; le tracé de broderie commencera désormais au milieu à droite et se déploiera dans le sens horaire.


Pour positionner votre texte en haut du cercle, vous devez **ajuster le point de départ** :
* Sélectionnez l’outil Nœud (`N`) et cliquez sur le **nœud inférieur** du cercle.
* Coupez le tracé à cet endroit en appuyant sur `Maj + B`.
* Pour vérifier la coupure, cliquez et faites glisser légèrement le nœud (sans relâcher le bouton de la souris). Un deuxième nœud apparaîtra en dessous.

Appuyez sur `Échap` pour annuler le déplacement et remettre le nœud en place.

Votre nouveau point de départ est maintenant défini en bas, ce qui centre le texte en haut.

Pour modifier le point de départ d’un tracé déjà coupé, sélectionnez simplement les deux nœuds séparés, réunissez-les (`Maj + J`) et coupez le tracé à l’endroit souhaité.
{: .notice--info}

Il nous faut maintenant déterminer le **sens du chemin**. Pour cela, il est utile d'[afficher le sens du chemin](/fr/docs/customize/#noeuds-activation-de-la-direction-des-chemins). Vous pouvez également le vérifier à l'aide du simulateur.

Si le sens du chemin est incorrect, corrigez-le avec `Chemin > Inverser`.

Voici un exemple : mêmes paramètres, mais sens de chemin inversés. La position du texte est définie sur « Centré ».

![Deux textes, chacun aligné sur un chemin. Dans un cas, le chemin va de gauche à droite et le texte est superposé. Dans l'autre cas, le chemin va de droite à gauche et le texte est suspendu en bas du chemin, également de droite à gauche.](/assets/images/docs/text_along_path_path_direction.jpg)

#### Alignement vertical

L'alignement vertical vous permet de déterminer si le texte doit être affiché entièrement au-dessus du tracé (« haut »), si le tracé sert de ligne de base (« ligne de base ») ou si le texte est affiché entièrement en dessous du tracé (« bas »). Voici un exemple où du texte a été placé sur un tracé en utilisant les options dans cet ordre précis.

![Texte aligné à l'aide des trois options d'alignement. La différence entre « haut » et « ligne de base » est particulièrement visible ici avec la lettre « p ». L'option « haut » place le texte entièrement au-dessus du tracé, tandis que l'option « ligne de base » place le texte sur le tracé, ce qui fait que la jambe du « p » dépasse la ligne.](/assets/images/docs/text_along_path_vertical_alignment.jpg)

**Exemple : Patch**

1. Pour aligner le texte en haut, le chemin doit être ouvert en bas. Le sens du chemin est horaire. La position du texte est définie sur « Centre » et l'alignement vertical sur « Haut ».

2. Pour aligner le texte en bas, le chemin doit être ouvert en haut. Le sens du chemin est antihoraire. La position du texte est centrée et l'alignement vertical est sur « Bas ».

3. Assemblé sous forme de patch.

![Texte sur un cercle, positionné en haut et en bas, et assemblé sous forme de patch.](/assets/images/docs/text_along_path_patch.jpg)

## Lettrage par lots {#batch-lettering}

Le lettrage par lot permet de créer facilement des fichiers de texte multiples

###  Exemple

![Un écusson avec 4 noms différents](/assets/images/docs/batch-lettering.png)

* Préparez un fichier de broderie.
   Si le fichier contient un chemin  avec le label  `batch lettering` , il sera utilisé pour la position du texte de manière similaire à celle 
   de [Lettrage le long d'un chemin](/docs/lettering/#lettering-along-path). Si vous souhaitez positionner un lettrage standard uttilisez  un chemin horizontal.
* Allez dans « Fichier > Enregistrer une copie... » et cliquez sur la petite flèche dans le champ de sélection du format de fichier pour ouvrir la liste des formats de fichier disponibles.
* Choisissez « Ink/Stitch : Lettrage par lots (.zip) »
* Accédez au dossier de sortie souhaité et cliquez sur « Enregistrer ».

### Options

* **Texte** : Saisissez le texte. Par défaut, chaque nouvelle ligne sera placée dans son propre fichier.
* **Séparateur personnalisé** :  Spécifiez un autre séparateur que fin de ligne si vous souhaitez que votre fichier texte contienne du texte sur plusieurs lignes.
Le texte sera divisé et placé dans un nouveau fichier à chaque occurrence du séparateur personnalisé.
* **Nom de la police** : Nom de la police que vous souhaitez utiliser. Consultez la [bibliothèque de polices](/fr/fonts/font-library/) pour trouver la liste des polices disponibles. La police peut être une police d'ink/stitch ou une police de votre répertoire de police personnalisé.
* **Échelle (%) :** Valeur d'échelle pour redimensionner une police. La valeur sera limitée à la plage d'échelle disponible pour la police concernée.
* **Tri par couleur :** Indique si les polices multicolores doivent être triées par couleur ou non.
* **Ajouter des coupes :** Indique si des coupes doivent être ajoutés ou non (jamais, après chaque ligne, mot ou lettre).
* **Utiliser des symboles de commande :** Indique si les coupes doivent être ajoutés comme symboles de commande ou comme option de paramètre (pertinent uniquement pour la sortie SVG).
* **Aligner le texte multi-ligne :** Définit l'alignement du texte multi-ligne.
* **Lettrage le long du chemin**
  * **position du texte :** Position du texte sur le chemin `batch lettering`.
  * **vertical text position:** The vertical position in relation to the `batch lettering` path
* **Formats de fichier :** Saisissez une liste de [formats de fichier] (/fr/docs/file-formats/#writing) séparés par des virgules.

Par exemple, si vous souhaitez créer les 4 patchs illutrés plus haut,utilisez le fichier d'exemple et paramétrez la fenêtre qui s'ouvre à l'enregistrement ainsi:

[Télécharger le fichier d'exemple](/assets/images/docs/batch_lettering_template_example.svg){: title="Download SVG File" download="batch_lettering_template_example.svg" }

### Usage en ligne de commande

Voici un exemple minimal d'utilisation de l'extension de lettrage par lots en ligne de commande :

```
./inkstitch --extension=batch_lettering --text="Hello\nworld" --font="Abecedaire" --file-formats="svg,dst" input_file.svg > output_file.zip
```

#### Options

Option             | Type|Valeurs
---------- --------|----------|------

`--text`           |string  |ne peut pas être vide
`--separator`      |string    |par défault: '\n'
`--font`           |string    |doit être un nom de police valide
`--scale`          |integer   |default: 100
`--color-sort`     |string    |off, all, line, word<br>  par défaut: off
`--trim`           |string    |off, line, word, glyph<br> par défaut: off 
`--command_symbols`|bool      |defaut: False
`--text-align`     |string    |left, center, right, block, letterspacing<br>defaut: gauche
`--file-formats`   |string    |au minimum un format de sortie valide

## Fichiers exemple concernant  le lettrage

{% include tutorials/tutorial_list key="techniques" value="Lettering" %}

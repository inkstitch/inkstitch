---
title: "Outil lettrage"
permalink: /fr/docs/lettering/
last_modified_at: 2025-04-03
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
{% include upcoming_release_params.html %}

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

## Lettrage le long d'un chemin  {#lettering-along-path}

Les lettres d'Ink/Stitch ont été soigneusement dessinées pour une broderie optimale. Si vous essayez de les modifier avec les outils usuels d'inkscape, il se peut que cela ne fonctionne pas comme vous le souhaitez. Placez les lettres le long  d'un chemin est un gros travail. Cet outil va vous aider à le faire.

![Alignement d'un texte sur un cheminn avec les diverses options](/assets/images/docs/text_along_path_alignment.png)

### Usage

* Sélectionnez un chemin et un groupe de lettrage 
* Exécutez `Extensions > Ink/Stitch > Lettrage > Lettrage le long d'un chemin ...`
* Si `Étendre` est coché Ink/Stitch va étendre les espaces entre les lettres pour que le texte utilise tout le chemin. Sinon il gardera les distances du texte original. 
* Cliquez sur 'Appliquer'

Le lettrage suivra  la direction du chemin. Inverser le sens du chemin si nécessaire (`Chemin > ReverseInverser`).
{: .notice--info}

## Bibliothèque de polices

Un aperçu de toutes les polices disponibles se trouve dans la [bibliothèque de polices](/fr/fonts/font-library/).

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
* **Lettrage le long du chemin : position du texte :** Position du texte sur le chemin `batch lettering`.
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


## Créer de nouvelle polices pour Ink/Stitch
Lire le [tutoriel de création de police](/fr/tutorials/font-creation/).

Contactez nous  sur  [GitHub](https://github.com/inkstitch/inkstitch/issues) si vous souhaitez publier votre police dans l'outil de lettrage d'Ink/Stitch.

## Fichiers exemple concernant  le lettrage

{% include tutorials/tutorial_list key="techniques" value="Lettering" %}

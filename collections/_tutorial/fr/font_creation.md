---
permalink: /fr/tutorials/font-creation/
title: "Création de fonte pour Ink/Stitch"
language: fr
last_modified_at: 2025-12-29
excerpt: "Création de fonte pour Ink/Stitch "
image: "/assets/images/tutorials/font_creation_complement/multifont3.jpg"
tutorial-type: 
stitch-type:
tool:
techniques:
field-of-use:
user-level: 
toc: true

---
<!--

![Sample](/assets/images/tutorials/font_creation_complement/multifont3.jpg)
-->


**Attention** :
Une partie des outils Ink/Stitch présentés ici ne font pas partie d'Ink/Stitch 3.2.2. 
Le texte est assez long, mais il est recommandé de le lire entièrement avant de se lancer dans la création d'une fonte. 
{: .notice--warning }

L'objet de ce tutoriel est la création d'une fonte utilisable par le module de lettrage d'Ink/Stitch à partir d'un fichier de fonte ttf ou otf.
## Qu'est ce qu'une fonte pour le lettrage d'Ink/Stitch?

Les fichiers qui composent une fonte du lettrage sont regroupés dans un dossier spécifique à la fonte, qui réside dans le dossier des fontes d'Ink/Stitch (fontes intégrées à Ink/Stitch) ou dans le [dossier personnel de fonte](fr/docs/font-tools/#custom-font-directory) pour les fontes personnelles de l'utilisateur.

Chaque dossier de fonte doit comporter au moins deux fichiers :
- un fichier font.json qui contient les caractéristiques de la fonte
- au moins un fichier de calques de glyphes, qui comporte un calque par glyphe. 
La plupart des fontes du module de lettrage sont définies à l'aide d'un unique fichier de calque de glyphe, nommé ltr.svg. 

Ce fichier est prévu pour une broderie qui s'effectue de gauche à droite. 

Une fonte arabe ou hébreu du lettrage voit ses glyphes définis dans un fichier rtl.svg. 

Certaines polices, comme par exemple déjà vu, comportent les deux fichiers ltr.svg et rtl.svg. Dans ce cas, un texte multi ligne pourra être brodé en aller retour: dans le fichier ltr.svg, la broderie d'une lettre s'effectue de la gauche vers la droite tandis que dans le fichier rtl.svg, elle s'effectue de la droite vers la gauche. Le module de lettrage utilisera alternativement les deux fichiers sur les différentes lignes qui composent le texte.

Ces noms sont impératifs.... sauf si la fonte comporte beaucoup de glyphes, auquel cas, vous pouvez pour une fonte qui s'écrit de gauche à droite répartir vos glyphes dans plusieurs fichiers svg (pas de contrainte de nommage sur ces fichiers) que vous regroupez dans un dossier qui lui doit impérativement être nommé ltr.

Les dossiers des fontes du module de lettrage comportent aussi:
- un fichier preview.png (généralement 90x1100 px) qui contient l'aperçu brodé du nom de la fonte qui apparait dans le dialogue du lettrage.
- un fichier LICENSE, qui donne des informations sur la LICENCE de la police. Pour qu'une police de broderie créée à partir d'une fonte ttf ou otf ou autre puisse être légalement intégrée au module de lettrage, il faut que la licence de la fonte d'origine le permette. Attention, les licences dites commerciales ne permettent généralement pas l'intégration dans Ink/Stitch. C'est en revanche possible pour les fontes sous licence SIL (OFL), Apache et d'autres licences open source. Pour une utilisation uniquement personnelle de la fonte, moins de restrictions s'appliquent. Attention aux restrictions incluses dans la licence: par exemple il est impératif de modifier le nom d'une police sous licence OFL sauf à obtenir du créateur le droit de garder le nom initial de la police.

## Choix de la fonte
Le choix de la fonte et sa taille dépendent essentiellement du type de fonte que l'on souhaite créer: satins, points-droits, remplissage, appliqué. Une colonne satin ne peut être ni trop étroite (on considère qu'il faut au moins 1.5mm) ni trop large (au dessus 7mm il y a des risques de fragilité, au delà de 12mm beaucoup de machines ne savent pas faire), de ce fait, des lettres où l’épaisseur du trait est très variable seront difficiles à traiter en colonne satin. Les polices avec empattement sont plus difficiles à numériser que les polices sans empattement. Pour une police en appliqué au contraire on cherchera une police assez large. Le principal élément de choix reste malgré tout l'intérêt que l'on porte à la fonte. 

Symétriquement, si l'on est fixé sur une fonte particulière, la forme des lettres doit être prise en compte dans les choix de paramètrage de broderie.


## Création du fichier de glyphes

En plus de respecter les conventions de nommage, tout fichier de glyphes doit:
- comporter un calque par glyphe et le calque qui contient le glyphe A doit impérativement s'appeler GlyphLayer-A.
- un guide nommé "baseline" qui correspond a la ligne sur laquelle on écrit. Ink/Stitch a besoin de ce guide pour que le lettrage le long d'un chemin fonctionne correctement.
- il peut comporter d'autres éléments

### A la main
Il est tout a fait possible de créer manuellement un fichier de glyphes, mais c'est rarement la meilleure option:
- en partant d'un fichier de fonte .ttf ou .otf, vous bénéficiez de tout le travail de crénage fait par le créateur originel de la fonte
- en partant de fichiers de broderie il ne vous reste presque rien à faire.


### A partir de fichiers de broderie

Si vous disposez déjà d'un ensemble de fichiers de broderie (un fichier par lettre , dans un format machine ou en format svg), vous pouvez utiliser l'extension
[lettres vers police](/fr/docs/font-tools/#letters-to-font) pour regrouper tous ces glyphes dans un unique fichier de glyphes. 

### A partir d'une fonte ttf ou otf 

Dans ce cas vous pouvez utilisez [FontForge](https://fontforge.org/en-US/) pour créer un fichier de fonte svg, puis utiliser Ink/Stitch pour transformer ce fichier en fichier de calques de glyphe.
#### Création du fichier de fonte svg avec FontForge
Les fontes ttf ou otf comportent généralement un très grand nombre de glyphes et vous ne souhaitez probablement pas tous les convertir en broderie. 

Une première étape va donc être la
##### Sélection des glyphes 
On va effacer de la fonte tous les glyphes que l'on ne souhaite pas convertir en broderie
Ouvrez le fichier de fonte à l'aide de fontforge pour obtenir :

![FontForge](/assets/images/tutorials/font_creation/open_fontforge_fr.png)

Première solution : sélectionnez tous les glyphes que vous voulez conserver, puis `Édition > Sélectionner> Inverser` la sélection suivie de `Édition > Effacer`.

Si l'on ne sait pas vraiment où sont les glyphes que l'on veut conserver, il peut être utile de procéder de la manière suivant.

Choisissez dans les menus `Éléments> Info Fonte > Intervalle unicode`, pour obtenir ce type d'information:

![UnicodeIntervals](/assets/images/tutorials/font_creation/unicode_intervals_fr.png)

En cliquant sur un intervalle unicode de la liste, on sélectionne tous les glyphes de l'intervalle, il n'est pas rare de pouvoir effacer ou conserver tous les glyphes de l'intervalle. 

Lorsque, d'une manière ou d'une autre, l'on a effacés tous les glyphes indésirables, il ne reste plus qu'à faire `Fichier > Génerer Fonte`, choisir le type "police svg" et cliquer sur `Générer`.

![Generate fonts](/assets/images/tutorials/font_creation/generate_font_fr.png)

##### Transformation du fichier de fonte svg en fichier de calques de glyphes
Ouvrir le fichier svg ainsi créé dans Inkscape. Il a l'air complètement vide, c'est normal !! 

`Extensions > Ink/Stitch > Gestion des polices > Convertir la fonte svg en calques de glyphes`

![Convert to glyph layers](/assets/images/tutorials/font_creation/convert_to_glyph_layers_fr.png)

C'est le moment de décider quelle taille vous souhaitez pour votre police. 

Pour cela choisissez un caractère de référence dont vous savez qu'il est dans votre police svg (le M est une référence courante) et décidez de la hauteur souhaitée pour lui.

Cliquez sur `Appliquer`.

Votre fichier est alors converti en fichier de calques de glyphes, vous avez maintenant de nombreux calques.

En plus du guide "baseline", d'autres guides ont été posés. Il est judicieux de les vérouiller pour travailler ultérieurement dans ce fichier sans les déplacer. Cela peut être fait soit dans les propriétés du document, soit en cliquant sur le cadenas dans le coin supérieur gauche du canevas.

Les chemins de ce fichier ont leurs couleurs de contour et de remplissage indéterminées.
Sélectionnez tous les chemins dans tous les calques (si vos préférences inkscape n'autorisent pas la sélection d'objets cachés vous devrez montrer tous les objets pour cela), et donnez leur une couleur de remplissage, dites aussi qu'il n'y a pas de couleur de contour (ou donnez une couleur de contour et dites qu'il n'y a pas de couleur de fond). Vous pouvez masquez à nouveau les calques.

Si vous souhaitez créer une police qui se brode de gauche à droite, enregistrez ce fichier sous le nom ltr.svg dans un nouveau dossier situé dans votre dossier personnel de fontes.

## Création du fichier font.json
Une fois que le fichier ltr.svg existe, il est possible de créer le fichier font.json associé. Il est recommandé de faire cette opération dès maintenant.

`Extensions > Ink/Stitch > Gestion des polices > Génerer JSON....`

Cette extension va extraire des informations du fichier ltr.svg et les stocker dans un fichier font.json. Le dialogue de cette extension vous permet aussi d'ajouter des informations. La documentation est [ici](/fr/docs/font-tools/#generate-json).

Vous pourrez modifier ultérieurement ces informations grâce à `Extensions > Ink/Stitch > Gestion des polices > Modifier le fichier JSON....`
La documentation est [là](/fr/docs/font-tools/#edit-json).
### Le crénage, c'est quoi et ça fonctionne comment ?
Cette section est là pour les curieux, elle peut être passée au moins dans un premier temps.
Le crénage, c’est l’art d’ajuster l’espacement entre les lettres afin d’optimiser la lisibilité et l’esthétique d’un texte. Pour que cet espacement soit harmonieux et semble uniforme, il ne doit pas être identique entre toutes les paires de lettres. 
#### Où sont les informations
En particulier, ce fichier font.json contient les informations de crénage,extraites du fichier ltr.svg lors de la création du fichier font.json. Elles vont très fortement contribuer au positionnement des glyphes les uns par rapports aux autres. Pour décider de la position d'un glyphe, ink/stitch utilise trois types d'information:
- déplacer horizontalement ou verticalement un glyphe dans son calque influence sur sa position (sauf le tout premier caractère d'une ligne de texte qui lui est systématiquement à gauche toute sur la page (du moins avec un alignement des lignes à gauche). Le déplacement vertical est toujours pris en compte.
- des informations dites "horiz_adv_x". Il y a une valeur par défaut, et on peut associer une valeur à chaque glyphe. Le fichier de fonte généré par FontForge comporte cette information pour tous les glyphes qui n'ont pas été effacés. Cette information est intégrée au fichier font.json lors de sa création.
- des informations dites "hkern". Celles ci ne sont pas associées à des glyphes mais à des couples de glyphes (pas tous). Le fichier de fonte généré par FontForge comporte cette information pour tous les couples de glyphes pour lesquels le concepteur de la fonte ttf ou otf a donné cette information, que les glyphes aient été effacés ou non. Cette information est intégrée au fichier font.json lors de sa création.

Si vous n'êtes pas parti d'un fichier ttf, vous pouvez obtenir un crénage basique en donnant à horiz_adv_x_default la valeur 0 dans le fichcier json. Dans ce cas, Ink/Stitch utilise la largeur de chaque glyphe pour calculer le crénage.

#### Schématiquement, ça fonctionne comment ?
Ink/Stitch décompose un texte en ligne, une ligne en mots et un mot en glyphes.

Supposons que l'on veuille broder le mot Test
On suppose un alignement à gauche, et on parle ici de la position sur l'horizontale. L'extrémité gauche de la page est en x=0

- En début de ligne, le curseur est à 0, le premier caractère "T" est dessiné en démarrant en x =0
- avant de broder la suite, le curseur est
     * avancé de la valeur horiz_adv_x associée à T (la sienne si elle existe, sinon la valeur par défaut)
     * si le dessin du e, commence un peu avant le bord gauche de la page, on recule le curseur d'autant, si il commence après cela avance le curseur
     * si il y a une valeur hkern pour la paire "Te", on décale d'autant (une valeur positive diminue l’écart, une valeur négative l'augmente)

 ....et ainsi de suite pour toutes les lettres du mots

#### Comment rectifier un éventuel problème de crénage
Si vous constatez à l'usage un problème de crénage avec un certain glyphe :
- vérifiez que le glyphe est placé correctement dans son calque, il peut avoir été déplacé malencontreusement.
- si le problème se produit avec la plupart des autres glyphes, il faut modifier la valeur de horiz_adv_x pour ce glyphe
- si le problème ne se produit qu'avec quelques autres glyphes, il faut modifier (ou ajouter) les valeurs de hkern pour les couples de glyphes concernés

Ces deux dernières opérations se font en utilisant l'extension :
`Extensions > Ink/Stitch > Gestion des polices > Éditer le fichier json`

## Vérifiez que tout va bien
Si vous avez créés ces deux fichiers et qu'ils sont dans un dossier de votre dossier de fontes personnelles, votre fonte apparait dès maintenant dans le module de lettrage. La broderie de chaque lettre est paramétrée comme un remplissage automatique (si vous avez bien mis une couleur de remplissage sur chaque glyphe) ou comme un point droit (si vous avez mis une couleur de contour sur chaque glyphe). Il est trop tôt pour une broderie effective de qualité, mais tout doit être fonctionnel.

Vous pouvez aussi utiliser 

`Extensions > Ink/Stitch > Gestion des polices > Test de police` pour voir l'ensemble des glyphes des votre police. [Voir la documentation](/fr/docs/font-tools/#font-sampling). A tout instant, Test de police vous permettra de voir tous les glyphes non verrouillés de votre fichier de calques de glyphes.


## Passer à une fonte réellement brodable
Il faut maintenant passer de lettres qui ont été conçues pour être imprimées à des lettres prêtes à être brodées.
Chaque lettre est en soi une petite broderie, et toute la problématique usuelle des broderies s'applique.

Il est **très fortement recommandé de traiter entièrement quelques lettres** par exemple A, H, M , G, o, a, p pour avoir des lettres aux dessins assez différents, et de vérifier que tout se passe bien à la broderie. C'est le bon moment de décider par exemple comment [traiter les pointes](/fr/tutorials/satin-edges/) d'une fonte en colonne satin. Répondre à cette question rapidement vous permettra ensuite d'avoir la même approche sur toutes les pointes de la fonte. Quels paramètres vous semblent bien convenir par exemple quelle densité, quelle compensation. Pas trop d'inquiétude à ce sujet, il sera facile vers la fin du processus d'uniformiser les paramètres et de les modifier globalement pour l'ensemble de la police.


Le fait de travailler sur une fonte implique quelques problèmes particuliers.

### Les sauts de fil et les points d'arrêts.
#### Point trop n'en faut
En général plusieurs lettres seront brodées et vous voudrez avoir aussi peu de sauts et de point d'arrêt que possible. Un bon routage doit permettre la broderie d'une lettre connectée sans saut de fil, bien sur si la lettre est disconnectée (par exemple à cause d'accent) ou entre deux lettres, il est possible qu'il faille avoir des sauts de fil, mais à vous de faire en sorte qu'il y en ait le moins possible. Avant et après chaque saut, la machine fait un point d'arrêt, ce qui la ralentit et a de plus tendance à déformer la broderie. Evitez les donc autant que possible. Si la fonte doit être intégrée à Ink/Stitch, prenez en compte le fait que tout le monde n'a pas une machine qui coupe les fils, donc évitez les grands déplacements entre deux lettres, surtout si la machine vient à broder par dessus. Souvent, l'on commence une lettre en bas à gauche et on la termine en bas à droit justement pour éviter cela. 
Si vous n'êtes pas très familier avec les notions de points d'arrêts et de saut de fil, [la documentation est là](/fr/docs/stitches/lock-stitches/).

Si votre fonte est en colonne satin, essayez de faire en sorte que les points d'arrêts ne soient pas localisés sur les pointes des colonnes satins, c'est là qu'ils sont le plus visibles. Vous pouvez utiliser une commande position de fin sur une colonne satin qui est suivie d'un saut pour forcer la position du point d'arrêt.
#### Mais il en faut suffisamment.
Il faut aussi prendre un compte que de nombreux utilisateurs aiment a couper les sauts de fils entre les lettres ou entre le corps d'une lettre et son accent. Pour que la coupe puisse se faire sans que la broderie en souffre, il faut que le saut de fil soit réellement un saut de fil au sens d'Ink/Stitch, c'est à dire suivi et précédé d'un point d'arrêt, en particulier lorsque le saut suit une partie constitutive de la lettre (par exemple un colonne satin), il n'est pas forcement nécessaire entre deux chemins de dessous (par exemple un chemin de dessous dans le corps de la lettre suivi après un saut d'un chemin de dessous dans un accent)

`Extensions > Ink/Stitch > Gestion des polices > Forcer des points d'arrêt` permet de simplifier le processus. En particulier pour les fontes en colonnes satin constituées de lettres détachées, il est possible de forcer les points d'arrêts sur la dernière colonne satin de chaque glyphe. Pour gérer les points d'arrêt à la fin des accents, il est possible de grouper les éléments constitutifs des accents dans un groupe puis de forcer les points d'arrêt sur le dernier élément de chaque groupe. La documentation se trouve [là](/fr/docs/font-tools/#force-lock-stitches).
Alternativement, on peut utiliser le paramètre longueur minimum de saut pour s'assurer de la présence de points d'arrêts

### Coupes
Le lettrage d'Ink/Stitch permet à l'utilisateur d'ajouter s'il le souhaite des commandes de coupe après chaque lettre, ou chaque mot ou chaque ligne. Donc le seul endroit ou il peut être intéressant que vous en mettiez c'est à l'intérieur d'une lettre, quand celle-ci est composée de plusieurs morceaux

### Lettres avec diacritiques et organisation du travail
Les utilisateurs d'Ink/Stitch ont de nombreuses nationalités et pratiquent de nombreux langages, c'est pourquoi il est souhaitable que les fontes d'Ink/Stitch comportent de quoi satisfaire le plus de monde possible. Sans chercher à atteindre l'universalité, ajouter des lettres avec diacritiques permet de satisfaire un plus grand nombre d'utilisateurs.
Les diacritiques sont ces petits signes placés a coté d'une lettre. Ils sont souvent utilisés pour modifier la prononciation de la lettre. Les diacritiques comprennent tous les accents, mais aussi la cédille, le ogonek et autres apendices.

`Extensions > Ink/Stitch > Gestion des polices> Organiser les glyphes  vous aide à organiser votre travail pour éviter de faire plusieurs fois le même travail de digitalisation. Cette extension permet aussi quelques autres optimisation du travail à faire. 


L'objectif de cette extension est d'aider le numériseur de polices à organiser son travail étape par étape.

À chaque étape, un groupe de glyphes est placé en haut de la pile d'objets, et le créateur de polices doit numériser ces glyphes avant de passer à l'étape suivante.

Les étapes sont organisées de manière à diviser le travail en plus petits morceaux et à maximiser la réutilisation des lettres déjà numérisées.

Il faut vraiment tester ce qu'on fait à une étape car ce sera recopier pour d'autres lettres et on veut éviter de devoir corriger plusieurs fois la même bêtise:

- utiliser test de polices pour générer toutes les lettres non vérouillées
	- détection de problème 
	- simulation pour chasser les sauts malvenus. A faire de préférence avec les lettres augmentées au maximum permis
	- aperçu réaliste
	- broderie en vraie

 [Voir les différentes étapes](/fr/docs/font-tools/#organize-glyphs).



### Les utilisateurs d'Ink/Stitch
Il leur arrive de faire des choses étranges. Parmi les précautions à prendre:
#### Éviter les soucis dus à des choix inhabituels de préférences
Donner une valeur locale aux paramètres "longueur minimum de saut" et "longueur minimum de point" vous permet de vous assurer que l'utilisateur ne brodera pas votre fonte avec des valeurs étranges. 
#### Redimensionnements intempestifs
Les utilisateurs sont supposés redimensionner les fontes dans l'outil de lettrage. La réalité est parfois autre. Une précaution utile pour les lettrages en colonne satin est d'ajouter une longueur maximum de point.

### Réglage du redimensionement
Le créateur de fonte doit indiquer dans le json les valeurs de redimensionnement possible pour la fonte. Cela necessite d'essayer et de determiner ce qui convient. 

Dans le cas d'une fonte en satin, ce qui est primordial est la largeur des colonnes. 

`Extensions > Ink/Stitch > Résolution de problèmes> Information sur l'élément` vous permet de connaitre la longueur maximum et la longueur minimum des points de tous les éléments de broderie. Vous pouvez depuis l'onglet Aide, copier les résultats dans le presse papier puis dans un tableur pour trier et trouver quelles sont vos colonnes les plus larges et les plus étroites. Ces valeurs vous aideront a décider des redimensionnements possibles pour votre fonte.


### Ajout ou Suppression de glyphes
Si l'on ajoute ou supprime des glyphes après avoir créé les fichiers de la fonte , il faut impérativement lancer l'extension Modifier le fichier JSON afin que la liste des glyphes soit mise à jour. Attention si le glyphe n'était pas dans le fichier à partir duquel on a généré le fichier font.json, il faudra aller modifier la valeur horiz_adv_x du glyphe, on ne l'aura pas récupérée lors de la création du fichier json (en revanche les infos de type hkern elles sont bien là). Pour cette raison, en cas de doute, il vaut mieux au départ embarquer trop de glyphes que pas assez !


### Les fontes multicolores
Si l'on souhaite que le résultat du lettrage puisse être trié selon les couleurs, il y a deux manipulations à faire
- le prévoir dans le fichier font.json (soit à la création soit en éditant le fichier), la fonte doit être déclarée comme "triable".
- attacher à chaque chemin un [index de couleur](https://inkstitch.org/fr/docs/font-tools/#set-color-index). Dans la plupart des cas (toutes les lettres ont les mêmes couleurs dans le même ordre , tous les chemins d'une couleur donné à l'intérieur d'un glyphe sont consécutifs) on peut tout afficher dans tous les calques, choisir un des glyphes, sélectionner le premier objet à broder, sélectionner tous les objets de la même couleur (sélectionner même couleur de fond ou sélectionner même couleur de contour,ou les deux séquentiellement) et leur attribuer l'index un, puis choisir un objet de la prochaine couleur à broder, sélectionner tous les objets de la même couleur, leur attribuer l'index deux, etc.... Dans les cas plus compliqués il faudra réfléchir un peu plus pour déterminer les index.
- attention si votre fichier contient des groupes de commandes ,des lignes guide ou des textures il faut leur donner le même indice de couleur que les éléments auwxquels ils sont attachés.



### Limites de l'outil de lettrage
On ne peut pas (encore) utiliser toutes les fonctionalités d'ink/Stitch dans les fichiers de calques, par exemple les clones, les effets de chemins, les dégradés ne sont pas gérés par le lettrage.
On ne peut pas (encore) écrire une police pour toutes les langues du monde, mais depuis Ink/Stitch 3.2.0, les variantes contextuelles de l'alphabet arabe sont reconnues.

## Un petit plus bien sympathique
il est possible d'avoir des calques multiglyphes, pas seulement pour les ligatures. Par exemple dans la fonte allegria55, il existe un GlyphLayer-Inkscape_logo qui contient le logo d'inkscape.

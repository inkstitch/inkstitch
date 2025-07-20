---
permalink: /fr/tutorials/font_creation_complement/
title: "Création de fonte pour Ink/Stitch compléments "
language: fr
last_modified_at: 2025-06-22
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


![warning](/assets/images/tutorials/font_creation/work_in_progress.png)

Attention : fichier en cours de rédaction

Le texte  est assez long, mais il est recommandé de le lire entièrement avant de se lancer dans la création d'une fonte.....

L'objet de ce tutoriel est la création d'une fonte utilisable par le module de lettrage d'Ink/Stitch.
## Qu'est ce qu'une fonte pour le lettrage d'Ink/Stitch?`

Les fichiers qui composent une fonte du lettrage sont regroupés dans un dossier spécifique à la fonte,  qui réside dans le dossier des fontes d'Ink/Stitch (fontes intégrées à Ink/Stitch) où dans un [dossier personnel de fonte](fr/docs/font-tools/#custom-font-directory) pour les fontes personnelles de l'utilisateur.

Chaque dossier de fonte doit comporter au moins deux fichiers :
- un fichier font.json qui contient les caractéristiques de la fonte
- au moins un fichier de calques de glyphes, qui comporte un calque par glyphe. 
La plupart des fontes du module de lettrage sont définies à l'aide d'un unique fichier de calque de glyphe, nommé →.svg. 

Ce fichier est prévu pour une broderie qui s'effectue de gauche à droite (le sens de la flèche). 

Une fonte arabe ou hébreu du lettrage voit ses glyphes définis dans un fichier ←.svg. 

Certaines polices, comme par exemple  déjà vu, comportent les deux fichiers →.svg et ←.svg. Dans ce cas,  un texte multi ligne pourra être brodé en aller retour: dans le fichier →.svg, la broderie d'une lettre s'effectue de la gauche vers la droite tandis que dans le fichier ←.svg, elle s'effectue de la droite vers la gauche. Le module de lettrage  utilisera alternativement les deux fichiers sur les différentes lignes qui composent le texte.

Ces noms sont impératifs.... sauf si la fonte comporte beaucoup de glyphes, auquel cas, vous pouvez pour une fonte qui s'écrit de gauche à droite répartir vos glyphes dans plusieurs fichiers svg (pas de contrainte de nommage sur ces fichiers) que vous regroupez dans un dossier qui lui doit impérativement être nommé →

Les dossiers des fontes du module de lettrage comportent aussi:
- un fichier preview.png (généralement 90x1100 px) qui contient l'aperçu brodé du nom de la fonte qui apparait dans le dialogue du lettrage
- un fichier LICENSE, qui donne des informations sur la LICENSE de la police. Pour qu'une police de broderie créée à partir d'une fonte ttf ou otf ou autre puisse être légalement intégrée au module de lettrage, il faut que la licence de la fonte d'origine le permette. Attention, les licences dites commerciales ne permettent généralement pas l'intégration dans Ink/Stich. C'est en revanche possible pour les fontes sous licence SIL (OFL), Apache et d'autres licences open source. Pour une utilisation uniquement personnelle de la fonte, moins de restrictions s'appliquent. Attention aux restrictions incluses dans la license: par exemple il est impératif de modifier le nom d'une police sous licence OFL sauf à obtenir du créateur le droit de garder le nom initial de la police.

## Choix de la fonte
Le choix de la fonte  et sa taille dépendent essentiellement du type de fonte que l'on souhaite créer: satins, points-droits, remplissage, appliqué. Une colonne satin ne peut être ni trop étroite (on considère qu'il faut au moins 1.5mm) ni trop large (au dessus 7mm il y a des risques de fragilité, au delà de 12mm beaucoup de machines ne savent pas faire), de ce fait, des lettres où l’épaisseur du trait est très variable seront difficiles à traiter en colonne satin. Les polices avec empattement sont plus difficiles à numériser que les polices sans empattement. Pour une police en appliqué au contraire on cherchera une police assez large. Le principal élément de choix reste malgré tout l'intérêt que l'on porte à la fonte. 

Symétriquement, si l'on est fixé sur une fonte particulière, la forme des lettres doit être prise en compte dans les choix de pramètrage de broderie.


## Création du fichier de glyphes
En plus de respecter les conventions de nommage, tout fichier de glyphes doit:
- comporter un calque par glyphe et le calque qui contient le glyphe A doit impérativement s'appeler GlyphLayer-A.
- un guide nommé "baseline" qui correspond a la ligne sur laquelle on écrit. Ink/Stitch a besoin de ce guide pour que le lettrage le long d'un chemin fonctionne correctement.
- il peut comporter d'autres éléments

### A la main
Il est tout a fait possible de créer manuellement un fichier de glyphe, mais c'est rarement la bonne option.

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

![FontForge](/assets/images/tutorials/font_creation/open_fontforge.png)

Première solution : sélectionnez tous les glyphes que vous voulez conserver, puis `Édition > Sélectionner> Inverser` la sélection suivie de `Édition > Effacer`.

Si l'on ne sait pas vraiment où sont les glyphes que l'on veut conserver, il peut être utile de procéder de la manière suivant.

Choisissez dans les menus `Éléments> Info Fonte > Intervalle unicode`, pour obtenir ce type d'information:

![UnicodeIntervals](/assets/images/tutorials/font_creation/unicode_intervals.png)
En cliquant sur un intervalle unicode de la liste, on sélectionne tous les glyphes de l'intervalle, il n'est pas rare de pouvoir effacer ou conserver tous les glyphes de l'intervalle. 

Lorsque, d'une manière ou d'une autre, l'on a effacés tous les glyphes indésirables, il ne reste plus qu'à faire `Fichier > Génerer Fonte`, choisir le type "police svg" et cliquer sur `Générer`.

![UnicodeIntervals](/assets/images/tutorials/font_creation/generer_fonte.png)

##### Transformation du fichier de fonte svg en fichier de calques de glyphes
Ouvrir le fichier svg ainsi créé dans Inkscape. Il a l'air complètement vide, c'est normal !! 
<span color=blue>

`Extensions > Ink/Stitch > Gestion des polices > Convertir la fonte svg en calques de glyphes`

![UnicodeIntervals](/assets/images/tutorials/font_creation/convert_to_glyphs.png)
Choisissez un nombre de glyphes supérieur au nombre de glyphes de votre police, sauf si  vous  êtes en phase de test et souhaitez limiter le nombre de glyphes.
C'est surtout  le moment  de décider quelle taille vous souhaitez pour votre police. 

Pour  cela choisissez un caractère de référence dont vous savez qu'il est dans votre police svg  (le M est une référence  courante) et décidez de la hauteur souhaitée pour lui.

Cliquez sur `Appliquer`.

Votre fichier est alors converti en fichier de calques de glyphes, vous avez maintenant de nombreux calques.

En plus du guide "baseline", d'autres guides ont été posés. Il est judicieux de les vérouiller pour travailler ultérieurement dans ce fichier sans les déplacer.

Les chemins de ce fichier ont leurs couleurs de contour et de remplissage indéterminées.
Sélectionnez tous les chemins dans tous les calques (si vos préférences inkscape n'autorisent pas la sélection d'objets cachés vous devrez montrer tous les objets pour cela), et donnez leur une couleur de remplissage, dites aussi qu'il n'y a pas de couleur de contour (ou donnez une couleur de contour et dites qu'il n'y a pas de couleur de fond). Vous pouvez masquez à nouveau les calques.

Si vous souhaitez créer une police qui se brode de gauche à droite, enregistrez ce fichier sous le nom →.svg dans un nouveau dossier situé dans votre dossier personnel de fontes.


## Création du fichier font.json
Une fois que le fichier →.svg  existe,  il est possible de créer le fichier font.json associé. Il est recommandé de faire cette opération dès maintenant.

`Extensions > Ink/Stitch > Gestion des polices > Génerer JSON....`

Cette extension va extraire des informations du fichier →.svg et les stocker dans un fichier font.json. Le dialogue de cette extension vous permet aussi d'ajouter des informations. La documentation est [ici](/fr/docs/font-tools/#generate-json).

Vous pourrez modifier ultérieurement ces informations grâce à  `Extensions > Ink/Stitch > Gestion des polices > Modifier le fichier JSON....`
La documentation est [là](/fr/docs/font-tools/#edit-json).
### Le crénage, c'est quoi et ça fonctionne comment ?
Cette section est là pour les curieux, elle peut être passée au moins dans un premier temps.
#### Où sont les informations
En particulier, ce fichier font.json contient les informations de crénage,extraites du fichier →.svg lors de la création du fichier font.json.  Elles vont très fortement contribuer au positionnement des glyphes les uns par rapports aux autres. Pour décider de la position d'un glyphe,  ink/stitch utilise trois types  d'information:
- déplacer horizontalement ou verticalement un glyphe dans son calque influence sur sa position (sauf le tout premier caractère d'une ligne de texte qui lui est systématiquement à gauche toute sur la page (du moins avec un alignement des lignes à gauche). Le déplacement vertical est toujours pris en compte.
- des informations dites "horiz_adv_x". Il y a une valeur par défaut, et on peut associer une valeur à chaque glyphe. Le fichier de fonte généré par FontForge comporte cette information pour tous les glyphes qui n'ont pas été effacés.  Cette information est intégrée au fichier font.json lors de sa création.
- des informations dites "hkern". Celles ci ne sont pas associées à des glyphes mais à des couples de glyphes (pas tous). Le fichier de fonte généré par FontForge comporte cette informations pour tous les couples de  glyphes pour lesquels le concepteur de la fonte ttf ou otf a donné cette information, que les glyphes aient été effacés ou non. Cette information est intégrée au fichier font.json lors de sa création.
#### Schématiquement,  ça fonctionne comment ?
Ink/stitch décompose un texte en ligne, une ligne en mots et un mot en glyphes.

Supposons que l'on veuille broder le mot Test
On suppose un alignement à gauche, et on parle ici de la position sur l'horizontale. L'extrémité gauche de la page est en x=0

- En début de ligne,  le curseur est à 0, le premier caractère "T" est dessiné en démarrant en x =0
- avant de broder la suite, le curseur est
  * avancé de la valeur horiz_adv_x  associée à T  (la sienne si elle existe, sinon la valeur par défaut)
  * si le dessin du e, commence un peu avant le bord gauche de la page, on recule le curseur d'autant, si il commence après cela avance le curseur
  * si il y a une valeur hkern pour la paire "Te", on décale d'autant (une valeur positive diminue l’écart, une valeur négative l'augmente)

   ....et ainsi de suite pour toutes les lettres du mots






## Vérifiez que tout va bien
Si vous avez créer ces deux fichiers et qu'ils sont dans un dossier de votre dossier de fontes personnelles, votre fonte apparait dès maintenant dans le module de lettrage. La broderie de chaque lettre est paramétrée comme un remplissage automatique (si vous avez bien mis une couleur de remplissage sur chaque glyphe) ou comme un point droit (si vous avez mis une couleur de contour sur chaque glyphe). Il est trop tôt pour une broderie effective de qualité, mais tout doit être fonctionnel.

Vous pouvez aussi utiliser 

`Extensions > Ink/Stitch > Gestion des polices > Test de police` pour voir l'ensemble des glyphes des votre police. [Voir la documentation](/fr/docs/font-tools/#font-sampling). A tout instant, Test de police vous permettra de voir tous les glyphes non vérouillés de votre fichier de calques de glyphes

:thinking: A partir d'ici c'est incomplet et dans le désordre. 
## Passer à une fonte réellemment brodable
On en arrive à la phase ou il faut passer d'une numérisation automatique à des choix pertinents pour une belle broderie.
La problèmatique est quasiment la même que pour toute conception de broderie.

Il est **très fortement recommmmandé de traiter entièrement quelques lettres**  par exemple  A, H, M , G, o, a, p pour avoir des lettres aux dessins assez différents, et de vérifier que tout se passe bien  à la broderie. C'est le bon moment de décider par exemple comment [traiter les pointes](/fr/tutorials/satin-edges/) d'une fonte. en colonne satin. Répondre à cette question rapidement vous permettra ensuite d'avoir la même approche sur toutes les pointes de la fonte. Quels paramètres vous semblent bien convenir par exemple quelle densité, quelle compensation. Pas trop d'inquiétude à ce sujet, il sera facile vers la fin du processus d'uniformiser les paramètres et de les modifier globalement pour l'ensemble de la police.

### Les sauts de fils
Il y aura forcément des sauts de fils, mais à vous de faire en sorte qu'il y en ait le moins possible. Avant et après chaque saut, la machine fait un point d'arrêt, ce qui la ralentit et a de plus tendance à déformer la broderie. Evitez les donc autant que possible. Si la fonte doit être intégrée à Ink/Stitch, prenez en compte le fait que tout le monde n'a pas une machine qui coupe les fils, donc évitez les grands déplacements  entre deux lettres, surtout si la machine vient à broder par dessus. Souvent, l'on commence une lettre en bas à gauche et on la termine en bas à droit justement pour eviter cela. 
Si vous n'êtes pas très familier avec les notions de points  d'arrêts et de saut de fil, [la documentation est là](/fr/docs/stitches/lock-stitches/).


### Les commandes de coupe : 
Le lettrage d'Ink/Stitch permet  à l'utilisateur d'ajouter s'il le souhaite des commmandes de coupe après chaque lettre, ou chaque mot ou chaque ligne. Donc le seul endroit ou il peut être interessant que vous en mettiez c'est à l'intérieur d'une lettre, quand celle-ci est composée de plusieurs morceaux
### Cas d'une fonte en point droits
Selon la fonte de départ, le travail à faire est très différent. 

![running_stitch_samples](/assets/images/tutorials/font_creation/running_stitch-sample.png)

Pour la police du bas, utiliser les contours des lettres pour créer les points droits donne un résultat correct, mais pas vraiment pour la police du haut. 


S'il n'est pas possible d'utiliser les contours des lettres, soit on redessine manuellement les lettres, ou l'on utilise l'extension 
`Extensions > Ink/Stitch > Outils traits > Remplissage en  trait`, avec probablements des retouches à faire.

Dans tous les cas, il faudra traiter la questions des sauts de fil, aussi bien à l'intérieur des lettres qu'entre les lettres.
Il faudra pour cela séparer (Inkscape > Chemin > Séparer) chaque chemin (à faire globalement sur tous les calques).

Lorsqu'un caractère est composé de plusieurs chemins, il faut prévoir un routage, c'est à dire décider où commence et termine la broderie de chaque lettre, et autant que faire se peut éviter des sauts de fils. Si le dessin de la lettre est connexe, on essayera de n'avoir aucun saut de fil. Vous pouvez faire le outage vous même  ou utiliser l'arrangement automatique de points droits d'inkstitch
Remarque : il existe de très rares polices "singleline" svg qui donnent directement un resultat exploitable en point droit. Plus d'infos [ici](https://cutlings.datafil.no/single-line-fonts-in-inkscape-revisited/)

### Cas d'une fonte en remplissage ou en appliqué

### Cas d'une fonte en colonnes satins
Les fontes en colonnes satins  sont en souvent celles qui prennent le plus de temps. Plusieurs outils s'offrent maintenant à nous pour transformer les remplissages en satin. Rien de totalement automatique ici, il faut intervenir sur chaque calque : 
- l'extension Extensions > Inkstitch > Outils Satin : Remplissage en Satin est probablement le plus rapide. Lorsque la forme de la lettre est très tarabiscotée, ou lorsqu'on maitrise mal l'outil (mais au bout de quelques lettres, vous allez vous améliorer)  on peut commencer par découper la lettres en plusieurs morceaux plus faciles à gerer, à l'aide de l'outil  de construction de forme (tracer quelques chemins là ou vous voulez découper)
- chacune des méthodes de construction de colonne satin d'Innk/Stitch peut convenir, à vous de choisir.
- attention à la position des points d'arrêt, sur une pointe de satin ils sont particulièrement visibles. A vous de faire en sorte qu'une colonne satin qui est suivie d'un saut ne termine pas sur une de ses extrémités. 

### La question des sauts de fil et des commandes de coupe
Faut il ajouter des commandes de coupe ? 
Chasser les sauts de fils inutiles à l'interieur des lettres
Assurer qu'il y a bien des noeuds là où ils sont necessaires, mais pas là ou il n'en faut pas

### Les lettres accentuées

### Influence des préférences de l'utilisateur
ou comment faire en sorte qu'il n'y en ait pas en donnant des valeurs locales à la longueur minimum de point (indispensable par ailleurs si on prévoit une petite fonte) et à la longueur minimum de saut.

###  Les tests de broderie
a faire sur quelques lettres au depart avant  de tout digitaliser
a faire sur toutes les lettres ulterieurement, à taille min et à taille max


### Les outils de simulation

### Les retouches sur le crénage

### Ajout ou Suppression de glyphes
Si l'on ajoute ou supprime des glyphes, il faut impérativement lancer l'extension Modifier le fichier JSON afin que la liste des glyphes soit mise à jour. Attention si le glyphe n'était pas dans le fichier à partir duquel on a généré le fichier font.json, il faudra aller modifier la valeur horiz_adv_x du glyphe, on ne l'aura pas récupérée lors de la création du son (en revanche les infos de type hkern elles sont bien là). Pour cette raison, en cas de doute, il vaut mieux au départ embarquer trop de glyphes que pas assez !


### Les fontes multicolores
Si l'on souhaite que le résultat du lettrage puisse être trié selon les couleurs, il  y a deux manipulations à faire
- le prévoir dans le fichier font.json (soit à la création soit en éditant le  fichier), la fonte doit être déclarée comme "triable".
- attacher à chaque chemin un [index de couleur](https://inkstitch.org/fr/docs/font-tools/#set-color-index). Dans la plupart des cas (toutes les lettres ont les mêmes couleurs dans le même ordre , tous les chemins d'une couleur donné à l'interieur d'un glyphe sont consécutifs) on peut tout afficher dans tous les calques, choisir un des glyphes, selectionner le premier objet  à broder, sélectionner tous les objets de la mêmme couleur(selectionner même couleur de fond ou selectionner même couleur de contour,ou les deux séquentiellement) et leur attribuer l'index un, puis choisir un objet de la prochaine couleur à broder, sélectionner tous les objets de la même couleur, leur attribuer l'index deux, etc.... Dans les cas plus compliqués il faudra réflechir un peu plus pour déterminer les index.



## Routage



## limites de l'outil de lettrage
on ne peut pas (encore) utiliser toutes les fonctionalités d'ink/stitch dans les fichiers de calques,par exemple  les clones, les effets de chemins  ne sontpas férées correctement par le lettrage
on ne peut pas (encore) écrire une police  pour toutes les langues du monde, en particulier aujourd'hui, seules les variantes contextuelles de l'alphabet arabe sont reconnues
actuellement lors ce qu'il y a plusieurs fichiers de calques de glyphes dans  un fichier fleche.svg,  la  gestion de la liste des glyphes se fait mal.

## les petits plus 
il est possible d'avoir des calques  multiglyphes, pas seulement  pour les ligatures 

les outils utiles  à citer là ou il faut pas
Troubleshooting , et comment rendre les fontes plus robustes
information sur l'élément : pourchasser les satins trop larges et etablir une valeur raisonable sur la taille min et max  de broderie de la fonte
saut en trait







 


 









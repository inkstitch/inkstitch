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

L'objet de ce tutoriel est la création d'une fonte utilisable par le module de lettrage d'Ink/Stitch.
## Qu'est ce qu'une fonte pour le lettrage d'Ink/Stitch?
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
- un fichier LICENSE, qui donne des informations sur la LICENSE de la police. Pour qu'une police de broderie créée à partir d'une fonte ttf ou otf ou autre puisse être légalement intégrée au module de lettrage, il faut que la licence de la fonte d'origine le permette. Attention, les licences dites commerciales ne permettent généralement pas l'intégration dans Ink/Stich. C'est en revanche possible pour les fontes sous licence SIL (OFL), Apache et d'autres licences open source. Pour une utilisation uniquement personnelle de la fonte, moins de restrictions s'appliquent.

## Choix de la fonte
Le choix de la fonte  et sa taille dépendent essentiellement du type de fonte que l'on souhaite créer: satins, points-droits, remplissage, appliqué. Une colonne satin ne peut être ni trop étroite (on considère qu'il faut au moins 1.5mm) ni trop large (au dessus 7mm il y a des risques de fragilité, au delà de 12mm beaucoup de machines ne savent pas faire), de ce fait, des lettres où l’épaisseur du trait est très variable seront difficiles à traiter en colonne satin. Les polices avec empattement sont plus difficiles à numériser que les polices sans empattement. Pour une police en appliqué au contraire on cherchera une police assez large. Le principal élément de choix reste malgré tout l'intérêt que l'on porte à la fonte. 


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

Dans ce cas vous pouvez utilisez [FontForge](https://fontforge.org/en-US/) pour créer un fichier de fonte svg, puis utiliser Ink/Stitch pour transformer ce fichier en fichiers de calques de glyphe.
#### Création du fichier de fonte svg avec FontForge
Les fontes ttf ou otf comportent généralement un très grand nombre de glyphes et vous ne souhaitez probablement pas tous les convertir en broderie. 

Une première étape va donc être la
##### Sélection des glyphes 
On va effacer de la fonte tous les glyphes que l'on ne souhaite pas convertir en broderie
Ouvrez le fichier de fonte dans à l'aide de fontforge pour obtenir :

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

`Extensions > Ink/Stitch > Gestion des polices > Convertir la fonte svg en calques de glyphes`

![UnicodeIntervals](/assets/images/tutorials/font_creation/convert_to_glyphs.png)
Choisissez un nombre de glyphes supérieur au nombre de glyphes de votre police, sauf si  vous  êtes en phase de test et souhaitez limiter le nombre de glyphes.
C'est surtout  le moment  de décider quelle taille vous souhaitez pour votre police. 

Pour  cela choisissez un caractère de référence dont vous savez qu'il est dans votre police svg  (le M est une référence  courante) et décidez de la hauteur souhaitée pour lui.

Cliquez sur `Appliquer`.

Votre fichier est alors converti en fichier  de calques de glyphes, vous avez maintenant de nombreux calques.

En plus du guide "baseline", d'autres guides ont été posés. Il est judicieux de les vérouiller pour travailler ultérieurement dans ce fichier sans les déplacer.

Les chemins de ce fichier ont leur couleur de contour et de remplissage indeterminées.
Sélectionnez tous les chemins dans tous les calques (si vos préférences inkscape n'autorisent pas la sélection d'objets cachés vous devrez montrer tous les objets pour cela), et donnez leur une couleur de remplissage, dites aussi qu'il n'y a pas de couleur de contour (ou donnez une couleur de contour et dites qu'il n'y a pas de couleur de fond). Vous pouvez masquez à nouveau les calques.

Si vous souhaitez créer une police qui se brode de gauche à droite, enregistrez ce fichier sous le nom →.svg dans un nouveau dossier situé dans votre dossier personnel de fontes.


## Création du fichier font.json
Une fois que le fichier →.svg  existe,  il est possible de créer le fichier font.json associé.

`Extensions > Ink/Stitch > Gestion des polices > Génerer JSON....`

Cette extension va extraire des informations du fichier →.svg et les stocker dans un fichier font.json. Le dialogue de cette extension vous permet aussi d'ajouter des informations. La documentation est [ici](/fr/docs/font-tools/#generate-json).

Vous pourrez modifier ultérieurement ces informations grâce à  `Extensions > Ink/Stitch > Gestion des polices > Modifier le fichier JSON....`
La documentation est [là](/fr/docs/font-tools/#edit-json).

## Vérifiez que tout va bien
Si vous avez créer ces deux fichiers et qu'ils sont dans un dossier de votre dossier de fontes personnelles, votre fonte apparait dès maintenant dans le module de lettrage. La broderie de chaque lettre est paramétrée comme un remplissage automatique (si vous avez bien mis une couleur de remplissage sur chaque glyphe) ou comme un point droit (si vous avez mis une couleur de contour sur chaque glyphe). Il est trop tôt pour une broderie effective de qualité, mais tout doit être fonctionnel.

Vous pouvez aussi utiliser 

`Extensions > Ink/Stitch > Gestion des polices > Test de police` pour voir l'ensemble des glyphes des votre police. [Voir la documentation](/fr/docs/font-tools/#font-sampling)



## La suite à écrire : travailler les fichiers de calques de glyphes
pour l'instant en vrac et dans le desordre ne pas oublier 
Faut il ajouter des commandes de coupe ? 
Chasser les sauts de fils inutiles à l'interieur des lettres
Assurer qu'il y a bien des noeuds là où ils sont necessaires, mais pas là ou il n'en faut pas
Uniformiser le paramètrage
Routage
Tester la fonte
cas des fontes en couleurs
on ne peut pas (encore) utiliser toutes les fonctionalités d'ink/stitch dans les fichiers de calques,par exemple  les clones, les effets de chemins  ne sontpas férées correctement par le lettrage
on ne peut pas (encore) écrire une police  pour toutes les langues du monde
il est possible d'avoir des calques  multiglyphes, pas seulement  pour les ligatures 

les outils utiles  à citer:
Troubleshooting , et comment rendre les fontes plus robustes
information sur l'élément : pourchasser les satins trop larges et etablir une valeur raisonable sur la taille min et max  de broderie de la fonte
saut en trait







 


 









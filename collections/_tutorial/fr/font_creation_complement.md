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

Attention : fichier en cours de rédaction

L'objet de ce tutoriel est la création d'une fonte utilisable par le module de lettrage d'Ink/Stitch.
## Qu'est ce qu'une fonte pour le lettrage d'Ink/Stitch?
Les fichiers qui composent une fonte du lettrage sont regroupés dans un dossier spécifique à la fonte,  qui réside dans le dossier des fontes d'Ink/Stitch (fontes intégrées à Ink/Stitch) où dans un [dossier personnel de fonte](fr/docs/font-tools/#custom-font-directory) pour les fontes personnelles de l'utilisateur.

Chaque dossier de fonte doit comporter au moins deux fichiers :
- un fichier json qui contient les caractéristiques de la fonte
- au moins un fichier de calques de glyphes, qui comporte un calque par glyphe. 
La plupart des fontes du module de lettrage sont définies à l'aide d'un unique fichier de calque de glyphe, nommé →.svg. 

Ce fichier est prévu pour une broderie qui s'effectue de gauche à droite (le sens de la flèche). 

Une fonte arabe ou hébreu du lettrage voit ses glyphes définis dans un fichier ←.svg. 

Une police comme déjà vu comporte elle les deux fichiers →.svg et ←.svg, un texte multi ligne pourra être brodé en aller retour: dans le fichier →.svg, la broderie d'une lettre s'effectue de la gauche vers la droite tandis que dans le fichier ←.svg, elle s'effectue de la droite vers la gauche. 

Ces noms sont impératifs.... sauf si la fonte comporte beaucoup de glyphes, auquel cas, vous pouvez pour une fonte qui s'écrit de gauche à droite répartir vos glyphes dans plusieurs fichiers svg (pas de contrainte de nommage sur ces fichiers) que vous regroupez dans un dossier qui lui doit impérativement être nommé →

Les dossiers des fontes du module de lettrage comportent aussi:
- un fichier preview.png (généralement 90x1100 px) qui contient l'aperçu brodé du nom de la fonte qui apparait dans le lettrage
- un fichier LICENSE, qui donne des informations sur la LICENSE de la police. Pour qu'une police de broderie créée à partir d'une fonte ttf ou otf ou autre puisse être légalement intégrée au module de lettrage, il faut que la licence de la fonte d'origine le permette. Attention, les licences dites commerciales ne permettent généralement pas l'intégration dans Ink/Stich. C'est en revanche possible pour les fontes sous licence SIL (OFL), Apache et d'autres licences open source. Pour une utilisation uniquement personnelle de la fonte, moins de restrictions s'appliquent.

## Choix de la fonte
Le choix de la fonte dépend essentiellement du type de fonte que l'on souhaite créer: satins, points-droits, remplissage, appliqué.


## Création du fichier de glyphes
En plus de respecter les conventions de nommage, tout fichier de glyphes doit:
- comporter un calque par glyphe et le calque qui contient le glyphe A doit impérativement s'appeler GlyphLayer-A.
- un guide nommé "baseline" qui correspond a la ligne sur laquelle on écrit. Ink/Stitch a besoin de ce guide pour que le lettrage le long d'un chemin fonctionne correctement.
- il peut comporter d'autres éléments

### A la main
Il est tout a fait possible de créer manuellement un fichier de glyphe, mais c'est rarement la bonne option.

### A partir de caractères de broderie

Si vous disposez déjà d'un ensemble de fichiers de broderie (un fichier par lettre , dans un format machine ou en format svg), vous pouvez utiliser l'extension
[lettres vers police](/fr/docs/font-tools/#letters-to-font) pour regrouper tous ces glyphes dans un unique fichier de glyphes. 

### A partir d'une fonte ttf ou otf

Dans ce cas vous pouvez utilisez [fontforge](https://fontforge.org/en-US/) pour créer un fichier de fonte svg, puis utiliser Ink/Stitch pour transformer ce fichier en fichiers de calques de glyphe.
#### Création du fichier de fonte svg
Les fontes ttf ou otf comportent généralement un très grand nombre de glyphes et vous ne souhaitez probablement pas tous les convertir en broderie. 

Une première étape va donc être la
##### Sélection des glyphes 
On va effacer de la fonte tous les glyphes que l'on ne souhaite pas convertir en broderie
Ouvrez le fichier de fonte dans à l'aide de fontforge pour obtenir :

![FontForge](/assets/images/tutorials/font_creation/open_fontforge.png)

Première solution : sélectionnez tous les glyphes que vous voulez conserver, puis `Édition > Sélectionner> Inverser` la sélection suivie de `Édition > Effacer`.

Si l'on ne sait pas vraiment où sont les glyphes que l'on veut conserver, il peut être utile de procéder de la manière suivant.

Choisissez dans les menus `Élements> Info Fonte > Intervalle unicode`, pour obtenir ce type d'information:

![UnicodeIntervals](/assets/images/tutorials/font_creation/unicode_intervals.png)
En cliquant sur un intervalle unicode de la liste, on sélectionne tous les glyphes de l'intervalle, il n'est pas rare de pouvoir effacer ou conserver tous les glyphes de l'intervalle. 

Lorsque, d'une manière ou d'une autre, l'on a effacés tous les glyphes indésirables. Il ne reste plus qu'à faire `Fichier > Génerer Fonte`, choisir le type "police svg" et cliquer sur `Générer`.

![UnicodeIntervals](/assets/images/tutorials/font_creation/generer_fonte.png)

#### Transformation du fichier de fonte svg en fichier de calques de glyphes
Ouvrir le fichier svg ainsi créé dans Inkscape. Il a l'air complètement vide, c'est normal !!

`Extensions > Ink/Stitch > Gestion des polices > Convertir la fonte svg en calques de glyphes`

![UnicodeIntervals](/assets/images/tutorials/font_creation/convert_to_glyphs.png)


## Utilisation d'Ink/Stitch pour créer un fichier de calques de glyphes
## Créer le fichier json, 
## Créer les lettres
### Fonte en colonne satin
### Fonte en points droits
### Fonte en appliqué






 


 









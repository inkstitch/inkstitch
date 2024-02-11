---
title: "Documentation"
permalink: /fr/developers/documentation/
last_modified_at: 2022-05-29
toc: true
---
Nous voulons décrire toutes les fonctions possibles avec du texte, des images et/ou des vidéos. Egalement fournir des instructions sur le processus d'installation et donnez un aperçu du meilleur flux de travail. De plus, nous souhaitons fournir des exemples de fichiers que d'autres utilisateurs peuvent utiliser. Il serait également agréable d'obtenir des exemples d'images de motifs brodés pour prouver ce que Ink/Stitch est capable de faire.

Une autre partie encore incomplète de la documentation concerne  l'aide aux nouveaux développeurs qui commencent à plonger dans le code:  nous  souhaiterions  leur  permettre  d'introduire de nouvelles fonctionnalités dans Ink/Stitch ou tout ce qu'ils pourraient proposer.

## S'impliquer

Ce site web a besoin de beaucoup de soins pour la  génération de nouveau contenu et la mise à jour de contenu existant pour suivre le développement continu d'Ink/Stitch. Nous pourrions utiliser n'importe quel coup de main.

Vous n'avez pas besoin de savoir comment créer un site Web, car nous utilisons [Markdown](https://help.github.com/articles/basic-writing-and-formatting-syntax/) pour la mise en forme du texte. Tous les fichiers nécessaires à la création du site Web se trouvent dans le [gh-pages-branch](https://github.com/inkstitch/inkstitch/tree/gh-pages) GitHub.

Si vous souhaitez aider avec la documentation, déposez un rapport d'erreur (issue) sur [github](https://github.com/inkstitch/inkstitch/issues) et dites-nous que vous êtes prêt à aider.

## Travailler sur les pages Github

Les pages Github utilisent [Jekyll](https://jekyllrb.com/), un générateur de pages statiques. Il est également possible de l'installer localement à des fins de test. Pour obtenir des instructions, consultez leur site Web.
Nous utilisons le [Thème Minimal Mistake] (https://mmistakes.github.io/minimal-mistakes/), avec très peu de personnalisation.

### Structure de base des fichiers 
* `_collections/_posts/langue`   actualités
* `_collections/_docs/langue` documentation 
* `_collections/_tutorials/language` pages principales du tutoriel
* `_collections/_tutorial/language` tutoriels spécifiques  
*  _collections/_developers/language` documentation pour les développeurs
* `_pages/langue` pages statiques telles que les informations, les termes ou le plan du site
*  `assets/language` fichiers multimédias(images) et style de site Web (css)
* `_data/navigation_language.yml` données de navigation  sur le site Web

### Modification des fichiers existants
Modifiez le contenu comme vous le souhaitez. Stylez votre texte avec [markdown](https://help.github.com/articles/basic-writing-and-formatting-syntax/), qui est également utilisé pour les rapports d'erreur (issue) de github, etc.

Avant d'enregistrer le fichier, veuillez également modifier la date en haut de la page.

### Ajout de nouveaux fichiers


#### Documents, Tutoriels, Développeurs

Lors de l'ajout de nouvelles pages, faites attention à la numérotation des noms de fichiers (docs et tutoriels).

Les nombres sont définis pour pouvoir utiliser les liens précédents/suivants sous l'article. Ils s'adaptent également à la structure du menu de la barre latérale, que vous devez également mettre à jour lors de l'ajout de nouvelles pages.

La modification des noms de fichiers n'empêchera pas le site Web de trouver les fichiers, car ils utilisent des permaliens. Vous pouvez donc modifier les chiffres selon vos besoins.

Chaque page doit commencer par quelque chose comme ceci :


```
---
title: "Some Title"
permalink: /unique/permalink
excerpt: "Small description what the document is about"
last_modified_at: yyyy-mm-dd # e.g. 2018-05-05
toc: true # set to false or delete if you don't wish to display a table of contents
---
```

#### Posts (Actualités)

Les noms des fichiers d'actualité suivent une certaine structure, ils doivent être nommés comme suit : aaaa-mm-jj-titre.md

Chaque message doit commencer par l'entrée suivante :

```
---
title:  "Some News"
date:   yyy-mm-dd
categories: news-category
---
```
### Fonctions supplémentaires

#### Galeries

L'ajout de galeries est devenu très simple :  creer un nouveau dossier dans `/assets/images/galleries/` et ytélécharger des fichiers.
Puis ajouter:

{% raw %}
```
{% include folder-galleries path="new-folder-name/" %}
```
{% endraw %}
là  où  souhaitez afficher une galerie contenant le contenu de `new-folder-name`.

Si vous souhaitez fournir des images d'aperçu pour un chargement plus rapide, ajoutez -th au nom du fichier. Par exemple `image.jpg` utiliserait `image-th.jpg` comme aperçu. Les deux fichiers doivent se trouver dans le même dossier que celui spécifié dans l'instruction d'inclusion.

#### Catégorisation des tutoriels

Les tutoriels  du dossier `_tutorial` doivent contenir dans leur en-tête des mots-clés qui les caractèrisent. 
Cela pourrait ressembler à ceci :


```
---
permalink: /tutorials/applique/
title: Applique
last_modified_at: 2018-05-11
excerpt: "Applique example file"
image: "/assets/images/tutorials/samples/Applique Color Change.svg"
language: en
tutorial-type:
  - Sample File
  - Text
stitch-type: 
  - Running Stitch
  - Fill Stitch
  - Satin Stitch
techniques:
  - Applique
field-of-use:
user-level: Beginner
---
```
Ces catégories peuvent ensuite être utilisées pour lister les tutoriels avec un mot-clé spécifique, par exemple
{% raw %}
```
{% include tutorials/tutorial_list key="stitch-type" value="Fill Stitch" %}
```
{% endraw %}
afficherait une liste de tous les  tutoriels  qui listent  "Fill Stitch" parmi  les types  de points de leur en-tête.

Ils peuvent également être utilisés pour afficher une liste complète des catégories. 
Dans ce cas, les catégories doivent être spécifiées par chaque appel de listes de didacticiels. 

Exemple:


{% raw %}
```
{% assign tutorial_cats = 'Tutorial Type*Stitch Type*Techniques*Field Of Use*User Level' | split: '*' %}
{% include tutorials/display_tutorials tutorial_cats=tutorial_cats %}
```
{% endraw %}



---
permalink: /fr/tutorials/cross_stitch_lettering/
title: "Lettrage au point de croix"
language: fr
last_modified_at: 2026-05-14
excerpt: "Lettrage au point de croix "
image: "/assets/images/tutorials/tutorial-preview-images/hello.png"
tutorial-type: 
stitch-type: 
 - Cross Stitch
tool:
techniques:
field-of-use:
user-level: 
toc: true
---

{% include upcoming_release.html %}
## Lettrage au point de croix



### Utiliser le module de lettrage

La méthode la plus simple est d'utiliser une fonte prête pour la broderie du module de lettrage, parmi la vingtaine de fontes en point de croix présentes.

Il est facile de limiter le menu de sélection des fontes à celles en point de croix, simplement en choisissant point de droit dans le menu déroulant en haut à droite.

![selection des fontes en points de croix](/assets/images/tutorials/cross_stitch_lettering/fr/choix_point_de_croix.jpg)



### Utiliser une fonte pixelisée



Il existe de nombreuses fontes pixélisées.
Vous pouvez en trouver sur [fonts.google.com](https://fonts.google.com) en filtrant sur l'apparence pixel, mais il y en a bien d'autres libre de droit sur le web.


Nous allons utiliser pour ce tutoriel la fonte doto disponible sur fonts.google.com
![doto](/assets/images/tutorials/cross_stitch_lettering/doto.jpg)

On suppose dans la suite, que cette fonte est installées sur votre ordinateur.

Rappel : Si vous installez une nouvelle fonte dans inkscape, il est possible (selon votre système) qu'il vous faille redémarrer Inkscape pour la voire apparaitre dans le menu déroulant des fontes installées pour l'outil Texte d’Inkscape.

Chaque "pixel" de la fonte va devenir un point de croix. Avec du fil standard, il est raisonable de produire des croix de hauteur comprise entre 1.8 mm et 4 mm. L'usage d'un fil plus fin permet de descendre en dessous de 1.8mm, l'usage d'un fil plus épais permet des croix encore plus grandes.
#### Marche à suivre
Les étapes sont les suivantes :

- Vérifier que vos préférences Inkscape , onglet interface, la ligne "origine en haut et a gauche, axe des y pointant vers le bas" est bien cochée.

- Décider de la taille des croix : dans cette exemple, nous allons chercher à obtenir des croix de 3mm de haut et de large. Cette dimension convient à toutes les sortes de point de croix disponibles dans Ink/Stitch

- Afficher une grille avec un espacement horizontal et vertical de 3mm, soit en utilisant les propriétés du document, soit en utilisant l'assistant point de croix (Ne rien sélectionner, puis `Ink/Stich > Outils: Remplissage > Assistant Point de Croix` , définir l'espacement horizontal de la grille dans l'onglet paramètres, et cocher afficher la grille dans l'onglet Options de sortie)


- Sélectionner l'outil texte, vérifiez que son style comporte bien une couleur de fond et pas de couleur de contour
- Sélectionner la fonte doto dans le menu déroulant des fontes
- Écrire votre texte dans la fenêtre de lettrage
- Éventuellement, redimensionner, jusqu'a obtenir un petit carré ("pixel") par case de la grille.
 
![hello1](/assets/images/tutorials/cross_stitch_lettering/hello1.jpg)

- Convertir le texte en chemin, ici il suffit d'utiliser `Inkscape > Chemin > Objet en chemin`
- Sélectionner les chemins créés, et `Ink/Stich > Outils: Remplissage > Assistant Point de Croix`

![hello1](/assets/images/tutorials/cross_stitch_lettering/fr/assistant1.jpg)

Dans l'onglet paramètre, les paramètres important ici sont :
- l'espacement horizontal de la grille
- le pourcentage de couverture du remplissage: Ici comme les "pixels" sont petits par rapport aux cases de la grille, il faut mettre une petite valeur dans ce paramètre.
- la méthode de point de croix choisie sera automatiquement choisie pour le paramétrage qui peut être fait dans cette même opération à condition

dans l'onglet Options de sortie
- de cocher la case paramètres.
- de cocher la case pixeliser. 

L'aspect du canevas change et le paramétrage en point de croix est fait:
![pixelateandparams](/assets/images/tutorials/cross_stitch_lettering/fr/pixelateandparams.jpg)

Chaque lettre est devenue une unique forme, à la broderie les sauts ne se produisent que de lettre en lettre.

#### Le pourquoi du comment
Vous pouvez arrêter la lecture de cette section ici, mais si vous aimez bien tout comprendre, la lecture de la suite peut vous intéresser.

Rapellons que l'assistant point de croix a trois fonctions **indépendantes** que nous venons d'utiliser:

- La création d'une grille sur le canevas. C'est un outil visuel qui montre comment Ink/Stitch découpe l'espace pour y calculer la couverture par un remplissage (couleur par couleur). L'affichage de la grille est totalement facultatif. Cette grille peut être affichée via l'assistant point de croix ou via les propriétés du document, sans que cela ne change quoi que ce soit.
- Le paramétrage. Il peut être fait via l'assistant de point de croix, ou via l'extension Paramètres d'Ink/Stitch. L'assistant point de croix par défaut ajoute un petit élargissement (0.1) à chaque forme
- La pixelisation. Elle modifie les formes : chaque fois que le taux de couverture est atteint sur un carré, la forme est agrandie pour occuper tout le carré. Si deux carrés se touchent, les formes qui les contiennent sont fusionnés. Dans l'exemple précédent, après pixelisation, chaque lettre devient une forme unique. Attention, la pixélisation est faite pour un espacement de grille donné, si vous changez d'avis ensuite sur la taille des croix, elle ne refletera plus la forme exacte de la broderie!

Que ce serait-il passer si l'on avait uniquement coché la case paramètre et pas la case pixeliser

Dans ce cas, l'aspect sur le canevas inchangé. Mais le paramétrage a été appliqué.
Si l'on appelle a nouveau le paramétrage pour voir le résultat on obtient ceci :
![pixelateandparams](/assets/images/tutorials/cross_stitch_lettering/fr/cross_stitch.jpg)

Chaque croix continue à occuper entierement les carrés, même si les formes ne sont pas pixélisées.

Le paramétrage porte sur les formes initiales, c'est à dire chacune des lettres.  Mais qu'est ce qu'une lettre ici ? C'est un forme composée de plusieurs carrés séparés les uns des autres, qui ne se touchent pas. Comme pour tous les remplissages d'Ink/Stich , pour chaque lettre, chaque carré est traité indépendamment, et Ink/Stich  ordonne les carrés à sa manière. Ici cela masque un peu la séquentialité (broderie croix par croix) car les croix adjacentes sont assez bien traitées, mais pas parfaitement, comme on peut voir par exemple a regardant le "e".

On voit mieux l'ordre de traitement des carrés (qui reste identique!) si l'on choisit un remplissage automatique :
![pixelateandparams](/assets/images/tutorials/cross_stitch_lettering/fr/autofill.jpg)

La pixelisation a donc deux rôles :
 
 - une meilleure visualisation du résultat : on voit quel espace occupera la broderie (à condition que la pixelisation ait été effectué avec la même taille de croix que le paramètrage)
 - une meilleure broderie : une fois que les carrés entiers sont occupés, ils se touchent et peuvent être fusionnés. Il y aura beaucoup moins de sauts dans le résultat final.

Néanmoins, la pixelisation n'est aucunement obligatoire. 



### Utiliser n'importe quelle fonte

Il est en fait possible d'utiliser à peu près n'importe quelle fonte. Cela peut même parfois être très simple. 

#### Exemple d'une fonte en lettres attachées
Utilisons la fonte Good Vibes, elle aussi disponible sur fonts.google.com

![good vibes](/assets/images/tutorials/cross_stitch_lettering/good_vibes.jpg)

* En vert, ce que vous obtenez directement avec l'outil texte. Notez comme l'intersection du H et du e n'est pas colorée en noir.

* Une manière simple d'obtenir la forme en noir est de :
- sélectionner le texte
- `Inkscape > Texte > Texte en Glyphes`
- Sélectionner tous les glyphes `Inkscape > Chemins > Union`

Pour un résultat satisfaisant, il est préférable d'avoir un nombre assez important de croix, c'est pourquoi ici le texte a une hauteur de 60 mm et les croix sont des croix de 2 mm. Évidement, plus on a de croix, plus on peut être fidèle à la forme initiale du texte.

Pixeliser n'est pas obligatoire, mais permet d'obtenir la troisième forme visible sur l'image, sous laquelle se trouve la simulation de la broderie.

Avec une fonte en lettres attachées comme celle-ci, on obtient un résultat sans aucun saut de fil.

#### Exemple d'une fonte en lettres détachées
Utilisons cette fois la fonte audiowide, toujours disponible sur fonts.google.com
C'est une fonte de largeur quasi constante, sans détails trop fins, qui va se prêter assez bien à l'exercice.

![audiowide](/assets/images/tutorials/cross_stitch_lettering/audiowide.jpg)

* En vert ce que donne directement l'outil texte d'Inkscape.

Cette fois-ci il est important de pouvoir placer les lettres une par une sur la grille pour cela
* sélectionner le texte et `Inkscape > Texte> Texte en Glyphes`
Il est maintenant possible de déplacer chaque lettre, résultat en noir
![positioning](/assets/images/tutorials/cross_stitch_lettering/positioning.jpg)

* convertir chaque lettre en chemin

* paramétrer  et pixéliser avec l'assistant point de croix
* 
Vous pouvez utiliser la prévisualisation du svg pour tester différentes valeurs pour le pourcentage de couverture.
![positioning](/assets/images/tutorials/cross_stitch_lettering/fr/svg_preview.jpg)

Le résultat est en marron, il peut être modifié à la main, par exemple pour obtenir un o bien symmétrique (résultat en rouge).

Cette fois chaque lettre se brode sans interruption, mais il y a un saut entre chaque lettre.



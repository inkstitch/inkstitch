---
permalink: /fr/tutorials/cookie_cutter_tiling/
title: "Pavage à l'emporte pièce"
language: fr
last_modified_at: 2023-05-08
excerpt: "Pavage"
image: "/assets/images/tutorials/tutorial-preview-images/cloth_line.jpg"
tutorial-type:
stitch-type:
  - "Running Stitch"
  - "Bean Stitch"
  - "Circular Fill"
techniques:
field-of-use:
tool:
  - "Stroke"
  - "Fill"

user-level:
toc:
  true
---

{% include upcoming_release.html %}

![Brodé](/assets/images/tutorials/tutorial-preview-images/cloth_line.jpg)

Le but de ce tutorial est de montrer comment remplir une forme en découpant  la répétition régulière de motifs obtenue  en utilisant l'effet de chemin pavage.



## Pavages
L'effet de chemin pavage répéte un dessin un nombre spécifié de fois en lignes et en colonnes, avec des options permettant de varier espacement, décalage, rotation, d'ajouter des symmétries, etc.

Ces pavages sont particulièrement intéressants pour la broderie, que ce soit pour créer des textures sur des remplissages, ou pour créer des remplissages en motif.

Ils peuvent être utilisés tel quel pour les textures, mais un peu de travail est necessaire pour les remplissages en motif, c'est ce que nous verrons ici.

Voici quelques exemples:

 ![tiles](/assets/images/tutorials/cookie_cutter_tiling/all_png.png) 
 
Vous reconnaitrez (ou pas) parmi ces exemple les 4 pavages qui ont été utilisés pour créer la broderie de la corde la linge.
* le remplissage du T shirt à gauche provient du pavage du milieu de la première rangée
* le haut et le bas de la robe proviennent des deux derniers pavage de la dernière rangée
* la ceinture de la robe, exception de cet exemple, est un remplissage circulaire avec alternance de point simples et de points triples
* le remplissage du maillot de bain provient du dernier pavage de la rangée du milieu. Moins évident à l'oeil....

[Télécharger le fichier contenant tous ces pavages](/assets/images/tutorials/cookie_cutter_tiling/tiles_ideas.svg) 

Dans tous ces exemples, tous les chemins constituant le motif sont regroupés, et l'effet de chemin est appliqué sur le groupe. 

Ils sont assez faciles à obtenir car toute modification est réfléchie immédiatement sur le canevas d'inkscape. Vous pouvez modifer un chemin du motif, ajouter un chemin au motif ou faire une modification depuis le pannneau Effet de Chemin et voir immédiatement l'effet sur le canevas.

Vous pouvez utiliser ces pavages pour remplir vos propres formes, et bien sur créer vos propres pavages. C'est simple.

Voici comment la broderie de la corde à linge a été composée.

## Préparation  des  vêtements

Les svg des trois vêtements ont été créés par Bernd Lakenbrink du [Noun Project](https://thenounproject.com/browse/collection-icon/clothes-icon-set-158916/?p=1).

Le svg du  [T Shirt](https://thenounproject.com/browse/icons/term/womans-shirt/) doit être modifié. En effet, ce type de svg parfait pour les écrans ou les machines de découpe ne convient pas tel quel pour la broderie : ce qui apparait à l'oeil comme des traits est en fait constitué de remplissages. 



* Téléchargez le fichier  du T Shirt.
* Sélectionnnez les chemins constituant le vêtement.
* `Extensions > Ink/Stitch > Outils: Remplissage > Convertir remplissage en trait`.
* L'extension a créé un groupe avec beaucoup de chemins, dont certains sont inutiles. Il est utile de les simplifier avant de reconstitué la forme que l'on souhaite remplir ainsi que les détails suplémentaires à broder.

Les quatre images ci dessous montrent successivement l'apparence du svg à l'écran, ce à quoi il ressemble  en supprimant le remplissage et en  ajoutant  un contour, ce que l'extension de conversion permet d'obtenir, et ce que l'on utilisera finalement : une forme fermée (orange) et deux détails en rouge.

![T-Shirt](/assets/images/tutorials/cookie_cutter_tiling/Tshirt.png) 

Les vêtéments préparés, se trouvent dans le calque "Clothes" du  fichier cloth_path.svg qui contient ausi tous les pavages necessaires dans le calque "Tilings".
Vous  y trouverez aussi le résultat de chaque étape jusqu'à la broderie finale.

![cloth_line](/assets/images/tutorials/cookie_cutter_tiling/cloth_line.svg) 

[Télécharger cloth_line.svg](/assets/images/tutorials/cookie_cutter_tiling/cloth_line.svg)




## Recouvrir chaque surface à remplir par un pavage
L'étape suivante consiste à recouvrir chaque surface à remplir par un pavage. Voici le choix qui a été fait (et que vous pouvez retrouver dans le calque "Clothline preparing pattern fill")

![cloth_line](/assets/images/tutorials/cookie_cutter_tiling/tiled_cloths.png) 

Vous pouvez modifier le nombre de lignes et de colonnes du pavage, modifier les dimensions, tourner le pavage, l'adapter au mieux pour couvrir la surface à remplir sans avoir trop de lignes ou de colonnes inutiles.

Vous ne  devriez  rencontrer aucune difficulté à cette étape.

## Passer au  remplissage de chaque vêtement
Le but est d'obtenir ceci
![final](/assets/images/tutorials/cookie_cutter_tiling/clothline_final.png) 

Selon le pavage choisi, le résultat est plus ou moins facile à atteindre

### Exemple d'un résultat facile : le T -Shirt 

On part avec :
* shape : forme fermée du contour extérieur du T-Shirt.
* details : les petits trucs en plus qu'on traitera à la fin indépendament du reste.
* un groupe "Moulins" constitué de :
  *  un unique chemin (path8 : un petit triangle) sur lequel est appliqué l'effet de chemin pavage  .


![starting_point](/assets/images/tutorials/cookie_cutter_tiling/T-shirt-1.jpg)

Examinons le panneau Effet de Chemin  :

Dans un rectangle rouge se trouve l'oeil qui permet de masquer et demasquer l'effet.

A sa droite, un menu comportant entre autre la possibilié d'applatir l'effet de chemin.

Dans un autre rectangle rouge le  symbole ![symbole](/assets/images/tutorials/cookie_cutter_tiling/tiling_moulin.jpg) qui dicte la manière dont les triangles sont répétés. 

Pour plus facilement comprendre, redressons le pavage et limitons nous à deux lignes et deux colonnes:

![starting_point](/assets/images/tutorials/cookie_cutter_tiling/tiling_moulin2x2.jpg)

Le symbole indique quelles transformations  le chemin initial (rose sur le symbole), path8 pour nous, doit effectuer lors des recopies en ligne et en colonne.

Cliquez sur un autre symbole, et vous aurez un tout autre pavage, à vous de choisir celui que vous préférez.
![mirroring](/assets/images/tutorials/cookie_cutter_tiling/mirroring.jpg)


Faites toutes les modifications souhaitées, puis finalement applatissez (flatten) l'effet de chemin. 
Maintenant, path8 est un chemin composite constitué des multiples répétitions du triangle initial. 
Impossible après cela de modifier le nombre de lignes et de colonnes, ni les symmétries.

En mode édition de noeuds, voici ce que vous devez voir si vous sélectionnez les noeuds de path8 :

![flattened](/assets/images/tutorials/cookie_cutter_tiling/flatened.jpg)

Si vous sépariez ce chemin vous obtiendriez de nombreux triangles. Mais ne séparez pas.

* Dupliquez shape, la forme du T-shirt
* Sélectionnez une copie de shape et path8  
* `Chemin > Intersection` 

On obtient
![flattened](/assets/images/tutorials/cookie_cutter_tiling/after_intersection.jpg)

Ici l'intersection fonctionne très bien, car le triangle initial est un chemin fermé. 

* Sélectionnez le résultat de l'intersection et la copie restante de shape. Supprimez le remplissage si nécessaire, ajoutez un contour si nécessaire. 
* `Extensions > Ink/Stitch > Paramètres `

pour choisir vos paramètres de broderie. Ici on a choisit un point multiple.

Avec toujours ces deux éléments sélectionnés

* `Extensions > Ink/Stitch > Outils : Trait > Agencement automatique de points droits`.

On constate dans le résultat  (le groupe "Agencement automatique....") une multitude de tous petits chemins. On pourrait les éliminer, mais le plus simple est d'aller dans les préférences  (`Extensions > Ink/Stitch > Préférences`) et pour ce fichier seulement augmenter la longueur minimum de point à 1mm.
Il ne reste plus qu'à paramétrer les deux petits détails du T Shirt.

### Exemple d'une suprise : le maillot de bain

La démarche est identique, mais le pavage de départ est constitué de trois chemin ouverts.
Rien à modifier jusqu'à l'étape de l'intersection.

#### Première tentative d'intersection
Sans rien toucher au motif du pavage,  j'ai aplati l'effet puis pris l'intersection avec la forme du maillot de bain.
![intersection_1](/assets/images/tutorials/cookie_cutter_tiling/ss_intersection_1.jpg )
Logique en fait, l'intersection appliqué à 4 chemins, a pris l'intersection des 4....

Mais pas terrible pour la broderie, trop de sauts de fils en perspective.
#### Deuxième tentative d'intersection
Cette fois ci j'ai combiné les trois chemins du motifs avant d'applatir l'effet. Puis intersecté avec la forme du maillot .

![intersection_2](/assets/images/tutorials/cookie_cutter_tiling/ss_intersection_2.jpg )

Le résultat n'est pas  forcement celui auquel on s'attend. L'intersection de deux remplissages est toujours  conforme à ce que l'on attend. Intersecter deux chemins  ouverts ou un remplissage et un chemin ouvert est plus suprenant. L'intersection  renvoit ce qu'elle considère comme à l'intérieur de chacun des objets intersectés, et la  définition de l'intérieur de notre chemin de remplissage est compliquée.

Mais le résultat m'a plu. Je l'ai conservé.


J'aurai pu aussi utiliser la division : en selectionant le maillot et le chemin combiné du pavage, avec le maillot plus bas dans la liste d'objets, on divise le maillot par le pavage pour obtenir ![idivision](/assets/images/tutorials/cookie_cutter_tiling/division.jpg)

L'intérêt de l'intersection et de la division c'est qu'elles éliminent tout ce qui est en dehors de la forme. L'inconvénient c'est que faute de partir d'une pavage constituée de chemins fermés combinés, le résultat n'est pas forcement celui auquel  on s'attendait.



#### Découper le chemin
Pour obtenir un vrai découpage du pavage par le maillot, il convient d'utiliser l'opération de chemin "Découper le chemin". 

On va placer cette fois le pavage (après avoir combiné et applati, - un seul chemin donc) sous une copie du maillot.

L'intersection est symmétrique peut importe d'intersecter A avec B ou B avec A. La division et le découpage ne sont pas symmétriques. D'où l'importance de la position relative des deux éléments dans la pile d'objets.

* Sélectionner le chemin du pavage et le maillot (maillot plus haut que le pavage)
* `Chemin > Découper le chemin`


C'est comme si vous preniez un emporte pièce de la forme du maillot pour couper dans le pavage. Le chemin du pavage est découpé, mais rien n'est éliminé.

Mais l'emporte pièce a coupé en deux tout ce qui traverse la frontière du maillot de bain.

L'unique chemin initial du pavage devient une foule de morceaux parmi lesquels il faut faire le ménage et éliminer tout ce qui est en dehors du maillot. 

![cut_path](/assets/images/tutorials/cookie_cutter_tiling/cut_path.jpg)


Ma manière préferrée de faire le ménage consiste à :
* vérouiller le reste des objets (ici la deuxieme copie du maillot et le decolleté)
* en maintenant les touches majuscule et alt enfoncées tracé un chemin (qui va s'afficher en rouge) qui rencontre (et donc sélectionne) des objets à supprimer. 
* supprimer les objets que je viens de sélectionner.
* En quelques passages le ménage est fait.

![cut_path](/assets/images/tutorials/cookie_cutter_tiling/ss.jpg)

Le reste des étapes est identique.


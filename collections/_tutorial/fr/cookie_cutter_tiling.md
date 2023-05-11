---
permalink: /fr/tutorials/cookie_cutter_tiling/
title: "Pavage à l'emporte pièce"
language: fr
last_modified_at: 2023-05-12
excerpt: "Utiliser l'effet de chemin Pavage, la découpe et l'agencement automatique de point droit pour créer un remplissage en motif"
image: "/assets/images/tutorials/tutorial-preview-images/cookie_cutter_tiling.jpg"
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

![Brodé](/assets/images/tutorials/tutorial-preview-images/cookie_cutter_tiling.jpg)

Le but de ce tutorial est de montrer comment Utiliser l'effet de chemin Pavage, la découpe et l'agencement automatique de point droit pour créer un remplissage en motif.


## Pavages
L'effet de chemin pavage répète un dessin un nombre spécifié de fois en lignes et en colonnes, avec des options permettant de varier espacement, décalage, rotation, d'ajouter des symétries, etc.

Ces pavages sont particulièrement intéressants pour la broderie, que ce soit pour créer des textures sur des remplissages, ou pour créer des remplissages en motif.

Ils peuvent être utilisés tel quel pour les textures, mais un peu de travail est nécessaire pour les remplissages en motif, c'est ce que nous verrons ici.

Voici quelques exemples:

 ![tiles](/assets/images/tutorials/cookie_cutter_tiling/all_png.png) 
 
Vous reconnaitrez parmi ces exemples les 4 pavages qui ont été utilisés pour créer la broderie de la corde la linge.
* le remplissage du T shirt à gauche provient du pavage du milieu de la première rangée
* le haut et le bas de la robe proviennent des deux derniers pavage de la dernière rangée
* la ceinture de la robe, exception de cet exemple, est un remplissage circulaire avec alternance de point simples et de points triples
* le remplissage du maillot de bain provient du dernier pavage de la rangée du milieu. Moins évident à l'oeil....

[Télécharger le fichier contenant tous ces pavages](/assets/images/tutorials/cookie_cutter_tiling/tiles_idea.svg){: download="tiles_idea.svg" }

Dans tous ces exemples, tous les chemins constituant le motif sont regroupés, et l'effet de chemin est appliqué sur le groupe. 

Ils sont assez faciles à obtenir car toute modification est réfléchie immédiatement sur le canevas d'inkscape. Vous pouvez modifier un chemin du motif, ajouter un chemin au motif ou faire une modification depuis le panneau Effet de Chemin et voir immédiatement l'effet sur le canevas.

Vous pouvez utiliser ces pavages pour remplir vos propres formes, et bien sur créer vos propres pavages. C'est simple.

Voici comment la broderie de la corde à linge a été composée.

## Préparation  des  vêtements

Les svg des trois vêtements ont été créés par Bernd Lakenbrink du [Noun Project](https://thenounproject.com/browse/collection-icon/clothes-icon-set-158916/?p=1).

Il nous faut les adapter à notre fin. Voyons pourquoi et comment sur le [T Shirt](https://thenounproject.com/browse/icons/term/womans-shirt/). 

Ce type de svg parfait pour les écrans ou les machines de découpe ne convient pas tel quel pour la broderie : ce qui apparait à l'oeil comme des traits est en fait constitué de remplissages. 

* Téléchargez le fichier  du T Shirt.
* Sélectionnez les chemins constituant le vêtement.
* `Extensions > Ink/Stitch > Outils: Remplissage > Convertir remplissage en trait`.
* L'extension a créé un groupe "Centerline" avec beaucoup de chemins, dont certains sont inutiles. Il est utile de les simplifier. Reconstituer la forme extérieure du vêtement en utilisant l'outil noeud pour joindre des noeuds ou briser des chemins Garder les détails supplémentaires à broder

Les quatre images ci dessous montrent successivement l'apparence du svg à l'écran, ce à quoi il ressemble  en supprimant le remplissage et en  ajoutant  un contour, ce que l'extension de conversion permet d'obtenir, et ce que l'on utilisera finalement : une forme fermée (orange) et deux détails en rouge.

![T-Shirt](/assets/images/tutorials/cookie_cutter_tiling/Tshirt.png) 

Le fichier cloth_line.svg file contient les vêtements déjà préparés, dans le calque   "Clothes Preparation" .

Son calque Tilings, contient à nouveau tous les pavages vus au dessus.

Il contient aussi le résultat de toutes les étapes jusqu'à la broderie finale.

Chaque étape de ce tutorial correspond à un calque du fichier, de bas en haut. Pour travailler sur un calque, n'oubliez pas de le démasquer et de le dévérouiller. Laissez les autres calques masqués.

![cloth_line](/assets/images/tutorials/cookie_cutter_tiling/cloth_line.svg) 

[Télécharger cloth_line.svg](/assets/images/tutorials/cookie_cutter_tiling/cloth_line.svg){: download="cloth_line.svg" }




## Recouvrir chaque surface à remplir par un pavage
L'étape suivante consiste à recouvrir chaque surface à remplir par un pavage. Voici le choix qui a été fait (et que vous pouvez retrouver dans le calque "Covering each shape with a tiling")

![cloth_line](/assets/images/tutorials/cookie_cutter_tiling/tiled_cloths.png) 

Vous pouvez modifier le nombre de lignes et de colonnes du pavage, modifier les dimensions, tourner le pavage, l'adapter au mieux pour couvrir la surface à remplir sans avoir trop de lignes ou de colonnes inutiles.

Ne faites pas comme moi, j'ai utilisé un pavage trop petit pour le bas de la robe, il manque un morceau du remplissage.

## Remplissage en motif
Voici notre but final
![final](/assets/images/tutorials/cookie_cutter_tiling/final_embroidery.png) 

Pour l'atteindre, suivez les étapes suivantes, en respectant scrupuleusement l'ordre.

Pour chaque futur remplissage en motif, vous avez un groupe au nom du vêtement ou de la partie du vêtement concerné qui contient:


 * shape: forme fermée du contour extérieur 
 * Details: un groupe qui contient les petits trucs en plus qu'on traitera à la fin indépendamment du reste.
 * Tiling:  le groupe qui porte l'effet de chemin Pavage et dans le quel se trouve tous les chemins du pavage.
 
 ###  Effet de Chemin Pavage
 Regardons de plus prêt l'effet de chemin appliqué au pavage sur le T-shirt.



![starting_point](/assets/images/tutorials/cookie_cutter_tiling/T-shirt-1.jpg)

Examinons le panneau Effet de Chemin  :

Dans un rectangle rouge se trouve l'oeil qui permet de masquer et démasquer l'effet.

A sa droite, un menu comportant entre autre la possibilité d'aplatir l'effet de chemin.

Dans un autre rectangle rouge le  symbole ![symbole](/assets/images/tutorials/cookie_cutter_tiling/tiling_moulin.jpg) qui dicte la manière dont les triangles sont répétés. 

Pour plus facilement comprendre, redressons le pavage et limitons nous à deux lignes et deux colonnes:

![starting_point](/assets/images/tutorials/cookie_cutter_tiling/tiling_moulin2x2.jpg)

Le symbole indique quelles transformations  le chemin initial (rose sur le symbole), path8 pour nous, doit effectuer lors des recopies en ligne et en colonne.

Cliquez sur un autre symbole, et vous aurez un tout autre pavage, à vous de choisir celui que vous préférez.
![mirroring](/assets/images/tutorials/cookie_cutter_tiling/mirroring.jpg)


Faites toutes les modifications souhaitées, puis finalement aplatissez (flatten) l'effet de chemin. 
Maintenant, path8 est un chemin composite constitué des multiples répétitions du triangle initial. 
Impossible après cela de modifier le nombre de lignes et de colonnes, ni les symétries.

En mode édition de noeuds, voici ce que vous devez voir si vous sélectionnez les noeuds de path8 :

![flattened](/assets/images/tutorials/cookie_cutter_tiling/flattened.jpg)

Si vous sépariez ce chemin vous obtiendriez de nombreux triangles. Mais ne séparez pas.

Ici il n'y avait qu'un chemin dans le pavage, mais en général il faut 

### Combiner les chemins des pavages puis aplatir l'effet ( Calque: Combine  paths in Tiling groups  and flatten  effect )
Pour chaque pavage :
*  S'il y a plus d'un chemin dans le groupe de pavage, combinez tous les chemins (les sélectionner puis `Chemin > Combiner`)
*  Sélectionner le groupe de pavage et aplatir l'effet de chemin

Si vous regardez le canevas, il semble que rien n'a changé.



### Dupliquer chaque forme et l'utiliser pour découper le pavage (Calque: Duplicate shape, and use it to Clip Tiling)
Pour chaque pavage
* Dupliquez shape
* Sélectionnez l'unique chemin du groupe de pavage et une copie de shape qui doit être au dessus du groupe de pavage dans le panneau Calques et Objets
* `Object  > Découpe > Définir une découpe` 

Voici ce que vous devriez obtenir
![clipped](/assets/images/tutorials/cookie_cutter_tiling/after_clip.png)

###  Se préparer à paramètrer pour la broderie (Calque: Prepare for Embroidery Parameters)
Pour chaque pavage:
* La dernière copie de shape doit avoir un contour mais pas de remplissage
* La couleur de contour de shape et du pavage doivent être identiques
* Pour les détails choisissez aussi la même couleur si vous voulez limiter les changements de fils, ou une couleur différente si vous préférez.



###  Ajouter les paramètres de broderie (Calque: Add Embroidery Parameters)
* Sélectionnez shape,Tiling et Details
* Lancez  `Extensions > Ink/Stitch > Paramètres `

Pour un point triple: 
  *  Choisir la méthode  Point Droit / Point Multiple
  *  Longueur de point droit  2 mm au moins
  *  Nombre de répétitions pour le point triple 1

En procédant vêtement par vêtement:
  *  Sélectionnez tout le groupe 
  * Lancez `Extensions > Ink/Stitch > Visualiser et Exporter > Prévisualisation du plan de broderie`



![Before_Autoroute](/assets/images/tutorials/cookie_cutter_tiling/before_autorouting.jpg)

Si  visualiser les sauts est coché, vous voyez qu'un ordonnancement des chemins est necessaires, ce sera l'étape suivante.

Si vous décochez, vous pourrez plus facilement vérifier que tout à l'air en ordre.

### Agencement automatique (Calque: Autoroute)

Pour chaque pavage: 
  * Sélectionnez le chemin du groupe de pavage et shape
  * Lancez  `Extensions > Ink/Stitch > Outils : Trait > Agencement automatique de point droit` en sélectionnant uniquement l'option "ajouter des noeuds aux intersections"


Un vêtement à la fois:
 *  Sélectionnez tout le groupe 
  * Lancez `Extensions > Ink/Stitch > Visualiser et Exporter > Prévisualisation du plan de broderie`


et vous verrez que les sauts de fils ont quasiment disparus.

On constate dans le résultat  (le groupe "Agencement automatique....") une multitude de tous petits chemins. 

On pourrait les éliminer, mais le plus simple est 


 * `Extensions > Ink/Stitch > Préference`
 *  pour ce fichier seulement augmenter la longueur minimum de point à 1mm.


### Etape finale

* Supprimez tous les groupes vides

Les derniers sauts restants sont entre deux détails, ou entre le dernier chemin du  groupe Autoroute et le  premier détail.
Vous pouvez au choix :
  - ne rien faire , et soit votre machine convertira le saut en coupe, soit vous couperez vous même le fil
  - ajouter une commande coupe
  - remplacer le saut par un chemin de liaison

`Extensions > Ink/Stitch > Outils: Trait >  Convertir saut en chemin ` peut vous aider
Si vous sélectionner deux chemins entre lesquels il y a un saut, l'extension va créer un chemin en ligne droite de la fin du premier chemin au début du second.
Il ne vous restera qu'à le modifier pour le faire se camoufler dans les motifs de remplissage (voir l'exemple du T Shirt)



<!--
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

### Exemple d'une surprise : le maillot de bain

La démarche est identique, mais le pavage de départ est constitué de trois chemins ouverts.
Rien à modifier jusqu'à l'étape de l'intersection.

#### Première tentative d'intersection
Sans rien toucher au motif du pavage,  j'ai aplati l'effet puis pris l'intersection avec la forme du maillot de bain.
![intersection_1](/assets/images/tutorials/cookie_cutter_tiling/ss_intersection_1.jpg )
Logique en fait, l'intersection appliqué à 4 chemins, a pris l'intersection des 4....

Mais pas terrible pour la broderie, trop de sauts de fils en perspective.
#### Deuxième tentative d'intersection
Cette fois ci j'ai combiné les trois chemins du motifs avant d'aplatir l'effet. Puis fait l'intersection avec la forme du maillot .

![intersection_2](/assets/images/tutorials/cookie_cutter_tiling/ss_intersection_2.jpg )

Le résultat n'est pas  forcement celui auquel on s'attend. L'intersection de deux remplissages est toujours  conforme à ce que l'on attend. L'intersection de deux chemins  ouverts ou d'un remplissage et d'un chemin ouvert est plus surprenant. L'intersection  renvoie ce qu'elle considère comme à l'intérieur de chacun des objets intersectés, et la  définition de l'intérieur de notre chemin de remplissage est compliquée.

Mais le résultat m'a plu. Je l'ai conservé.


J'aurai pu aussi utiliser la division : en sélectionant le maillot et le chemin combiné du pavage, avec le maillot plus bas dans la liste d'objets, on divise le maillot par le pavage pour obtenir ![division](/assets/images/tutorials/cookie_cutter_tiling/division.jpg)

L'intérêt de l'intersection et de la division c'est qu'elles éliminent tout ce qui est en dehors de la forme. L'inconvénient c'est que faute de partir d'une pavage constituée de chemins fermés combinés, le résultat n'est pas forcement celui auquel  on s'attendait.



#### Découper le chemin
Pour obtenir un vrai découpage du pavage par le maillot, il convient d'utiliser l'opération de chemin "Découper le chemin". 

On va placer cette fois le pavage (après avoir combiné et aplati, - un seul chemin donc) sous une copie du maillot.

L'intersection est symétrique peut importe de  faire  l'intersection de  A et B ou  de B et A. La division et le découpage ne sont pas symétriques. D'où l'importance de la position relative des deux éléments dans la pile d'objets.

* Sélectionner le chemin du pavage et le maillot (maillot plus haut que le pavage)
* `Chemin > Découper le chemin`


C'est comme si vous preniez un emporte pièce de la forme du maillot pour couper dans le pavage. Le chemin du pavage est découpé, mais rien n'est éliminé.

Mais l'emporte pièce a coupé en deux tout ce qui traverse la frontière du maillot de bain.

L'unique chemin initial du pavage devient une foule de morceaux parmi lesquels il faut faire le ménage et éliminer tout ce qui est en dehors du maillot. 

![cut_path](/assets/images/tutorials/cookie_cutter_tiling/cut_path.jpg)


Ma manière préférée de faire le ménage consiste à :
* vérouiller le reste des objets (ici la deuxième copie du maillot et le décolleté)
* en maintenant les touches majuscule et alt enfoncées tracer un chemin (qui va s'afficher en rouge) qui rencontre (et donc sélectionne) des objets à supprimer. 
* supprimer les objets que je viens de sélectionner.
* En quelques passages le ménage est fait.

![cut_path](/assets/images/tutorials/cookie_cutter_tiling/ss.jpg)

Le reste des étapes est identique.
-->

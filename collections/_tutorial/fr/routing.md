---
title: Optimisation du chemin de broderie
permalink: /fr/tutorials/routing/
last_modified_at: 2024-09-09
language: fr
excerpt: "L'optimisation du chemin de broderie est un élément  très important du processus de digitalisation. Apprenez comment  Ink/Stitch peut vous assister dans cette tâche"
image: /assets/images/tutorials/routing/routing.png

tutorial-type:
  - Text
stitch-type:
  - Fill stitch
  - Guided Fill
  - Circular Fill
  - Meander Fill
  - Satin
  - E-Stitch
  - S-Stitch
  - Running Stitch
  - Bean Stitch
techniques:
field-of-use:
user-level: 

toc: true
---
L'optimisation du chemin de broderie est un élément  très important du processus de digitalisation. 

Apprenez ici comment  Ink/Stitch peut vous assister dans cette tâche.

Une broderie diffère complètement d'un ensemble de divers éléments à imprimer sur une feuille de papier: 
broder nécessite d’anticiper le déplacement de l’aiguille et du fil, c’est très différent d’une impression. En particulier, lorsque vous créez une broderie, il est essentiel de:
* **Donner un ordre logique aux éléments**
  * Pour éviter les changements de couleurs inutiles
  
    Il peut parfois être nécessaire d'ajouter un changement de couleur supplémentaire par exemple si une couleur se trouve à la fois au dessus et en dessous d'une autre couleur ou pour éviter des problèmes d'étirements.
   
  * Pour éviter les problèmes de décalage
  * Pour éviter les plissements du support de broderie
* **Éviter les sauts**

  Il ne devrait pas y avoir de sauts inutiles dans votre fichier. La solution n'est pas de les remplacer systématiquement par des commandes de coupe.
  Des coupes inutiles (et les points d'arrêts qui vont avec) risquent de provoquer des amas de fils au dos de votre broderie et  ralentissent fortement la machine.
  
Chaque  fichier est un cas particulier, et vous êtes le concepteur qui doit décider de la manière d'organiser vos chemins de points de broderie. Ce tutoriel passe en revue les divers outils dont Ink/Stitch dispose  pour vous aider dans cette tâche. 


## Options de routage générales à tous les points de broderie

### Réordonner des éléments par leur ordre de sélection

Déplacer les éléments dans le panneau Calque et Objet peut être fastidieux. Sélectionnez les éléments dans l'ordre où vous désirez les broder et lancez l'extension Ink/Stitch [Édition > Réempiler les objets dans l'ordre de leur sélection](/fr/docs/edit/#re-stack-objects-in-order-of-selection) pour accomplir cette tâche.
### Convertir des sauts en traits

Après avoir mis vos éléments dans le bon ordre et vous être assuré qu'ils commencent  et terminent bien là où vous le souhaitez,
exécutez  [Outils Trait > Saut en Trait](/fr/docs/stroke-tools/#jump-to-stroke) pour créer un chemin droit qui relie la position finale du premier élément à la position de départ du deuxième élément.

Vous pouvez ensuite modifier ce chemin pour qu'il soit masqué sous d'autres éléments qui seront brodés après lui. 

Si la distance est courte (par exemple du petit lettrage) vous pouvez également utiliser ce chemin tel quel pour faire s'enfoncer le point de raccordement dans le tissu et ainsi le masquer tout en évitant un saut supplémentaire.


![Jump to stroke process](/assets/images/docs/jump_to_stroke.png)

*1: Avant Saut en Trait 2: Après Saut en Trait 3: Après ajustement manuel*

## Options de routage  spécifiques aux points droits


Par défaut les éléments de type point droit sont brodés du début du chemin à sa fin.

### Activez l'affichage de la direction des chemins.

![Stroke with visible path direction](/assets/images/tutorials/routing/path_direction.png)

La manière de personnaliser Inkscape pour que  la direction des chemins soit visible rendant facile la détection du point de départ et du point final d'un chemin est  décrite dans la section  [Personnaliser Ink/Stitch](/fr/docs/customize/#activation-de-la-direction-des-chemins) 

### Modifier si nécessaire la direction d'un chemin

Lorsque  vous sélectionnez un chemin et lancez  `Chemin > Inverser`,  Inkscape inverse la direction du chemin et la broderie se fait donc dans l'ordre inverse.
Vous risquez d'utiliser beaucoup cette fonction, et il est intéressant d'avoir un raccourci clavier pour cela. Pour plus de détails, voir la section
[Personnaliser Ink/Stitch](/fr/docs/customize/#raccourcis-clavier)

### Paramètres: adapter le nombre de répétitions 

Si vous avez besoin que la broderie d'un chemin commence et termine au même endroit vous pouvez dans le [dialogue de paramétrage](/fr/docs/params/) choisir un nombre de répétitions pair. Alternativement, si vous ne voulez pas de cela (par exemple parce que vous avez choisi un point triple et que vous ne voulez pas qu'il se repète deux fois ce qui conduirait à 6 répétitions de chaque oint), vous  pouvez aussi  dupliquer le chemin, changer la direction de la copie et si necessaire la paramétrer en point droit simple.

### Agencement automatique de points droits / Redwork

Lorsqu'il y a  beaucoup de chemins,  il  peut  être long et  difficile de les agencer correctement.

Ink/Stitch  a maintenant deux outils pour cela. Dans la plupart des cas, il vaut mieux choisir l'outil [Redwork](/fr/docs/stroke-tools/#redwork) qui assurera qu'il y a exactement deux passages sur chaque chemin.  A l'aide des [commandes visuelles](/fr/docs/commands/) (Position de départ pour l'agencement automatique des points droits) vous pouvez choisir le point de départ, qui sera  aussi le point final. Si vous souhaitez terminer et commencer la broderie à deux endroits différents, alors il se peut que [l'agencement automatique  de points droits](/fr/docs/stroke-tools/#autoroute-running-stitch) soit une meilleure  option pour vous en utilisant les deux commandes visuelles Position de départ/fin pour l'agencement automatique des points droits.


## Options de routage  spécifiques aux colonnes satin

Les colonnes satin sont brodées depuis le début d'un de ses rails vers la fin de l'autre rail.

Evitez d'utiliser des chemins fermés pour les rails. Ink/Stitch accepte un chemin fermé pour un rail,  mais vous n'avez alors aucun contrôle sur les points de départ et d'arrivée et vous risquez d'obtenir des résultats inattendus.

### Agencement automatique de colonnes satin

De même que pour les points droits, Ink/Stitch possède [une  extension d'agencement des colonnes satin](/fr/docs/satin-tools/#auto-route-satin-columns).

Avant de lancer cette extension, vous pouvez ajouter des [commandes visuelles](/fr/docs/commands/) pour définir le point de départ et le point  d'arrivée de l'agencement automatique de colonnes satin.
Attention : 

* Si  vous activez l'option `préserver l'ordre des colonnes satin` alors il n'y aura pas de points  droits générés pour passer d'une colonne à la suivante si elles ne se touchent pas (mais vous pouvez ajouter vous même  des chemins qui seront cachés par la broderie  de colonnes brodées ultérieurement).

* Si vous  désactivez cette option des chemins de  dessous seront générés, mais si des colonnes se croisent vous ne contrôlez plus laquelle  vient au dessus  de l'autre.

Vous obtiendrez un résultat optimal si vous préparez soigneusement l'ordre de broderie (utilisez l'extension mentionnée plus haut pour cela) et lancez l'agencement automatique  de colonnes satin avec l'option `préserver l'ordre des colonnes satin`. Puis après avoir sélectionnés tous les éléments de l'agencement automatique, lancez l'extension   `Saut en Trait ` puis chaque fois que  possible cachez les chemins de liaison créés par cette extension sous  des éléments brodés ultérieurement. Lorsque ce n'est  pas possible, supprimez le chemin de liaison.

### Paramètres: Échanger les rails
Les deux rails d'une colonne satin n'ont pas tout à fait le même role : par défaut,la broderie commence au début d'un des rails et termine à la fin de l'autre  rail.
Dans le [dialogue de paramétrage](/fr/docs/params/), il est possible d'échanger le rôle des deux rails. En conséquence de cet échange, le rail où les points de broderie commencent et le rail où ils terminent  sont échangés. Attention  toutefois, toutes  les propriétés asymétriques seront elles aussi échangées. Par exemple, si vous avez ajouté une  compensation d'étirement unilatérale elle changera de coté. Par défaut  une colonne satin n'a pas de propriété asymétrique.

### Paramètres: Scinder une colonne satin
Si vous souhaitez commencer ou finir votre broderie au milieu d'une rail et non à l'extrémité d'un rail, alors il vous faudra en fait découper votre
colonne satin en deux.  Il est possible de le faire  sans  perdre  le  paramétrages en utilisant l'extension  [Ink/Stitch > Outils Satin > Scinder colonne satin](/fr/docs/satin-tools/#scinder-une-colonne-satin).


### Paramètres: Inverser la direction des rails

Dans le  [dialogue de paramétrage](/fr/docs/params/),  vous pouvez  aussi inverser la direction de  la colonne satin. Cela ne modifie pas le rôle des rails, la broderie commence toujours sur le même rail, mais a son autre extrémité

### Paramètres: adapter le nombre de répétitions de la sous couche  centrale 

Si vous donnez une valeur  impaire  au nombre de répétition de la sous-couche centrale, alors la colonne satin commence et termine du même coté de la colonne satin (mais pas sur le même rail toutefois).
Dans certains  cas  c'est une manière simple d'éviter de devoir ajouter manuellement  un point droit.

## Options de routage spécifiques aux remplissages

### Commandes Position de départ/fin de remplissage

Les positions de départ et de fin de remplissages peuvent être définies à l'aide  des  [commandes visuelles](/fr/docs/commands/). 
Si vous avez ajouté de nombreuses commandes cela  peut encombrer quelque peu le canevas il est donc bon de savoir que ces commandes sont actives même lorsque qu'elles sont masquées.

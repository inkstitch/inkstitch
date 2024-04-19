---
title: Satin Multicolore
permalink: /fr/tutorials/multicolor_satin/
last_modified_at: 2024-04-18
language: fr
excerpt: "Simuler des colonnes satin multicolore"
image: "assets/images/tutorials/multicolor_satin/snake.jpg"
tutorial-type:
stitch-type: 
  - Satin Stitch
techniques:
field-of-use:
user-level: 
---
![compensation](/assets/images/tutorials/multicolor_satin/snake.jpg)
# Simuler une colonne satin multicolore.
On parle ici de simulation, car il ne s'agit pas d'une seule colonne satin  multicolore, mais d'un effet similaire obtenu en 
utilisant plusieurs  copies superposées d'une même colonne satin, simplement en modifiant les paramétrages.

## Commençons par le bicolore
### Augmentation aléatoire de la largeur des colonnes satins
Le paramètre des colonnes satin qui va nous être indispensable est "augmentation aléatoire de la largeur des colonnes satins". C'est un paramètre dans lequel il est possible de n'entrer qu'une valeur, auquel cas elle est appliquée à chacun des deux cotés de la colonne; mais aussi d'entrer deux valeurs séparées par un espace, auquel cas le premier est appliqué au premier rail, le second au second rail. Dans le jargon Ink/Stitch, ce paramètre est dit asymètrique

![random increase_different_seeds](/assets/images/tutorials/multicolor_satin/random_increase_different_seeds.png)

* Quand le paramètre vaut 0, la colonne (en noire) est composée de zig-zags qui restent entre les deux rails
* Quand le paramètre vaut 50, la colonne  (en rouge), chaque zig  (ou zag) est allongé vers la gauche et la droite d'une valeur comprise entre 0 et 50% de la longueur  du zig. La nouvelle colonne est donc élargie différement selon les endroits, au maximum elle peut être deux fois plus large que la noire (50% a gauche et 50% à droite), elle n'est jamais plus étroite.
* Quand le paramètre vaut 0 50, la colonne (en vert) est inchangée à gauche, mais à droite, elle est allongée jusqu'à 50% de longueur supplémentaire.
* Quand le paramètre vaut 50,0, la colonne (en bleu) c'est la même chose, mais en échangeant la gauche et la droite
* Si l'on superpose les trois colonnes ayant une valeur non nulle pour le paramètre, l'élargissement semble bien aléatoire, les frontières des colonnes sont bien différentes, même si elles sont similaires.

Quelles sont les valeurs que l'on peut saisir dans ce paramètre ? Ink/Stitch accepte ici tout couple de valeurs numériques. Elles peuvent être positives ou nulles, et elles peuvent dépasser la valeur 100. Toutefois, si l'on peut augmenter ainsi les zigs sans limite, la diminuation est de facto limité, au pire le zig serait un simple  point sur la ligne médiane.


![negative augmentation](/assets/images/tutorials/multicolor_satin/negative_augmentation.png)


### La graine aléatoire
Chaque fois que l'on utilise  un ou des paramètres aléatoire, on peut si l'on n'est pas content du résultat  cliquer sur "relançer les dés" pour obtenir un résultat différent. Techniquement, relancer les dés, c'est donner une nouvelle valeur au paramètre "graine aléatoire". 
Il est aussi possible de donner manuellement une valeur à ce paramètre. C'est surtout utile lorsque l'on désire que plusieurs objets qui utilisent des paramètres aléatoires soient en fait parfaitement identique. Il suffira alors de leur donner la même valeur de graine aléatoire.

Si l'on reprend le premier exemple  mais en donnant cette fois à toutes les colonnes la même valeur pour la graine aléatoire, voici ce que l'on obtient:
![random increase_same_seeds](/assets/images/tutorials/multicolor_satin/random_increase_same_seed.png)

Maintenant lorsque l'on superpose les trois colonnes, on constate qu'il y a une parfaite superposition des frontieres. La colonne rouge à élargie à gauche comme la colonne bleu et à droite comme la colonne vert. En revanche, pour un même zig, l'élargissement à gauche est différent de l'élargissement à droite.

## Pourcentage de compensation d'étirement négatif asymétrique
Pour obtenir des colonnes satin multicolores, on va utiliser le paramètre "pourcentage de compensation d'étirement".

C'est un paramètre asymétrique, c'est à dire qu'il est possible de lui donner deux valeurs différentes (séparées par un espace), la première valeur s'appliquant au  premier rail, la seconde valeur s'appliquant au second rail.

Il  est courant de donner des valeurs positives aux compensations, mais il est aussi possible de leur donner des valeurs négatives, au lieu d'augmenter la largeur de la colonne satin, on la réduit.

Voici trois exemples de valeurs pour le paramètre pourcentage de compensation d'étirement, et le résultat
![compensation](/assets/images/tutorials/multicolor_satin/compensation.png)

Ici le premier rail est le bord gauche du satin.

Quand le paramètre vaut "0 -75" (en vert) on ne touche pas au bord gauche, mais tout se passe comme si le bord droit avait été rapproché régulièrement pour réduire la distance entre les deux rails au quart de la valeur initiale. On est en effet passé d'une largeur de 100% à une largeur de 100-75=25%

Quand le paramètre vaut "-25  -25" (en rouge) les deux bords se rapprochent du centre et la largeur de la colonne est uniformément réduite de moitié.

Quand le paramètre vaut "-75  0" (en bleu) on ne touche pas au bord droit, mais tout se passe comme si le bord gauche avait été rapproché régulièrement pour réduire la distance entre les deux rails au quart de la valeur initiale.

Si l'on superpose ces trois colonnes, on obtient un serpent tricolore.

![tricolor](/assets/images/tutorials/multicolor_satin/tricolor_snake.png)


**Remarque** Il est tout à fait possible d'utiliser sur la même colonne satin, une compensation d'étirement en mm et une compensation en pourcentage. Les deux paramètres sont asymétriques. Les deux paramètres acceptent des valeurs négatives.
{: .notice--info }


## Augmentation (et Diminution) de la largeur aléatoire de satin (en pourcentage)

Ces deux paramètres sont eux aussi asymétriques et supportent eux aussi des valeurs négatives. De ce fait,  on peut accroitre aléatoirement la largeur d'une colonne satin soit en utilisant une valeur positive d'augmentation de largeur, soit une valeur négative de diminution de largeur.

Plutôt qu'un serpent tricolore, on souhaite maintenant un serpent bicolore, tout vert à gauche, tout bleu à droite, et un mélange de bleu et de vert dans la  partie centrale. 

Première question à se poser, quelle part relative donner à ces trois zones ? Disons qu'on veut donner au vert à gauche l'exclusivité sur 30% de la largeur, et au bleu l'exclusivité à droite de 25% de la largeur, et qu'ils se partagent les 45 pourcent qui restent au centre.

### Première solution, en utilisant uniquement l'augmentation de la largeur aléatoire

Pour la partie verte  on va donner  au paramètre  "pourcentage de compensation d'étirement" la valeur "0 -70", enlevant du vert à droite, mais déjà sur les 30% les plus à gauche, c'est tout vert. En donnant au paramètre "augmentation de la largeur aléatoire de satin" la valeur "0 45", on autorise  le vert à aller jusqu'à 100-70+45= 75 % de la largeur. Donc le vert utilisera entre 30 et 75% de l'espace. Il n'empiète pas sur la zone exclusivement bleu.

Pour la partie bleue  on va donner  au paramètre  "pourcentage de compensation d'étirement" la valeur "-75 -0", enlevant du bleu à gauche, mais déjà sur les 25% les plus à droite, c'est tout bleu . En donnant au paramètre "augmentation de la largeur aléatoire de satin" la valeur "45 0", on  autorise le bleu à aller jusqu'à 100-75+45= 70 % de la largeur.  Le bleu oscillera donc entre 25 et 70% de la largeur. Il n'empiète pas sur la zone  exclusivement verte.

Voici le résultat obtenu: 

![wrong-bicolor](/assets/images/tutorials/multicolor_satin/wrongbicolor.png)

On constate des zones blanches blanches au milieu, et parfois le vert et le bleu se superposent. C'est simplement parce que chaque colonne utilise ses valeurs aléatoires et que ce ne sont pas les même.

Il n'est pas difficile d'éliminer la zone blanche si l'on accepte les superpositions, on pourrait par exemple ne pas mettre d'aléatoire sur le vert et lui donner "0 -25" comme pourcentage de compensation d'étirement.
On obtient alors ceci: 

![withoverlay](/assets/images/tutorials/multicolor_satin/withoverlay.png)


mais cette solution comporte des superpositions. 

### Solution sans superposition

Il existe une solution où il n'y a ni manque ni superposition dans la partie centrale, malgré l'aléatoire. C'est un peu étrange, mais ça fonctionne. On va faire en sorte que lorsque les deux colonnes sont calculées, elles utilisent des nombres aléatoires "synchronisés".


*Tentative d'explication certainement indigeste que vous pouvez tout à fait sauter :*

Il n'y a pas de vrai aléatoire en informatique, seulement du pseudo-aléatoire. Un générateur de nombre pseudoaléatoire  utilise une fonction pour calculer une suite de nombre, le premier nombre de la suite est appelé graine aléatoire, le second nombre est calculé en fonction du premier, le troisième à partir du second etc... La fonction est telle que la suite  ressemble fortement à de  l'aléatoire, mais en fait  tout est  déterministe.

Pour dessiner une colonne satin, Ink/Stitch calcule des couples de points, qui sans aléatoire ni compensation sont le premier sur le premier rail, le second sur le second rail.
S'il y  a des valeurs aléatoires, les valeurs des  points  de gauche sont calculées avec des indices pairs, les valeurs des points de droite sont calculées avec des indices impairs  des nombres de la suite pseudoaléatoire, ces valeurs sont calculées en tenant compte de tous les paramètres, compensation , augmentation, diminution de la largeur.

Donc même si l'on donne aux  deux  colonnes la  même valeur de graine aléatoire, si  l'on regarde le n-ième zig de la colonne verte la position aléatoire correspond au second rail et  c'est le 2*n-ième calcul aléatoire, tandis que sur le zig correspondant de la colonne  bleu, la position aléatoire correspond au premier rail et c'est le (2*n-1)-ième calcul aléatoire. Du coup les deux colonnes ne vont pas bien s'emboiter.

Mais on peut y arriver en jonglant  pour que les positions aléatoires correspondent dans les deux cas au même rail.

*Fin de la tentative d'explication*

On va modifier le paramétrage des  colonnes comme suit:

Colonne verte :
* Pourcentage de compensation d'étirement : 0 -70
* Augmentation aléatoire de la largeur du satin 0 45
* Diminution aléatoire de la largeur du satin 0 0
* Graine aléatoire  7 (ou n'importe quoi d'autre mais saisir une valeur)

Colonne bleu:
* Pourcentage de compensation d'étirement : 0 -75
* Cocher échanger les rails 
* Augmentation aléatoire de la largeur du satin 0 0
* Diminution aléatoire de la largeur du satin 0 -45   (ce sera donc une augmentation)
* Graine aléatoire 7 (où ce que vous avez saisi pour l'autre colonne)


![solution](/assets/images/tutorials/multicolor_satin/solution.png)

Téléchager [le fichier du serpent](/assets/images/tutorials/multicolor_satin/serpent.svg){: download="serpent.svg" }
On peut jouer avec beaucoup  plus que deux couleurs:

![ArcEnCiel](/assets/images/tutorials/multicolor_satin/arcenciel.svg)

Télécharger [le fichier arc en ciel](/assets/images/tutorials/multicolor_satin/arcenciel.svg){: download="arcenciel.svg" }


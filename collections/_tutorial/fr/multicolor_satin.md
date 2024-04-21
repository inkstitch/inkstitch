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
toc : true
---
![compensation](/assets/images/tutorials/multicolor_satin/snake.jpg)
# Simuler une colonne satin multicolore.
On parle ici de simulation, car il ne s'agit pas d'une seule colonne satin  multicolore, mais d'un effet similaire obtenu en 
utilisant plusieurs  copies superposées d'une même colonne satin, simplement en utilisant des paramètres aléatoires différents.

## Commençons par le bicolore
Revenons sur les paramètres "aléatoires" des colonnes satin.
### Augmentation aléatoire de la largeur du satin
Le paramètre "augmentation aléatoire de la largeur du satin" est un paramètre dit asymétrique car il est possible de l'appliquer différemment sur les deux rails. C'est un paramètre dans lequel il est possible de n'entrer qu'une valeur, auquel cas elle est appliquée à chacun des deux rails; mais aussi d'entrer deux valeurs séparées par un espace, auquel cas le premier est appliqué au premier rail, le second au second rail. 

![random increase_different_seeds](/assets/images/tutorials/multicolor_satin/random_increase_different_seeds.png)

* Quand ce paramètre vaut 0, la colonne (en noire) est composée de zig-zags qui restent entre les deux rails
* Quand ce paramètre vaut 50, la colonne  (en rouge), chaque zig  (ou zag) est allongé vers la gauche et la droite d'une valeur comprise entre 0 et 50% de la longueur  du zig. La nouvelle colonne est donc élargie différemment selon les endroits, au maximum elle peut être deux fois plus large que la noire (50% a gauche et 50% à droite), elle n'est jamais plus étroite.
* Quand ce paramètre vaut 0 50, la colonne (en vert) est inchangée à gauche, mais à droite, elle est allongée jusqu'à 50% de longueur supplémentaire.
* Quand ce paramètre vaut 50,0, la colonne (en bleu) c'est similaire en échangeant les rôles de la gauche et de la droite.
* Si l'on superpose les trois colonnes ayant une valeur non nulle pour le paramètre, l'élargissement semble bien aléatoire, les frontières des colonnes sont bien différentes, même si elles sont similaires.

Quelles sont les valeurs que l'on peut saisir dans ce paramètre ? Ink/Stitch accepte ici tout couple de valeurs numériques. Elles peuvent être positives ou nulles, et elles peuvent dépasser la valeur 100. Toutefois, si l'on peut augmenter ainsi les zigs sans limite, la diminution est de facto limitée, au pire le zig serait un simple  point sur la ligne médiane.

![negative augmentation](/assets/images/tutorials/multicolor_satin/negative_augmentation.png)



### Diminution aléatoire de la largeur du satin
Les colonnes satins disposent aussi du paramètre inverse, la diminution  aléatoire de la largeur du satin. Plutôt que d'augmenter de -50%, on peut décider de diminuer de 50%, c'est la même chose.

### Méthode simple, mais imparfaite
Grace à l'un ou l'autre de ces deux paramètres, on a déjà une première méthode imparfaite mais très simple pour simuler des colonnes satin bicolores: 

![first_bicolore_satin](/assets/images/tutorials/multicolor_satin/first_bicolor_satin.png)

* A gauche utilisation de la diminution aléatoire de largeur : la colonne rouge est réduite à gauche, la colonne verte est réduite à droite.  Mais attention la seconde couleur vient en superposition de la première et ici le vert cache une partie du rouge .
* A droite, on a laissé le rouge intact, le vert vient en superposition,réduit jusqu'au deux tiers plutôt que de la moitié

Mais cette méthode est imparfaite : elle assure que toute la colonne est colorée, il n'y a pas de manque, mais il y a superposition. 

Il est possible d'obtenir deux colonnes parfaitement emboitées, mais il faut pour cela utiliser aussi d'autres paramètres aléatoires


### La graine aléatoire
Chaque fois que l'on utilise  un ou des paramètres aléatoires, on peut si l'on n'est pas content du résultat  cliquer sur "relancer les dés" pour obtenir un résultat différent. Techniquement, relancer les dés, c'est donner une nouvelle valeur au paramètre "graine aléatoire". 
Il est aussi possible de donner manuellement une valeur à ce paramètre. C'est surtout utile lorsque l'on désire que plusieurs copies d'un objet qui utilise des paramètres aléatoires soient en fait parfaitement identiques. Il suffira alors de leur donner la même valeur de graine aléatoire.

Si l'on reprend le premier exemple  mais en donnant cette fois à toutes les colonnes la même valeur pour la graine aléatoire, voici ce que l'on obtient:
![random increase_same_seeds](/assets/images/tutorials/multicolor_satin/random_increase_same_seed.png)

Maintenant lorsque l'on superpose les trois colonnes, on constate qu'il y a une parfaite superposition des frontières. La colonne rouge à élargie à gauche comme la colonne bleu et à droite comme la colonne vert. En revanche, pour un même zig, l'élargissement à gauche est différent de l'élargissement à droite.

### Méthode presque aussi simple, avec emboitement parfait  mais hélas pas générale


![premiere_reussite](/assets/images/tutorials/multicolor_satin/first_good.png)

Cette fois, au lieu de superposer deux colonnes, elles sont posées l'une à coté de l'autre. Le bord droit de l'une étant superposé au bord gauche de l'autre

* Les deux colonnes ont la même graine aléatoire
* La colonne orange a pour valeur de la diminution aléatoire 50 0
* La colonne bleu a pour valeur de la diminution aléatoire -50 0 (c'est donc une augmentation). De plus on a  cocher la case Échanger les rails.

Comme les deux ont la même graine aléatoire et que les modifications dans les deux cas portent sur le même rail, à chaque zig  le calcul donne des valeurs qui assurent l'emboitement parfait.

Malheureusement, cette solution simple ne se généralise pas à de colonnes de forme quelconque. 

Pour une solution générale, nous allons utiliser un paramètre supplémentaire:

  
## Pourcentage de compensation d'étirement 
Pour obtenir des colonnes satin multicolores, on va utiliser le paramètre "pourcentage de compensation d'étirement".

C'est aussi un paramètre asymétrique.

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

### Méthode générale pour l'emboitement de deux couleurs dans une colonne satin

On va utiliser conjointement tous ces paramètres. 


<!---  
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
--->

Si l'on souhaite répartir les  100%  de largeur de la colonne en 
* G% à gauche exclusivement pour le bleu
* D% à droite exclusivement pour le vert
* et donc 100-(G+D) pourcents  au milieu pour un mélange vert bleu,

on utilisera ce paramétrage

|Paramètre | Satin bleu |Satin vert |
| --- | --- |--- |
| Pourcentage de compensation d'étirement  | 0 100-G| 0 100-D|
| Échanger les rails| non| oui |
| Augmentation aléatoire de la largeur du satin| 0  100-(G+D)| 0 |
| Diminution aléatoire de la largeur du satin| 0 | 0 G+D-100|
| Graine aléatoire| identique | identique |

Donc par exemple si l'on veut garder 25% unicolore de chaque coté, on utilisera ce paramétrage

Satin bleu :
* Pourcentage de compensation d'étirement : 0 -75
* Augmentation aléatoire de la largeur du satin 0 50
* Diminution aléatoire de la largeur du satin 0 
* Graine aléatoire  7 (ou "bonjour" ou n'importe quoi d'autre mais saisir une valeur)

Satin vert:
* Pourcentage de compensation d'étirement : 0 -75
* Cocher échanger les rails 
* Augmentation aléatoire de la largeur du satin 0 
* Diminution aléatoire de la largeur du satin 0 -50   (ce sera donc une augmentation)
* Graine aléatoire 7 (où ce que vous avez saisi pour l'autre colonne)



**Important** Si ça n'a pas l'air de marcher , vérifiez que  les rails de la colonne satin sont bien tous les deux dans la même direction, et non pas corrigés automatiquement. Vérifiez  aussi que les points courts ne sont pas déclenchés .
{: .notice--info }

![solution](/assets/images/tutorials/multicolor_satin/solution.png)

Télécharger [le fichier du serpent](/assets/images/tutorials/multicolor_satin/serpent.svg){: download="serpent.svg" }
# On peut jouer avec beaucoup  plus que deux couleurs:
### Pour trois couleurs
En supposant que l'on veut repartir les 100% de la largeur de la gauche vers la droite en 
* Les C1 premiers pourcents dans la couleur 1 exclusivement
* Les  C1!2 pourcents suivants partagés entre Couleur 1 et Couleur 2
* Les C2 pourcents suivants dans la couleur 2 exclusivement
* Les C2!3 pourcents suivants partagés entre Couleur 2 et Couleur 3
* Les derniers C3 pourcents exclusivement pour la Couleur 3

**Pour un résultat qui remplisse parfaitement la colonne sans aucun débordement, il faut s'assurer que  C1+C1!2+C2+C2!3+C3 = 100**


  
|Paramètre |Couleur 1 |Couleur 2 |Couleur 3 |
| --- | --- |--- |--- |
| Pourcentage de compensation d'étirement  | 0 -(C1!2+C2+C2!3+C3)| -(C2!3+C3)   -(C1+C1!2)|-(C1+C1!2+C2+C2!3) 0|
| Échanger les rails| non| oui |non|
| Augmentation aléatoire de la largeur du satin| 0  C1!2| C2!3 0|0|
| Diminution aléatoire de la largeur du satin| 0 | 0 -C1!2|-C2!3 0|
| Graine aléatoire| identique | identique |identique|


Donc si  l'on souhaite   un partage en bleu, blanc rouge avec aucune zone  monochrome, C1,C2 et C3 seront égaux à 0 et C1!2=C2!3=50 et le tableau devient :

|Paramètre |Bleu |Blanc |Rouge |
| --- | --- |--- |--- |
| Pourcentage de compensation d'étirement  | 0 -100| -50 -50|-100 0|
| Échanger les rails| non| oui |non|
| Augmentation aléatoire de la largeur du satin| 0  50| 50 0|0|
| Diminution aléatoire de la largeur du satin| 0 | 0 -50|-50 0|
| Graine aléatoire| identique | identique |identique|

si  l'on souhaite   plutôt réserver 20% à chacune des parties monochromes et partager le reste équitablement, on choisit C1=C2=C3=20 , il reste 40% donc  C1!2=C2!3=20 et le tableau devient :

|Paramètre |Bleu |Blanc |Rouge |
| --- | --- |--- |--- |
| Pourcentage de compensation d'étirement  | 0 -80| -40 -40|-80 0|
| Échanger les rails| non| oui |non|
| Augmentation aléatoire de la largeur du satin| 0  20| 20 0|0|
| Diminution aléatoire de la largeur du satin| 0 | 0 -20|-20 0|
| Graine aléatoire| identique | identique |identique|

![tricolore](/assets/images/tutorials/multicolor_satin/tricolore.png)


### Pour quatre couleurs 
Avec les mêmes notations on aura cette fois 

 C1+C1!2+C2+C2!3+C3+C3!4+C4 =100 
  
|Paramètre |Couleur 1 |Couleur 2 |Couleur 3 |Couleur 4 |
| --- | --- |--- |--- |--- |
| Pourcentage de compensation d'étirement  | 0 </br>C1-100| -(C2!3+C3+C3!4+C4)  </br> -(C1+C1!2)|-(C1+C1!2+C2+C2!3) </br>-(C3!4+C4)| 0</br>C4-100|
| Échanger les rails| non| oui |non|oui|
| Augmentation aléatoire de la largeur du satin| 0  C1!2| C2!3 0|0 C3!4|0|
| Diminution aléatoire de la largeur du satin| 0 | 0 -C1!2|-C2!3 0| 0 -C3!4|
| Graine aléatoire| identique | identique |identique|identique |

Toutes  les valeurs de  compensation sont négatives,toutes les augmentations sont positives toutes  les  diminutions sont négatives.

Cette fois ci, si l'on ne veut pas de zone monochome et un partage égal du reste, C1=C2=C3=C4=0 et C1!2=C2!3=C3!4=33.3.

Si  l'on souhaite   plutôt réserver 15% à chacune des parties monochromes et partager le reste équitablement, on choisit C1=C2=C3=C4=5 , il reste 40% donc  C1!2=C2!3=C3!4=13.3 

![tricolore](/assets/images/tutorials/multicolor_satin/quadricolor.png)


**Remarque** Pour une broderie de qualité, il faut aussi ajouter de la  compensation d'étirement pour..... compenser..... l'étirement ! Brodé tel quel les couleurs n'auront pas tout à fait l'air jointives, car les points déforment la broderie. Le plus simple  est d'ajouter un peu  de compensation en mm. 
{: .notice--info }

### Pour un nombre quelconque de couleurs

  Pour un partage en N couleurs, choisir des valeurs positives ou nulles pour les N parties monochromes C1,C2,.....CN et les N-1 parties bicolores C1!2, C2!3, ....CN-1!N. La somme des 2N-1 valeurs doit être 100.

Préparer un tableau à N colonnes
  
Dans  la i-ième colonne indiquer 

**Si i est impair**

|Paramètre |Couleur I|
| --- | --- |
| Pourcentage de compensation d'étirement  | C1+C1!C2+C2+C2!C3+.....C(I-1)!I   CI!C(I+1)+C(I+1)+C(I+1)!(I+2)+.....CN| 
| Échanger les rails| non|
| Augmentation aléatoire de la largeur du satin| 0  CI!(I+1)| 
| Diminution aléatoire de la largeur du satin|  -C(I-1)!I 0|
| Graine aléatoire| toujours_le_meme_truc | 

Dans le pourcentage de compensation d'étirement vient en première position la somme des largeurs réservées a tout ce qui est avant la couleur I, et en deuxième position la zome des largeurs réservées à tout ce qui est après la couleur I.

**Si i est pair**

on coche Échanger les rails, et on interverti  les deux valeurs du couple dans chaque paramètre.

|Paramètre |Couleur I|
| --- | --- |
| Pourcentage de compensation d'étirement  |   CI!C(I+1)+C(I+1)+C(I+1)!(I+2)+.....CN C1+C1!C2+C2+C2!C3+.....C(I-1)!I | 
| Échanger les rails| oui|
| Augmentation aléatoire de la largeur du satin| CI!(I+1) 0| 
| Diminution aléatoire de la largeur du satin| 0 -C(I-1)!I |
| Graine aléatoire| toujours_le_meme_truc | 





* Pour la première  colonne  C(-1) sera pris égal à 0 si l'on ne veut pas de débordement, on peut lui donner une valeur  positive,si l'on veut que la première couleur déborde à gauche.
* De même pour  la dernière colonne C(N+1) sera pris égal à 0 si l'on ne veut pas que la dernière couleur déborde de la forme.

Et voilà à vous les arc-en-ciel.....

Pour cet exemple, on a fait déborder la première et la dernière couleur
![ArcEnCiel](/assets/images/tutorials/multicolor_satin/arcenciel.svg)

Télécharger [le fichier arc en ciel](/assets/images/tutorials/multicolor_satin/arcenciel.svg){: download="arcenciel.svg" }


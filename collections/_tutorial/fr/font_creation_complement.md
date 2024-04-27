---
permalink: /fr/tutorials/font_creation_complement/
title: "Création de fonte pour Ink/Stitch compléments "
language: fr
last_modified_at: 2024-02-15
excerpt: "Compléments à la création de fonte pour Ink/Stitch"
image: "/assets/images/tutorials/font_creation_complement/multifont3.jpg"
tutorial-type: 
stitch-type:
tool:
techniques:
field-of-use:
user-level: 
---
<!--

![Sample](/assets/images/tutorials/font_creation_complement/multifont3.jpg)
-->

Attention : fichier en cours de redaction


Voici quelques informations complémentaires aux instructions d'@Augusa.

## Création du fichier json et du fichier de glyphes
* Décidez de la **hauteur** que vous souhaitez pour votre fonte: Par exemple, disons que vous souhaitez une fonte dont les lettres font environ 25mm de haut. Convertir cette valeur en pixel, ici 95.
* A l'aide des instructions d'@Augusa (mais suivre les autres étapes ici, c'est  simplifié), choisissez  vos glyphes dans fontforge
* Créer un premier fichier de fonte svg sans changer les paramètres dans font info, fonte_sans_reduction.svg (notez les valeurs du cadratin, de ascent et descent, par exemple 2048, 1638, 410- le premier est toujours la somme des deux derniers)
* Créer un second fichier fonte_reduite.svg de fonte svg en  entrant 95 comme valeur de cadratin (em-size). Notez les nouvelles valeurs de ascent et descent (19 et 76 dans mon cas)

* Depuis inkscape, ouvrir fonte_reduite.svg puis extensions > typographie  > parametrer le canevas typographique. Entrer les valeurs du cadratin (95) du jambage inférieur(19) et du  jambage superieur (76). Mettre hauteur de X et hauteur de capitale à 0
 
* Extension/Typographie/Convertir la police en calques de glyphes , renommer le fichier en →.svg

* Créer un dossier pour la fonte dans votre dossier de fontes personnalisées, y mettre le fichier →.svg

* Créer tout  de suite le fichier json: extensions > ink/stitch > gestion des polices > generer json en indiquat la taille du cadratin (95 ici) dans le  paramètre taille; pour les autres paramètres du json,  [voir ici](/fr/docs/font-toolsr/#generate-json).Ce json contient les bonnes informations  pour la taille visée.
* Si vous supprimez des glyphes ultérieurement, pensez à mettre à jour la liste de glyphes

* Je suppose ici que la fonte ne comportera pas de remplissage. Si c'est le cas, il vous faudra adapter.
## Premier test
Dans le fichier →.svg
* Objet> Montrer tout
* Edition > Selectioner tout
* enlever les fonds, ajouter un contour

Ouvrir un nouveau fichier puis
* Inkstitch > Gestion des polices > Sampling font

Tous les contours de vos lettres s'affichent.
Si ces lettres ont des contours corrects, tant mieux. Mais parfois la reduction opérée dans font forge donne des résultats pas terribles. Dans ce cas, on va conserver le json, mais refaire le ficher svg en procedant soi même à la reduction.

Vous pouvez aussi des maintenant utiliser votre fonte via le lettrage, les lettres sont en  point droit. Ce n'est pas encore utilisable pour la broderie en vrai toutefois!!

## Faire un "meilleur" fichier →.svg

### On commence par récupérer quelques informations:

Dans le fichier →.svg
* Objet > Montrer tout
* Se mettre en mode selection
* Edition > Tout selectionner dans tous calques
* Notez  les valeurs affichés dans X, Y L et H (je vais les appeler X0, Y0, L0 et H0)

### On va recréer un fichier svg, cette fois ci a partir du fichier sans reduction:
* Depuis inkscape, ouvrir fonte_sans_reduction.svg
* extensions > typographie  > parametrer le canevas typographique
* entrer les valeurs du cadratin (2048) du jambage inférieur(410) et du  jambage superieur (1638).Mettre hauteur de X et hauteur de capitale à 0
* convertir la police svg en fichiers de glyphes

A nouveau, 
* Objet > Montrer tout
* Se mettre en mode selection
* Edition > Tout selectionner dans tous calques

### Maintenant procédons à la réduction
* Objet > Transformer dans Dimensions Largeur mettre le rapport d'echelle, pas besoin de calculette, le calcul se fait sur place, pour moi c'est 95/2048, donc 4,639% Cocher redimensionner proportionellement, décocher appliquer à chaque objet séparement
* cliquez sur Appliquez. Vérifiez que les nouvelles valeurs dans L et H sont bien L0 et H0
* Les lettres sont à la bonne  taille, mais pas à la bonne place, le canevas n'est pas bien dimensionné on va y remédier.

### Positionner les lettres et les guides au bon endroit
* Edition Supprimer tous les guides
* extensions > typographie  > parametrer le canevas typographique avec cette fois  les valeurs du cadratin (95) du jambage inférieur(19) et du  jambage superieur (76). Mettre hauteur de X et hauteur de capitale à 0
 
* Mettre dans X la valeur X0 et dans Y la valeur YO.

Il n'y a plus qu'a enregistrer ce fichier comme  →.svg à la place du précédent

**Ne  pas refaire le fichier json il serait faux, il faut garder le premier**

Refaire le test avec font sampling, cette fois ci les courbes devraient être bien meilleures.

## Travailler le fichier de glyphes

### Penser à faire régulièrement des copies du fichier

### Consignes pour les colonnes satin
Pour des colonnes satin facile à interpréter par ink/stitch et qui supportent des déformations,il est recommandé de respecter les consignes suivantes :

* Evitez de superposer les extrémités des rails, un petit écart ne changera rien au résultat
* N'arrêtez pas vos traverses juste sur les rails, faites les dépasser de chaque coté.
* Evitez les colonnes satin sans traverses ou avec une seule traverse
* Simplifiez au maximum vos chemins.

Avoir aussi à l'esprit que pour un joli résultat final, il faut éviter  d'avoir des points d'arrêts à des endroits où ils déforment les lettres, l'idéal etant d'avoir les noeuds soit sur les chemins de dessous soit au milieu d'une  colonne satin, mais pas sur une extrémité de lettre

### Paramètrage
Pour tous les paramètres que vous souhaitez uniformes, ne vous en souciez qu'à la fin. Pour les points d'arrêt laissez tout sur les valeurs par défaut.  Tout ça se fera globalement à la fin.  Bien sur si vous vouoez tester quelques lettres en vrai vous les parametrez pour le test.


### tests avant de se lancer dans les diacritiques

#### Dépistage de problèmes
Faire d'abord toutes les lettres en un seul morceau, et faire un "sampling font". Supprimer les lettres non  faites du résultat et lancer Résolution de problèmes > Dépistage de problèmes avec les objets.
Corriger toutes les bétises, comme  ça si vous utiliser un E pour faire un É, vous ne devrez pas corriger la même bêtise deux fois, ou trois, ou quatre, ou cinq.....

#### Chasser les satins trop longs
Refaire un sampling font avec les lettres corrigées. Tout sélectionner et 
Résolution de problèmes > Information sur l'élement et regarder la longueur maximum de point. C'est normalement la largeur maximum de vos colonnes satin. Si cette largeur est trop grande, refaire  ligne par ligne puis lettre par lettre pour trouver les coupables et voir si on ne peut pas faire mieux. Sauf bien sur si c'est voulu et que vous voulez ensuite mettre un point max pour déclencher un découpage des satins.




### Consignes pour les lettres en plusieurs morceaux
Si toutes les lettres étaient connexes, le jeu serait plus simple, comme elle ne le sont pas pour profiter au maximum des outils de gestion de police, dans chaque glyphe lorsqu'on doit absolument sauter pour aller d'un objet à un autre, comme par exemple pour passer du corps du é à son accent, l'ideal est de ne jamais avoir les deux extrémités d'un saut dans le  même groupe.
Donc une fois vos  éléments de broderie ordonnés, par exemple grouper les éléments à partir de la fin jusqu'au premier saut, puis les suivants jusqu'au second saut, etc....Pas besoin de groupe pour un A.

### A la fin....
Le but est d'obtenir des lettres qui se brodent avec le nombre minimum de points d'arrêts.Il en faut uniquement là  où  la   machine fait un saut susceptible d'etre coupé par un ou une brodeuse. Entre les lettres, et entre le corps d'une lettre et son accent. Plus suptilement, si  le saut est entre deux chemins de dessous, il n'y a pas besoin de points d'arrêt. En revanche s'il commence ou termine  sur un satin, il faut des points d'arrêt.  Idéalement les sauts ne se feraient que  de chemin de dessous a chemin de dessous. 

#### Refaire un dépistage de problème sur un nouveau sampling font
#### Eliminez un maximum de sauts
  faite une copie de votre fichier →.svg 
 dans le fichier →.svg 
 * Objet > Déverouiller tout
 * Objet > Montrer tout
 * Edition > Tout selectionner dans tous les calques 

* Outils Traits : Sauts en Trait
 Options : 
 - Convertir les sauts pas plus courts que :0.5
 - pas plus grands que : laisser 0
 - Connecter : dans le même groupe
 - Paramètres de sortie : regler longueur du point et tolerance, et ne cocher le premier que le premier fusionnner que si vous n'avez que des points simples, si vous mélangez points droits et points triples il vaut mieux ne pas cocher.
- Appliquez
- Faire a nouveau un font sampling.
Si vous avez convenablement groupé au prealable, il n'y aura pas de saut converti en chemin alors qu'il ne le fallait pas. Plus probablement il y en aura un peu. Repérez les, et allez les supprimer dans le fichier →.svg

Maintenant  les seuls endroits ou il y a des sauts de longueur inférieur 


#### Ajouter des points d'arrêts forcés

 Gestion des polices > Forcer des points d'arrêts

 * Cliquer restreindre aux satins
 * mettre 0.5mm comme distance minimale
 * et le plus possible comme distance max
 * cliquer aussi ajout de l'attribut force lock stitch au dernier element de chaque glyphe.

   Donc maintenant on a des points d'arrêt forcés partout ou il faut  ( à moins de 0.5mm personne ne va couper) et seulement là.
   On a laisser autoriser des points d'arret partout, on va les empecher là ou ils ne sont pas forcés à l'aide du paramètre longueur maximum du point.

#### Uniformiser les paramètres des colonnes satins

* Objet > Déverouiller
* Objet > Montrer tout

  Si l'extension  ink/stitch > Edition > Selectionner des éléments de broderie fonctionne l'utiliser pour selectionner tous les satins.
Sinon inkscape > edition> rechercher et remplacer. Rechercher satin_column dans les propriétés étendu à tout avec comme options uniquement le nom de l'attribut et uniquement sur les chemins.
  en principe tous vos satins sont visibles et selectioner appeler paramètres et paramètrer tout le monde en même temps.
Je donne à la distance minimum de point la valeur 0.5 pour les fontes standards, mais il faut diminuer pour les petites fontes souvent jusqu'à 0.2. C'est un paramètre à tester à la simulation, on voit très vien son effet.
Je donne à la distance minimum de saut la valeur 3mm ( en fait n'importe quoi de plus que 0.5*pourcentage max  d'augmentation convient). Ceci assure qu'il n'y aura pas de point d'arret après les satins a part les points d'arret forcé, qui sont prioritaire sur la  distance minimum de saut

Je masque toutes les colonnes satins (elles sont toutes selectionnnées, en masquer une les masque toutes)

#### broderie ondulée 
On fera de même mais pour la broderie ondulée on cherche non pas  satin_column mais ripple_stitch

#### points multiples
On fera de même mais pour les points triples on cherche non pas  satin_column mais bean_stitch_repeats

#### les points droits
Maintenant, on a masqué tout sauf les points de dessous. On les selectionne tous et on lance Paramètres.  On uniformise et  cette fois ci je vais donner a distance minimum de saut une très grande valeur 20mm par exemple pour eviter les points d'arret entre deux chemins de dessous.  Pendant qu'ils sont tous sélectionnés on peut aussi uniformiser leur aspect (pointilles ou epaisseur)



### Simulation
Il est extrémement utile lors de la simulation d'utiliser le bouton "avancer jusqu'à la prochaine commande" qui va permettre sur le fichier font sampling de verifier qu'il ne reste plus de saut là où il ne faut pas. Sur une lettre connexe, on doit voir la lettre apparaitre en une seule fois, sinon, on avance de saut en saut








 


  









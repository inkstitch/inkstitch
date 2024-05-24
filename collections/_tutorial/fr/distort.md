---
title: Utiliser  les  effets de chemins de déformation
permalink: /fr/tutorials/distort/
last_modified_at: 2024-05-26
language: fr
excerpt: "Utiliser les effets de chemin de  deformation"
image: "/assets/images/galleries/fonts/multiple/multifont3.jpg"

tutorial-type:
  - Sample File
stitch-type: 
  - Satin Stitch
techniques:
   -Lettering
field-of-use:
user-level: 
---
{% include upcoming_release.html %}

![Distort effect](/assets/images/galleries/fonts/multiple/multifont3.jpg)

On  peut bien s'amuser en utilisant les effets de chemin de déformation sur des broderies. Vous pouvez pour cela utiliser ces effets:
* Courber
* Déformation par enveloppe
* Perspective et enveloppe
* Déformation par grille

Pour obtenir de bons résultats il est préférable  de: 
* simplifier les chemins  autant qu'il est possible
* éviter les trop petits objets

Les  colonnes satins font  les  difficiles : comme il n'y a rien dans le fichier svg qui distingue les rails des traverses dans le chemin composite qu'est la colonne satin, Ink/Stitch doit décider quels sont les deux rails parmi les  sous-chemins de la colonne.


Voici quelques recommandations  qui aideront Ink/Stitch a prendre la même décision sur le choix des  rails avant et après déformation :


- ne superposez pas  les extrémités des rails.
- les traverses  ne doivent  pas terminer  juste  sur les rails, mais plutôt les traverser nettement.
- n'utilisez pas de  colonne  satin sans traverse ou avec exactement deux traverses.

Si vous suivez  toutes ces  règles, il est très probable que votre colonne satin soit analysée par Ink/Stitch  de la même manière avant et après déformation.

La plupart des fontes du module de lettrage résistent bien à une déformation raisonnable. Pour certaines fontes il est préférable d'appliquer une simplification aux chemins avant de les déformer.

Toutefois si  les déformations  sont trop extrêmes,la broderie ne sera probablement pas très belle.



## Courber

L'effet courber est très facile à appliquer à un lettrage:

* Sélectionnez le groupe du lettrage. 
* Ajoutez l'effet "Courber" au groupe
* Dans le dialogue "Effet de chemins", cliquez sur le bouton  "Modifier sur la zone de travail",
et déformez le chemin vert qui apparait alors.


Si votre texte est multiligne, vous pouvez préférer appliquer l'effet indépendament sur chaque ligne
 
![Lettering Bend Example](/assets/images/tutorials/distort/peace_dove.svg)

[Download](/assets/images/tutorials/distort/peace_dove.svg){: download="peace_dove.svg" }

Bien sur cet effet peut-être appliqué à autre chose que des fontes,vous pouvez par  exemple prétendre avoir dessiné tout
un banc de raie mantas alors que vous n'en avez en réalité dessiné qu'une seule.

![Mantas Bend Example](/assets/images/tutorials/distort/Mantas.svg)

[Download](/assets/images/tutorials/distort/Mantas.svg){: download="Mantas.svg" }

## Déformation par enveloppe

Cela marche a peu près de la même manière, sauf que cette fois ci vous disposez de 4 chemins pour contrôler les déformations.
Utiliser tout ou partie des  4 boutons "Modifier sur la zone de travail" pour modifier  les chemins de  controle.

![Manger Enveloppe deformation example](/assets/images/tutorials/distort/manger.svg)

[Download](/assets/images/tutorials/distort/manger.svg){: download="manger.svg" }

Sur cet exemple,  la déformation par enveloppe a été appliquée indépendamment sur chaque ligne de texte.

## Perspective et Enveloppe
Cet effet est très utile pour appliquer un effet.... de perspective


![perspective example](/assets/images/tutorials/distort/perspective.svg)

[Download](/assets/images/tutorials/distort/manger.svg){: download="perspective.svg" }

Après avoir ajouté l'effet, activez le mode noeud et déplacez  les 4 coins de l'enveloppe rectangulaire qui apparait.

Avec cet  effet de  perspective, la fonte Marcellus semble être passée en italique:

![italique](/assets/images/tutorials/distort/italic.png)

## Déformation par grille

Après  avoir appliqué l'effet et  activé le mode noeud, vous disposez de 25 points de contrôle que vous pouvez déplacer pour déformer:
![grid](/assets/images/tutorials/distort/grid.png)

Utilisez le pour faire bouger vos fontes:

![italique](/assets/images/tutorials/distort/hello.png)



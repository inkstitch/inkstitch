---
permalink: /fr/tutorials/meandering-writing/
title: "Écrire avec des méandres, en positif ou en negatif"
language: fr
last_modified_at: 2023-04-26
excerpt: "Écrire avec le remplissage en méandres"
image: "/assets/images/tutorials/tutorial-preview-images/meandering_writing.jpg"
tutorial-type:
stitch-type:
  - "Meander Fill"
  - "Bean Stitch"
techniques:
field-of-use:
user-level:
---

{% include upcoming_release.html %}

![Brodé](/assets/images/tutorials/tutorial-preview-images/meandering_writing.jpg)

Ce tutoriel n'utilise pas le module lettrage de Ink/Stich, mais une fonte (.ttf ou .otf) qui doit avoir été installée sur votre machine **avant l'ouverture d'inkscape**
{: .notice--info }

Cette méthode ne permet pas d'obtenir des écritures de petite taille (comptez au moins 5cm de hauteur pour les lettres) et toutes les fontes ne conviennent pas.
En revanche vous pouvez obtenir de très grandes lettres qui se brodent très rapidement.
{: .notice--warning }




## Écrire en positif

* Utilisez l'outil texte d'inkscape pour écrire votre texte (court le texte) avec la fonte de votre choix (voir les conseils de choix)

![Choix de la fonte](/assets/images/tutorials/meandering_writing/font-chosing.jpg)

* Vous pouvez déformer le texte obtenu. Pour cet exemple,j'ai utilisé la police [Rubik dans sa version ultrabold](htps://fonts.google.com/specimen/Rubik), 
en allongeant les lettres sans les élargir. Vous pouvez aussi utiliser les fonctions de manipulation de texte d'inkscape.

* Sélectionnez votre texte et `Chemin > Objet en chemin`
* Dans le dialogue "Calques et Objets", votre objet texte est devenu un groupe de chemins
* Sélectionnez ce groupe de chemins et `Extensions > Ink/Stitch > Paramètres`
* Dans la fenêtre de paramétrage qui s'ouvre :
  * Désélectionnez sous-couche dans l'onglet sous-couche
  * Si vous préférez des coupes de fil aux sauts de fil, Cochez Couper Après. Seulement temporairement pour ne pas voir les sauts de fil dans le simulateur si vous preferez que votre machine à broder fasse des sauts et non des coupes
  * Jouez avec les paramètres pour choisir vos méandres préférés et leur paramètres
  * Vous pouvez aussi paramètrer lettre par lettre et choisir des méandres différents à chaque lettre. Parfois une lettre est plus difficile à remplir à cause de sa forme, traitez là à part
  * Le remplissage en méandres contient une part d'aléatoire, vous pouvez aussi tenter de relancer les dés (en bas du paramètrage) si une zone a été oubliée. Réduire la taille du méandre aide aussi à passer partout
  

![Paramètrage](/assets/images/tutorials/meandering_writing/meandering-parameter.jpg)

Cliquez sur Appliquer et Quitter et votre fichier est prêt pour la broderie.....



## Écrire en négatif
Les méandres sont très rapides à broder, mais un peu longs à calculer. Plus la zone à remplir est grande, plus c'est long. 
Ne commencez pas par une trop grande zone à remplir.

Dans l'exemple brodé en négatif, la broderie est constituée de deux phases, un point triple autour des lettres et un remplissage en méandres.

Dessinez un rectangle (ou une autre forme) autour de votre texte, là où vous souhaitez broder les méandres. Donnez lui une couleur de fond, mais pas de contour. 
Baissez l'opacité si vous le souhaitez, cela ne changera pas le résultat.

Avant de transformer votre objet texte en chemin, dupliquez-le, vous aurez besoin des deux copies

### Tour des lettres en point triple
* Sélectionnez une des copies de votre texte
* Enlevez le fond, et ajoutez un contour
* `Chemin > Objet en chemin`
* Dans le dialogue "Calques et Objets", votre objet texte est devenu un groupe de chemins
* Sélectionnez ce groupe de chemins et `Extensions > Ink/Stitch > Paramètres`
* Faites votre paramètrage en point triple

![Paramètrage pointdroit](/assets/images/tutorials/meandering_writing/bean-parameter.jpg)
* La simulation du paramètrage montre qu'il y aura des sauts de fils à l'intérieur des lettres, pour passer d'un bord à l'autre. Si vous souhaitez les transformer en coupe,sélectionnez les lettres et `Chemin > Séparer` 
* Vous devrez réappliquer le paramètrage

### Les lettres en négatif

* Sélectionnez l'autre copie du texte
* `Chemin > Objet en chemin`
* `Chemin > Combiner`
* Vous avez maintenant à la place de l'objet texte un groupe qui contient exactement un chemin. 
* Vérifiez que ce groupe est bien au dessus du rectangle de fond, au besoin déplacer le rectangle
* Sélectionnez le groupe qui contient le texte (ou le texte) et votre rectangle
* `Chemin > Exclusion`
*  Vérifiez que le résultat de l'opération est bien selectionné 
*  `Extensions > Ink/Stitch > Paramètres` et paramétrer vos méandres.

Et voilà il ne reste plus qu'à broder


## Indices pour un bon choix de fonte
Choisissez une fonte bien dodue, vous voulez éviter les zones étroites. Si possible au moins en bold. 



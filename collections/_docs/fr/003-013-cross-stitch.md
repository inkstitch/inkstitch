---
title: "Point de Croix"
permalink: /fr/docs/stitches/cross-stitch/
last_modified_at: 2026-03-27
toc: true

feature_row:
  - image_path: /assets/images/docs/cross_stitch_coverage.jpg
    alt: "Cross stitch grid with a fill. Fields covered by the fill for more than 50% show a cross on top"
  - image_path: /assets/images/docs/cross_stitch_coverage02.jpg
    alt: "Same image as before, but the fill element has moved. More crosses are build"
---

{% include upcoming_release.html %}

## Description

Le point de croix imite les techniques traditionnelles de broderie à la main.

Il se caractérise par de petites croix régulières, ce qui donne à l'image brodée un aspect plat et géométrique.

{% include folder-galleries path="butterfly-fill-project/cross/" captions="1:Point de croix" %}

[<i class="fa fa-download"></i> Download sample files](/assets/images/stitch-type-butterflies/cross_stitch.zip)

## Création

* Dessinez une forme fermée avec une couleur de remplissage.
* Ouvrez la boîte de dialogue des paramètres.
* Sélectionnez « Point de croix » comme méthode de remplissage.

### Grilles et paramètre de couverture

Il est important de comprendre le paramètre de **couverture** du point de croix.

Ce paramètre définit le pourcentage de recouvrement nécessaire pour chaque point de croix avec la zone de remplissage. Autrement dit, il détermine si un point de croix est réalisé ou non à un endroit précis.

Les points de croix sont alignés sur une grille à la taille de la cellule. Par défaut, la grille est alignée sur le coin supérieur gauche de la zone de travail.

Ink/Stitch vérifie le pourcentage de chaque case de la grille recouverte par le remplissage.

Si le recouvrement dépasse la valeur définie par l'option « couverture» (50 % par défaut), un point de croix est réalisé.

Dans l'exemple suivant, seuls les parties vertes sont recouvertes à plus de 50 % par le remplissage et reçoivent donc un point de croix.

Lorsque le remplissage est déplacé sur la zone de travail, davantage de points sont ajoutés.

{% include feature_row %}

Lorsque l'option « Aligner la grille avec le canevas » est désactivée, l'élément peut être déplacé sur la toile sans que cela ne modifie le résultat du point de croix.

Mais en conséquence les zones de point de croix adjacentes peuvent être désalignées.

{: .notice--info }

### Méthode de point de croix

Ink/Stitch permet l'utilisation de plusieurs méthodes de point de croix.

* **Point de Croix et Point de Croix Retourné**

C'est la méthode la plus courante. Deux diagonales forment une croix.

Lorsque deux croix sont reliées uniquement en diagonale, ajoutez une petite valeur d'expansion au remplissage sous-jacent pour assurer une broderie combinée sans saut.


  ![Méthode de point de croix: Point de Croix](/assets/images/docs/cross_stitch_method_cross_stitch.jpg)
  
* **Demi-Croix et Demi_Croix Retournée**
  
Les demi-croix ne constituent qu'un demi-point de croix (une diagonale). Les chemins de dessous suivent le contour de la forme.



  ![Cross stitch method: half cross](/assets/images/docs/cross_stitch_method_half_cross.jpg)
  
* **Point de Croix Horizontal et Point de Croix Horizontal Retourné**

  Un Point de Croix ayant subi une rotation qui le rend horizontal.

Veuillez noter que cette méthode de point de croix peut présenter des sauts lorsque les zones sont reliées uniquement en diagonale.

  ![Méthode de point de croix: Horizontal](/assets/images/docs/cross_stitch_method_upright.jpg)

* **Point de Croix Horizontal Dense et Point de Croix Horizontal Dense Retourné**

Le remplissage en Croix Horizontales est plus dense.

 La couverture est de 50% dans cet example.


  ![Cross stitch method:  dense upright cross](/assets/images/docs/cross_stitch_method_dense_upright.jpg)
  
  * **Double Croix et Double Croix retournée **
  
Une Combinaison de Point de Croix et de Point de Croix  Horizontal, avec la croix horizontale en dessous.

  ![Méthode de point de croix: Double Croix](/assets/images/docs/cross_stitch_method_double_cross.jpg)

  * **Smyrna cross and upright Smyrna cross**

Une Combinaison de Point de Croix et de Point de Croix Horizontal, avec la croix horizontale sur le dessus.
  
  ![Cross stitch method:Smyrna cross](/assets/images/docs/cross_stitch_method_smyrna.jpg)

### Assistant Point de Croix

Ink/Stitch inclut une extension qui vous permet d'effectuer toutes les tâches spécifiques au point de croix en une seule opération.

* Création d'une grille pour l'alignement des points de croix (et aide visuelle pendant la broderie)
* Application des paramètres de point de croix aux éléments sélectionnés
* Pixellisation du contour des éléments sélectionnés pour visualiser et ajuster facilement la position des points
* Convertir des images bitmap en remplissage en point de croix
  
L'extension calcule et affiche également la longueur des points en fonction des dimensions de la grille;  dans le paramétrage, la longueur maximale du point devrait être supérieure à cette valeur.

[En savoir plus](/fr/docs/fill-tools/#assistant-point-de-croix)

### Définir les points de départ et de fin

Par défaut, le remplissage automatique commence au plus près de l'élément de broderie précédent et se termine au plus près de l'élément suivant.

Pour modifier ce comportement, définissez les points de départ et de fin des objets de remplissage à l'aide des [commandes visuelles](/fr/docs/commands/).

## Paramètres

Exécutez **Extensions > Ink/Stitch > Paramétres** pour ajuster les paramètres selon vos besoins.

{% include params.html stitch_type='cross_stitch'%}

## Fichiers d'exemple incluant des points de croix

{% include tutorials/tutorial_list key="stitch-type" value="Cross Stitch" %}

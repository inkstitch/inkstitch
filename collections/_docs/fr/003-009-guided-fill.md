---
title: "Remplissage guidé"
permalink: /fr/docs/stitches/guided-fill/
excerpt: ""
last_modified_at: 2022-05-25
toc: true
---
{% include upcoming_release.html %}

## De quoi s'agit-il ?



![Fill stitch detail](/assets/images/docs/guided-fill-detail.jpg)
Tout comme le remplissage usuel, le remplissage guidé est composé de rangées décalées parallèles, mais au lieu de suivre des lignes droites,  les rangées peuvent être courbées par une ligne-guide.

## Comment le créer

* Créez une **forme fermée avec une couleur de remplissage**. Cette forme  peut comporter des trous.
* Créez une ligne-guide pour définir la forme des rangées de points :
    * Dessinez un trait (chemin avec une couleur de contour et sans couleur de remplissage)
    * Selectionnez ce trait
    * Lancez `Extensions > Ink/Stitch > Edition > Selection vers ligne-guide`
* Sélectionnez les deux et groupez les ensemble (`Ctrl + G`).
* Ouvrez le dialogue de paramètrage (`Extensions > Ink/Stitch > Paramètres`) et sélectionnez `Remplissage guidé` comme méthode de remplissage.

Chaque groupe peut contenir plusieurs objets de remplissage, mais une seule ligne-guide qui est utilisée par toutes les formes pleines du groupe, 
chaque forme utilisant la portion de la ligne-guide qui l'intersecte. Dans ce cas, une forme pleine qui n'intersecte pas la ligne guide ne sera pas réellement remplie. Le groupe peut aussi contenir des traits qui n'ont pas été transformés en ligne-guide et qui seront brodés normalement

Si plusieurs lignes-guide sont présentes, une seule d'entre elles est prise en compte. Sur le canevas, un marqueur permet de distinguer les lignes-guide des éléments de broderie standard.

### Plusieurs formes de remplissage dans un même groupe

![Guided Fill Group](/assets/images/docs/guided-fill-group.png)

### Une seule forme de remplissage dans le groupe

![Guided Fill One in a Group](/assets/images/docs/fr/guided-fill-single-fr.png)

## Définir le point de départ et d'arrivée
Définir le point de départ et d'arrivée pour les remplissages automatiques avec les [commandes visuelles](/fr/docs/commands/).

## Paramètres

Lancez `Extensions > Ink/Stitch  > Paramètres`. Choisir "Remplissage guidé" dans la méthode de remplissage et ajustez les réglages selon vos besoins

Lisez les informations détaillées dans la section  [Guided Fill Params](/docs/fr/params/).

## Sous couche

La sous-couche du remplissage guidé  n'utilise pas la ligne-guide, mais tout comme pour le remplissage standard, il utilise l'angle de remplissage qui peut être défini dans les 
[paramètres](/docs/params/#fill-underlay) de la sous-couche.
##  Exemple de fichiers qui utilisent le remplissage guidé
{% include tutorials/tutorial_list key="stitch-type" value="Guided Fill" %}

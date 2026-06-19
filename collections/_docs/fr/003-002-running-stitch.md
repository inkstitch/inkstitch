---
title: "Point droit / Point triple"
permalink: /fr/docs/stitches/running-stitch/
last_modified_at: 2026-06-19
toc: true
---
## Description


Le point droit produit une série de petits points suivant une ligne ou une courbe.

Une simple répétition est généralement trop fine, c'est pourquoi le point droite est souvent réalisé en point triple ou plus généralement en point multiple. 
Cela rend la ligne plus large et plus visible.

{% include folder-galleries path="butterfly-fill-project/running/" captions="1:Running stitch mandala (redwork)" %}

## Création

Un point droit est créé à l'aide d'un chemin muni d'une couleur de contour.

Le sens de la broderie est influencé par [la direction du chemin](/fr/docs/customize/#activation-de-la-direction-des-chemins). Si vous souhaitez échanger le départ et l'arrivée de votre point droit, exécutez `Chemin > Inverser`.

Si un objet est constitué de plusieurs chemins combinés, ils seront brodés l'un après l'autre, avec un saut entre chaque. 

## Paramétres

Ouvrir `Extensions > Ink/Stitch  > Paramètres` pour paramétrer selon vos besoins.

{% include upcoming_release_params.html %}

Paramètres|Description
---|---
Points droits le long des chemins |Doit être activé pour que ces paramètres prennent effet
Méthode                           |Choisir `Point droit / Point multiple`
Répétitions                         |Définir combien de fois aller et revenir le long du chemin<br />◦ Par défaut: 1 (aller une fois du début à la fin du chemin)<br />◦ Nombre impair: les points se termineront à la fin du chemin<br />◦ Nombre pair: la broderie va revenir au début du chemin
Nombre de répétitions du point triple |◦ Repasse sur chaque point le nombre de fois indiqué.<br />◦ Une valeur de 1 triplera chaque point (avant, arrière, avant).<br />◦ Une valeur de 2 permettra de quintupler chaque point, etc..<br />◦ Il est possible de définir un motif de répétitions en entrant plusieurs valeurs séparées par un espace (ces valeurs seront utilisées alternativement par les points)
Longueur du point droit           |Détermine la longueur des points. En saisissant plusieurs valeurs, il est possible de définir un motif répétitif personnalisé. Par exemple, `2 4` créera des points de longueur 2 et 4 mm en alternance.
Tolerance du point droit          |Les points ne peuvent pas être éloignés du chemin de plus que cette distance. Une tolerance basse peut impliquer des points plus courts dans les courbes. Une tolerance haute entraine un arrondissement des angles aigus.
Rendre aléatoire                    |Rendre la longueur du point aléatoire plutôt que de découper ou décaler régulièrement. 
Mouvement aléatoire de la longueur du point                    |Pourcentage maximum de variation de la longueur du point (appliqué si la longueur est rendue aléatoire).
Graine Aléatoire                   |Rouler le dé ou entrer une valeur modifie les points aléatoires
Longueur minimum de point|Est prioritaire par rapport à la valeur de la longueur minimum de point définie dans les préférences. Les points plus courts seront supprimés.
Longueur minimum de saut|Est prioritaire par rapport à la valeur de la longueur minimum de saut définie dans les préférences. Si la distance à l'objet suivant est inférieure, il n'y aura pas de points d'arrêt, sauf si les points d'arrêts sont forcés.
Autoriser des points d'arrêts     |Permet l'ajout d'un point d'arrêt à la ou les positions choisies si la longueur minimum de saut (locale ou à défaut globale au fichier) l'impose.
Forcer des points d'arrêts        |Force un point d'arrêt après l'objet indépendament de la valeur de "longueur minimum de saut".
Point d'arrêt initial                   |Choisir le  [style désiré](/fr/docs/stitches/lock-stitches/)
Point d'arrêt final                 |Choisir le  [style désiré](/fr/docs/stitches/lock-stitches/)
Couper après                      |Couper le fil après avoir brodé cet objet
Arrêter après                     |Arrêter (pause machine) après avoir brodé cet objet. Avant l'arrêt, il y aura un saut vers la position d'arrêt si elle a été définie

## Routage (agencement automatique)

Lorsque plusieurs objets consécutifs sont paramétrés en point droit, il est souvent souhaitable de les réagencer pour éviter au maximum les sauts. 

Essayez les deux extensions `Agencement automatique de points droits ` et `Redwork` dans  [Outils: Traits](/fr/docs/stroke-tools/).

## Motif sur point droit

Lire le [tutoriel](/fr/tutorials/patterned-unning-stitch/) pour créer facilement un motif sur point droit

![patterned running stitch](/assets/images/tutorials/pattern-along-path/copy-paste.png)

## Fichiers exemple avec point droit
{% include tutorials/tutorial_list key="stitch-type" value="Running Stitch" %}

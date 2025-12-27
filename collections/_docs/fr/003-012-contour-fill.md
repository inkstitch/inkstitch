---
title: "Remplissage selon le contour"
permalink: /fr/docs/stitches/contour-fill/
last_modified_at: 2025-04-12
toc: true
---
## De quoi s'agit-il ?

![Contour fill detail](/assets/images/docs/contour-fill-detail.jpg)

Le remplissage selon le contour remplit les objets en suivant leur contour.


## Comment le créer

Créez une **forme fermée avec une couleur de remplissage**



## Définir le point de départ et d'arrivée
Définir le point de départ et d'arrivée pour les remplissages automatiques avec les [commandes visuelles](/fr/docs/commands/).

## Paramètres

Lancez `Extensions > Ink/Stitch  > Paramètres`. Choisir "Remplissage selon le contour" dans la méthode de remplissage et ajustez les réglages selon vos besoins

|Paramètres||Description|
|---|---|---|
|Autoremplissage avec des points de broderie| ☑ |Doit être activé pour que ces paramètres prennent effet.|
|Méthode de remplissage                     |Remplissage selon le contour| Remplissage selon le contour doit être selectionné pour broder des lignes en spirale suivant le contour.|
|Stratégie de remplissage selon le contour  |![Inner to Outer](/assets/images/docs/contour-fill-innertoouter-bottlenecks.jpg)<br>![Contour spirals](/assets/images/docs/contour-fill-spirals.jpg)|**Intérieur vers extérieur** (valeur par défaut) est capable de remplir des formes avec un goulot d'étranglement<br>**Spirale Simple**  remplit une forme avec une spirale unique de l'extérieur vers l'intérieur<br>**Spirale doublel** remplit une forme avec une double spirale, en commençant et terminant sur la frontière extérieure de la forme.|
|Style de jointure |Rond, à onglet, biseauté|Méthode pour gérer les arêtes lorsque la taille du contour est réduite pour les spirales intérieures|
|Eviter l'auto croisement|![Avoid self crossing effect](/assets/images/docs/contour-fill-self-crossing.jpg)|Choisir si intérieur vers extérieur est autorisé à se croiser, ne s'applique pas aux autres stratégies de remplissage.|
|Sens des aiguilles d'une montre            ||Direction de déplacement autour du contour.|
|Lissage||Lisse la broderie. Le lissage détermine la mesure dans laquelle le chemin lissé peut s'éloigner du chemin originel. Essayez de petites valeurs comme 0.2. Attention, il est possible qu'il faille aussi modifier la tolérance du point droit.|
Élargir                                      ||Étend la forme avant le remplissage pour éviter les trous entre les formes. Les valeurs négatives contractent.
|Longueur maximale du point de remplissage  |![Exemple de longueur de point](/assets/images/docs/params-fill-stitch_length.png) |La longueur de chaque point dans une rangée. "Max", c'est parce qu'un point plus court peut être utilisé au début ou à la fin d'une ligne.|
|Espacement entre les rangées               |![Exemple d'espacement](/assets/images/docs/params-fill-spacing_between_rows.png) |Distance entre les rangées de points.|
|Tolérance du point droit                   |![Exemple de tolerance](/assets/images/docs/contourfilltolerance.svg) |Tous les points doivent rester au plus à cette distance du chemin. Une tolérance plus faible (en haut sur le dessin) signifie que les points seront plus rapprochés. Une tolérance plus élevée (en bas) signifie que les angles vifs peuvent être arrondis.|
|Rendre aléatoire                           |☑ |Rendre la longueur du point aléatoire plutôt que de découper ou décaler régulièrement. Ceci est recommandé lorsque le remplissage est dense pour éviter les effets de moiré.|
|Mouvement aléatoire de la longueur du point||Pourcentage maximum de variation de la longueur du point appliqué si la longueur est rendue aléatoire.|
|Graine Aléatoire                   ||Rouler le dé ou entrer une valeur modifie les points aléatoires|
|Longueur minimum de point          ||Est prioritaire par rapport à la valeur de la longueur minimum de point définie dans les préférences. Les points plus courts seront supprimés.|
|Longueur minimum de saut           ||Est prioritaire par rapport à la valeur de la longueur minimum de saut définie dans les préférences. Si la distance à l'objet suivant est inférieure, il n'y aura pas de points d'arrêt, sauf si les points d'arrêts sont forcés.|
|Autoriser les points d'arrêts      | ☑|Ajoute un point d'arrêt à la ou les positions choisies.|
|Forcer les points d'arrêts         |☑|Force un point d'arrêt après l'objet indépendament de la valeur de "Saut de fil" dans les Préférences d'Ink/Stitch.|
|Point d'arrêt initial              ||Sélectionnez le type du  [point d'ancrage](/fr/docs/stitches/lock-stitches).|
|Point d'arrêt final                ||Sélectionnez le type du [point d'arrêt](/fr/docs/stitches/lock-stitches).|
|Couper après                       |☑|Couper le fil après avoir brodé cet objet.|
|Arrêter après                      |☑|Faire faire une pause à la machine après avoir brodé  cet objet. Si une position d'arrêt est définie, elle est rejointe  par un saut avant la pause de la machine.|

## Sous-couche

La sous-couche de remplissage selon le contour ne suit pas le contour, mais utilise l'angle de remplissage qui peut être défini dans les 
[paramètres](/fr/docs/stitches/fill-stitch/#sous-couche) de la sous-couche.

## Exemples de fichier qui utilisent le remplissage suivant le contour
{% include tutorials/tutorial_list key="stitch-type" value="Contour Fill" %}

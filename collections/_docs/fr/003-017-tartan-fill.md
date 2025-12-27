---
title: "Remplissage Tartan"
permalink: /fr/docs/stitches/tartan-fill/
last_modified_at: 2024-05-07
toc: true
---
## Qu'est ce que c'est

[![Tartan Fill Sample](/assets/images/docs/tartan-fill.jpg){: width="200x"}](/assets/images/docs/tartan-fill.svg){: title="Download SVG File" .align-left download="tartan-fill.svg" }
Un Tartan et un tissu à motif de rayures horizontales et verticales. Il est en particulier connu pour son utilisation pour les kilt écossais.  Ce point de broderie essaye d'imiter ces motifs.

## Comment le créer

* Créer un **chemin fermé avec une couleur de remplissage**. La forme peut avoir des trous ou ne pas être connexe.
* Ouvrir l'extension:  `Extensions > Ink/Stitch > Outils: Remplissage > Tartan`  et créer votre propre motif de tartan
* Vous pouvez modifier d'avantages de paramètres dans le dialogues de paramétrage (`Extensions > Ink/Stitch > Paramètres`)

## Edition des motifs de Tartan.

L'éditeur de Tartan se trouve dans  `Extensions > Ink/Stitch > Outils: Remplissage > Tartan`

[En savoir plus sur l'éditeur de Tartan](/fr/docs/fill-tools#tartan)

## Paramètres

Lancez `Extensions > Ink/Stitch  > Paramètres` pour modifier les réglages selon vos besoins.

|Paramètres||Description|
|---|---|---|
|Autoremplissage avec des points de broderie| ☑ |Doit être activé pour que ces paramètres prennent effet.|
|Méthode de remplissage|Remplissage Tartan| Doit être sur Remplissage Tartan.|
|Compensation d'étirement - Élargir|![Expand example](/assets/images/docs/params-fill-expand.png) |Étend la forme avant le point de remplissage pour compenser les écarts entre les formes en raison de l'étirement du tissu.|
|Angle des lignes de points|![Angle exemple](/assets/images/docs/params-fill-angle.png) |L'angle des rangées de points, en degrés. 0 est horizontal et l'angle augmente dans le sens contraire des aiguilles d'une montre. Les angles négatifs sont autorisés.|
|Longueur maximale du point de remplissage|![Exemple de longueur de point](/assets/images/docs/params-fill-stitch_length.png) |La longueur de chaque point dans une rangée. "Max", c'est parce qu'un point plus court peut être utilisé au début ou à la fin d'une ligne.|
|Espacement entre les rangées|![Exemple d'espacement](/assets/images/docs/params-fill-spacing_between_rows.png) |Espacement entre les rangées de points.|
|Décaler les rangées autant de fois avant de répéter|![Décalage exemple](/assets/images/docs/params-fill-stagger.png) |Les points sont décalés de manière à ce que les rangées de points voisines ne tombent pas toutes dans la même colonne (ce qui créerait un effet de vallée). Ce paramètre détermine la longueur du cycle de décalage des rangées. Les fractions sont autorisées et peuvent produire des diagonales moins visibles que les valeurs entières.|
|Longueur de point droit|![Exemple de Longueur de point droit](/assets/images/docs/params-fill-running_stitch_length.png) |Longueur des points utilisés pour passer d'une section à l'autre.|
|Tolérance du point droit|| Les points ne peuvent pas être éloignés du chemin de plus que cette distance. Une tolérance basse peut impliquer des points plus courts. Une tolérance haute entraine un arrondissement des angles aigus.|
|Nombre de répétitions pour le point multiple ||◦ Active le [Mode point multiple](/fr/docs/stitches/bean-stitch/)<br />◦ Repasse sur chaque point le nombre de fois indiqué.<br />◦ Une valeur de 1 triplera chaque point (avant, arrière, avant).<br />◦ Une valeur de 2 permettra de quintupler chaque point, etc..<br />|
|Nombre de rangées par fil  du Tartan|| Nombre de rangées consécutives de la même couleur|
|Largeur de chevron   ||Defini la largeur du motif en chevron. Choisir 0 pour des bandes normales. Il est recommandé d'utiliser un multiple ou une fraction de la largeur de bande (ou d'utiliser seulement une couleur pour la trame et une autre couleur pour la chaîne).|
|Longueur minimum de point||Est prioritaire par rapport à la valeur de la longueur minimum de point définie dans les préférences. Les points plus courts seront supprimés.|
|Longueur minimum de saut||Est prioritaire par rapport à la valeur de la longueur minimum de saut définie dans les préférences. Si la distance à l'objet suivant est inférieure, il n'y aura pas de points d'arrêt, sauf si les points d'arrêts sont forcés.|
|Autoriser les points d'arrêts | ☑|Ajoute si nécessaire un point d'arrêt à la ou les positions choisies.|
|Forcer les points d'arrêts |☑|Force un point d'arrêt après l'objet indépendamment des valeurs de "longueur minimum de saut" dans les Préférences d'Ink/Stitch et localement.|
|Point d'arrêt initial       ||Sélectionnez le type du  [point d'ancrage](/fr/docs/stitches/lock-stitches).|
|Point d'arrêt final       ||Sélectionnez le type du [point d'arrêt](/fr/docs/stitches/lock-stitches).|
|Arrêter après                       |☑ |Faire faire une pause à la machine après avoir brodé cet objet. Si une position d'arrêt a été définie, elle est rejointe par un saut avant la pause. |
|Couper après                        |☑ |Couper le fil après avoir brodé cet objet.|
{: .params-table}



## Sous Couche

La sous couche d'un remplissage tartan est la même que pour un remplissage automatique et utilise l'angle de remplissage qui peut être défini dans les
paramètres](/fr/docs/stitches/fill-stitch#sous-couche) de la sous couche.

## Exemples de fichiers utilisant le remplissage tartan
{% include tutorials/tutorial_list key="stitch-type" value="Tartan Fill" %}

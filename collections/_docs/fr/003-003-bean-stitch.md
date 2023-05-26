---
title: "Point triple"
permalink: /fr/docs/stitches/bean-stitch/
excerpt: ""
last_modified_at: 2023-04-19
toc: true
---
## Qu’est-ce que c’est
[![Bean Stitch Dog](/assets/images/docs/bean-stitch-example.jpg){: width="200x"}](/assets/images/docs/bean-stitch.svg){: title="Download SVG File" .align-left download="bean-stitch.svg" }
Le point triple décrit une répétition de points droits avant arrière. Il en résultera un point plus fourni.

![Bean Stitch Detail](/assets/images/docs/bean-stitch-detail.jpg){: width="350x" }

## Comment le créer
1. Sélectionner un trait pointillé et ouvrir  `Extensions > Ink/Stitch  > Paramètres`.

2. Définissez le nombre de répétitions dans `Nombre de répétitions de points triples` dans [paramètres de point droit](/fr/docs/stitches/running-stitch).

   ![Bean Stitch Params](/assets/images/docs/fr/params-bean-stitch.jpg)

   * Une valeur de 1 triplera chaque point (avant, arrière, avant).
   * Une valeur de 2 permettra de quintupler chaque point, etc.
   * Il est possible de définir un motif de répétitions en entrant plusieurs valeurs séparées par un espace
  
## Paramètres

Ouvrir `Extensions > Ink/Stitch  > Paramètres` pour paramétrer selon vos besoins.

Paramètres||Description
---|--|---
Points droits le long des chemins |Doit être activé pour que ces paramètres prennent effet
Méthode                           |Choisir Point Droit
Placement de points manuels       |Non Activé pour ne pas déclencher [le mode point manuel](/fr/docs/stitches/manual-stitch/)
Répéter                           |Définir combien de fois aller et revenir le long du chemin<br />◦ par défaut: 1 (aller une fois du début à la fin du chemin)<br />◦ Nombre impair: les points se termineront à la fin du chemin<br />◦ Nombre pair: la broderie va revenir au début du chemin
Nombre de répétitions du point triple |Active le [Mode point triple](/fr/docs/stitches/bean-stitch/)<br />◦ Repasse sur chaque point le nombre de fois indiqué.<br />◦ Une valeur de 1 triplera chaque point (avant, arrière, avant).<br />◦ Une valeur de 2 permettra de quintupler chaque point, etc..<br />◦ Il est possible de définir un motif de répétitions en entrant plusieurs valeurs séparées par un espace
Longueur du point droit           |Longueur des points 
Tolerance du point droit          |Les points ne peuvent pas être éloignés du chemin de plus que cette distance. Une tolerance basse peut impliquer des points plus courts. Une tolerance haute entraine un arrondissement des angles aigus.
Autoriser les points d'arrêts     |Ajoute un point d'arrêt à la ou les positions choisies
Forcer les points d'arrêts        |Force un point d'arrêt après l'objet indépendament de la valeur de "Saut de fil" dans les Préférences d'Ink/Stitch.
Point d'ancrage                  |Choisir le  [style désiré](/fr/docs/stitches/lock-stitches/)
Point d'arrêt                    |Choisir le  [style désiré](/fr/docs/stitches/lock-stitches/)
Couper après                      |Couper le fil après avoir brodé cet objet
Arrêter après                     |Arrêter (pause machine) après avoir brodé cet objet. Avant l'arrêt, il y aura un saut vers la position d'arrêt si elle a été définie

Il est possible définir soit même une sequence de nombre de répétitions de point triple. Par exemple saisir 0 1 permettra d'obtenir une alternance de point simple et de point triple. La suite peut être plus longue. Les valeurs entières doivent être séparées par un espace.



{: .params-table }

## Fichiers exemple avec point triple
{% include tutorials/tutorial_list key="stitch-type" value="Bean Stitch" %}

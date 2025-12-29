---
title: "Point triple"
permalink: /fr/docs/stitches/bean-stitch/
last_modified_at: 2025-12-29
toc: true
---
## Qu’est-ce que c’est
[![Bean Stitch Dog](/assets/images/docs/bean-stitch-example.jpg){: width="200x"}](/assets/images/docs/bean-stitch.svg){: title="Download SVG File" .align-left download="bean-stitch.svg" }
Le point triple décrit une répétition de points droits avant arrière. Il en résultera un point plus fourni.

![Bean Stitch Detail](/assets/images/docs/bean-stitch-detail.jpg){: width="350x" }

## Comment le créer
1. Sélectionner un trait et ouvrir  `Extensions > Ink/Stitch  > Paramètres`.

2. Définissez le nombre de répétitions dans `Nombre de répétitions de points triples` dans [paramètres de point droit](/fr/docs/stitches/running-stitch).

   ![Bean Stitch Params](/assets/images/docs/fr/params-bean-stitch.jpg)

   * Une valeur de 1 triplera chaque point (avant, arrière, avant).
   * Une valeur de 2 permettra de quintupler chaque point, etc.
   * Il est possible de définir un motif de répétitions en entrant plusieurs valeurs séparées par un espace (ces valeurs seront utilisées alternativement par les points)
  
## Paramètres

Ouvrir `Extensions > Ink/Stitch  > Paramètres` pour paramétrer selon vos besoins.

Paramètres||Description
---|---
Points droits le long des chemins |Doit être activé pour que ces paramètres prennent effet
Méthode                           |Choisir Point Droit
Répétitions                       |Définir combien de fois aller et revenir le long du chemin<br />◦ par défaut: 1 (aller une fois du début à la fin du chemin)<br />◦ Nombre impair: les points se termineront à la fin du chemin<br />◦ Nombre pair: la broderie va revenir au début du chemin
Nombre de répétitions du point triple |Active le [Mode point triple](/fr/docs/stitches/bean-stitch/)<br />◦ Repasse sur chaque point le nombre de fois indiqué.<br />◦ Une valeur de 1 triplera chaque point (avant, arrière, avant).<br />◦ Une valeur de 2 permettra de quintupler chaque point, etc..<br />◦ Il est possible de définir un motif de répétitions en entrant plusieurs valeurs séparées par un espace
Longueur du point droit           |Détermine la longueur des points. En saisissant plusieurs valeurs, il est possible de définir un motif répétitif personnalisé. Par exemple, `2 4` créera des points de longueur 2 et 4 mm en alternance.
Tolerance du point droit          |Les points ne peuvent pas être éloignés du chemin de plus que cette distance. Une tolerance basse peut impliquer des points plus courts. Une tolerance haute entraine un arrondissement des angles aigus.
Rendre aléatoire                     |Rendre la longueur du point aléatoire plutôt que de découper ou décaler régulièrement. Ceci est recommandé lorsque le remplissage est dense pour éviter les effets de moiré.
Mouvement aléatoire de la longueur du point                   |Pourcentage maximum de variation de la longueur du point appliqué si la longueur est rendue aléatoire.
Graine Aléatoire                   |Rouler le dé ou entrer une valeur modifie les points aléatoires
Longueur minimum de poin|Est prioritaire par rapport à la valeur de la longueur minimum de point définie dans les préférences. Les points plus courts seront supprimés.
Longueur minimum de saut|Est prioritaire par rapport à la valeur de la longueur minimum de saut définie dans les préférences. Si la distance à l'objet suivant est inférieure, il n'y aura pas de points d'arrêt, sauf si les points d'arrêts sont forcés.
Autoriser les points d'arrêts     |Ajoute un point d'arrêt à la ou les positions choisies
Forcer les points d'arrêts        |Force un point d'arrêt après l'objet indépendament de la valeur de "Saut de fil" dans les Préférences d'Ink/Stitch.
Point d'arrêt initial(point d'ancrage)                  |Choisir le  [style désiré](/fr/docs/stitches/lock-stitches/)
Point d'arrêt  final                  |Choisir le  [style désiré](/fr/docs/stitches/lock-stitches/)
Couper après                      |Couper le fil après avoir brodé cet objet
Arrêter après                     |Arrêter (pause machine) après avoir brodé cet objet. Avant l'arrêt, il y aura un saut vers la position d'arrêt si elle a été définie

Il est possible définir soit même une sequence de nombre de répétitions de point triple. Par exemple saisir 0 1 permettra d'obtenir une alternance de point simple et de point triple. La suite peut être plus longue. Les valeurs entières doivent être séparées par un espace.



{: .params-table }

## Fichiers exemple avec point triple
{% include tutorials/tutorial_list key="stitch-type" value="Bean Stitch" %}

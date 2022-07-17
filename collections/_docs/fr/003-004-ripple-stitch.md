---
title: "Broderie Ondulée"
permalink: /fr/docs/stitches/ripple-stitch/
excerpt: ""
last_modified_at: 2022-07-17
toc: true
---
# De quoi s'agit-il ?

[![Ripple butterfly](/assets/images/docs/ripplefly.jpg){: width="200x"}](/assets/images/docs/ripplefly.svg){: title="Download SVG File" .align-left download="ripplefly.svg" }La broderie ondulée tient à la fois du point droit et du remplissage : elle se comporte comme un point droit (on peut l'exécuter  en point triple par exemple), elle est définie à partir d'un trait, mais elle produit à l'arrivée une broderie qui s'étend sur une surface. Utilisée de manière lâche, le résultat ressemble à des ondes, d'où son nom. 


Regardez cette  appétissante video: {% include video id="cyvby3KJM10" provider="youtube" %}

Si  le chemin initial est fermé la forme sera remplie par une spirale (ondulations  circulaires). S'il est ouvert, la broderie se fera en va et vient (ondulations linéaires)



## Ondulations  circulaires 

* Créer **un chemin fermé simple avec une couleur de contour et sans couleur de remplissage** (pas une combinaison de sous-chemins)
* Créer  [une  cible ou des guides](#guiding-ripples) (optionel)
* Sélectionner ce chemin
* Ouvrir le dialogue de paramètrage (`Extensions > Ink/Stitch > Paramètres`) et sélectionner `Broderie ondulée` comme méthode.
* Définir les  [paramètres](#params) à votre convenence et Appliquer



![Exemples d'ondulations circulaires](/assets/images/docs/en/circular-ripple.svg)

[Télécharger les examples](/assets/images/docs/en/circular-ripple.svg)

## Ondulations linéaires

Les ondulations linéaires peuvent être créées de différentes manières. Le point de départ peut être un chemin simple ou bien être construit comme une colonne satin


* Créer une  forme ouverte ( un chemin simple, deux chemins combinés ou même une  colonne satin)
* Créer   [une  cible ou des guides](#guiding-ripples) (optionel)
* Sélectionner ce chemin
* Ouvrir le dialogue de paramètrage (`Extensions > Ink/Stitch > Paramètres`) et sélectionner `Broderie ondulée` comme méthode.
* Définir les  [paramètres](#params) à votre convenence et Appliquer

![Exemples d'ondulations linéaires](/assets/images/docs/en/linear-ripple.svg)

[Télécharger les examples](/assets/images/docs/en/linear-ripple.svg)

## Ondulations avec boucles

Les boucles sont autorisées et bienvenues pour toutes les ondulations.
Utilisez les pour toutes  sortes d'effets spéciaux....

![Ondulations avec boucles](/assets/images/docs/en/ripple-loops.svg)

[Télécharger les examples](/assets/images/docs/en/ripple-loops.svg)


##  Guider les ondulations

Les ondulations construites à partir d'un chemin simple  (une forme fermée ou une courbe de bézier simple) peuvent être guidées en utilisant l'une quelconque de ces trois méthodes.

###  Guidage par cible
Il est possible de définir le point cible de l'ondulation grace aux [commandes visuelles](/fr/docs/commands/).

* Ouvrir `Extensions > Ink/Stitch > Commandes  > Attacher des  commandes à des objets selectionnés  ...`
* Selectionner `Position de la cible de la broderie ondulée` et appliquer
* Selectionner le symbole et le déplacer à la position souhaitée.

En l'absence de  toute information de guidage,c'est le centre de l'ondulation initiale qui  tient lieu de point cible.


###  Guidage selon un chemin

* Directement dans le même groupe que la broderie ondulée (pas dans un sous-groupe), utilisez l'outil courbe de Beziers pour créer un chemin qui commence proche de l'ondulation puis s'en éloigne. 
* Selectionner cette courbe et exécuter  `Extensions > Ink/Stitch > Edition > Sélection vers guide`.
* Sélectionner la broderie ondulée 
* Ouvrir le dialogue de paramètrage (`Extensions > Ink/Stitch > Paramètres`) et sélectionner `Broderie ondulée` comme méthode.
* Définir les  [paramètres](#params) à votre convenence et Appliquer


La position des centres des réplications de l'ondulation initale est alors déterminée par le guide


### Guidage Satin 

Avec le guidage satin, vous pouvez  guider précisément les ondulations en utilisant une colonne satin pour guider au lieu d'un simple chemin. La largeur de la colonne satin a un effet sur la largeur des ondulations. 

* In the very same group of the ripple stitch object create a [satin column](/docs/stitches/satin-column/) like object with rails and rungs.
* Select the newly created object and run `Extensions > Ink/Stitch > Edit > Selection to guide line`.
* Select the ripple object and run params. Adapt parameters to your liking.

* Directement dans le même groupe que la broderie ondulée (pas dans un sous-groupe), créez un objet similaire à une [colonne satin](/docs/stitches/satin-column/) avec rails et traverses.
* Selectionner ce nouvel objet et exécutez  `Extensions > Ink/Stitch > Edition > Sélection vers guide`.
* Sélectionner la broderie ondulée 
* Ouvrir le dialogue de paramètrage (`Extensions > Ink/Stitch > Paramètres`) et sélectionner `Broderie ondulée` comme méthode.
* Définir les  [paramètres](#params) à votre convenence et Appliquer




## Comment la paramètrer

Paramètres||Description
---|---|---
Points droits le long des chemins   |  ☑  |Doit être activé pour que ces paramètres prennent effet.
Méthode      || Choisir Broderie Ondulée
Répéter                      || Définir combien de fois le chemin final de broderie est exécuté en va et vient le long du parcours <br />◦ par défaut: 1 (aller une fois du début à la fin du chemin)<br />◦ Nombre impair: les points se termineront à la fin du chemin<br />◦ Nombre pair: la couture va revenir au début du chemin
Nombre de répétitions du point triple || Activer [Mode point triple](/fr/docs/stitches/bean-stitch/)<br />◦ Repasse sur chaque point le nombre de fois indiqué.<br />◦ Une valeur de 1 triplera chaque point (avant, arrière, avant).<br />◦ Une valeur de 2 permettra de quintupler chaque point, etc..<br />
Longueur du point droit||Longueur des points dans le [Mode Point Droit](/fr/docs/stitches/running-stitch/)
Tolérance du point droit||Tous les points doivent rester au plus à cette distance du chemin. Une tolérance plus faible signifie que les points seront plus rapprochés. Une tolérance plus élevée signifie que les angles vifs peuvent être arrondis.
Nombre de lignes|<img src="/assets/images/docs/ripple_only_lines.svg" alt="Nombre de lignes"/>|Choisir le nombre de réplications de l'ondulation dans la broderie. La valeur par défaut est 10.
◦Sauter les premières lignes <br /> ◦Sauter les dernières lignes  |<img src="/assets/images/docs/ripple_only_skip.svg" alt="Sauter"/>| Permet de sauter (ne pas broder)  ce nombre de réplications au début et/ou à la fin
Exposant de la distance entre les lignes|<img src="/assets/images/docs/ripple_only_exponent.svg" alt="Exposant"/>| ◦ La valeur par défaut de 1 espace les réplications de manière constante<br />◦ Avec une valeur supérieure à  1 l'espace  entre deux réplications consécutives augmente au fur et à mesure qu'on s'éloigne du chemin qui définit l'ondulation  <br />◦ Avec une valeur inférieure à  1 l'espace  entre deux réplications consécutives diminue au fur et à mesure qu'on s'éloigne du chemin qui définit l'ondulation
Inverser effet exposant |☑  ou ▢| Échange le rôle de la  première et de la dernière réplication pour le calcul de la distance entre les réplications
Changer le sens |☑  ou ▢|  Change le sens du  chemin final de broderie . N'a pas d'effet sur les autres paramètres
Distance grille  maximum |<img src="/assets/images/docs/ripple_only_grid.svg" alt="Distance"/>| Si une distance positive est spécifiée, les ondulations de la broderie sont complétées  en une "grille", par un chemin "perpendiculaire" aux ondulations. Le paramètre contrôle l'écart de ces perpendiculaires. Intervertir  n'a pas  d'influence sur ce paramètre.
Démarrer à| seulement pour des ondulations guidées|Taille de la première ondulation en pourcentage.
Finir à| seulement pour des ondulations guidées |Taille de la dernière ondulation en pourcentage.
Tourner| ☑  ou ▢| seulement pour des ondulations guidées
Style de Jointure|<img src="/assets/images/docs/flat_or_point.svg" alt="Join Stile"/> |pour des ondulations ouvertes,les réplications peuvent être jointes par un segment (en haut) ou en un seul point (en bas)
Autoriser les points d'arrêts | ☑  ou ▢|Choix de l'ajout d'un point d'arrêt en début et en fin de broderie.
Forcer les points d'arrêts | ☑ ou ▢| Force un point d'arrêt après l'objet indépendament de la valeur de "Saut de fil" dans les Préférences d'Ink/Stitch.
{: .params-table }



Il existe de nombreuses manières d'exploiter toutes les possibilitéss :

![Ondulations diverses](/assets/images/docs/fr/rippleways_fr.svg)
[Download](/assets/images/docs/en/rippleways_fr.svg){: download="rippleways.svg" }





##  Exemples de fichiers qui utilisent la broderie ondulée 
{% include tutorials/tutorial_list key="stitch-type" value="Ripple Stitch" %}

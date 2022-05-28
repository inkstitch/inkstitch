---
title: "Broderie Ondulée"
permalink: /fr/docs/stitches/ripple/
excerpt: ""
last_modified_at: 2022-05-20
toc: true
---
{% include upcoming_release.html %}
# De quoi s'agit-il ?

[![Ripple butterfly](/assets/images/docs/ripplefly.jpg){: width="200x"}](/assets/images/docs/ripplefly.svg){: title="Download SVG File" .align-left download="ripplefly.svg" }La broderie ondulée tient à la fois du point droit et du remplissage : elle se comporte comme un point droit (on peut l'exécuter  en point triple par exemple), elle est définie à partir d'un trait, mais elle produit à l'arrivée une broderie qui s'étend sur une surface. Utilisée de manière lâche, le résultat ressemble à des ondes, d'où son nom. 



##  Comment la créer
A partir d'un  **trait (couleur de contour mais pas de remplissage)** qui peut être un  chemin  simple (la décomposition n'a aucun effet sur lui), ou un  chemin  combinant deux sous chemins (assimilable  aux  deux rails d'une colonne satin) 

* Créer **un chemin avec une couleur de contour et sans couleur de remplissage** simple ou composé de deux sous chemins 
* Sélectionner ce chemin
* Ouvrir le dialogue de paramètrage (`Extensions > Ink/Stitch > Paramètres`) et sélectionner `Broderie ondulée` comme méthode.

Une  fois le chemin créé, il sera possible d'influencer la manière dont les ondulations sont répliquées pour remplir une forme.




Il existe de nombreuses manières d'exploiter toutes les possibilitéss :

![Ondulations diverses](/assets/images/docs/fr/rippleways_fr.svg)

## Comment la paramètrer


### Paramètrage en partant d'un chemin simple (ne peut pas être décomposé)

Paramètres||Description
---|---|---
Points droits le long des chemins   |  ☑  |Doit être activé pour que ces paramètres prennent effet.
Méthode      || Choisir Broderie Ondulée
Répéter                      || Définir combien de fois le chemin final de broderie est excuté en va et vient le long du parcours <br />◦ par défaut: 1 (aller une fois du début à la fin du chemin)<br />◦ Nombre impair: les points se termineront à la fin du chemin<br />◦ Nombre pair: la couture va revenir au début du chemin
Nombre de répétitions du point triple || Activer [Mode point triple](/fr/docs/stitches/bean-stitch/)<br />◦ Repasse sur chaque point le nombre de fois indiqué.<br />◦ Une valeur de 1 triplera chaque point (avant, arrière, avant).<br />◦ Une valeur de 2 permettra de quintupler chaque point, etc..<br />
Longueur du point droit||Longueur des points dans le [Mode Point Droit](/fr/docs/stitches/running-stitch/)
Nombre de lignes|<img src="/assets/images/docs/ripple_only_lines.svg" alt="Nombre de lignes"/>|Choisir le nombre de réplications de l'ondulation dans la broderie. La valeur par défaut est 10.
◦Sauter les premières lignes <br /> ◦Sauter les dernières lignes  |<img src="/assets/images/docs/fr/ripple_only_skip_fr.svg" alt="Sauter"/>| Permet de sauter (ne pas broder)  ce nombre de réplications au début et/ou à la fin
Intervertir |☑  ou ▢|  Si toute les lignes sont brodées, revient à parcours le chemin final de broderie à l'envers. Si des lignes sont sautées, les deux paramètres de saut de lignes sont  aussi intervertis. A aussi un effet sur l'exposant
Distance grille || Inopérant dans ce cas
Exposant de la distance entre les lignes|<img src="/assets/images/docs/fr/ripple_only_exponent_fr.svg" alt="Exposant"/>| ◦ La valeur par défaut de 1 espace les réplications de manière constante<br />◦ Avec une valeur supérieure à  1 l'espace  entre deux réplications consécutives augmente au fur et à mesure qu'on s'éloigne du chemin qui définit l'ondulation  <br />◦ Avec une valeur inférieure à  1 l'espace  entre deux réplications consécutives diminue au fur et à mesure qu'on s'éloigne du chemin qui définit l'ondulation
Autoriser les points d'arrêts | ☑  ou ▢|Choix de l'ajout d' un point d'arrêt en début et en fin de broderie.
Forcer les points d'arrêts | ☑ ou ▢| Force un point d'arrêt après l'objet indépendament de la valeur de "Saut de fil" dans les Préférences d'Ink/Stitch.


### Paramètre additionnel uniquement en partant d'un chemin composé de deux sous chemins
Ces deux chemins, vont  se comporter un peu comme les rails d'une colonne satin. Il est possible d'ailleurs d'avoir plus de deux sous-chemins si on leur adjoint des traverses, voir plus loin

Paramètre additionnel||Description
---|---|---
Distance grille |<img src="/assets/images/docs/ripple_only_grid.svg" alt="Distance"/>| Si une distance positive est spécifiée, les ondulations de la broderie sont complétées  en une "grille", par un chemin "perpendiculaire" aux ondulations. Le paramètre contrôle l'écart de ces perpendiculaires. Intervertir  n'a pas  d'influence sur ce paramètre.

## Guidage additionnel
Il existe trois  méthodes pour guidage additionnel de déplacement des ondulations

### Pour toutes les broderies ondulées : Guidage selon un chemin
Il  est possible d'ajouter une chemin de guidage à une broderie ondulée.
Pour cela
- Creer une broderie ondulée
- Creer un trait. 
- Transformer ce trait en guide en effectuant: `Extensions > Ink/Stitch  > Edition > Selection en Guide`
- Grouper la broderie ondulée et le guide dans un même groupe

La position des centre des réplications de l'ondulation initale est alors déterminée par le guide


### Pour les  broderies ondulées définies à partir d'un chemin simple: Guidage par cible
Il est possible de définir le point cible de l'ondulation grace aux [commandes visuelles](/fr/docs/commands/). En l'absence de  toute information de guidage,c'est le centre de l'ondulation première qui  tient lieu de point cible

### Pour les  broderies ondulées définies à partir d'un chemin simple composée de deux rails : Guidage par traverses
Fonctionne de manière analogue aux traverses des colonnes satin



##  Exemples de fichiers qui utilisent la broderie ondulée 
{% include tutorials/tutorial_list key="stitch-type" value="ripple" %}

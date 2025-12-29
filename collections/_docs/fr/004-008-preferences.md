---
title: "Préférences"
permalink: /fr/docs/preferences/
last_modified_at: 2025-12-29
toc: true
---
On accède aux préférences via `Extensions > Ink/Stitch > Préférences`.

Vous pouvez soit donner des valeurs globales qui seront appliquées à tous le nouveaux documents svg, soit donner des valeurs spécifiques pour le document courant qui ont priorité sur les valeurs globales.

Ces paramètres concernent **tous les éléments du document**.

## Réglages de sortie

### Sauts de fil (mm)

Un saut de fil plus court que cette valeur sera traité comme un point normal (sans point de sureté).

Par exemple si cette valeur est à 2 mm, chaque fois qu'il y a un saut de fil  d'une longueur inférieure à 2 mm entre  deux chemins consécutifs, les points d'arrêt  du premier et les points d'ancrage du second ne sont effectués que  si dans leurs paramètres vous avez activé  "Forcer les points d'arrêt". 

Pour les sauts de fils plus longs que 2 mm, le paramétrage des points de sureté est respecté.

A partir de la version  v 3.1.0 il  est possible de surcharger la valeur globale pour des éléments particuliers dan [le dialogue de paramétrage](/doc/params).

### Longueur minimum de points (mm)

#### De quoi s'agit-il ?

Tous les points plus courts que cette valeur seront sautés (à l'exception des points de sureté). Cette valeur est utilisée uniquement à la fin du calcul de la broderie pour filtrer les points trop courts. 

Soyez conscient que ce paramètre ne fait peut-être pas ce que vous croyez. Par exemple si  la *Longueur minimum de points* est paramétrée à 2 mm dans préférence et si vous avez un chemin en point droit paramétré avec une *longueur de point droit* de 1.5 mm, un point sur deux sera sauté, et in fine le point droit aura une longueur de points de 3 mm.

La simulation tient compte de ces paramètres.

Voici les résultats de la simulation d'un point droit  paramétré avec une *longueur de point droit* égale à 1.5 mm avec dans les préférences *Longueur minimum de points* d'abord à 0.5 mm puis à 2 mm.

![simulation](/assets/images/docs/preference_msl_paths.png)

Quand la *Longueur minimum de points* vaut 2 mm, un point sur deux est sauté (à l'exception des points de sûreté) car 1.5 est plus petit que 2 mais 1.5+1.5 plus grand que 2. Le nombre de points est donc divisé par deux (hors point de sureté).

Si la valeur de  *Longueur minimum de points* avait été 3.1 mm, on aurait obtenu des points de 4.5mm

A partir de la version  v 3.1.0 il  est possible de surcharger la valeur globale pour des éléments particuliers dan [le dialogue de paramétrage](/doc/params).

#### Quel effet sur la broderie ?

*Longueur minimum de points*  modifie aussi les **bords des remplissages** (d'une façon similaire à *Sauter le dernier point dans chaque rangée*, -améliorant la qualité de la broderie des remplissages denses)  lorsque sa valeur est 
inférieure à celle de l'*espacement entre les rangées*. *Longueur minimum de points* modifie aussi **les angles aigus des points droits** où la longueur réelle des points peut être très inférieure à la valeur de *longueur de point droit* (la *tolérance* joue aussi dans cette situation)

*Longueur minimum de points* |  Remplissage automatique avec *espacement des rangées* à 0.25 | Remplissage guidée avec *espacement des rangées* à 0.25 | *longueur du point droit* 1.5 mm et largeur du dessin 10mm
---|---|---|---
0|![square 0](/assets/images/docs/preference_fill_0.png)|![square 0](/assets/images/docs/preference_guided_0.png)|![running_0](/assets/images/docs/preference_running_stitch_0.png)
0.5|![square 0.5](/assets/images/docs/preference_fill_half.png)|![square 0.5](/assets/images/docs/preference_guided_half.png)|![running_0](/assets/images/docs/preference_running_stitch_half.png)
1|![square 1](/assets/images/docs/preference_fill_1.png)|![square 1](/assets/images/docs/preference_guided_1.png)|![running_0](/assets/images/docs/preference_running_stitch_1.png)

Elle modifie aussi les  **colonnes satin** et en conséquence certaines fontes du lettrage. Vous ne voulez certainement pas de ça sur les **petites fontes** telle que *ink/stitch small* ou *glacial tiny*:


*Minimum stitch length* |  *Ink/Stitch Small* | *Glacial Tiny*
---|---|---
0 or 0.5|![ink_stitch_O](/assets/images/docs/preference_ink_small_0.png)|![glacial_O](/assets/images/docs/preference_glacial_0.png)
1|![ink_stitch_1](/assets/images/docs/preference_ink_small_1.png)|![glacial_1](/assets/images/docs/preference_glacial_1.png)

Les  **points manuels** sont eux aussi affectés  par *Longueur minimum de points*. Vous pouvez en tirer parti pour réduire un motif en point manuel sans obtenir de très petits points. Il peut y avoir un peu de déformation, mais en général le résultat est plutôt bon.

 **Si vous utilisez une W6 machine:** Réglez votre longueur minimum de point global à au moins 0.3mm, sinon vous risquez des points manquants à des endroits inattendus.
{: .notice--warning }

### Seulement pour le document courant : Tourner à l'export
Cette option permet de tourner le motif de 90°. Utile pour les brodeuses qui ne tournent pas automatiquement un motif qui nécessite une rotation pour tenir dans le cadre

### Seulement en global: Taille du cache (mb)
Elle définit la taille maximum occupée sur votre disque dur par les plans de broderie mis en cache. 

Plus cette valeur est grande, plus il sera possible de possible de stocker des plans de broderie. 

Un plan de broderie mis en cache sera affiché beaucoup plus rapidement. 

La valeur par défaut est 100. 

Le cache peut être vidé depuis les préférences globales.

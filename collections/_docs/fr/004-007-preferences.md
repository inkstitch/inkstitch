---
title: "Préférences"
permalink: /fr/docs/preferences/
excerpt: ""
last_modified_at: 2023-04-30
toc: false
---
La version courante (v 2.2.0) n'a pas de réglage global.

{% include upcoming_release.html %}

On accède aux préférences via `Extensions > Ink/Stitch > Préférences`.
Vous pouvez soit donner des valeurs globales qui seront appliquées à tous le nouveaux documents svg, soit donner des valeurs spécifiques pour le document courant.


## Réglages de sortie

* Sauts de fil (mm): Un saut de fil plus court que cette valeur sera traité comme un point normal (sans point de sureté). Par exemple si cette valeur est à 2 mm, chaque fois qu'il y a un saut de fil entre le chemin1 et le chemin2  d'une longueur inférieure à 2 mm, le points d'arrêt  du chemin1 et le point d'ancrage du chemin2 ne sont pas effectués que  si dans les paramètres vous avez activé  "Forcer les points d'arrêt". Pour les sauts de fils plus longs que 2 mm, le paramètrage des points de sureté sera respecté.
 
* Longueur minimum de points (mm): Les points plus courts que cette valeur seront sautés (à l'exception des points de sureté). Cette valeur est utilisée uniquement à la fin du calcul de la broderie pour filtrer des points trops courts. Par exemple, si vous avez un chemin en point droit paramétré à une longueur de 1.5 mm et que vous avez donnés à Longueur minimum de points la valeur de 2 mm, le premier point de 1.5 sera sauté, mais sa longueur ajoutée au point suivant qui de ce fait sera exécuté, avec une longueur du point  de 1.5+1.5 = 3 mm, et ainsi de suite, résultant finalement une série de points de 3 mm (et non 2 mm comme l'on pourrait croire). Le nombre de points est ainsi divisé par deux.

La simulation tient compte de ces préférences.

* Seulement en global: **Taille du cache (mb)**  définit la taille maximum occupée sur votre disque dur par les plans de broderie mis en cache. Plus cette valeur est grande, plus il sera possible de possible de stocker des plans de broderie. Un plan de broderie mis en cache sera affiché beaucoup plus rapidement. La valeur par défaut est 100.


**Si vous utilisez une W6 machine:** Réglez votre longueur minimum de point global à au moins 0.3mm, sinon vous risquez des points manquants à des endroits inattendus.
{: .notice--warning }

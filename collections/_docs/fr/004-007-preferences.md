---
title: "Préférences"
permalink: /fr/docs/preferences/
excerpt: ""
last_modified_at: 2023-04-15
toc: false
---
La version courante (v 2.2.0) n'a pas de réglage global.

{% include upcoming_release.html %}

On accède aux préférences via `Extensions > Ink/Stitch > Préférences`.
Vous pouvvz soit donner de valeurs globales qui seront appliquées à tous le nouveaux documents svg, soit donner des valeurs spécifiques pour le document courant.


## Réglages de sortie

* Sauts de fil (mm): Un saut de fil plus court que cette valeur sera traité comme un point normal (sans point d'arrêt)
* Longueur minimum de points (mm): Les points plus petit que cette valeur seront sautés (à l'exception des noeuds).

* Seulement en global: **Taille du cache (mb)**  définit la taille maximum occupée sur votre disque dur par les plans de broderie mis en cache. Plus cette valeur est grande, plus il sera possible de possible de stocker des plans de broderie. Un plan de broderie mis en cache sera affiché beaucoup plus rapidement. La valeur par défaut est 100.


**W6 machine:** Réglez votre longueur minimum de point global à au moins 0.3mm, sinon vous risquez des points manquants à des endroits inattendus.
{: .notice--warning }

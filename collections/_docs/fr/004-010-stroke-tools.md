---
title: "Tools: Stroke"
permalink: /fr/docs/stroke-tools/
excerpt: ""
last_modified_at: 2022-05-20
toc: true
---


{% include upcoming_release.html %}
## Agencement automatique de points droits

{% include upcoming_release.html %}

Cet  outil **remplace** un ensemble de points droits par un nouvel ensemble de points droits  empilés dans un ordre logique de broderie qui évite autant que faire se peut les sauts de fil. Lorsque necessaire des chemins (chemins de dessous) sont ajoutés, sous les chemins existants pour assurer les connexions. Les points droits résultants conservent tous les  paramètres des points droits originaux, dont la longueur de point droit, le  nombre de répétitions, le nombre de répétitions pour le point triple.  Les chemins de dessous ne conservent que la longueur du point, le nombre de répétitions est remis à un et et le nombre de répétitions de point triple à zéro.



### Usage
- Sélectionnez des chemins paramétrés en points droits
- Excutez 'Extensions > Ink/Stitch > Outils : Trait > Agencement automatique  de points droits'
- Choisir les options désirées et cliquer sur "Appliquer et quitter"
  
Par défaut, l'extension choisira de commencer par le noeud le plus à gauche et de terminer par le noeud le plus à droite même si ces noeuds ne sont pas des noeuds terminaux. Vous pouvez attacher les commandes " Début/Fin d'agencement automatique de point droit" pour forcer les positions de début et de fin.


{: .notice--info }
### Options
- Cocher "Ajouter des noeuds aux intersections" donnera un meilleure résultat de routage, avec des chemins de dessous qui auront leurs extrémités aux intersections ou aux noeuds terminaux. Ne décocher cette option que si vous avez manuellement ajouté des noeuds là ou vous souhaitez les coupures de chemin.
- Cocher "Préserver l'ordre des points droits" si vous souhaitez préservez l'ordre initial des points droits.
- Cocher "Couper les sauts de fil",  pour  utiliser des commandes de coupe plutôt que des sauts de fil. Les commandes de coupe sont ajoutées au svg, vous pouvez donc ensuite les modifier/supprimer à votre guise.
   

   

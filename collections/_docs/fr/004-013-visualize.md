---
title: "Simulation"
permalink: /fr/docs/visualize/
excerpt: ""
last_modified_at: 2023-04-18
toc: true
---
## Simulateur/ Aperçu Réaliste

Sélectionnez les objets que vous souhaitez voir dans un aperçu simulé. Si vous souhaitez voir toute votre conception simulée, sélectionnez tout (`Ctrl+A`) ou rien.

Puis faites `Extensions > Ink/Stitch  > Visualiser et Exporter > Simulateur / Aperçu Réaliste`.

![Simulator](/assets/images/docs/en/simulator.jpg)
{: style="border: 2px solid gray; padding: 5px;"}

### Raccourcis pour la Simulation 

Raccourci | Effet
-------- | --------
<key>space</key> | start animation
<key>p</key> | Pause animation
<key>→</key> | Avancer
<key>←</key> | Reculer
<key>↑</key> | Accélérer
<key>↓</key> | Ralentir
<key>+</key> | Une image en avant
<key>-</key> | Une image en arrière
<key>Page down</key> | Jump to previous command
<key>Page up</key> | Jump to next command

C'est aussi possible de **zoomer** et de **déplacer** la simulation avec la souris.

## Simulation du plan de broderie

Lancez `Extensions > Ink/Stitch > Visualiser et Exporter  > Simulation du plan de broderie...`.

Plutôt que d'appliquer le plan de broderie, vous pouvez aussi utilisez l'option Live preview de l'extension. Vous n'aurez alors pas besoin de supprimer le plan de broderie. 
Si vous appliquez le plan de broderie, vous aurez la possibilité de l'inspecter et de la modifier à votre convenance. Utilisez l'extension "Annuler l'aperçu du plan de broderie" si vous souhaitez le supprimer.

Vous disposez des options suivanes:
* **Positionner le plan de broderie hors du canevas** Positionne le plan de broderie  à la droite du canevas. Si la case n'est pas cochée, le plan de broderie sera placé au dessus de vos objets. Dans ce cas vous pouvez choisir de modifier la visibilité de vos objets, soit en les cachant soit en nmodifiant l'opacité.
* **Visibilité du calque de conception** permet de choisir la visibilité du calque originel de conception.
  * **Inchangé** laisse l'opacité du calque de conception telle quelle
  * **Caché** cache le calque de conception
  * **Baisser l'opacité** montre le cache de conception avec une opacité amoindrie
 
* **Points de l'aiguille** si coché, montre les points de l'aiguille
* **Vérouiller** rend le plan de broderie insensible aux interactions de la souris, facilitant le travail sur les objets de broderie quand le plan de broderie est actif.


{% include folder-galleries path="stitch-plan/" captions="1:Stitch plan beside canvas;2:Layer visibility set to hidden;3:Layer visibility set to lower opacity;4:Needle points enabled | disabled" caption="<i>Example image from [OpenClipart](https://openclipart.org/detail/334596)</i>" %}

## Annuler l'aperçu du plan de broderie
Utiliser l'aperçu du plan de broderie au dessus d'objets de broderie cachés ou ayant une opacité amoindrie aide à se faire une idée visuelle de la broderie finale.
Il est parfois utile de garder le plan de broderie de objets déjà présents pour ajouter de nouveaux objets de broderie,mais pour l'export ou pour modifier des éléments existants vous aurez besoin des objets initiaux.
Pas très rigolo de devoir à chaque fois supprimer le calque du plan de broderie et rétablir l'opacité des éléments originels. 
Using a stitch plan overlay with hidden or lower density elements helps to get a visual idea of how the design will look in the end.
Cette extension le fait pour vous et vous aidera si vous utilisez cette méthode de travail.


Lances `Extensions > Ink/Stitch > Visualisr et Exporter > Annuler le plan de broderie`

## Carte de densité

* Sélectionnez des objets si vous ne souhaitez la carte de densité que pour ces objets là, sinon lancez l'extension sans rien sélectionner
* Lancez `Extensions > Ink/Stitch > Visualiser et Exporter > Carte de densité`
* Choisissez les valeurs de densité associées aux couleurs et appliquez
* Inspectez (zoomez)
* Vous pouvez annuler avec `Ctrl + Z`

Ceci montrera des points rouges, jaunes et verts au dessus de vos éléments, pour vous permettre d'identifier facilement les zones à forte densité. Tous les points d'une même couleur sont dans un groupe du calque Densité, ce qui vous permet de masquer facilement tous les points d'une couleur donnée.



## Export PDF

Les informations sur l'export PDF sont dans une autre section: [plus d'info sur l'export PDF](/fr/docs/print-pdf)

---
title: "Simulation"
permalink: /fr/docs/visualize/
last_modified_at: 2026-04-15
toc: true
---
## Simulateur

Sélectionnez les objets que vous souhaitez voir dans un aperçu simulé. Si vous souhaitez voir toute votre conception simulée, sélectionnez tout (`Ctrl+A`) ou rien.

Puis faites `Extensions > Ink/Stitch  > Visualiser et Exporter > Simulateur`.

![Simulator](/assets/images/docs/fr/simulateur.jpg)
{: style="border: 2px solid gray; padding: 5px;"}

### Boutons et raccourcis du simulateur 

Bouton | Effet | Raccourci
-------- | -------- | --------
**Contrôles**||
|<img src="/assets/images/docs/icons/backward_command.png" >|Retourner à la dernière commande| <key>Page down</key>
|<img src="/assets/images/docs/icons/backward_stitch.png" >|Reculer d'un point| <key>←</key>
|<img src="/assets/images/docs/icons/forward_stitch.png" >|Avancer d'un point| <key>→</key>
|<img src="/assets/images/docs/icons/forward_command.png" >|Aller à la prochaine commande| <key>Page up</key> 
|<img src="/assets/images/docs/icons/direction.png" >|Changer le sens de l'animation| 
|<img src="/assets/images/docs/icons/play.png"> | Début/pause de l'animation |<key>space</key> /  <key>p</key>
|<img src="/assets/images/docs/icons/restart.png" >|Redémarrer au début| <key>r</key>
**Vitesse**||
|<img src="/assets/images/docs/icons/slower.png" >|Moins vite| <key>↓</key> 
|<img src="/assets/images/docs/icons/faster.png" >|Plus vite| <key>↑</key> 
**Montrer**||
|<img src="/assets/images/docs/icons/npp.png" >|Points de pénétration de l'aiguille| <key>o</key>
|<img src="/assets/images/docs/icons/jump.png" >|Sauts| 
|<img src="/assets/images/docs/icons/trim.png" >|Coupes| 
|<img src="/assets/images/docs/icons/stop.png" >|Arrêts| 
|<img src="/assets/images/docs/icons/color_change.png" >|Changements de couleur| 
**Info**||
|<img src="/assets/images/docs/icons/info.png" >|Information sur la broderie| 
**Paramètres**||
|<img src="/assets/images/docs/icons/change_background.png" >|Changer la couleur de l'arrière plan| 
|<img src="/assets/images/docs/icons/cursor.png" >|Montrer la position courante de l'aiguille| 
|<img src="/assets/images/docs/icons/page.png" >|Montrer les limites de la page| 
|<img src="/assets/images/docs/icons/settings.png" >|Ouvrir le paramétrage pour choisir la vitesse, l'épaisseur du trait et la taille des points de l'aiguille| 

C'est aussi possible de **zoomer** et de **déplacer** la simulation avec la souris.

## Simulation du plan de broderie {#stitch-plan-preview}
La prévisualisation du plan de broderie insert un plan de broderie sur le canevas. Selon vos réglages, ce plan sera placé au dessus de votre dessin ou sur le coté droit du canevas (option : positionner le plan de broderie hors du canevas)

Pour y accéder faire 
 `Extensions > Ink/Stitch > Visualiser et Exporter > Prévisualisation du plan de broderie...`.

### Options

![Modes de rendu simple et realistes](/assets/images/docs/stitch-plan-preview-modes.jpg)

<i>De gauche à droite: 1. Rendu simple, 2. Rendu simple avec les points de l'aiguille, 3. Rendu réaliste<br>
Source de l'image: [Pixabay](https://pixabay.com/vectors/fox-red-fox-creature-mammal-svg-2530031/)</i>


- **Visibilité du calque de conception** : définit la visibilité du calque de conception du momtif.
  - **Inchangé** : laisse tel quel.
  - **Caché** : masque le motif original.
  - **Baisser l'opacité** : affiche le motif original avec une opacité réduite.
- **Mode de rendu**
  - **Simple** : dessin au trait simple.
  - **Réaliste** : aperçu réaliste au format PNG (8 bits) intégré au canevas.
  - **Réaliste haute qualité** : aperçu réaliste au format PNG (16 bits) intégré au canevas.
  - **Vecteur réaliste (lent)** : rendu vectoriel avec filtres réalistes.

Lent signifie que ce mode peut ralentir Inkscape après le rendu, voire le bloquer.

À utiliser avec précaution pour les motifs complexes et enregistrez votre motif avant de lancer le rendu du plan de broderie.

{: .notice--warning }

- **Positionner le plan de broderie hors du canevas**
  Affiche l'aperçu à droite de la zone de travail. Si cette option est désactivée, le plan de broderie sera placé au-dessus de votre motif.
  Dans ce cas, vous pouvez masquer votre motif ou réduire son opacité.
- **Points de l'aiguille** : affiche les points de pénétration de l'aiguille si cette option est activée.
- **Verrouiller** : rend le plan de broderie insensible aux interactions de la souris (facilite le travail sur le motif principal lorsque le plan de broderie est visible).
- **Montrer les symboles de commande**
- **Montrer les sauts**

- **Ajouter la commande « Ignorer le calque »**
- **Écraser le dernier plan de broderie**

Si cette option est cochée, le nouveau plan de broderie remplacera le précédent. Décochez-la si vous souhaitez conserver le plan de broderie précédent.

### Optimisation du flux de travail avec les raccourcis clavier

Configurez des [raccourcis clavier](/docs/customize/#shortcuts) pour l'aperçu du plan de broderie et l'annulation du plan de broderie (voir ci-dessous) afin d'optimiser votre flux de travail.

* Nous vous recommandons de choisir l'option « Aucune préférence » dans le menu des raccourcis clavier.

L'extension s'exécutera alors directement (sans passer par la fenêtre de paramètres) avec les derniers paramètres appliqués.

* Activez l'option « Verrouiller » pour pouvoir accéder à tous les tracés sans interférence avec les éléments du plan de broderie.
* Assurez-vous que l'option « Remplacer le dernier plan de broderie » est activée, sinon plusieurs plans de broderie s'afficheront sur la zone de travail.

{% include video id="vyTMwLvkkiw4vgwDcTJS6e" provider="diode" %}

{% comment %}
Lancez `Extensions > Ink/Stitch > Visualiser et Exporter  > Simulation du plan de broderie...`.

Plutôt que d'appliquer le plan de broderie, vous pouvez aussi utilisez l'option Live preview de l'extension. 

Vous n'aurez alors pas besoin de supprimer le plan de broderie. 

En revanche,si vous appliquez le plan de broderie, vous aurez la possibilité de l'inspecter et de la modifier à votre convenance. 

Utilisez l'extension "Annuler l'aperçu du plan de broderie" si vous souhaitez le supprimer.

{% endcomment %}

## Annuler l'aperçu du plan de broderie

Utiliser l'aperçu du plan de broderie au dessus d'objets de broderie cachés ou ayant une opacité amoindrie aide à se faire une idée visuelle de la broderie finale.

Il est parfois utile de garder le plan de broderie de objets déjà présents pour ajouter de nouveaux objets de broderie,mais pour l'export ou pour modifier des éléments existants vous aurez besoin des objets initiaux.

Pas très rigolo de devoir à chaque fois supprimer le calque du plan de broderie et rétablir l'opacité des éléments originels. 

Cette extension le fait pour vous et vous aidera si vous utilisez cette méthode de travail.


Lancez `Extensions > Ink/Stitch > Visualiser et Exporter > Annuler le plan de broderie`

## Carte de densité {#density-map}

* Sélectionnez des objets si vous ne souhaitez la carte de densité que pour ces objets là, sinon lancez l'extension sans rien sélectionner
* Lancez `Extensions > Ink/Stitch > Visualiser et Exporter > Carte de densité`
* Choisissez les valeurs de densité associées aux couleurs et appliquez
* Un nouveau calque non brodable est créé
* Inspectez (zoomez)
* Vous pouvez annuler avec `Ctrl + Z`

Ceci montrera des marqueurs rouges, jaunes et verts au dessus de vos éléments, pour vous permettre d'identifier facilement les zones à forte densité. Tous les marqueurs d'une même couleur sont dans un groupe du calque Densité, ce qui vous permet de masquer facilement tous les marqueurs d'une couleur donnée.

### Options

* Marqueurs jaunes et rouges
 Définir à partir de quel nombre de points de l'aiguille dans quel rayon autour  d'un point la coloration est rouge ou jaune

* Visibilité du calque de conception
Définir si Ink/Stitch doit laisser le calque de conception tel quel,le cacher  ou baisser son opacité

* Indicateur de taille
Définir la taille des marqueurs (l'unité est celle du document)

## Afficher l'ordre de broderie {#display-stacking-order}

Lancez `Extensions > Ink/Stitch > Visualiser et Exporter> Afficher l'ordre de broderie...`.

Choisir la taille de la fonte et cliquer sur  Appliquer pour créer un nouveau calque (non brodable) de texte qui numérote les éléments de broderie dans l'ordre de broderie, c'est à dire dans l'ordre  inverse de la  pile d'objets.

![Display stacking order](/assets/images/docs/stacking_order.png)

## Export PDF

Les informations sur l'export PDF sont dans une autre section: [plus d'info sur l'export PDF](/fr/docs/print-pdf)

---
title: "Outils Remplissage"
permalink: /fr/docs/fill-tools/
last_modified_at: 2023-05-01
toc: true
---
## Briser les objets de remplissage

Les objets de remplissage peuvent être traités au mieux s'ils sont des éléments uniques sans bordures qui se croisent. Parfois, ces règles ne sont pas faciles à respecter et votre forme aura de minuscules petites boucles impossibles à découvrir dans Inkscape.

Par conséquent, les messages d'erreur pour les zones de remplissage sont souvent peu parlants et ennuyeux pour les utilisateurs. Cette extension vous aidera à corriger les formes de remplissage défectueuses. Exécutez-la sur toutes les formes de remplissage qui vous causent des problèmes. Elle réparera votre élément de remplissage et séparera les formes avec des bordures croisées en les partageant en plusieurs parties si nécessaire.

### Usage

* Selectionner un remplissage ou plus
* Exécutez: Extensions > Ink/Stitch  > Outils de remplissage > Briser les objets de remplissage
* Pour la plupart des formes `simple` sera suffisant. Si vous avez encore des problèmes essayez `complex`.

### Simple ou Complexe

Toujours préférer simple si c'est possible. Il conserve les trous et répare "bordure se croise" en divisant les boucles en objets séparés ou en les supprimant si elles sont trop petites pour être brodées.

Bien que "simple" divise les boucles, il ne respectera pas les sous-chemins qui se chevauchent. Il les traitera comme des objets séparés. Complexe est capable de reconnaître les chemins qui se chevauchent et de bien les traiter

"Briser les objets de remplissage" peut être traduit dans les fonctions natives d'Inkscape:

 1. Chemin > Union (Résout les problèmes de sous-chemin)
 2. Chemin > Briser (Séparer les objets)
 3. Supprimer les objets trop petits pour être brodés
 4. Chemin > Combiner (si vous voulez maintenir les trous)
 5. Chemin > Combiner (si vous voulez conserver encore plus de trous)

Info: Pour les chemins qui se chevauchent, l'étape 1 n'est effectuée que par complexe.
{: .notice--info}

![Break apart fill objects](/assets/images/docs/en/break_apart.jpg)
[Download SVG](/assets/images/docs/en/break_apart.svg)


## Convertir en blocs de dégradés 

Convertir en blocs de dégradé va découper un remplissage dont la couleur de fond est un dégradé linéaire en plusieurs blocs monochromes avec un espacement de ligne adequat pour rendre l'effet de dégradé.

### Usage

1. Depuis Fond et Contour, appliquez un dégradé linéaire comme couleur de fond à un élement.

   ![linear gradient](/assets/images/docs/en/linear-gradient.png)
   
   Choisir l'angle du dégradé à l'aide de  poignées du dégradé (passer en mode edition de noeud pour les voirs
   
2. Lancez `Extensions > Ink/Stitch > Outils: Remplissage > Convertir en blocs de dégradé

   ![color blocks](/assets/images/docs/color_blocks.png)
   
   Choisir l'espacement final des rangées


## Tartan

{% include upcoming_release.html %}

The Stripe Editor can be found in `Extensions > Ink/Stitch > Tools: Fill > Tartan`

### Customize

#### Positioning

The pattern can be rotated, scaled (%) and translated (mm) as a whole

#### Pattern Settings

* Symmetry: Patterns can be reflected or repeated.
  * A reflected pattern will reverse the stripes every second time (without repeated the pivot point). This means a pattern with three colors (green, black, yellow) will be rendered as follows:
  green, black, yellow, black, green, black, yellow, ...
  * A repeating sett will simply repeat the whole pattern over and over again: green black yellow, green, black, yellow, green, ...

* Equal threadcount for warp and weft
  * if disabled you can define different color setts for warp and weft
  * if enabled warp and weft are the same

#### Stripes

* Add colors with the `Add` button
* Remove colors by clicking on `X` behind a stripe
* Alter stripe positions by click and drag `⁝` (use with care)
* Enable, disable stripe rendering with the checkbox (☑)
* When equal threadcount is disabled: warp defines the vertical lines, weft defines the horizontal lines
* Click on the colored field to select an other color
* When you want to change a color in multiple stripes at once, enable `Link colors` and equal colors will update simultanously

### Palette Code

The Ink/Stitch code is what will be saved into the svg, but can also be edited directly.

A palette code looks for example like this: `(#000000)/5.0 (#FFFFFF)/?5.0`.

* Stripes are separated by spaces
* Each color is encapsulated in round brackets `(#000000)`
* A slash (`/`) indicates a symmetrical/reflective order, whereas three points at the start and end of the code (`...`) represent a asymmetrical/repeating sett `...(#000000)5.0 (#FFFFFF)?5.0...`.
* A pipe (`|`) is a separator for warp and weft and should only be used if they differ in threadcount

**Info**: The [Scottish Register of Tartans](https://www.tartanregister.gov.uk/) has a huge collection of registered tartan patterns. Ink/Stitch is capable to use their code which they send out per mail and convert it into the Ink/Stitch color code. Please respect their particular license regulations. Make sure to define the width of one tartan thread before you click on `Apply Code`.<br><br>Here's an example code you can try out: `...B24 W4 B24 R2 K24 G24 W2...` ([source](https://www.tartanregister.gov.uk/threadcount))
{: .notice--info}

### Embroidery Settings

In the embroidery settings you can decide if you want to render the tartan as a single embroidery element or if you want to receive multiple svg elements which you can edit and transform afterwards to your liking.

#### Embroidery Element

Rendering a tartan as a embroidery element will result in a uniform look with optimal stitch placement. You can set various parameters which can also be refined in the params dialog.

Please refer to the params listed on the [tartan fill page](/docs/stitches/tartan-fill/).

The only param that will only show up here is the `Minimum stripe width for fills`. Stripes smaller than this value will be rendered a running stitch/bean stitch on top of the fill stripes.

#### SVG Elements

* Define a stitch type (Legacy Fill or AutoFill) and choose your prefered stitch settings. Stripes smaller than the `Minimum stripe width for fills` value will turn into strokes (running stitches). Elements can be edited on canvas after clicking on `Apply`.

**Info**: For AutoFill the final routing will be better than shown in the simulator. Hit `Apply` can run the stitch plan to see the final result.
{: .notice--info}


## Tutoriaux utilisant Outils: Remplissage

{% include tutorials/tutorial_list key="tool" value="Fill" %}

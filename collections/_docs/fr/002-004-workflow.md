---
title: "Organisation du travail"
permalink: /fr/docs/workflow/
last_modified_at: 2025-12-29
toc: true
---
![Ink/Stitch workflow](/assets/images/docs/en/workflow-chart.svg)

## ![Create Icon](/assets/images/docs/workflow-icon-create.png) Etape 1: Créer une image vectorielle

Au début, vous avez besoin d’une idée ou d’une image à transférer dans un fichier de broderie. Vous pouvez la dessiner vous même à partir de zéro ou utiliser une image existante.

### Dessiner avec Inkscape

#### Créer des chemins
Inkscape offre des outils variés pour créer des images vectorielles. Vous pouvez, par exemple, utiliser

* ![dessiner des lignes à main levée](/assets/images/docs/inkscape-tools-freehand.png) Lignes à main levée (<key>P</key>)
* ![Courbes de Bézier](/assets/images/docs/inkscape-tools-bezier.png) Courbes de Bézier (<key>B</key>)

Essayez aussi d'autres outils de la barre des outils. Par exemple pour créer des formes spécifiques comme

* ![carré icon](/assets/images/docs/inkscape-tools-square.png) Rectangle
* ![cercle icon](/assets/images/docs/inkscape-tools-circle.png) Cercle
* ![polygone icon](/assets/images/docs/inkscape-tools-polygon.png) Etoile/Polygone
* ![spirale icon](/assets/images/docs/inkscape-tools-spiral.png) Spirale

####  Modifier les chemins
Modifier les objets et les chemins avec:
* ![outil de sélectionicon](/assets/images/docs/inkscape-tools-select.png) Outil de sélection (<key>S</key>) et 
* ![outil noeud icon](/assets/images/docs/inkscape-tools-node.png) Outil d'édition de noeuds (<key>N</key>)

Utilisez l'outil de sélection pour manipuler un objet dans son ensemble que ce soit pour le  mettre à l'échelle, le faire pivoter ou le déplacer. L'éditeur de nœuds lui sert à manipuler une partie seulement d'un objet : un ou des noeuds sélectionnés.

Vous pouvez aussi utiliser les effets de chemin (`Chemin> Effets de chemin`).

### Utiliser une image / un graphique existant

Lorsque vous basez un dessin sur une image ou un graphique existant, chargez-le dans Inkscape dans son propre calque. Certains graphiques sont compatibles avec [la fonction de traçage automatique](https://inkscape.org/fr/doc/tutorials/tracing/tutorial-tracing.html) d'Inkscape (`Chemin > Vectoriser une image matricielle` ou `Shift+Alt+B`), surtout si vous simplifiez d’abord l’image dans un éditeur graphique (par exemple avec [GIMP](https://www.gimp.org/)).

Après le traçage, nettoyez les formes vectorielles en utilisant `Chemin> Simplifier` (`Ctrl + L`) et en supprimant les nœuds à la main lorsque cela est possible. Le but est d’utiliser le moins de courbes de Bézier possible pour représenter l’image. 

Souvent la vectorisation produit des objets très petits qu'il n'est pas possible de broder. En conséquence, pensez à  nettoyer votre document en utilisant `Extensions > Ink/Stitch > Résolution de problèmes > Nettoyer le document`.

Lorsque l’image doit être tracée à la main, utilisez l’outil de dessin à main levée. Cet outil crée des chemins avec beaucoup de noeuds, simplifiez donc autant que possible les courbes.

**Astuce:** Travailler avec une image SVG existante peut vous faire gagner beaucoup de temps. Songez donc à utiliser votre moteur de recherche avec le filtre de recherche d'image défini sur SVG.
{: .notice--info }

### Texte
Ink/Stitch vous offre la possibilité d'utiliser des polices prêtes à broder qui peuvent être inserrées dans votre document via `Extensions > Ink/Stitch > Lettrage`

Si vous souhaitez utiliser une  police non présente dans le lettrage, choisissez la avec soin : il est assez difficile de faire en sorte que le satin soit beau quand il fait 1 mm de large ou moins. 

Les polices sans empattement (sans serif) ont tendance à être les plus faciles à numériser. 

Pour un texte de moins de 4 mm de hauteur, il vous sera très difficile de donner une belle apparence aux lettres minuscules. Par conséquent, envisagez des majuscules. 

Les polices Cursive / Script peuvent bien fonctionner, mais ce ne sera pas aussi facile que vous le pensez.

Ink/Stitch contient des fontes  prêtes à être brodées.

Vous pouvez inserrer ces fontes dans votre document en selectionant **Extensions > Ink/Stitch > Lettrage**. 

Cet outil crée des objects textuels déjà optimisés pour la broderie.



## ![Vectorize](/assets/images/docs/workflow-icon-vectorize.png) Etape 2: Convertir en vecteurs pour la broderie et paramétrer

À ce stade, vous aurez une représentation graphique vectorielle de votre image. La prochaine chose à faire est de convertir vos vecteurs en un type compris par Ink/Stitch.

### Le dialogue Calque et Objets

Nous vous recommandons de faire un usage intensif des calques et des groupes à ce stade.

Dans le panneau Calque et objets (ouvert avec <key>Cmd</key> <key>Shift</key> <key>L</key>), vous pouvez gérer des calques, des groupes et des objets.
Vous pouvez enregistrer l'image d'origine en dupliquant le calque:

* Faites un clic droit sur le calque (si vous n'avez pas renommé le calque, il s'appellera `Calque 1`)
* Cliquez sur `Dupliquer le calque actif`
* Fermez l'oeil en cliquant dessus.

Cela rendra le premier calque invisible. Tout calque, groupe ou forme vectorielle défini comme invisible sera ignoré par Ink/Stitch.

Nous allons maintenant travailler avec la copie.

![Dialogue objet](/assets/images/docs/fr/objects-panel.png)

### Groupes

Utilisez les groupes pour structurer votre document:

* Sélectionnez des objets avec votre souris
* Ajoutez ou supprimez des objets avec <key>shift</key> <key>click</key>
* Appuyez sur <key>Ctrl</key><key>G</key> pour les grouper


Dégrouper des objets fonctionne comme suit:

* Sélectionnez le(s) groupe(s)
* Appuyez sur <key>Ctrl</key><key>Shift</key><key>G</key> pour les dégrouper

### Remarque concernant les types de points

Ink/Stitch prend en charge plusieurs types de points. Les trois principales catégories sont disponibles :

1. **Points de remplissage**

Ces points remplissent une forme fermée. Ils sont utilisés pour les grandes surfaces et créent un effet texturé, tout en assurant une bonne couverture et en préservant la souplesse du tissu.

2. **Traits : points de contour**

Ces points suivent la direction d'un tracé. Ils sont utilisés pour les contours, les lignes fines et les accents décoratifs, lorsqu'une ligne de point étroite est plus appropriée qu'une forme pleine.

3. **Points satin**

Ces points recouvrent les formes étroites avec des points lisses et parallèles. Ils parcourent la forme en va-et-vient, créant un aspect brillant et en relief, idéal pour les bordures, les lettres et les détails fins.

Vous pouvez configurer le comportement des points via **Objet > Fond et contour** ou en appuyant sur <key>Ctrl</key><key>Shift</key><key>F</key>. Consultez le tableau ci-dessous et suivez les liens pour apprendre à configurer correctement chaque type de point.

Regardez ce tableau et suivez les liens pour comprendre comment créer un type de point spécifique:

Objet chemin | Type de point
---|---
Trait en pointillé ou continu|[point droit](/fr/docs/stitches/running-stitch/), [point manuel](/fr/docs/stitches/manual-stitch/) , [point triple](/fr/docs/stitches/bean-stitch/), [point zig-zag](/fr/docs/stitches/zigzag-stitch/), [broderie ondulée](/fr/docs/stitches/ripple/)
Deux traits combinés (avec traverses optionnelles) ou trait simple d'épaisseur supérieure à 0.3mm| [colonne satin](/fr/docs/stitches/satin-column), [point en E](/fr/docs/stitches/e-stitch), [broderie ondulée](/fr/docs/stitches/ripple/)
Chemin fermé avec une couleur de remplissage | [point de remplissage](/fr/docs/stitches/fill-stitch/), [remplissage selon contour](/fr/docs/stitches/contour-fill/), [remplissage guidé](/fr/docs/stitches/guided-fill/),  [remplissage en méandres](/fr/docs/stitches/meander-fill/), [remplissage guidé](/fr/docs/stitches/circular-fill/), [point de croix](/docs/stitches/cross-stitch/)
{: .equal-tables }

### Paramétrer

La boîte de dialogue **Extensions > Ink/Stitch > Params** permet de contrôler la génération des points de broderie par Ink/Stitch pour les objets sélectionnés. Les paramètres varient selon le type de point et incluent des valeurs telles que la longueur, la densité, la sous-couche, la direction et la compensation d'étirement.

Chaque paramètre est accompagné d'une brève description. Des explications plus détaillées sont disponibles dans la section [Paramètres](/fr/docs/params/) de cette documentation. Consultez ces références pour comprendre l'impact des modifications sur la qualité et l'apparence des points.

Lorsque vous modifiez les valeurs des paramètres, Ink/Stitch affiche un aperçu. Cet aperçu vous permet d'évaluer le résultat avant d'appliquer les modifications au motif. Selon la taille et la complexité du fichier, l'affichage de l'aperçu peut prendre un certain temps. Ajustez les valeurs jusqu'à ce que l'aperçu corresponde au résultat souhaité, puis sélectionnez **Appliquer et fermer**. Cette action enregistre les valeurs des paramètres directement dans le fichier SVG.

Une fois les paramètres mis à jour, enregistrez votre fichier SVG. Si Inkscape devient lent ou ne répond plus, fermez-le et rouvrez-le avant de continuer. Le redémarrage peut améliorer les performances lors de projets plus longs ou plus complexes.

## ![Create Icon](/assets/images/docs/workflow-icon-order.png) Etape 3: Ordonner le plan de broderie  & Mettre des commandes

### Ordre de broderie

Lorsque vous concevez des motifs pour des machines à broder qui ne peuvent pas couper le fil au milieu de la broderie ou changer de couleur automatiquement, vous souhaiterez optimiser les chemin de points pour réduire ou masquer les sauts de points et effectuer le minimum de changements de fil. Essayez également d'éviter autant que possible de broder sur les sauts de points, car il est très pénible de les couper à la main quand vous le faites.

L'ordre des points affecte également la façon dont le tissu est étiré et rétréci. Chaque point déformera le tissu et vous devrez en tenir compte et compenser en conséquence. [Pour en savoir plus](/tutorials/push-pull-compensation/)

Une fois que vous avez créé tous les vecteurs, il est temps de tout mettre dans le bon ordre. Optimisez votre ordre pour minimiser les changements de couleur et réduire ou masquer les sauts de points.

Vous pouvez également utiliser la fonction de tri d'Ink/Stitch pour réorganiser les objets selon votre ordre de sélection. Consultez [Réempiler les objets selon l'ordre de sélection](/fr/docs/edit/#re-stack-objects-in-order-of-selection) pour plus de détails.


Ink/Stitch traite les objets dans l'ordre d'apparition dans le panneau des objets, en commençant par le bas de la pile et en remontant. Cet ordre détermine directement la façon dont le motif est brodé sur la machine à broder. Le dernier objet de la liste sera brodé en premier et le premier en dernier.

Lorsque la distance entre deux objets est importante, Ink/Stitch insère automatiquement un point de liaison pour déplacer l'aiguille entre eux. La couleur du fil est déterminée par la couleur de l'objet ; ainsi, un changement de couleur d'un objet à l'autre entraîne un changement de fil dans le fichier de broderie exporté.


Ink/Stitch vous offre plusieurs outils pour vous aider à optimiser l'ordre de broderie :
* La fenêtre 'Calque et objets' vous permet de voir l'ordre des objets dans la pile et de déplacer les objets dans cette pile
* `Extension  > Ink/Stitch > Edition > Reempiler les objets dans l'ordre de leur selection` vous aide à réordonner manuellement des objets
* `Extension  > Ink/Stitch >Outils: Satin >Arrangement automatique de colonnes satins` appliqué après avoir selectionné des colonnes satin, permet un réordonnnement automatique de ces colonnes satin, avec un eventuel ajout de chemins de dessous en point droit pour éviter les sauts de fils
* `Extension  > Ink/Stitch >Outils:Trait >Arrangement automatique de points droits` appliqué après avoir selectionné des points droits permet un réordonnnement automatique de ces point droits, avec un eventuel ajout de chemins de dessous en point droit pour éviter les sauts de fils



**Astuce:** Le menu Objet d'Inkscape vous permet de "monter" et "descendre" des objets dans l'ordre d'empilement, et aussi de monter au premier plan et de descendre à l'arrière plan. Vous pouvez associer des raccourcis à ces éléments de menu [Plus d'Information](/fr/docs/customize/#shortcut-keys)
{: .notice--info }

**Info:** Vous pouvez également modifier manuellement la structure XML SVG sous-jacente à l'aide du dialogue Editeur XML d'Inkscape (`CTRL-SHIFT-X`). Ses boutons "Monter" et "Descendre" agissent directement sur l'ordre des balises XML dans le fichier SVG et ne sont pas soumis aux mêmes limitations que les Page haut et Page bas d'origine. Notez que l'ordre des balises XML dans l'outil XML Editor est l'_inverse_ de l'ordre des objets dans l'outil Objects.
{: .notice--info }

### Commandes
[Commandes](/fr/docs/commands/) aide également à optimiser votre chemin de points. 

Ces outils permettent de définir les points de départ et d'arrivée, de déplacer le cadre à broder et d'ajouter des instructions de coupe. L'utilisation des commandes offre un contrôle plus précis sur la broderie. Elles permettent de définir les points de départ et d'arrivée, de contrôler les coupes, les sauts, les arrêts et les changements de couleur, et de déplacer le cadre à broder. L'utilisation des commandes contribue à réduire sauts de fil visibles, à limiter les coupes manuelles et à améliorer la fluidité générale de la broderie.



## ![Create Icon](/assets/images/docs/workflow-icon-visualize.png)  Etape 4: Visualiser

Ink/Stitch propose trois modes de prévisualisation de votre motif avant exportation :

- [Simulateur ](/fr/docs/visualize/#simulator)

Affiche la broderie étape par étape, avec un effet tissu optionnel.

- [Aperçu avant impression](/fr/docs/print-pdf/)

Crée un aperçu imprimable du motif, utile pour choisir les couleurs, la taille et l’emplacement.

- [Affichage du plan de broderie](/fr/docs/visualize/#stitch-plan-preview)

Affiche l’ordre et les tracés des points directement dans le document. Vous pouvez annuler cet affichage avec **Ctrl+Z**.




## ![Create Icon](/assets/images/docs/workflow-icon-export.png) Etape 5: Enregistrer le fichier broderie

Une fois que tout est dans le bon ordre, lancez  `Fichier > Enregistrer sous...` pour  [exporter](/fr/docs/import-export/) dans un format de fichier supporté par votre machine. La plupart des machines peuvent prendre en charge le format DST et certaines machines Brother préfèrent le PES. 

**N'oubliez pas de sauvegarder également votre fichier au format SVG. Sinon, il sera difficile de changer les détails plus tard.**

## ![Create Icon](/assets/images/docs/workflow-icon-testsew.png) Etape 6: Test de broderie

Il y a toujours place à l'amélioration!

Les tests permettent d'identifier les axes d'amélioration. Préparez un tissu similaire au tissu final. Utilisez le même stabilisateur et le même type de tissu. Pour les t-shirts, choisissez un jersey similaire, car ce type de tissu nécessite une stabilisation importante.

Brodez le motif en observant la machine. Repérez les espaces vides qui pourraient indiquer une déformation du tissu. Vérifiez également les zones où les points sont trop serrés et où la machine peine à coudre. Ces signes indiquent généralement une densité de points trop élevée et signalent la nécessité d'ajustements avant la production finale.


## ![Create Icon](/assets/images/docs/workflow-icon-optimize.png) Etape 7+: Optimisation

Après l'essai, revenez au motif et ajustez les paramètres si nécessaire. Plusieurs itérations sont souvent nécessaires pour obtenir le résultat souhaité, et de petites améliorations peuvent considérablement optimiser la qualité et l'aspect des points.



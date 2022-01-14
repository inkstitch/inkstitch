---
title: "Organisation du travail"
permalink: /fr/docs/workflow/
excerpt: ""
last_modified_at: 2019-10-19
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

Essayer aussi d'autres outils de la barre des outils. Par exemple des formes spécifiques comme

* ![carré icon](/assets/images/docs/inkscape-tools-square.png) Rectangle
* ![cercle icon](/assets/images/docs/inkscape-tools-circle.png) Cercle
* ![polygone icon](/assets/images/docs/inkscape-tools-polygon.png) Etoile/Polygone
* ![spirale icon](/assets/images/docs/inkscape-tools-spiral.png) Spirale

####  Modifier les chemins
Modifier les objets et les chemins avec:
* ![outil de sélectionicon](/assets/images/docs/inkscape-tools-select.png) Outil de sélection (<key>S</key>) and 
* ![outil noeud icon](/assets/images/docs/inkscape-tools-node.png) Outil d'édition de noeuds (<key>N</key>)

Mettez à l'échelle, faites pivoter et déplacez tout l'objet avec l'outil de sélection. L'éditeur de nœuds sert à manipuler les nœuds sélectionnés, etc.
De plus, vous pouvez utiliser les effets de chemin (`Chemin> Effets de chemin`). N'oubliez pas de toujours reconvertir l'objet résultant en un chemin, (`Chemin> Objet en chemin`).

### Utiliser une image / un graphique existant

Lorsque vous basez un dessin sur une image ou un graphique existant, chargez-le dans Inkscape dans son propre calque. Certains graphiques sont compatibles avec [la fonction de traçage automatique](https://inkscape.org/fr/doc/tutorials/tracing/tutorial-tracing.html) d'Inkscape (`Chemin > Vectoriser une image matricielle` ou `Shift+Alt+B`), surtout si vous simplifiez d’abord l’image dans un éditeur graphique (par exemple avec [GIMP](https://www.gimp.org/)).

Après le traçage, nettoyez les formes vectorielles en utilisant `Chemin> Simplifier` (` Ctrl + L`) et en supprimant les nœuds à la main lorsque cela est possible. Le but est d’utiliser le moins de courbes de Bézier possible pour représenter l’image. Souvent la vectorisation va produire des objets très petits qu'il n'est pas possible de broder. En conséquence, il est préférable de nettoyer votre document en utilisant `Extensions > Ink/Stitch > Résolution de problèmes > Nettoyer le document`.

Lorsque l’image doit être tracée à la main, utilisez l’outil de dessin à main levée. Cet outil crée des chemins avec beaucoup de noeuds, simplifiez donc autant que possible les courbes.

**Astuce:** Travailler avec une image SVG existante peut vous faire gagner beaucoup de temps. Songez donc à utiliser votre moteur de recherche avec le filtre de recherche d'image défini sur SVG.
{: .notice--info }

### Texte

Pour le texte, choisissez une police avec soin. Il est assez difficile de faire en sorte que le satin soit beau quand il fait 1mm de large ou moins. Les polices sans empattement (sans serif) ont tendance à être les plus faciles. Pour un texte de moins de 4 mm de hauteur, il vous sera très difficile de donner une belle apparence aux lettres minuscules. Par conséquent, envisagez des majuscules. Les polices Cursive / Script peuvent bien fonctionner, mais ce ne sera pas aussi facile que vous le pensez.

Ink/Stitch vous offre la possibilité d'utiliser des fontes prêtes à broder qui peuvent être inserrées dans votre document via `Extensions > Ink/Stitch > Lettrage`

## ![Vectorize](/assets/images/docs/workflow-icon-vectorize.png) Etape 2: Convertir en vecteur de broderie et paramétrer

À ce stade, vous aurez une représentation graphique vectorielle de votre image. La prochaine chose à faire est de convertir vos vecteurs en un type compris par Ink/Stitch.

### Le dialogue Objets

Nous vous recommandons de faire un usage intensif des calques et des groupes à ce stade.

Dans le panneau des objets (ouvert avec <key>Ctrl</key> <key>Shift</key> <key>O</key>, vous pouvez gérer des calques, des groupes et des objets.
Vous pouvez enregistrer l'image d'origine en dupliquant le calque:

* Faites un clic droit sur le calque (si vous n'avez pas renommé le calque, il s'appellera `Calque 1`)
* Cliquez sur `Dupliquer`
* Fermez l'oeil en cliquant dessus.

Cela rendra le premier calque invisible. Tout calque, groupe ou forme vectorielle défini comme invisible sera ignoré par Ink/Stitch.

Nous allons maintenant travailler avec la copie.

![Dialogue objet](/assets/images/docs/en/objects-panel.png)

### Groupes

Utilisez les groupes pour structurer votre document:

* Sélectionnez des objets avec votre souris
* Ajoutez ou supprimez des objets avec <key>shift</key> <key>click</key>
* Appuyez sur <key>Ctrl</key> <key>G</key>


Dégrouper des objets fonctionne comme suit:

*Sélectionnez le(s) groupe(s)
* Appuyez sur <key>Ctrl</key> <key>Shift</key> <key>G</key>-----


### Types de point

Ink/Stitch propose différents types de points. Selon le type de point que vous souhaitez utiliser, vous devez définir la couleur de remplissage ou les paramètres de trait avec`Objet > Fond et forme...` (<key>Ctrl</key><key>Shift</key><key>F</key>).
Regardez ce tableau et suivez les liens pour comprendre comment créer un type de point spécifique:

Objet chemin | Type de point
---|---|---
Trait(pointillé) |[point droit](/fr/docs/stitches/running-stitch/), [point manuel](/fr/docs/stitches/manual-stitch/), [point zig-zag](/fr/docs/stitches/zigzag-stitch/), [point triple](/fr/docs/stitches/bean-stitch/)
Deux traits combinés (avec traverses optionnelles) | [colonne satin](/fr/docs/stitches/satin-column), [point en E](/fr/docs/stitches/e-stitch)
Chemin fermé avec une couleur de remplissage | [point de remplissage](/fr/docs/stitches/fill-stitch/)
{: .equal-tables }

### Paramétrer

Définir les paramètres en utilisant `Extensions > Ink/Stitch  > Paramètres`. Vous trouvez une description pour chaque paramètre dans la section [Paramètres](/fr/docs/params/) de cette documentation. Chaque fois que vous modifiez les valeurs des paramètres, vous pourrez voir le résultat simulé dans une fenêtre d'aperçu. Une fois que vous êtes satisfait du résultat, cliquez sur `Appliquer et fermer` pour enregistrer les valeurs dans votre fichier SVG.


A ce stade, enregistrez votre fichier SVG. Si Inkscape commence à ralentir (en raison d'une fuite de mémoire Inkscape), redémarrez-le avant de continuer.

## ![Create Icon](/assets/images/docs/workflow-icon-order.png) Etape 3: Ordonner le plan de broderie  & Mettre des commandes

### Ordre de broderie

Lorsque vous concevez des motifs pour des machines à broder qui ne peuvent pas couper le fil au milieu de la broderie ou changer de couleur automatiquement, vous souhaiterez optimiser les chemin de points pour réduire ou masquer les sauts de points et effectuer le minimum de changement de couleur. Essayez également d'éviter autant que possible de broder sur les sauts de points, car il est très pénible de les couper à la main quand vous le faites.

L'ordre des points affecte également la façon dont le tissu est étiré et rétréci. Chaque point déformera le tissu et vous devrez en tenir compte et compenser en conséquence. [Voir plus](/tutorials/push-pull-compensation/)

Une fois que vous avez créé tous les vecteurs, il est temps de tout mettre dans le bon ordre. C'est ici que l'outil Objets d'Inkscapes (`Objets> Objets ...`) est utile. Optimisez votre ordre pour minimiser les changements de couleur et réduire ou masquer les sauts de points.
Vous pouvez aussi utiliser la fonction de tri d'Ink/Stitch.

Ink/Stitch brodera les objets dans l'ordre exact dans lequel ils apparaissent dans votre document SVG, du plus bas au plus élevé dans l'ordre d'empilement. Si la distance entre deux objets est longue, Ink/Stitch ajoutera automatiquement un point de saut entre eux. Il utilise la couleur de l'objet pour déterminer la couleur du fil. Par conséquent, si vous changez de couleur d'un objet à l'autre, une instruction de changement de fil sera ajoutée au fichier de sortie de la broderie.

**Astuce:** Inkscape vous permet de "monter" et "descendre" des objets dans l'ordre d'empilement à l'aide des touches Page haut et Page bas. Les nouvelles fonctions "Monter" et "Descendre" vous donneront un bien meilleur contrôle de l'ordre d'empilement. Nous recommandons donc de leur lier Page haut et Page bas. [Plus d'Information](/fr/docs/customize/#shortcut-keys)
{: .notice--info }

**Info:** Vous pouvez également modifier manuellement la structure XML SVG sous-jacente à l'aide du dialogue Editeur XML d'Inkscape (`CTRL-SHIFT-X`). Ses boutons "Monter" et "Descendre" agissent directement sur l'ordre des balises XML dans le fichier SVG et ne sont pas soumis aux mêmes limitations que les Page haut et Page bas d'origine. Notez que l'ordre des balises XML dans l'outil XML Editor est l'_inverse_ de l'ordre des objets dans l'outil Objects.
{: .notice--info }

### Commandes
[Commandes](/fr/docs/commands/) aide également à optimiser votre chemin de point. Vous pouvez définir les points de début et de fin, déplacer le cadre dans des positions définies ou définir les commandes de coupe, etc.

## ![Create Icon](/assets/images/docs/workflow-icon-visualize.png)  Etape 4: Visualiser

Ink/Stitch prend en charge trois façons de prévisualiser votre conception:

* [Simulateur](/fr/docs/simulate/)
* [Aperçu d'impression](/fr/docs/print/)
* [Affichage du plan de broderie](/fr/docs/import-export/#method-2-display-stitch-plan) (Undo with <key>Ctrl</key><key>Z</key>)

## ![Create Icon](/assets/images/docs/workflow-icon-export.png) Etape 5: Enregistrer le fichier broderie

Une fois que tout est dans le bon ordre, lancez  `Fichier > Enregistrer sous...` pour  [exporter](/fr/docs/import-export/) dans un format de fichier supporté par votre machine. La plupart des machines peuvent prendre en charge le format DST et certaines machines Brother préfèrent le PES. N'oubliez pas de sauvegarder également votre fichier au format SVG. Sinon, il sera difficile de changer les détails plus tard.

## ![Create Icon](/assets/images/docs/workflow-icon-testsew.png) Etape 6: Test de broderie

Il y a toujours place à l'amélioration! Pour tester votre conception, préparez un morceau de tissu qui correspond le mieux à votre tissu final. Utilisez le même stabilisateur et le même tissu, si possible. Pour les t-shirts, essayez de trouver un tissu similaire (généralement tricoté). Ces tissus ont besoin de beaucoup de stabilisation.
Brodez le motif en regardant la machine pour vous assurer qu'il n'y a pas de surprises. Faites attention aux espaces entre des zones qui indiquent que le tissu a été déformé. Recherchez également les zones où les points se superposent trop et où la machine a du mal à coudre, ce qui indique que la densité de points est trop élevée.
## ![Create Icon](/assets/images/docs/workflow-icon-optimize.png) Etape 7+: Optimisation

Revenez ensuite et ajustez votre motif. Espérons que cela ne prendra que quelques essais pour l'obtenir comme vous le souhaitez. Une fois que vous avez terminé, copiez le fichier de broderie final à partir de votre répertoire de sortie afin d'éviter tout écrasement accidentel à l'avenir.

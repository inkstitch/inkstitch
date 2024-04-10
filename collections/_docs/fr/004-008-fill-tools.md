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
L'éditeur de bandes du tartan se trouve dans   `Extensions > Ink/Stitch > Outils: remplissage > Tartan`
### Personnaliser

#### Positionnement

Le motif dans son ensemble peut être tourné, mis à l'échelle (%) et translaté (mm).

#### Paramètrage du motif

* Symmetrie:  Les motifs peuvent être soit réfléchis soit répétés.
  * Un motif réfléchi verra l'ordre de ses bandes inversé d'une fois sur l'autre (sans répétion des bandes pivots). Ceci signifie qu'un motif à trois couleurs (vert, noir, jaune) sera rendu de la manière suivante :
    vert, noir, jaune, noir, vert, noir, jaune,....
  * Un motif répété repète simplement toujours le même motif : vert, noir, jaune, vert, noir, jaune, vert, noir, jaune,...

* Même nombre de fils pour la chaine et la trame
  *  si désactivé, vous pouvez définir deux motifs différents, l'un pour la chaîne, l'autre pour la trame
  *  si activé, chaîne et trame suivent le même motif
 
    
#### Bandes

* Ajouter des couleurs avec le bouton "Ajouter"
* Supprimer des couleurs en cliquant sur le  X à droite de la couleur
* Modifier l'ordre des bandes en glissant deposant  `⁝` (à utiliser avec beaucoup de précautions)
* Autoriser ou non le rendu d'une bande avec la case à cocher (☑)
* Lorsque "Même nombre de fils pour la chaîne et la trame" est désactivé : la chaîne définit les lignes verticales, la trame définit les lignes horizontales
* Cliquez sur le champ coloré pour sélectionner une autre couleur
* Lorsque vous souhaitez modifier une couleur dans plusieurs bandes à la fois, activez « Lier les couleurs » et les couleurs identiques seront mises à jour simultanément.
  
### Code de Palette 
Ce code de palette est ce que Ink/Stitch sauvegarde dans le svg, mais peut aussi être édité directement.

Un code de palette peut ressembler à ceci : `(#000000)/5.0 (#FFFFFF)/5.0`.

* Les bandes sont séparées par des espaces
* Chaque couleur est entourée par des parenthèses `(#000000)`
* Une barre oblique (`/`) indique un motif symétrique/réfléchi, alors que trois points au début et à la fin du code (`...`) représentent un motif asymétrique/répété `...(#000000)5.0 (# FFFFFF)5.0...`.
* Un pipe (`|`) est un séparateur pour la chaîne et la trame et ne doit être utilisé que s'ils ne suivent pas le même motif.
* Une bande desactivé se traduit par un '?'

**Info**:Le [Scottish Register of Tartans](https://www.tartanregister.gov.uk/) possède une vaste collection de motifs de tartan enregistrés. Ink/Stitch est capable d'utiliser leur code qu'ils envoient par courrier et de le convertir en code couleur Ink/Stitch. Veuillez respecter leurs réglementations particulières en matière de licence. Assurez-vous de définir la largeur d'un fil tartan avant de cliquer sur `Appliquer le code`.<br><br>Voici un exemple de code que vous pouvez essayer : `...B24 W4 B24 R2 K24 G24 W2...` ( [source](https://www.tartanregister.gov.uk/threadcount)) 
{: .notice--info}

### Paramètres de broderie

Dans les paramètres de broderie, vous pouvez décider si vous souhaitez rendre le tartan comme un seul élément de broderie ou si vous souhaitez recevoir plusieurs éléments svg que vous pourrez ensuite modifier et transformer à votre guise.

####  Elément de broderie

Le rendu d'un tartan comme élément de broderie se traduira par un aspect uniforme avec un placement de point optimal. Vous pouvez définir divers paramètres qui peuvent également être affinés dans la boîte de dialogue des paramètres.

Veuillez vous référer aux paramètres répertoriés sur la [page de remplissage tartan](/fr/docs/stitches/tartan-fill/).

Le seul paramètre qui n'apparaîtra qu'ici est la « Largeur minimale de bande pour les remplissages ». Les bandes plus étroites que cette valeur seront rendues en point droit/point multiple au-dessus des rayures de remplissage.

#### Éléments SVG

* Définissez un type de point (Legacy Fill ou Remplissage automatique) et choisissez vos paramètres de point préférés. Les bandes plus étroites que la valeur « Largeur de bande minimale pour les remplissages » se transformeront en traits (points droits ou multiples). Les éléments peuvent être modifiés sur le canevas après avoir cliqué sur « Appliquer ».

**Info** : Pour Remplissage automatique, le routage final sera meilleur que celui affiché dans le simulateur. Appuyez sur « Appliquer » pour exécuter le plan de points pour voir le résultat final.

{: .notice--info}


## Tutoriaux utilisant Outils: Remplissage

{% include tutorials/tutorial_list key="tool" value="Fill" %}

---
title: "Outils Remplissage"
permalink: /fr/docs/fill-tools/
last_modified_at: 2025-05-26
toc: true
---
## Briser les objets de remplissage {#break-apart-fill-objects}

Les objets de remplissage peuvent être traités au mieux s'ils sont des éléments uniques sans bordures qui se croisent. Parfois, ces règles ne sont pas faciles à respecter et votre forme aura de minuscules petites boucles impossibles à découvrir dans Inkscape.

Par conséquent, les messages d'erreur pour les zones de remplissage sont souvent peu parlants et ennuyeux pour les utilisateurs. Cette extension vous aidera à corriger les formes de remplissage défectueuses. Exécutez-la sur toutes les formes de remplissage qui vous causent des problèmes. Elle réparera votre élément de remplissage et séparera les formes avec des bordures croisées en les partageant en plusieurs parties si nécessaire.

### Usage

* Sélectionner un remplissage ou plus
* Exécutez: Extensions > Ink/Stitch > Outils de remplissage > Briser les objets de remplissage
* Pour la plupart des formes `simple` sera suffisant. Si vous avez encore des problèmes essayez `complexe`.

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

## Convertir en blocs de dégradés {#convert-to-gradient-blocks}

Convertir en blocs de dégradé va découper un remplissage dont la couleur de fond est un dégradé linéaire en plusieurs blocs monochromes avec un espacement de ligne adéquat pour rendre l'effet de dégradé.

### Usage

1. Depuis Fond et Contour, appliquez un dégradé linéaire comme couleur de fond à un élement.

 ![linear gradient](/assets/images/docs/en/linear-gradient.png)

 Choisir l'angle du dégradé à l'aide de poignées du dégradé (passer en mode édition de nœud pour les voir

2. Lancez `Extensions > Ink/Stitch > Outils: Remplissage > Convertir en blocs de dégradé

 ![color blocks](/assets/images/docs/color_blocks.png)

 Choisir l'espacement final des rangées

## Assise de points couchants à partir de la sélection {#knockdown-fill}

Cette extension permet de générer:

* soit une zone de remplissage sous tous les éléments sélectionnés, avec un décalage positif ou négatif. Cette méthode peut s'avérer très utile pour travailler avec des tissus à poils longs (généralement avec un décalage positif) ou pour créer une sous-couche globale (généralement avec un décalage négatif).
* soit une zone de remplissage en forme de cercle ou de rectangle autour  des éléments sélectionnés (mais pas sous eux). Ceci peut être utile pour créer un effet d'embossage avec des tissus à poils longs.

![A figure with a surrounding knockdown stitch](/assets/images/docs/knockdown.png)

* Sélectionner des éléments
* Ouvrir `Extensions > Ink/Stitch > Outils : Remplissage > Sélection vers remplissage en points couchants` 
* Adapter les paramètres (la longueur maxiumum du point détermine aussi l'espacement entre les rangées)
* Cliquer sur `Appliquer`
* Adaptez les paramètres de remplissage dans la boîte de dialogue du paramétrage (`Extensions > Ink/Stitch > Paramètres`)

 
### Paramètres

#### Onglet Options

* Conserver les trous : Choisissez si la forme doit contenir des trous.
* Décalage : Décalage (mm) autour de la sélection. Ce décalage peut être positif ou négatif.
* Méthode (arrondi, onglet, biseau) : Modifie l'aspect des bords.
* Limite d'onglet : Modifie l'aspect des bords.

#### Onglet Embossage

* Forme : Si la  valeur choisie est "Aucune", l'extension crée une zone de remplissage sous les éléments sélectionnés, en tenant compte de la valeur de décalage (de l'onglet Options). Si vous souhaitez un effet d'embossage, choisissez entre rectangle et cercle pour créer un remplissage autour des éléments sélectionnés, en excluant la zone située sous les éléments sélectionnés (en tenant toujours compte du décalage).
* Décalage de la forme : Toute valeur positive étend la zone d'embossage. La zone exclue peut être modifiée à l'aide du paramètre de décalage dans l'onglet Options.
* Méthode (arrondi, biseau, onglet) : influence l'aspect des bords.

Remarque : si l'on choisit une forme d'embossage  (cercle ou rectangle), la zone exclue correspond exactement à la forme du remplissage avec la forme définie sur Aucune. Si le décalage de forme est nul, le bord extérieur de l'embossage correspond au plus petit cercle/rectangle contenant la zone exclue. Si le décalage de forme est positif, le bord extérieur du cercle/rectangle est étendu dans toutes les directions selon cette valeur. La zone exclue reste inchangée.

## Tartan

L'éditeur de bandes du tartan se trouve dans `Extensions > Ink/Stitch > Outils: remplissage > Tartan`

![A seahorse rendered with tartan fill](/assets/images/docs/fr/tartan_stripe_editor.png)

### Personnaliser

#### Positionnement

Le motif dans son ensemble peut être tourné, mis à l'échelle (%) et translaté (mm).

#### Paramétrage du motif

* Symétrie: Les motifs peuvent être soit réfléchis soit répétés.
 * Un motif réfléchi verra l'ordre de ses bandes inversé d'une fois sur l'autre (sans répétition des bandes pivots). Ceci signifie qu'un motif à trois couleurs (vert, noir, jaune) sera rendu de la manière suivante :
 vert, noir, jaune, noir, vert, noir, jaune,....
 * Un motif répété répète simplement toujours le même motif : vert, noir, jaune, vert, noir, jaune, vert, noir, jaune,...

* Même nombre de fils pour la chaine et la trame
 * si désactivé, vous pouvez définir deux motifs différents, l'un pour la chaîne, l'autre pour la trame
 * si activé, chaîne et trame suivent le même motif

#### Bandes

* Ajouter des couleurs avec le bouton "Ajouter"
* Supprimer des couleurs en cliquant sur le X à droite de la couleur
* Modifier l'ordre des bandes en glissant déposant `⁝` (à utiliser avec beaucoup de précautions)
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
* Une bande désactivée se traduit par un '?'

**Info**:Le [Scottish Register of Tartans](https://www.tartanregister.gov.uk/) possède une vaste collection de motifs de tartan enregistrés. Ink/Stitch est capable d'utiliser leur code qu'ils envoient par courrier et de le convertir en code couleur Ink/Stitch. Veuillez respecter leurs réglementations particulières en matière de licence. Assurez-vous de définir la largeur d'un fil tartan avant de cliquer sur `Appliquer le code`.<br><br>Voici un exemple de code que vous pouvez essayer : `...B24 W4 B24 R2 K24 G24 W2...` ( [source](https://www.tartanregister.gov.uk/threadcount)) 
{: .notice--info}

### Paramètres de broderie

Dans les paramètres de broderie, vous pouvez décider si vous souhaitez rendre le tartan comme un seul élément de broderie ou si vous souhaitez recevoir plusieurs éléments svg que vous pourrez ensuite modifier et transformer à votre guise.

#### Éléments de broderie

Le rendu d'un tartan comme éléments de broderie se traduira par un aspect uniforme avec un placement de point optimal. Vous pouvez définir divers paramètres qui peuvent également être affinés dans la boîte de dialogue des paramètres.

Veuillez vous référer aux paramètres répertoriés sur la [page de remplissage tartan](/fr/docs/stitches/tartan-fill/).

Le seul paramètre qui n'apparaîtra qu'ici est la « Largeur minimale de bande pour les remplissages ». Les bandes plus étroites que cette valeur seront rendues en point droit/point multiple au-dessus des rayures de remplissage.

#### Éléments SVG

* Définissez un type de point (Legacy Fill ou Remplissage automatique) et choisissez vos paramètres de point préférés. Les bandes plus étroites que la valeur « Largeur de bande minimale pour les remplissages » se transformeront en traits (points droits ou multiples). Les éléments peuvent être modifiés sur le canevas après avoir cliqué sur « Appliquer ».

**Info** : Pour Remplissage automatique, le routage final sera meilleur que celui affiché dans le simulateur. Appuyez sur « Appliquer » pour exécuter le plan de points pour voir le résultat final.

{: .notice--info}

## Tutoriels utilisant Outils: Remplissage

{% include tutorials/tutorial_list key="tool" value="Fill" %}

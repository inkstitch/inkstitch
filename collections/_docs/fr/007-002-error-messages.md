---
title: "Messages d'erreur"
permalink: /fr/docs/error-messages/
last_modified_at: 2019-10-25
toc: true
classes: equal-tables
---

## Broder

Message d'erreur|Description
---|---
Seeing a 'no such option' message?<br />Please restart Inkscape to fix.|
No embroiderable paths selected.<br />Tip: use Path -> Object to Path to convert non-paths before embroidering.|Ink / Stitch ignore tous les objets non-chemin. Convertir votre forme en un chemin résoudra le problème (`Ctrl+Shift+C`).
No embroiderable paths found in document.<br />Tip: use Path -> Object to Path to convert non-paths before embroidering.|Ink / Stitch ignorera tous les objets non-chemin. Convertir votre forme en un chemin résoudra le problème: sélectionnez tous les objets avec `Ctrl+A` et taper `Ctrl+Shift+C` pour les convertir.

## Fils

Error Message|Description
---|---
Thread palette installation failed|L'installation de palette de fils à échoué
Installation Failed|

## Paramètres

Message d'erreur|Description
---|---
Some settings had different values across objects.  Select a value from the dropdown or enter a new one.|Certains paramètres ont des valeurs différentes selon les objets. Sélectionnez une valeur dans la liste déroulante ou entrez-en une nouvelle.
Preset "%s" not found.|Le préréglage avec le nom donné n’existe pas. Affichez une liste de tous les préréglages disponibles en cliquant sur la flèche en regard du champ de saisie.
Preset "%s" already exists.<br />Please use another name or press "Overwrite"|Vous ne pouvez pas `Ajouter` des préréglages avec le même nom. Si vous souhaitez conserver les anciens paramètres prédéfinis, modifiez le nom - sinon, utilisez `Overwrite`.
No embroiderable paths selected.<br />Tip: use Path -> Object to Path to convert non-paths before embroidering.|Ink/Stitch ignorera tous les objets non-chemin. Convertir votre forme en un chemin résoudra le problème.
No embroiderable paths found in document.<br />Tip: use Path -> Object to Path to convert non-paths before embroidering.|Ink/Stitch ignorera tous les objets non-chemin. Convertir votre forme en un chemin résoudra le problème.

## Unités

Message d'erreur|Description
---|---
parseLengthWithUnits: unknown unit %s|
Unknown unit: %s|

## Simulation

Message d'erreur|Description
---|---
No embroiderable paths selected.<br />Tip: use Path -> Object to Path to convert non-paths before embroidering.|Ink/Stitch ignorera tous les objets non-chemin. Convertir votre forme en un chemin résoudra le problème.
No embroiderable paths found in document.<br />Tip: use Path -> Object to Path to convert non-paths before embroidering.|Ink/Stitch ignorera tous les objets non-chemin. Convertir votre forme en un chemin résoudra le problème.

## Colonne Satin

Message d'erreur|Description
---|---
One or more rails crosses itself, and this is not allowed.<br />Please split into multiple satin columns.|Avec l'*outil édition de noeud* sélectionnez un nœud à la position où vous souhaitez diviser votre chemin. Cliquer sur `Briser le chemin aux noeuds sélectionnés` dans la *Barre de contôle des outils*.<br /><br />![Split Path](/assets/images/docs/en/split-path.jpg)<br />Tapez `Ctrl+Shift+K` séparer toutes les pièces. Recombinez les rails et les barreaux sélectionnés avec `Ctrl+K`. Appliquez ensuite les réglages de paramétrage aux deux colonnes satin séparées. 
satin column: One or more of the rungs doesn't intersect both rails.|Assurez-vous que les traverses de direction coupent les deux rails.<br />[plus d'information](/fr/docs/stitches/satin-column/#méthode-des-traverses)
Each rail should intersect both rungs once.|Assurez-vous que les traverses de direction coupent les deux rails..<br />[Plus d'information](/fr/docs/stitches/satin-column/#méthode-des-traverses)
satin column: One or more of the rungs intersects the rails more than once.|Assurez-vous que les traverses de direction coupent les deux rails. Si c'est déjà le cas et que vous recevez toujours ce message, une ou plusieurs traverses peuvent être plus longues que les rails. Dans ce cas, vous devriez envisager d'utiliser la [méthode des noeuds](/fr/docs/stitches/satin-column/#méthode-des-noeuds) ou de prolonger les rails.
satin column: object %s has a fill (but should not)|Supprimez la couleur de remplissage de l'objet:<br />`Objet > Fond et contour...` La boîte de dialogue apparaîtra à droite. Cliquez sur le X dans l'onglet de remplissage.
satin column: object %(id)s has two paths with an unequal number of points (%(length1)d and %(length2)d)|Si vous recevez ce message, vous devriez envisager d’utiliser les avantages de la [méthode des traverses](/fr/docs/stitches/satin-column/#méthode-des-traverses),ce qui permet une quantité inégale de nœuds. Sinon, vérifiez s'il y a des doublons sur chaque nœud et comptez tous les nœuds sur chaque chemin.

## Traits

Message d'erreur|Description
---|---
Legacy running stitch setting detected!<br />It looks like you're using a stroke smaller than 0.5 units to indicate a running stitch, which is deprecated.  Instead, please set your stroke to be dashed to indicate running stitch.  Any kind of dash will work.|Plus d'informations sur [mode point droit](/fr/docs/stitches/running-stitch/)

## Auto-remplissage

Message d'erreur|Description
---|---
Unable to autofill.<br />This most often happens because your shape is made up of multiple sections that aren't connected.|[Remplissage](/fr/docs/stitches/fill-stitch/) doit être affecté à des chemins fermés avec une couleur de remplissage, mais il semble y avoir au moins deux lacunes dans votre forme.<br />Pour savoir où votre chemin n’est pas connecté, sélectionnez un nœud avec l’outil de modification de nœud et appuyez sur`Ctrl+A`. Il sélectionnera tous les nœuds connectés et les lacunes deviendront évidentes à l’endroit où la sélection se termine.
Unexpected error while generating fill stitches. Please send your SVG file to lexelby@github.|Ce message d'erreur indique que vous avez découvert un bug inconnu. Merci de nous faire un rapport pour aider Ink/Stitch à s'améliorer.

## Imprimer

Message d'erreur|Description
---|---
No embroiderable paths found in document.<br />Tip: use Path -> Object to Path to convert non-paths before embroidering.|Ink/Stitch ignorera tous les objets non-chemin. Convertir votre forme en un chemin résoudra le problème.
⚠ lost connection to Ink/Stitch.|Le navigateur a perdu la connexion à Ink/Stitch. Vous pourrez toujours imprimer et appliquer des modifications au document, mais toutes les modifications seront perdues lors de la prochaine ouverture de l'aperçu avant impression.

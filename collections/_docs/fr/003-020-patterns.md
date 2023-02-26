---
title: "Textures"
permalink: /fr/docs/stitches/patterns/
excerpt: ""
last_modified_at: 2022-01-18
toc: true
---
Il est possible de créer des textures en forçant la position de certains points.

![Pattern](/assets/images/docs/stitch-type-pattern.png)

[Télécharger un fichier d'exemple](/assets/images/docs/pattern.svg)

## Générer des textures 
Dans Ink/Stitch il est possible de générer des textures en ajoutant ou en supprimant des points à un élément de broderie existant.


1. **Créez un ou des élément(s) de broderie** Ces éléments peuvent être des remplissages ou des colonnes satin.  Les textures vont aussi fonctionner sur des traits, mais ce n'est peut-être pas la meilleure option....

2. **Créez un ou des élément(s) de texture.** Une texture est consitutée de trait et/ou d'aires de remplissage. Les traits seront utilisés pour ajouter des points aux éléments de broderie  tandis que les remplissages serviront à supprimer des points des éléments de broderie

3. Sélectionnez à la fois les éléments de broderie et les éléments de textures, faire  `Ctrl+G` pour **grouper le tout**.

4. **Convertissez en texture.** Sélectionnez uniquement les éléments de texture et exécutez  `Extensions > Ink/Stitch > Edition > Selection vers texture`. Ceci ajoutera un marqueur au début de l'élément de texture pour indiquer qu'il ne sera pas brodé mais qu'il sera utilisé comme élément de texture pour tous les éléments de son groupe. Des éléments appartenant à des sous-groupe de ce même groupe ne seront pas affectés.

   ![Pattern groups](/assets/images/docs/en/pattern.png)

## Supprimer le marqueur de texture

Le marqueur de texture peut être supprimé dans le panneau "Fond et Contour" (`Ctrl+Shift+F`). Ouvrez l'onglet "Style de contour" et choisissez la toute premiere option (vide) dans le premier menu déroulant. Après suppression du marqueur, le chemin n'est plus une texture, mais un chemin ordinaire.

![Remove pattern](/assets/images/docs/fr/stitch-type-remove-pattern.png)

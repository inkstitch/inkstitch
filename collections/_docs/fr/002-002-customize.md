---
title: "Personnaliser Ink/Stitch"
permalink: /fr/docs/customize/
last_modified_at: 2026-01-06
toc: true
---
## Raccourcis Clavier

Vous pouvez accelerer votre travail sous Ink/Stitch en utilisant des raccourcis clavier.

La liste suivante décrit les raccourcis claviers qui sont définis dans le fichier à télécharger ci-dessous.

Certains de ces raccourcis remplacent des raccourcis natifs d'Inkscape. Dans le tableau ci dessous vous pouvez voir quels sont ces raccourcis et  comment continuer à acceder à ces fonctions.
{: .notice--warning }

Raccourcis&nbsp;Clavier | Effet | Remplace
-------- | --------| --------
<key>Page Haut</key>                          | Monter dans la pile d'objets* | Objet > Monter (voir aussi les boutons de la barre d'outils)
<key>Page Pas </key>                          | Descendre dans la pile d'objets* | Objet > Descendre (voir aussi les boutons de la barre d'outils)
<key>ctrl</key>+<key>R</key>                  | Renverser la direction d'un chemin.**
<key>ctrl</key>+<key>shift</key>+<key>P</key> | Paramètres | Edition > Préférences
<key>ctrl</key>+<key>shift</key>+<key>L</key> | Simulateur en direct
<key>ctrl</key>+<key>shift</key>+<key>/</key> | Prévisualisation du plan de broderie  | Chemin > Division (use Strg+/ instead)
<key>ctrl</key>+<key>shift</key>+<key>O</key> | Briser des objets de remplissage... (O  pour Objet) | Objet > Propriétés de l'objet
<key>ctrl</key>+<key>shift</key>+<key>I</key> | Export PDF 
<key>ctrl</key>+<key>shift</key>+<key>Q</key> | Lettrage (Q pour QWERTY) | Objet > Selecteurs et CSS
<span style="white-space: nowrap;"><key>ctrl</key>+<key>shift</key>+<key>Del</key></span> | Dépistage de problèmes avec les objets
<key>ctrl</key>+<key>shift</key>+<key>+</key> | Attacher des commandes aux objets selectionnés
<key>ctrl</key>+<key>shift</key>+<key>U</key> | Trait en satin  (U ressemble à deux rails) | Objet > Grouper (utiliser Ctrl+G à la place)
<key>ctrl</key>+<key>shift</key>+<key>J</key> | Intervertir les rails satin  (J ressemble à une flèche)
<key>ctrl</key>+<key>shift</key>+<key>B</key> | Scinder colonne satin  (B est coupé en deux parties) | Chemin > Union (utiliser Ctrl++ à la place )
<key>ctrl</key>+<key>shift</key>+<key>*</key> | Agencement automatique de colonnes satin (ordonne tout)

\* Monter et Descendre dans la pile d'objets permet de contrôler précisement l'ordre dans lequel les objets sont brodés. Très utile en combinaison avec le panneau Calques et Objets (`Objet > Calques et Objets`).  L'ordre de la pile défini l'ordre dans lequel les éléments sont brodés (le bas de la pile en premier, pour finir par le haut de la pile).<br><br>** Pour les colonnes satin et les points droits, ceci change la direction des points. A utiliser avec `Afficher le sens des chemins sur le contour` selectionné dans `Edition > Préférences > Outils > Noeuds`. Si vous selectionnez un seul sommet en utilisant l'éditeur de noeuds et que vous effectuez un `Ctrl+R`, Inkscape ne renverse que le sous-chemin qui contient ce noeud. Vous pouvez de cette manière vous assurer que les deux rails d'une colonne satin sont orientés dans le même sens.
{: .notice--info }
{: style="font-size: 70%" }

### Télécharger et importer des raccourcis clavier

* [Téléchargez le fichier de raccourcis clavier](/assets/files/inkstitch.xml){: download="inkstitch.xml" }
* Allez à  `Edition > Préférences > Interface > Clavier`
* Cliquez sur  `Importer...`
* Sélectionnez votre fichier de raccourcis (inkstitch.xml)
* Cliquez sur ouvrir 

Vous pouvez maintenant utiliser les raccourcis claviers décrits ci dessus.

Si vous voulez définir vos propres raccourcis, entrez simplement la combinaison de touches dans le dialogue de raccourci.
Utiliser la fonction de recherche pour trouver les extensions plus rapidement. [Plus d'informations](http://wiki.inkscape.org/wiki/index.php/Customizing_Inkscape)
{: .notice--info }


## Correction du facteur de zoom

Pour broder il est essentiel d'avoir une bonne idée de la véritable taille du dessin. Inkscape a un réglage pour adapter le niveau de zoom à votre écran:

* Allez à `Edition > Préférences > Interface`
* Tenez une régle sur votre ecran et ajuster le curseur jusqu'à ce que les longueurs correspondent.
 
![Correction de zoom](/assets/images/docs/fr/customize-zoom-correction.png)

## Grilles

Pour aligner correctement vos formes vectorielles, vous pouvez utiliser la fonctionnalité de grille d’Inkscape. Aller à  `Affichage` et activer  la `Grille`. N'oubliez pas d'activer le magnetisme (en haut à droite) et  vérifiez que `Aimanter aux grilles` est activé. Il est également possible de régler l'espacement et l'origine de vos grilles dans `Fichier> Propriétés du document> Grilles`.

![Grids](/assets/images/docs/fr/grille.png)

## Activation de la direction des chemins

Il est important de connaître les directions de chemin en travaillant avec Ink/Stitch. Par conséquent, nous vous recommandons d'activer les cases à cocher **Afficher la direction du chemin sur les contours** et **Afficher le contour temporaire pour les chemins sélectionnés** dans `Édition > Préférences > Outils > Noeuds`.

Vérifier aussi que **Afficher le contour du chemin** est activé dans la  `Barre de contrôle de l'outil noeud` comme dans l'image ci-dessous
[![Path outlines & directions](/assets/images/docs/fr/contour.png)

## Travailler avec des modèles

Si vous décidez d'utiliser plus fréquemment Ink/Stitch pour vos travaux de broderie, vous en aurez peut-être assez de mettre tout en scène à chaque fois. Dans ce cas, vous êtes prêt à créer un modèle pour votre configuration de broderie de base. Une fois que vous avez tout organisé comme vous le souhaitez, sauvegardez simplement votre fichier dans votre repertoire de modèles  (`Fichiers > Enregistrer un modèle...`). Vous pouvez maintenant accéder à ce modèle par `Fichier > Nouveau à partir d'un modèle  > Personnalisé `.

Si vous utilisez Inkscape principalement pour la broderie, vous pouvez cocher l'option  `définir comme modèle par défaut` lors de l'enregistrement du modèle.

**Astuce:** Obtenez des [modèles prédéfinis](/fr/tutorials/resources/templates/) dans notre section tutoriel.
{: .notice--info }

## Installer des palettes de fils 

Ink/Stitch est livré avec de nombreuses palettes de couleurs de fils des fabricants qui peuvent être installées dans Inkscape. Cela permet de créer les designs en gardant à l’esprit les bonnes couleurs.
Les couleurs apparaîtront dans la sortie PDF et seront également incluses dans votre fichier de broderie, si votre format de fichier le prend en charge.

[En savoir plus](/fr/docs/thread-color/#installer-des-palettes-de-couleurs-de-fils-%C3%A0-broder-pour-inkscape)


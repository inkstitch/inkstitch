---
title: "Personnaliser Ink/Stitch"
permalink: /fr/docs/customize/
excerpt: ""
last_modified_at: 2022-01-16
toc: true
---
## Raccourcis Clavier

Vous pouvez accelerer votre travail sous Ink/Stitch en utilisant des raccourcis clavier.

La liste suivante décrit les raccourcis claviers qui sont définis dans le fichier à télécharger ci-dessous.

Certains de ces raccourcis remplacent des raccourcis natifs d'Inkscape. Dans le tableau ci dessous vous pouvez voir quels sont ces raccourcis et  comment continuer à acceder à ces fonctions. {: .notice--warning }

Raccourcis&nbsp;Clavier | Effet | Remplace
-------- | --------
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
<key>ctrl</key>+<key>shift</key>+<key>U</key> | Convertir ligne en satin  (U ressemble à deux rails) | Objet > Grouper (utiliser Ctrl+G à la place)
<key>ctrl</key>+<key>shift</key>+<key>J</key> | Intervertir les rails satin  (J ressemble à une flèche)
<key>ctrl</key>+<key>shift</key>+<key>B</key> | Scinder colonne satin  (B est coupé en deux parties) | Chemin > Union (utiliser Ctrl++ à la place )
<key>ctrl</key>+<key>shift</key>+<key>*</key> | Agendement automatique de colonnes satin (ordonne tout)

Dans Ink/Stitch la [simulation](/fr/docs/visualize/) inclut déjà le raccourci.

\* Monter et Descendre dans la pile d'objets permet de contrôler précisement l'ordre dans lequel les objets sont brodés. Très utile en combinaison avec le panneau Objet (`Objet > Objets ...`).  L'ordre de la pile défini l'ordre dans lequel les éléments sont brodés (le bas de la pile en premier, pour finir par le haut de la pile).<br><br>** Pour les colonnes satin et les points droits, ceci change la direction des points. A utiliser avec `Afficher le sens des chemins sur le contour` selectionné dans `Edition > Préférences > Outils > Noeuds`. Si vous selectionnez un seul sommet en utilisant l'éditeur de noeuds et que vous effectuez un `Ctrl+R`, Inkscape renverse seulement le chemin qui contient ce noeud dans l'objet. Vous pouvez de cette manière vous assurer que les deux rails d'une colonne satin sont orientés dans le même sens.
{: .notice--info }
{: style="font-size: 70%" }

### Télécharger et importer des raccourcis clavier

* [Téléchargez le fichier de raccourcis clavier](/assets/files/inkstitch.xml)
* Allez à  `Edition > Préférences > Interface > Raccourcis clavier`
* Cliquez sur  `Importer...`
* Selectionnez votre fichier de raccourcis (inkstitch.xml)
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
Pour aligner correctement vos formes vectorielles, vous pouvez utiliser la fonctionnalité de grille d’Inkscape. Aller à  `Affichage` et activer  la `Grille`. Dans la `Barre des magnétismes` vérifier que `Aimanter aux grilles` est activé. Il est également possible de régler l'espacement et l'origine de vos grilles dans `Fichier> Propriétés du document> Grilles`.

![Grids](https://user-images.githubusercontent.com/11083514/40359052-414d3554-5db9-11e8-8b49-3be75c5e9732.png)

## Activation de la direction des chemins

Il est important de connaître les directions de chemin en travaillant avec Ink/Stitch. Par conséquent, nous vous recommandons d'activer les cases à cocher **Afficher la direction du chemin sur les contours** et **Afficher le contour temporaire pour les chemins sélectionnés** dans `Édition > Préférences > Outils > Noeuds`.

Vérifier aussi que **Afficher le contour du chemin** est activé dans la  `Barre de contrôle de l'outil noeud` comme dans l'image ci-dessous
[![Path outlines & directions](https://user-images.githubusercontent.com/11083514/40360721-f294ef0a-5dbe-11e8-9d4d-98f469ff1fba.png)](https://user-images.githubusercontent.com/11083514/40360721-f294ef0a-5dbe-11e8-9d4d-98f469ff1fba.png)

## Travailler avec des modèles

Si vous décidez d'utiliser plus fréquemment Ink/Stitch pour vos travaux de broderie, vous en aurez peut-être assez de mettre tout en scène à chaque fois. Dans ce cas, vous êtes prêt à créer un modèle pour votre configuration de broderie de base. Une fois que vous avez tout organisé comme vous le souhaitez, enregistrez simplement votre fichier dans votre dossier de modèles. Vous pouvez maintenant y accéder par `Fichier > Nouveau à partir d'un modèle`.

Système|Dossier des modèles
---|---
Linux|`~/.config/inkscape/templates`
Windows|`C:\Users\%USERNAME%\AppData\Roaming\inkscape\templates`
MacOS|`/Users/%USERNAME%/Library/Application\ Support/org.inkscape.Inkscape/config/inkscape/templates`

Retrouvez le dossier utilisateur dans vos préférences inkscape. Voir [FAQ](/fr/docs/faq/#jai-t%C3%A9l%C3%A9charg%C3%A9-et-d%C3%A9compress%C3%A9-la-derni%C3%A8re-version-o%C3%B9-je-la-mets).

**Astuce:** Obtenez des [modèles prédéfinis](/fr/tutorials/resources/templates/) dans notre section tutoriel.
{: .notice--info }

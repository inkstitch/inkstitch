---
title: "Personnaliser Ink/Stitch"
permalink: /fr/docs/customize/
excerpt: ""
last_modified_at: 2019-10-12
toc: true
---
## Raccourcis Clavier

vous pouvez accélérer votre travail en créant des raccourcis clavier.
Aller à: `Edition > Préférences > Interface > Raccourcis clavier` et entrer les combinaisons clavier souhaitées. [Plus d'information](http://tavmjong.free.fr/INKSCAPE/MANUAL_v14/html_fr/Customize.html)

La liste suivante est suggérée par lexelby:

Raccourci&nbsp;clavier | Effet
-------- | --------
<key>ctrl</key>+<key>shift</key>+<key>O</key> | Dialogue objets (Menu objet -> Objets)
<key>ctrl</key>+<key>shift</key>+<key>P</key> | Paramètres de l'extension, sans le dialogue des préférences d'extension d'inkscape
<key>ctrl</key>+<key>shift</key>+<key>L</key> | Simulation (mnemonic: Live simulation)
<key>ctrl</key>+<key>shift</key>+<key>E</key> | Extension broder, sans le dialogue des préférences d'extension d'Inkscape
<key>Page haut</key>                             | "Monter" (Inkscape version >= 0.92.2)*
<key>Page bas</key>                           | "Descendre" (Inkscape version >= 0.92.2)*
<key>ctrl</key>+<key>R</key>                  | Inverse la direction d'un chemin.**

*Une nouvelle fonction dans Inkscape 0.92.2 qui vous permet de monter ou descendre un objet dans l'ordre d'empilement, même s'il n'y a pas de chevauchement. Monter et Descendre donne un contrôle précis sur l'ordre dans lequel les objets sont brodés. Très utile en combinaison avec le dialogue Objets (`Objet > Objets ...`). L'ordre d'empilement définit l'ordre dans lequel les éléments sont brodés (de bas en haut).).
{: style="font-size: 70%" }

**Pour le point satin et le point droit, cela change le sens des points. Activez ceci dans les préférences d'Inkscape dans les paramètres de l'outil Nœud, `Afficher le sens des chemins sur le contour`. Si vous sélectionnez un seul sommet à l'aide de l'éditeur de nœud et appuyez sur les touches `Ctrl+R`, Inkscape inversera un seul chemin dans un objet. De cette façon, vous pouvez vous assurer que les deux rails d'une colonne satin pointent dans la même direction.
{: style="font-size: 70%" }

### Simulation : Raccourci

Dans Ink/Stitch la [simulation](/docs/simulate) inclut déjà le raccourci.

## Grilles
Pour aligner correctement vos formes vectorielles, vous pouvez utiliser la fonctionnalité de grille d’Inkscape. Aller à  `Affichage` et activer `Grille`. Dans la`Barre des magnétismes` vérifier que `Aimanter aux grilles` est activé. Il est également possible de régler l'espacement et l'origine de vos grilles dans `Fichier> Propriétés du document> Grilles`.

![Grids](https://user-images.githubusercontent.com/11083514/40359052-414d3554-5db9-11e8-8b49-3be75c5e9732.png)

## Activation de la direction des chemins

Il est important de connaître les directions de chemin en travaillant avec Ink/Stitch. Par conséquent, nous vous recommandons d'activer les cases à cocher **Afficher la direction du chemin sur les contours** et **Afficher le contour temporaire pour les chemins sélectionnés** dans `Édition > Préférences > Outils > Noeuds`.

Vérifier aussi que **Afficher le contour du chemin** est activé dans la  `Barre de contrôle de l'outil noeud` comme dans l'image ci-dessous
[![Path outlines & directions](https://user-images.githubusercontent.com/11083514/40360721-f294ef0a-5dbe-11e8-9d4d-98f469ff1fba.png)](https://user-images.githubusercontent.com/11083514/40360721-f294ef0a-5dbe-11e8-9d4d-98f469ff1fba.png)

## Travailler avec des modèles

Si vous décidez d'utiliser plus fréquemment Ink / Stitch pour vos travaux de broderie, vous en aurez peut-être assez de mettre tout en scène à chaque fois. Dans ce cas, vous êtes prêt à créer un modèle pour votre configuration de broderie de base. Une fois que vous avez tout organisé comme vous le souhaitez, enregistrez simplement votre fichier dans votre dossier de modèles. Vous pouvez maintenant y accéder par `Fichier > Nouveau à partir d'un modèle`.

Système|Dossier des modèles
---|---
Linux|`~/.config/inkscape/templates`
Windows|`C:\Users\%USERNAME%\AppData\Roaming\inkscape\templates`
Retrouvez le dossier utilisateur dans vos préférences inkscape. Voir [FAQ](/docs/faq/#i-have-downloaded-and-unzipped-the-latest-release-where-do-i-put-it).

**Astuce:** Obtenez des [modèles prédéfinis](/tutorials/resources/templates/) dans notre section tutoriel.
{: .notice--info }

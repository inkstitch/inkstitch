---
title: "Personnaliser Ink/Stitch"
permalink: /fr/docs/customize/
excerpt: ""
last_modified_at: 2019-10-12
toc: true
---
## Raccourcis Clavier

You can speed up your work with Ink/Stitch, if you assign shortcut keys.

The following list shows shortcut keys provided in the downloadable file below.

Some of the defined shortcut keys will replace others which are native to Inkscape. In the table you will see which they are and how you can still access these functions.
{: .notice--warning }

Shortcut&nbsp;Keys | Effect | Replaces
-------- | --------
<key>PageUp</key>                             | Stack Up* | Object > Raise (see also toolbar buttons)
<key>PageDown</key>                           | Stack Down* | Object > Lower (see also toolbar buttons)
<key>ctrl</key>+<key>R</key>                  | Reverse the direction of a path.**
<key>ctrl</key>+<key>shift</key>+<key>P</key> | Params | Edit > Preferences
<key>ctrl</key>+<key>shift</key>+<key>L</key> | Simulator (Live simulation)
<key>ctrl</key>+<key>shift</key>+<key>/</key> | Stitch plan preview (beside of the canvas) | Path > Division (use Strg+/ instead)
<key>ctrl</key>+<key>shift</key>+<key>O</key> | Break apart fill objects... (O for Object) | Object > Object properties
<key>ctrl</key>+<key>shift</key>+<key>I</key> | PDF Export
<key>ctrl</key>+<key>shift</key>+<key>Q</key> | Lettering (Q for QWERTY) | Object > Selectors and CSS
<span style="white-space: nowrap;"><key>ctrl</key>+<key>shift</key>+<key>Del</key></span> | Troubleshoot objects (remove errors)
<key>ctrl</key>+<key>shift</key>+<key>+</key> | Attach commands to selected objects
<key>ctrl</key>+<key>shift</key>+<key>U</key> | Convert line to satin column (U looks like two rails) | Object > Group (use Ctrl+G instead)
<key>ctrl</key>+<key>shift</key>+<key>J</key> | Flip satin column rails (J looks like an arrow)
<key>ctrl</key>+<key>shift</key>+<key>B</key> | Cut satin column (B is cut in half) | Path > Union (use Ctrl++ instead)
<key>ctrl</key>+<key>shift</key>+<key>*</key> | Auto-route satin (puts everything in order)

Dans Ink/Stitch la [simulation](/fr/docs/visualize/) inclut déjà le raccourci.

\* Stack Up and Stack Down give precise control over the order that objects are stitched in. Very useful in combination with the Objects panel (`Objects > Objects ...`). The stacking order defines, in which order elements are stitched out (from bottom to top).<br><br>** For satins and running stitch, this changes the direction the stitches go in. Use with `Show path direction on outlines` selected in `Edit > Preferences > Tools > Node`. If you select just one vertex using the node editor and press `Ctrl+R`, Inkscape will reverse just one path in an object. This way you can make sure that both rails in a satin point the same direction.
{: .notice--info }
{: style="font-size: 70%" }

### Download and import custom shortcut keys

* [Download the Ink/Stitch shortcut key file](/assets/files/inkstitch.xml)
* Go to `Edition > Préférences > Interface > Raccourcis clavier`
* Click on `Import...`
* Select your shortcut key file (inkstitch.xml)
* Click open

Now you will be able to use the shortcut keys described above.

If you want to define your own custom shortcut keys simply enter your desired key combinations in the shortcut dialog.
Use the search function to find the extensions quicker. [More information](http://wiki.inkscape.org/wiki/index.php/Customizing_Inkscape)
{: .notice--info }

## Zoom correction factor

For embroidery it is essential to get a sense of the actual size of the design. Inkscape has a setting to adapt zoom levels to your display size.

* Go to `Edit > Preferences > Interface`
* Hold a ruler onto your display and adjust the slider until the length matches
 
![Zoom correction](/assets/images/docs/fr/customize-zoom-correction.png)

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
Retrouvez le dossier utilisateur dans vos préférences inkscape. Voir [FAQ](/fr/docs/faq/#jai-t%C3%A9l%C3%A9charg%C3%A9-et-d%C3%A9compress%C3%A9-la-derni%C3%A8re-version-o%C3%B9-je-la-mets).

**Astuce:** Obtenez des [modèles prédéfinis](/fr/tutorials/resources/templates/) dans notre section tutoriel.
{: .notice--info }

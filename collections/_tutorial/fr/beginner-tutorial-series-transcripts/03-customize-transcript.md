---
title: Transcript - 03 Customize - Beginner Tutorial Series
permalink: /fr/tutorials/resources/beginner-video-tutorials/03-customize-transcript
last_modified_at: 2019-04-11
language: fr
image: '/assets/images/tutorials/video-preview-images/beginner-tutorial-series.png'

toc: true

exclude-from-tutorial-list: true
---
[← Back](/fr/tutorials/resources/beginner-video-tutorials/)

##  Bienvenue dans la série de tutoriels pour débutants Ink/Stitch.

**Dans cette partie, nous allons personnaliser Inkscape.**

Les personnalisations ne sont pas obligatoires, mais elles rendront plus confortable le travail avec Ink/Stitch.

Ce tutoriel vous apprendra à :

* Installer les modules complémentaires Ink/Stitch pour Inkscape
    Le programme d'installation des modules complémentaires Ink/Stitch ajoutera des palettes de couleurs du fabricant et des symboles spécifiques Ink/Stitch à votre installation Inkscape

* Définir des touches de raccourci pour un accès rapide et facile aux fonctions souvent utilisées

* Afficher les contours du chemin pour rendre visible la direction du point

* Utilisez des grilles pour aligner votre motif

* Créer et charger des modèles en tant que configuration de page de base



## Modules complémentaires

Commençons par les modules complémentaires Ink/Stitch

En fait, ces modules complémentaires sont deux fichiers qui doivent être placés dans des dossiers spécifiques de votre installation d'Inkscape.

Lancez `Extensions > Ink/Stitch > Install add-ons for Inkscape` et cliquez sur installer.

Vous devrez redémarrer Inkscape pour que cela ait un effet.

Ouvrez le panneau des palettes de couleurs et vous trouverez de nombreuses nouvelles palettes. Elles commencent toutes par Ink/Stitch, vous pouvez donc facilement les reconnaître.

Vous pouvez maintenant planifier votre conception directement avec les palettes de couleurs de vos fabricants de fils. Les noms de fils seront également affichés dans la sortie du navigateur afin que vous puissiez les partager directement avec votre client.

### Commandes visuelles

La deuxième fonctionnalité que nous apprendrons à mieux connaître dans ce didacticiel sont les commandes visuelles. Des symboles sont utilisés pour donner à Ink/Stitch plus d'informations sur la façon dont votre dessin doit être brodé.

Ajoutons par example un symbole Ignorer à un objet. Cela indique que cet objet particulier ne doit pas être brodé du tout.

Créez deux objets et lancez le simulateur. Les deux objets sont affichés.

Avec un objet sélectionné, allez dans `Extensions > Ink/Stitch > Commandes > Ajouter commande aux objets sélectionnés `.

Cochez la case Ignorer et cliquez sur Appliquer.

Maintenant, lancez à nouveau le simulateur. Un seul des deux objets est représenté.

Il y a beaucoup plus d'options dans la section des commandes visuelles.

## Raccourcis claviers

Dans Ink/Stitch, il existe de nombreuses fonctions que vous utiliserez fréquemment. Pour eviter de cliquer sur le menu tout le temps, vous voudrez utiliser des raccourcis clavier.

Nous ne passerons pas en revue toutes les possibilités ici, mais nous vous montrerons seulement comment configurer les touches de raccourci, afin que vous puissiez en ajouter d'autres plus tard
Il y a une liste sur <https://inkstitch.org> pour vous donner des conseils supplémentaires sur les combinaisons de touches que vous pourriez utiliser.

Ouvrez les Préférences via Edition > Préférences. Accédez à "Interface" et choisissez "Clavier".

* Recherchez "Paramètres". Vous le trouverez sous `Effets`. Cliquez dans le champ sous `raccourci` et entrez `Control + Shift + C`.
* Ensuite, recherchez "Simuler" et entrez `Control + Shift + L`
* Ensuite, ajoutez `Control + R` pour "inverser la direction du chemin"
* et enfin `Page down` pour "stack down" et `Page up` pour "stack up"

Examinons de plus près les fonctions  "vers le haut  de pile" et "vers le bas de pile".

Ouvrez le panneau d'objets. Il affiche une liste complète de tous les calques, groupes et objets du document dans son "ordre d'empilement".

Supprimez le symbole d'ignorance que nous avons précédemment ajouté et déplacez les objets afin qu'ils se chevauchent.

Si vous utilisez les boutons de montée et de descente sur le premier objet, vous verrez comment leur ordre d'empilement change de position.

Cela ne fonctionne pas si les objets ne se chevauchent pas.

Utilisez maintenant vos touches de raccourci nouvellement créées et voyez que l'ordre d'empilement change à nouveau. Les boutons haut et bas du panneau des objets feront la même chose que vos raccourcis clavier.

La position des objets définira l'ordre de bas en haut de la façon dont votre motif est cousu, ce qui en fait une caractéristique principale tout en planifiant soigneusement votre conception.



## Contours 

Les contours du chemin vous montreront la direction du chemin.

La direction du chemin est importante pour tous les types de points, à l'exception des points de remplissage. Il définit à quelle extrémité du trait la broderie commencera.

Dans `Preferences > Outils > Noeud, cochez les cases suivantes `Afficher le sens des chemins sur le  contour` et `Affichez temporairement  le contour des chemins sélectionnés`.

Avec les objets sélectionnés, appuyez sur 'N' pour activer l'outil de nœud et activer 'Afficher le contour du chemin'.

Vous verrez un chemin rouge entourant les objets. Les flêches indiquent la direction du chemin.

## Grilles

Vous pouvez utiliser des grilles pour aligner correctement les motifs.
Pour les activer, ouvrez Fichier> Propriétés du document et passez à l'onglet "Grilles".
Cliquez sur Nouveau et changez les unités en mm (il s'agit de l'unité commune utilisée pour la longueur de point, etc.) et réglez l'espacement x et y sur 1.
Si vous effectuez un zoom arrière, la ligne principale de la grille s'affichera. Il est par défaut à 5, changez-le en 10, puis vous avez 1 cm à afficher.

Vos objets s'aligneront sur les bords de la grille par défaut. Vous pouvez changer cela en désactivant l'alignement ou en désactivant l'alignement sur les grilles uniquement.
Si vous souhaitez masquer temporairement la grille, appuyez sur # ou modifiez-la via le menu : `Affichage > Grille de page`.

Jetez également un coup d'œil au panneau "aligner et distribuer" que vous pouvez trouver sous Objets dans le menu. Vous trouverez ici de nombreuses méthodes d'alignement utiles.

## Modèles

Ce  n'est pas très  amusant de configurer les mêmes propriétés de document encore et encore.
Vous préférez ouvrir un nouveau document et qu'il ait la taille de votre cadre de broderie.
Eh bien, c'est possible.

Une fois que vous avez tout organisé comme vous le souhaitez, enregistrez simplement votre fichier dans votre dossier de modèles.
Sélectionnez le chemin du dossier de modèles pour votre système d'exploitation dans la description ci-dessous.

Vous pouvez maintenant accéder à votre modèle via `Fichier > Nouveau à partir du modèle`.

Sur <https://inkstitch.org>, vous pouvez même télécharger un modèle prédéfini avec différentes tailles de cadre.

---

Nous espérons que vous avez apprécié le tutoriel. Vous êtes maintenant prêt à commencer votre travail créatif.

Si vous avez des questions sur Ink/Stitch, veuillez nous contacter sur GitHub.




[← Back](/tutorials/resources/beginner-video-tutorials/)


---
title: "Install Ink/Stitch"
permalink: /fr/docs/install-linux/
excerpt: "How to quickly install Ink/Stitch."
last_modified_at: 2021-05-03
toc: true
---
## Guide vidéo

Nous fournissons aussi aux débutants des tutoriels vidéo sur notre <i class="fab fa-youtube"></i> [chaine YouTube](https://www.youtube.com/channel/UCJCDCFuT_xQoI55e10HRiRw). Les vidéos sont en anglais. Mais il y a des sous-titres en français.

* <i class="fab fa-linux"></i> [Linux](https://www.youtube.com/watch?v=Dkb5UvsZUNg&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=2)

## Prérequis

* [Inkscape](https://inkscape.org/) Version 0.92.2 ou supérieure

C'est tout! Toutes les librairies python et dépendances externes sont incluses (en utilisant l'excellent [pyinstaller](http://www.pyinstaller.org)), de sorte que vous ne devriez pas avoir quoi que ce soit d'autre à installer.

## Installation rapide

### Télécharger
Télécharger, en tenant compte de votre plateforme.

* <i class="fa fa-download " ></i> [Français]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-linux-fr_FR.zip)
* <i class="fa fa-download " ></i> [Allemand]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-linux-de_DE.zip)
* <i class="fa fa-download " ></i> [Anglais]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-linux-en_US.zip)
* <i class="fa fa-download " ></i> [Finnois]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-linux-fi_FI.zip)
* <i class="fa fa-download " ></i> [Italien]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-linux-it_IT.zip)
* <i class="fa fa-download " ></i> [Dutch]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-linux-nl_NL.zip)
* <i class="fa fa-download " ></i> [Japanois]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-linux-ja_JP.zip)
* <i class="fa fa-download " ></i> [Russe]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-linux-ru_RU.zip)

**Dernière version:** [Ink/Stitch {{ site.github.latest_release.tag_name }} ({{ site.github.latest_release.published_at | date: "%Y-%m-%d" }})](https://github.com/inkstitch/inkstitch/releases/latest)

Le `LOCALE` sélectionné affecte les menus à l'intérieur d'Inkscape. Les dialogues d'Ink/Stitch sont dans la langue de votre OS (si cette langue est supportée).<br><br>Ink/Stitch n’existe pas dans votre langue? Aidez-nous à [traduire les dialogues dans votre langue maternelle](/fr/developers/localize/).
{: .notice--info }

### Installation
Dans Inkscape, allez à  `Edition > Préferences > Systeme` et cherchez dans ce tableau où se trouve votre dossier `Extensions utilisateur`.

![Extensions folder](/assets/images/docs/fr/extensions-folder-location-linux.jpg)

Décompressez l'archive Ink/Stitch dans ce dossier.
 
```
$ cd ~/.config/inkscape/extensions
$ unzip ~/Downloads/inkstitch-{{ site.github.latest_release.tag_name }}-linux-fr_FR.zip
```

### Exécuter Ink/Stitch

Redémarrez Inkscape.

Vous trouverez alors Ink/Stitch sous `Extensions > Ink/Stitch`.

## Installation Ink/Stitch

### J'ai téléchargé et décompressé la [dernière version](https://github.com/inkstitch/inkstitch/releases/latest). Où je la mets?

Dans Inkscape ouvrir: `Edition > Preferences > System` et vérifier les chemins pour les extensions.

![image](https://user-images.githubusercontent.com/11083514/37572872-899a7de0-2b09-11e8-93ed-e4be6228c414.png)

Vous devriez de préférence installer dans **USER EXTENSIONS**, car cela facilitera la mise à jour ultérieure.

Si vous avez des signes diacritiques dans votre nom d'utilisateur, essayez le chemin d'accès de **INKSCAPE EXTENSIONS** si vous rencontrez des difficultés pour exécuter Ink/Stitch.

### Ink/Stitch ne fonctionne pas!

**Confirmer le chemin d'installation**<br>

Check if you extracted Ink/Stitch into the correct folder. If the `User extensions folder` doesn't work out correctly, you can also try to install into the `Inkscape extensions folder`.
You can also look it up under `Edit > Preferences > System`.

**Confirm Ink/Stitch Version**

Verify if you have downloaded Ink/Stitch for Linux ([Download](#download))

**Confirm ownership/permissions**

Some users report false ownership/permissions can cause this issue.

### AttributeError: 'NoneType' object has no attribute 'title' in inkstitch.py

This error has been reported to us by users who have installed Inkscape through snap. Snap is known to cause issues for Ink/Stitch to run with Inkscape.
Please try an other installing method. Any described on [https://inkscape.org/](https://inkscape.org/releases/latest/) will be fine. 

### Ink/Stitch dialogues disappear after a few seconds

This issue can be caused by wayland. Start Inkscape with the following command: `export GDK_BACKEND=x11 && inkscape`.

This workaround has to be used until we moved all Ink/Stitch applications to the electron environment. 

### J'ai installé Ink / Stitch dans ma langue maternelle, mais les fenêtres de dialogue sont affichées en anglais!

Premièrement, il est possible que toutes les chaînes n'aient pas été traduites. Ceci est indiqué par **certaines chaînes de texte en anglais et d'autres dans votre langue maternelle**.

Si vous souhaitez terminer la traduction, consultez notre [description pour les traducteurs](/developers/localize/).

Ensuite, nous devons faire la distinction entre le menu Extension dans Inkscape et les fenêtres de dialogue.
La sélection du fichier ZIP a pour seule conséquuence la traduction du menu Extension dans une certaine langue.
Les fenêtres de dialogue sont construites différemment. Elles utiliseront la langue de votre système d'exploitation.
Si Ink/Stitch n'est pas sûr de la langue à prendre en charge, il retombera sur l'anglais.
Vous pouvez indiquer explicitement à Inkscape d'utiliser votre langue maternelle comme suit:
  * Aller à Edition > Preferences > Interface (Ctrl + Shift + P)
  * choisissez votre langue
  * Redémarrer Inkscape

![Preferences > Interface](/assets/images/docs/fr/preferences_language.png)


## Mise à jour

 * Il faut d'abord effacer tous les fichiers de l'ancienne extension:<br />
   Ouvrez le répertoire des extensions et supprimez chaque dossier ou fichier inkstitch*.
 * Puis procédez comme ci-dessus.

**Astuce:** Inscrivez-vous aux news pour avoir connaissance des mises à jour d'Ink/Stitch:<br />
 <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [GitHub Feed on new Releases](https://github.com/inkstitch/inkstitch/releases.atom)<br>
 <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [Ink/Stitch News](/feed.xml)<br />
{: .notice--info }

<p class="notice--info" style="margin-top: -3.5em !important;">Or watch the project on GitHub:<br /><iframe style="display: inline-block;" src="https://ghbtns.com/github-btn.html?user=inkstitch&repo=inkstitch&type=watch&count=true&v=2" frameborder="0" scrolling="0" width="170px" height="20px"></iframe></p>

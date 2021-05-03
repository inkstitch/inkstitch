---
title: "Install Ink/Stitch"
permalink: /fr/docs/install-windows/
excerpt: "How to quickly install Ink/Stitch."
last_modified_at: 2021-05-03
toc: true
---
## Guide vidéo

Nous fournissons aussi aux débutants des tutoriels vidéo sur notre <i class="fab fa-youtube"></i> [chaine YouTube](https://www.youtube.com/channel/UCJCDCFuT_xQoI55e10HRiRw). Les vidéos sont en anglais. Mais il y a des sous-titres en français.

* <i class="fab fa-windows"></i> [Windows](https://www.youtube.com/watch?v=U5htzWZSjA8&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=4)

## Prérequis

* [Inkscape](https://inkscape.org/releases) Version 1.0.2 ou supérieure

C'est tout! Toutes les librairies python et dépendances externes sont incluses (en utilisant l'excellent [pyinstaller](http://www.pyinstaller.org)), de sorte que vous ne devriez pas avoir quoi que ce soit d'autre à installer.

## Installation rapide

### Télécharger
Télécharger, en tenant compte de votre plateforme.

* <i class="fa fa-download " ></i> [Français]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-fr_FR.zip)
* <i class="fa fa-download " ></i> [Allemand]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-de_DE.zip)
* <i class="fa fa-download " ></i> [Anglais]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-en_US.zip)
* <i class="fa fa-download " ></i> [Finnois]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-fi_FI.zip)
* <i class="fa fa-download " ></i> [Italien]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-it_IT.zip)
* <i class="fa fa-download " ></i> [Néerlandaise]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-nl_NL.zip)
* <i class="fa fa-download " ></i> [Japanese]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-ja_JP.zip)
* <i class="fa fa-download " ></i> [Russe]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-ru_RU.zip)
{: .inline-table }

**Dernière version:** [Ink/Stitch {{ site.github.latest_release.tag_name }} ({{ site.github.latest_release.published_at | date: "%Y-%m-%d" }})](https://github.com/inkstitch/inkstitch/releases/latest)

Le `LOCALE` sélectionné affecte les menus à l'intérieur d'Inkscape. Les dialogues d'Ink/Stitch sont dans la langue de votre OS (si cette langue est supportée).<br><br>Ink/Stitch n’existe pas dans votre langue? Aidez-nous à [traduire les dialogues dans votre langue maternelle](/fr/developers/localize/).
{: .notice--info }

### Installation

Dans Inkscape, allez à  `Edition > Préferences > Systeme` et cherchez dans ce tableau où se trouve votre dossier `Extensions utilisateur`.

![Extensions folder](/assets/images/docs/fr/extensions-folder-location-windows.jpg)

Décompressez l'archive Ink/Stitch dans ce dossier.

### Exécuter Ink/Stitch

Redémarrez Inkscape.

Vous trouverez alors Ink/Stitch sous `Extensions > Ink/Stitch`.

## Problèmes d'Installation Ink/Stitch

### J'ai téléchargé et décompressé la [dernière version](https://github.com/inkstitch/inkstitch/releases/latest). Où je la mets?

Dans Inkscape ouvrir: `Edition > Preferences > System` et vérifier les chemins pour les extensions.

![image](https://user-images.githubusercontent.com/11083514/37572872-899a7de0-2b09-11e8-93ed-e4be6228c414.png)

Vous devriez de préférence installer dans **USER EXTENSIONS**, car cela facilitera la mise à jour ultérieure.

Si vous avez des signes diacritiques dans votre nom d'utilisateur, essayez le chemin d'accès de **INKSCAPE EXTENSIONS** si vous rencontrez des difficultés pour exécuter Ink/Stitch.

### Ink/Stitch ne fonctionne pas!

*   **Confirmer le chemin d'installation**<br>
    Check if you extracted Ink/Stitch into the correct folder. If the `User extensions folder` doesn't work out correctly, you can also try to install into the `Inkscape extensions folder`.
    You can also look it up under `Edit > Preferences > System`.

*   **Windows Anti-Virus**<br>
    Ceci est plus susceptible de se produire sous Windows, car python est condensé dans un exécutable,
    des rapports de logiciels antivirus utilisant des méthodes heuristiques cela marque l'extension comme un faux positif.
    Dans ce cas, la solution consiste à ajouter le dossier d’extensions Ink/Stitch à la liste des exceptions de l'antivirus. puis réinstaller l’extension et réessayer.

    Si votre logiciel antivirus a supprimé des fichiers, vous recevrez le message d'erreur suivant:
    ```
    Tried to launch: inkstitch\bin\inkstitch
    Arguments: ['inkstitch\bin\inkstitch', '--id=XXX', '--extension=XXX', 'C:\Users\XXX\AppData\Local\Temp\ink_ext_XXXXXX.svgXXXXX']
    Debugging information:

    Traceback (most recent call last):
      File "inkstitch.py", line 35, in <module>
        extension = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      File "C:\Program Files\Inkscape\lib\python2.7/subprocess.py", line 325, in __init__
        errread, errwrite)
      File "C:\Program Files\Inkscape\lib\python2.7/subprocess.py", line 575, in _execute_child
        startupinfo)
    WindowsError: [Error 2] The system cannot find the file specified
    ```

### J'ai installé Ink/Stitch mais le menu est grisé (désactivé)

C'est souvent le cas si la mauvaise version Ink / Stitch a été installée.
Veuillez vérifier si vous avez téléchargé la bonne version Ink / Stitch pour votre système d'exploitation.

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

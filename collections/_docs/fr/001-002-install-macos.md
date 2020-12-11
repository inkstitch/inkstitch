---
title: "Install Ink/Stitch"
permalink: /fr/docs/install-macos/
excerpt: "How to quickly install Ink/Stitch."
last_modified_at: 2020-12-11
toc: true
---
## Guide vidéo

Nous fournissons aussi aux débutants des tutoriels vidéo sur notre <i class="fab fa-youtube"></i> [chaine YouTube](https://www.youtube.com/channel/UCJCDCFuT_xQoI55e10HRiRw). Les vidéos sont en anglais. Mais il y a des sous-titres en français.

* <i class="fab fa-apple"></i> [macOS](https://www.youtube.com/watch?v=gmOVLNh9cu8&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=3)

**Attention:** La vidéo pour les utilisteurs de Mac est obsolète. Lisez la mise à jour des infos ["Etapes additionnelles pour Catalina / Big Sur"](#addtitional-steps-for-catalina--big-sur)
{: .notice--warning }

## Prérequis

* [Inkscape](https://inkscape.org/) Version 0.92.2 jusquà Mojave, 1.0.1 à partir de Catalina

C'est tout! Toutes les librairies python et dépendances externes sont incluses (en utilisant l'excellent [pyinstaller](http://www.pyinstaller.org)), de sorte que vous ne devriez pas avoir quoi que ce soit d'autre à installer.

## Installation rapide

### Télécharger
Télécharger, en tenant compte de votre plateforme.

Language|macOS Catalina / Big Sur | Sierra* | High Sierra* | Mojave*
---|---|---|---
**Allemand**|<i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-de_DE.zip)|<i class="fa fa-download " ></i> [Sierra]({{ site.github.releases_url }}/download/v1.26.2/inkstitch-v1.26.2-osx-sierra-x86_64-de_DE.tar.gz)|<i class="fa fa-download " ></i> [High Sierra]({{ site.github.releases_url }}/download/v1.26.2/inkstitch-v1.26.2-osx-high_sierra-x86_64-de_DE.tar.gz)|<i class="fa fa-download " ></i> [Mojave]({{ site.github.releases_url }}/download/v1.26.2/inkstitch-v1.26.2-osx-mojave-x86_64-de_DE.tar.gz)|
**Anglais**|<i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-en_US.zip)|<i class="fa fa-download " ></i> [Sierra]({{ site.github.releases_url }}/download/v1.26.2/inkstitch-v1.26.2-osx-sierra-x86_64-en_US.tar.gz)|<i class="fa fa-download " ></i> [High Sierra]({{ site.github.releases_url }}/download/v1.26.2/inkstitch-v1.26.2-osx-high_sierra-x86_64-en_US.tar.gz)|<i class="fa fa-download " ></i> [Mojave]({{ site.github.releases_url }}/download/v1.26.2/inkstitch-v1.26.2-osx-mojave-x86_64-en_US.tar.gz)|
**Finnois**|<i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-fi_FI.zip)|
**Français**|<i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-fr_FR.zip)|<i class="fa fa-download " ></i> [Sierra]({{ site.github.releases_url }}/download/v1.26.2/inkstitch-v1.26.2-osx-sierra-x86_64-fr_FR.tar.gz)|<i class="fa fa-download " ></i> [High Sierra]({{ site.github.releases_url }}/download/v1.26.2/inkstitch-v1.26.2-osx-high_sierra-x86_64-fr_FR.tar.gz)|<i class="fa fa-download " ></i> [Mojave]({{ site.github.releases_url }}/download/v1.26.2/inkstitch-v1.26.2-osx-mojave-x86_64-fr_FR.tar.gz)|
**Italien**|<i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-it_IT.zip)|
{: .inline-table }

\* There are no recent versions of Ink/Stitch for Sierra, High Sierra or Mojave. The files are from an older Ink/Stitch release: Ink/Stitch v1.26.2 (2019-08-20).

**Dernière version:** [Ink/Stitch {{ site.github.latest_release.tag_name }} ({{ site.github.latest_release.published_at | date: "%Y-%m-%d" }})](https://github.com/inkstitch/inkstitch/releases/latest)

Le `LOCALE` sélectionné affecte les menus à l'intérieur d'Inkscape. Les dialogues d'Ink/Stitch sont dans la langue de votre OS (si cette langue est supportée).<br><br>Ink/Stitch n’existe pas dans votre langue? Aidez-nous à [traduire les dialogues dans votre langue maternelle](/fr/developers/localize/).
{: .notice--info }


### Installation
Dans Inkscape, allez à  `Edition > Préferences > Systeme` et cherchez dans ce tableau où se trouve votre dossier `Extensions utilisateur`.

![Extensions Utilisateur](/assets/images/docs/fr/extensions-folder-location-macos.jpg)

Décompressez l'archive Ink/Stitch **directement** dans ce dossier.

Ce dossier doit présenter une structure semblable à l'exemple ci-dessous (avec juste un tas de fichiers en plus):
![File Structure](/assets/images/docs/en/file_structure.png)

Redémarrez Inkscape.

Vous trouverez alors Ink/Stitch sous `Extensions > Ink/Stitch`.

### Etapes additionnelles pour Catalina / Big Sur

Les nouvelles versions de macOS n’accepteront pas Ink / Stitch s'il est téléchargé via votre navigateur. Vous recevrez un message d'erreur comme celui-ci: `impossible d'ouvrir'Inkstitch' car le développeur ne peut pas être vérifié`.

Pour éviter ce message d'erreur, ouvrez votre application Terminal. Cliquez sur la petite icône en forme de loupe dans votre barre de menu dans le coin supérieur droit (ou appuyez <key>Commande (⌘)</key>+<key>Espace</key>). Cherchez `Terminal` et ouvrez l'application.

Dans le terminal, entrez la commande suivante:

```
xattr -r -d com.apple.quarantine ~/Library/Application\ Support/org.inkscape.Inkscape/config/inkscape/extensions/
```

Remplacer `~/Library/Application\ Support/org.inkscape.Inkscape/config/inkscape/extensions/` si le chemin de votre dossier d'extension Inkscape a un autre emplacement (vérifiez dans `Inkscape > Preferences > System>Extension Utilisateur`).

Les utilisateurs de **Big Sur** devront faire une étape supplémentaire pour terminer l'installation

```
cd ~/Library/Application\ Support/org.inkscape.Inkscape/config/inkscape/extensions/
cd inkstitch/bin
ln -s libpython2.7.dylib libc.dylib
```
### Exécuter Ink/Stitch

Relancer Inkscape.

Vous trouverez alors Ink/Stitch dans `Extensions > Ink/Stitch`.

## Problème d'Installation Ink/Stitch

### J'ai téléchargé et décompressé la [dernière version](https://github.com/inkstitch/inkstitch/releases/latest). Où je la mets?

Dans Inkscape ouvrir: `Edition > Preferences > System` et vérifier les chemins pour les extensions.

![image](https://user-images.githubusercontent.com/11083514/37572872-899a7de0-2b09-11e8-93ed-e4be6228c414.png)

Vous devriez de préférence installer dans **USER EXTENSIONS**, car cela facilitera la mise à jour ultérieure.

Si vous avez des signes diacritiques dans votre nom d'utilisateur, essayez le chemin d'accès de **INKSCAPE EXTENSIONS** si vous rencontrez des difficultés pour exécuter Ink/Stitch.

### Ink/Stitch ne fonctionne pas!

*   **Confirmer le chemin d'installation**<br>
    Vérifier si des fichiers ont éventuellement été extraits dans un *sous-dossier*.
   Vous devriez voir beaucoup de fichiers commençant par "inkstitch" **directement** dans le dossier d'extensions, à côté d'un dossier appelé "inkstitch".

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

### I installed Ink/Stitch but the menu is greyed out (disabled)

This is often the case, if the wrong Ink/Stitch version has been installed.
Please verify if you have downloaded the correct Ink/Stitch version for your operating system.

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

---
title: "Install Ink/Stitch"
permalink: /fr/docs/install-windows/
excerpt: "How to quickly install Ink/Stitch."
last_modified_at: 2025-12-29
toc: true
---
{% comment %}
## Guide vidéo

Nous fournissons aussi aux débutants des tutoriels vidéo sur notre <i class="fab fa-youtube"></i> [chaine YouTube](https://www.youtube.com/c/InkStitch). Les vidéos sont en anglais. Mais il y a des sous-titres en français.

* <i class="fab fa-windows"></i> [Windows](https://www.youtube.com/watch?v=U5htzWZSjA8&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=4)
{% endcomment %}

## Prérequis

Ink/Stitch est une extension pour Inkscape.
Vous devez **Télécharger et installer  [Inkscape](https://inkscape.org/release/) Version 1.0.2 ou supérieure** avant d'installer Ink/Stitch. 

## Télécharger

Téléchargez la dernière version disponible pour windows.

<p><a href="{{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-64bit.exe" class="btn btn--info btn--large"><i class="fa fa-download"></i> Téléchargez Ink/Stitch {{ site.github.latest_release.tag_name }} pour Windows 64bit</a></p>

**Dernière version:** [Ink/Stitch {{ site.github.latest_release.tag_name }} ({{ site.github.latest_release.published_at | date: "%Y-%m-%d" }})](https://github.com/inkstitch/inkstitch/releases/latest)

Signature du code fournie gratuitement par [SignPath.io](https://about.signpath.io),certificat par [SignPath Foundation](https://signpath.org).<br>Voir [notre politique de signature du code](/fr/code-signing-policy).
{: .notice--info }

### Téléchargement avec  Microsoft Edge

Si vous utilisez le navigateur Microsoft Edge, il se peut que le fichier ne soit pas téléchargé immédiatement. Voici les étapes à suivre pour que votre navigateur le télécharge quand même.

Cliquez sur le lien de téléchargement (ci-dessus).

* Votre navigateur affichera un message d'avertissement. Cliquez dessus.

  ![Download warning message](/assets/images/docs/en/windows-download/01-warning-message.png)

Cliquez ensuite sur le texte du message.
  
* Le message affichera une corbeille pour annuler le téléchargement et un bouton de menu.

  ![Download warning message with menu button](/assets/images/docs/en/windows-download/02-warning_message02.png)
  
Cliquez sur le bouton « Menu »

* Un menu apparaît.

  ![Download warnig message with menu](/assets/images/docs/en/windows-download/03-keep.png)

Cliquez sur  `Keep` (Conserver)
* Un autre avertissement s'affichera.
  
  ![An other warning](/assets/images/docs/en/windows-download/04-show-more.png)

Cliquez sur « Afficher plus »
* Trois options supplémentaires s'offrent à vous.

Pour nous aider et faciliter le téléchargement des prochains utilisateurs, cliquez sur `Report this app as safe` (Signaler cette application comme sûre).

Choisissez `Keep anyway` pour télécharger le fichier.

  ![Keep anyway option finally shows up](/assets/images/docs/en/windows-download/05-keep_anyway.png)

## Installation

Double cliquez  pour exécuter le fichier que vous avez téléchargé.

Jusqu'à ce que notre certificat windows gagne assez de confiance, vous devez autorisez l'éxecution du fichier.


Cliquez sur  `plus d'informations`.

![Ink/Stitch installer](/assets/images/docs/fr/windows-install/installer01.png)

Maintenant cliquez sur la nouvelle option `Exécuter quand même`.

![Ink/Stitch installer](/assets/images/docs/fr/windows-install/installer02.png)

Ink/Stitch doit être installé dans le dossier extensions d'Inkscape. Le chemin est déjà défini pour vous. Cliquez sur `Suivant`.

![Ink/Stitch installer](/assets/images/docs/fr/windows-install/installer03.png)

Puisque Inkscape est installé,  le dossier d'extensions existe déjà. Confirmez que vous voulez installer dans ce répertoire et cliquez sur  `Oui`.

![Ink/Stitch installer](/assets/images/docs/fr/windows-install/installer04.png)

L'installateur va vous montrer un résumé des paramètres d'installation. Clicquez sur  `Installer`.

![Ink/Stitch installer](/assets/images/docs/fr/windows-install/installer05.png)

Ink/Stitch est maintenant installé.

![Ink/Stitch installer](/assets/images/docs/fr/windows-install/installer06.png)

## Exécuter Ink/Stitch

Ouvrez Inkscape. Vous trouverez alors Ink/Stitch sous `Extensions > Ink/Stitch`.

![Ink/Stitch menu](/assets/images/docs/fr/windows-install/inkstitch-extensions-menu.png)

## Désinstaller Ink/Stitch

### Désinstaller des versions d'Ink/Stitch  à partir de la version  v2.1.0 

Ouvrir le menu Démarrer de Windows. Cliquez sur  `Paramètres`.

![Uninstall Ink/Stitch](/assets/images/docs/fr/windows-install/uninstall01.png)

Cliquez sur  `Applications et Programmes`.

![Uninstall Ink/Stitch](/assets/images/docs/fr/windows-install/uninstall02.png)

Faites défiler la liste des applications vers le bas jusqu'à trouver Ink/Stitch.
Cliquez sur `Ink/Stitch` et une option de désinstallation apparait. Cliquez sur  `Désinstaller`.

![Uninstall Ink/Stitch](/assets/images/docs/fr/windows-install/uninstall03.png)

Confirmez que vous voulez désinstaller Ink/Stitch.

![Uninstall Ink/Stitch](/assets/images/docs/fr/windows-install/uninstall04.png)

Ink/Stitch a été supprimé de votre ordinateur. Cliquez `OK`.

![Uninstall Ink/Stitch](/assets/images/docs/fr/windows-install/uninstall05.png)

### Désinstaller des versions d'Ink/Stitch plus anciennes que la version v2.1.0

Dans Inkscape, allez à  `Edition > Préférences > Système` et cherchez dans ce tableau où se trouve votre dossier `Extensions utilisateur`.

![Extensions folder](/assets/images/docs/fr/extensions-folder-location-windows.jpg)

Supprimez chaque dossier ou fichier inkstitch.

## Être informé des mises à jour d'Ink/Stitch 

Inscrivez-vous aux news pour avoir connaissance des mises à jour d'Ink/Stitch.

* <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [Ink/Stitch News](/feed.xml)
* <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [GitHub Feed on new Releases](https://github.com/inkstitch/inkstitch/releases.atom)
 
<p>Ou regardez l'intégralité du projet sur GitHub:<br /> <iframe style="display: inline-block;" src="https://ghbtns.com/github-btn.html?user=inkstitch&repo=inkstitch&type=watch&count=true&v=2" frameborder="0" scrolling="0" width="170px" height="20px"></iframe></p>

## Problèmes d'Installation Ink/Stitch

### Ink/Stitch ne fonctionne pas!

**Windows Anti-Virus**
C'est le cas le plus probable sous Windows, car python est compressé dans un exécutable, et des rapports de logiciels antivirus utilisant des méthodes heuristiques peuvent marquer l'extension comme un faux positif.
Dans ce cas, la solution consiste à ajouter le dossier d’extensions Ink/Stitch à la liste des exceptions de l'antivirus. Puis réinstaller l’extension et réessayer.

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

**Vérifiez la version d'Ink/Stitch **

Vérifiez que vous avez bien téléchargé Ink/Stitch pour Windows ([Téléchargement](#download))

**Confirmer le chemin d'installation**

Vérifiez si vous avez bien installé Ink/Stitch dans le bon dossier.  Si le  dossier `Extensions utilisateur` ne fonctionne pas correctement, vous pouvez aussi essayer d'installer dans le dossier `extensions Inkscape`.
Vous pouvez trouver leur localisation dans  `Edition > Préferences > Système`.

### PYTHONPATH
On nous a rapporté des messages d'erreur qui commencent comme ça :



```
Python path configuration:
PYTHONHOME = 'C:\Users\{username}\AppData\Roaming\inkscape\extensions\inkstitch\bin'
PYTHONPATH = (not set)
```

Réinstallez Inkscape en prenant garde à ce que "Ajout au chemin" soit coché quand la questions sur PYTHONPATH est posée.

### message d'erreur Windows 7

Si vous voyez ce message, merci d'installer les mises à jour de sécurité de Microsoft Windows.

```
Traceback (most recent call last):
File "Lib\site-packages\PyInstaller\hooks\rthooks\pyi_rth_multiprocessing.py", line 12, in
File "PyInstaller\loader\pyimod03_importers.py", line 495, in exec_module
File "multiprocessing_init_.py", line 16, in
File "PyInstaller\loader\pyimod03_importers.py", line 495, in exec_module
File "multiprocessing\context.py", line 6, in
File "PyInstaller\loader\pyimod03_importers.py", line 495, in exec_module
File "multiprocessing\reduction.py", line 16, in
File "PyInstaller\loader\pyimod03_importers.py", line 495, in exec_module
File "socket.py", line 49, in
ImportError: DLL load failed while importing _socket: Paramètre incorrect.
```

### Message d'erreur Windows 8

![The program can't start because api-ms-win-crt-math-l1-1-1-0.dll is missing from your computer. Try reinstalling the program to fix this problem](/assets/images/docs/en/windows-install/win8.png)
{: .img-half }
![Error loading Python DLL 'C:\Users\...\AppData\Roaming\inkscape\extensions\inkstitch\inkstitch\bin\python38.dll'. LoadLibrary: The specified module could not be found.](/assets/images/docs/en/windows-install/win8a.png)
{: .img-half }

Si vous rencontrer l'un de ces deux messages d'erreur sous Windows 8, téléchargez et installez  [Microsoft Visual C++ Redistributable packages](https://docs.microsoft.com/en-US/cpp/windows/latest-supported-vc-redist?view=msvc-170#visual-studio-2015-2017-2019-and-2022). Choose the file for your system architecture.

### J'ai installé Ink/Stitch mais le menu est grisé (désactivé)

C'est souvent le cas si une mauvaise version d'Ink/Stitch a été installée.
Veuillez vérifier si vous avez téléchargé la bonne version Ink/Stitch pour votre système d'exploitation.

### Les fenêtres de dialogue sont affichées en anglais!

Premièrement, il est possible que tous les textes n'aient pas été traduits. Ceci est indiqué par **certaines parties en anglais et d'autres dans votre langue maternelle**.

Si vous souhaitez terminer la traduction, consultez notre [description pour les traducteurs](/developers/localize/).

Ensuite, nous devons faire la distinction entre le menu Extension dans Inkscape et les fenêtres de dialogue.
La sélection du fichier ZIP a pour seule conséquence la traduction du menu Extension dans une certaine langue.
Les fenêtres de dialogue sont construites différemment. Elles utiliseront la langue de votre système d'exploitation.
Si Ink/Stitch n'est pas sûr de la langue à prendre en charge, il choisira l'anglais.
Vous pouvez indiquer explicitement à Inkscape d'utiliser votre langue maternelle comme suit:
  * Aller à Edition > Préférences > Interface (Ctrl + Shift + P)
  * Choisissez votre langue
  * Redémarrer Inkscape

![Preferences > Interface](/assets/images/docs/fr/preferences_language.png)

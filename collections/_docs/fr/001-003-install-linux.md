---
title: "Installer Ink/Stitch pour linux"
permalink: /fr/docs/install-linux/
excerpt: "Comment installer rapidement Ink/Stitch."
last_modified_at: 2025-06-19
toc: true
after_footer_scripts:
  - /assets/js/copy_code.js
---

## Prérequis

Ink/Stitch est une extension pour Inkscape. Téléchargez et installez  [Inkscape](https://inkscape.org/release/) Version 1.0.2 ou supérieure avant d'installer Ink/Stitch.

## Installation

{% assign tag_name = site.github.latest_release.tag_name %}
Téléchargez la dernière version disponible pour Linux (Ink/Stitch {{ tag_name }}).

{% assign tag_name = tag_name | slice: 1,tag_name.size %}

* x86_64:
  [tar.xz]({{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-linux-x86_64.tar.xz),
  [sh]({{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-linux-x86_64.sh),
  [rpm]({{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-1.x86_64.rpm),
  [deb]({{ site.github.releases_url }}/latest/download/inkstitch_{{ tag_name }}_amd64.deb)
* i386:
  [tar.xz]({{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-linux32-i386.tar.xz),
  [sh]({{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-linux32-i386.sh),
  [rpm]({{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-1.i386.rpm),
  [deb]({{ site.github.releases_url }}/latest/download/inkstitch_{{ tag_name }}_i386.deb)
* arm64:
  [tar.xz]({{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-linux-aarch64.tar.xz),
  [sh]({{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-linux-aarch64.sh),
  [rpm]({{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-1.aarch64.rpm),
  [deb]({{ site.github.releases_url }}/latest/download/inkstitch_{{ tag_name }}_arm64.deb)
* Arch linux: <https://aur.archlinux.org/packages/inkstitch>
* NixOS: <https://search.nixos.org/packages?channel=unstable&show=inkscape-extensions.inkstitch>

**Dernière version:** [Ink/Stitch {{ site.github.latest_release.tag_name }} ({{ site.github.latest_release.published_at | date: "%Y-%m-%d" }})](https://github.com/inkstitch/inkstitch/releases/latest)

### Installation avec DEB ou RPM

Double cliquez sur le fichier deb téléchargé et suivez le processus d'installation.

RPM: [GPG-Key](/assets/files/inkstitch.gpg)

### Installation avec SH

Utilisez cette version si vous utilisez la version AppImage d'Inkscape ou si vous voulez installer  Ink/Stitch uniquement pour votre propre utilisateur. Ce script est aussi utile si votre système ne supporte pas les paquets deb ou rpm.

Ouvrez votre terminal et naviguez jusqu'au répertoire qui contient le script que vous avez téléchargé et exécutez le script, par exemple

```
cd Downloads
sh inkstitch-{{ tag_name }}-linux.sh
```

#### Option pour les experts

Ce script va tenter de déterminer automatiquement où installer les extensions utilisateurs d'Inkscape. S'il se trompe, vous pouvez modifier une de ces variables d'environnement:

* `INKSCAPE_PATH` (ex: /usr/bin/inkscape)

  Le chemin vers l'exécutable inkscape.  Le script demandera à ce programme où installer les extensions en lui transmettant l'argument --user-data-directory.

* `INKSCAPE_EXTENSIONS_PATH` (ex: $HOME/.config/inkscape/extensions)

  Le chemin vers le repertoire d'extensions inkscape.  Utilisez cela pour contourner la methode `--user-data-directory` et spécifier vous même le repertoire.

Si vous preferrez l'installer vous même, exécutez ce script avec `--extract` pour produire le fichier original inkstitch-&lt;version&gt;.tar.xz dans le répertoire courant.

### Installation avex TAR.XZ

Allez à `Edition > Préférences > Système` et vérifiez où se trouve votre dossier `Extensions utilisateur`.

![Extensions folder location](/assets/images/docs/fr/extensions-folder-location-linux.jpg)

Décompressez l'archive Ink/Stitch dans ce dossier.

```
$ cd ~/.config/inkscape/extensions
$ tar -xvf ~/Downloads/inkstitch-{{ tag_name }}-linux.tar.xz
```

## Exécuter Ink/Stitch

Redémarrez Inkscape.

Vous trouverez alors Ink/Stitch sous `Extensions > Ink/Stitch`.

## Mettre à jour Ink/Stitch

###  Versions Récentes

Si vous voulez mettre à jour un paquet `deb` ou `rpm`, vous n'avez qu'à télécharger le nouveau paquet et exécuter l'installation comme décrit ci-dessus. Cela remplacera l'ancienne installation.
Le `script d'installation` lui aussi supprime les anciennes versions d'Ink/Stitch avant d'installer la nouvelle.

Attention, ceci n'est vrai que pour les installations précédentes qui ont été faites par la même méthode. Si vous avez installé autrement, suivez d'abord ces instructions de mise à jour pour les anciennes versions:

### Versions plus anciennes que  Ink/Stitch v2.1.0 ou  version tar.xz

Supprimez d'abord les anciens fichiers d'extension : allez au repertoire d'extension et supprimez tous les fichiers ou repertoires inkstitch*

Puis, suivre la procédure ci-dessus.

Les répertoires d'extension peuvent être trouvés dans Inkscape sous <code class="language-plaintext highlighter-rouge">Edition > Préférences > Système</code>.

## Avoir des informations sur les mises à jour

Inscrivez-vous aux news pour avoir connaissance des mises à jour d'Ink/Stitch
* <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [GitHub Feed on new Releases](https://github.com/inkstitch/inkstitch/releases.atom)
* <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [Ink/Stitch News](/feed.xml)
* <p>Ou regardez l'intégralité du projet sur GitHub: <iframe style="display: inline-block;" src="https://ghbtns.com/github-btn.html?user=inkstitch&repo=inkstitch&type=watch&count=true&v=2" frameborder="0" scrolling="0" width="170px" height="20px"></iframe></p>

## Dépannage

### J'ai téléchargé et décompressé la [dernière version](https://github.com/inkstitch/inkstitch/releases/latest). Où je la mets?

Dans Inkscape ouvrir: `Edition > Préférences > Système` et vérifier les chemins pour les extensions.

![image](https://user-images.githubusercontent.com/11083514/37572872-899a7de0-2b09-11e8-93ed-e4be6228c414.png)

Vous devriez de préférence installer dans **USER EXTENSIONS**, car cela facilitera la mise à jour ultérieure.

Si vous avez des signes diacritiques dans votre nom d'utilisateur, essayez le chemin d'accès de **INKSCAPE EXTENSIONS** si vous rencontrez des difficultés pour exécuter Ink/Stitch.

### Ink/Stitch ne fonctionne pas!

**Confirmer le chemin d'installation**<br>

Vérifiez que vous avez bien extrait Ink/Stitch dans le bon répertoire. Si le  `dossier extensions utilisateur` ne fonctionne pas correctement, vous pouvez aussi essayer d'installer dans le `dossier extensions Inkscape`.
Vous pouvez retrouver l'adresse de ces dossiers sous  `Edition > Préférences > Système`.

**Vérifiez la version d'Ink/Stitch**

Verifiez si vous avez bien téléchargé Ink/Stitch pour Linux ([Installation](#download))

**Vérifiez propriétaire/droits d'accès**

Certains utilisateurs ont signaler des problèmes dus à un mauvais propriétaire ou de mauvais droits


### AttributeError: 'NoneType' object has no attribute 'title' in inkstitch.py

Cette erreur a été signalée par des utilisateurs qui ont installé Inkscape via snap. Snap est connu pour causer des problèmes d'installation d'Ink/Stitch dans Inkscape. Merci d'essayer une autre méthode d'installation. N'importe quelle méthode décrite ici [https://inkscape.org/](https://inkscape.org/releases/latest/) convient. 

### Certains dialogues Ink/Stitch disparaissent après quelques secondes ou n'apparaissent paas

#### Use X11

Ce problème peut être causé par wayland. Démarrez Inkscape avec la commande suivante:

```
export GDK_BACKEND=x11 && inkscape
```

Lorsque vous utilisez le package flatpak Inkscape, la commande ressemble à ceci :

```
flatpak --env=GDK_BACKEND=x11 run org.inkscape.Inkscape
```

#### Extension du délai  d'expiration pour mutter

Dans les  versions de mutter ≥ 3.35.92, vous pouvez définir le délai d'expiration utilisé pour vérifier si une fenêtre est toujours active. Ceci est également utile pour le  X-forwarding via SSH avec une latence élevée.

Par exemple, vous pouvez définir le délai d'attente à 60 s (60 000 ms) en utilisant :

```gsettings set org.gnome.mutter check-alive-timeout 60000```

### ImportError: libnsl.so.1: cannot open shared object file. No such file or directory

Installez la bibliothèque manquante. 

Par exemple sous Fedora **Fedora** installez libnsl avec la commande suivante.

```
sudo dnf install libnsl
```

### J'ai installé Ink/Stitch dans ma langue maternelle, mais les fenêtres de dialogue sont affichées en anglais!

Premièrement, il est possible que toutes les phrases n'aient pas été traduites. Ceci est indiqué par **certaines phrases de texte en anglais et d'autres dans votre langue maternelle**.

Si vous souhaitez terminer la traduction, consultez notre [description pour les traducteurs](/developers/localize/).

Ensuite, nous devons faire la distinction entre le menu Extension dans Inkscape et les fenêtres de dialogue.
La sélection du fichier ZIP a pour seule conséquence la traduction du menu Extension dans une certaine langue.
Les fenêtres de dialogue sont construites différemment. Elles utiliseront la langue de votre système d'exploitation.
Si Ink/Stitch n'est pas sûr de la langue à prendre en charge, il retombera sur l'anglais.
Vous pouvez indiquer explicitement à Inkscape d'utiliser votre langue maternelle comme suit:
  * Allez à Edition > Préférences > Interface (Ctrl + Shift + P)
  * choisissez votre langue
  * Redémarrez Inkscape

![Preferences > Interface](/assets/images/docs/fr/preferences_language.png)

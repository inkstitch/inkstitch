---
title: "Installer Ink/Stitch sur macos"
permalink: /fr/docs/install-macos/
excerpt: "Comment installer rapidement Ink/Stitch."
last_modified_at: 2025-01-04
toc: true
---
## Télécharger

Téléchargez la dernière version d'Ink/Stitch pour votre version de macOS :

<!-- <p><a href="{{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-x86_64.pkg" class="btn btn--info btn--large"><i class="fa fa-download " ></i> Download Ink/Stitch {{ site.github.latest_release.tag_name }} for macOS<br><span style="color:lightblue;"> Pour Monterey ou plus récent (Intel)</span></a></p>

<p><a href="{{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-arm64.pkg" class="btn btn--info btn--large"><i class="fa fa-download " ></i> Download Ink/Stitch {{ site.github.latest_release.tag_name }} for macOS<br><span style="color:lightblue;"> Pour Monterey ou plus récent (Arm)</span></a></p> -->

<p><a href="{{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-x86_64.pkg" class="btn btn--info btn--large"><i class="fa fa-download " ></i> Download Ink/Stitch {{ site.github.latest_release.tag_name }} for macOS<br><span style="color:lightblue;"> Pour Monterey ou plus récent</span></a></p>

<p><a href="{{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-high-sierra-catalina-osx-x86_64.pkg" class="btn btn--info btn--large"><i class="fa fa-download " ></i> Download Ink/Stitch {{ site.github.latest_release.tag_name }} for macOS<br><span style="color:lightblue;">High Sierra / Mojave / Catalina / Big Sur</span></a></p>

**Dernière version:** [Ink/Stitch {{ site.github.latest_release.tag_name }} ({{ site.github.latest_release.published_at | date: "%Y-%m-%d" }})](https://github.com/inkstitch/inkstitch/releases/latest)

## Installation

Ink/Stitch est une extension pour Inkscape. Téléchargez et installez  [Inkscape](https://inkscape.org/release/) Version 1.0.2 ou supérieure avant d'installer Ink/Stitch. Vérifiez que vous avez bien **installé et lancé Inkscape** avant d'installer Ink/Stitch. Sinon l'installation va échouer.
{: .notice--warning .bold--warning }

Si vous avez un processeur arm, vérifiez que Rosetta est installée  (avec `softwareupdate --install-rosetta --agree-to-license`).
{: .notice--warning }

**Monterey ou plus récent:** Lancez l'installateur en cliquant sur le fichier que vous avez téléchargé.

**High Sierra / Mojave / Catalina / Big Sur:** Suivre les [instructions pour les versions non notarisées](#xxxx-ne-peut-pas-être-ouvert-car-lidentité-du-développeur-ne-peut-pas-être-confirmée)

Cliquez sur `Continuer`.

![Install Ink/Stitch](/assets/images/docs/fr/macos-install/installer01.png)

Cliquez sur `Installer`.

![Install Ink/Stitch](/assets/images/docs/fr/macos-install/installer02.png)

 A l'invitation de saisir votre mot de passe, entrez votre mot de passe utilisateur et cliquez sur `Installer le logiciel`.

![Install Ink/Stitch](/assets/images/docs/fr/macos-install/installer03.png)

Dans certains cas, votre système vous demandera si vous autorisez l'installateur à sauvegarder des fichiers dans votre répertoire utilisateur (home directory). Ink/Stitch doit être installé dans le dossier des extensions d'Inkscape. Répondez donc  'Oui'  à la question.
{: .notice--info }

Votre installation est maintenant terminée.

![Install Ink/Stitch](/assets/images/docs/fr/macos-install/installer04.png)

A la dernière question : Voulez vous placer le fichier d'installation dans la corbeille?, répondez ce que vous voulez. Ink/Stitch n'en a plus besoin.

![Install Ink/Stitch](/assets/images/docs/fr/macos-install/installer05.png)

## Installation alternative avec  Homebrew

Homebrew est un gestionnaire de paquets pour MacOS. Pour plus d'information voir <https://brew.sh/>
{: .notice--info}

Merci de désinstaller Inkscape s'il a été installé auparavant.  Brew installera Inkscape avec l'extension Ink/Stitch 
{: .notice--warning }

Ouvrir un terminal et entrer la commande suivante:

```
brew install inkstitch
```

## Exécuter Ink/Stitch

Ouvrez Inkscape. Vous trouverez alors Ink/Stitch dans `Extensions > Ink/Stitch`.

![Ink/Stitch menu](/assets/images/docs/fr/macos-install/inkstitch-extensions-menu.png)

## Mise à jour

Quand une nouvelle version d'Ink/Stitch est disponible, téléchargez là et lancez l'installateur comme décrit ci-dessus. Cela supprimera aussi l'ancienne version.
Les installations antérieures à 2.1.0 doivent être supprimées manuellement. Il faut supprimer les fichiers et dossiers inkstitch* du dossier d'extensions.

**Astuce:** Inscrivez-vous aux news pour avoir connaissance des mises à jour d'Ink/Stitch:<br />
 <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [GitHub Feed on new Releases](https://github.com/inkstitch/inkstitch/releases.atom)<br>
 <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [Ink/Stitch News](/feed.xml)<br />
{: .notice--info }

<p class="notice--info" style="margin-top: -3.5em !important;">Ou regardez l'intégralité du projet sur GitHub:<br /><iframe style="display: inline-block;" src="https://ghbtns.com/github-btn.html?user=inkstitch&repo=inkstitch&type=watch&count=true&v=2" frameborder="0" scrolling="0" width="170px" height="20px"></iframe></p>

## Problème d'installation Ink/Stitch

### 'xxxx' ne peut pas être ouvert, car l'identité du développeur ne peut pas être confirmée

Ce message est montré lors de l'installation de la version pour les anciens systèmes MacOs ou lors de l'installation d'une version de développement.

* Control + Clic  sur le fichier téléchargé
* Choisir Ouvrir dans le menu  contextuel
* Si nécessaire, entrer votre identifiant et mot de  passe administrateur pour démarrer l'installation

### Si l'installation échoue

Nous vous offrons aussi la possibilité de télécharger un zip qui peut être extrait dans le dossier d'extension utilisateur (voir ci-dessous: vérifier le chemin d'installation)

<!-- Pour Monterey ou plus récent [dowload ZIP (intel)]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-x86_64.zip), [dowload ZIP (arm)]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-arm64.zip) -->

Pour Monterey ou plus récent [dowload ZIP]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-x86_64.zip)

Pour des versions plus anciennes de macOS [download ZIP]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-high-sierra-catalina-osx-x86_64.zip)

### Ink/Stitch ne fonctionne pas!

**Vérifier le chemin d'installation**

Vérifiez que vous avez bien extrait Ink/Stitch dans le bon répertoire. Si votre repertoire "Extensions utilisateur" ne fonctionne pas correctement, vous pouvez aussi essayer d'utiliser le repertoire des extensions d'Inkscape.
Vous pouvez trouver leur localisation sous `Inkscape > Preferences > Systeme`.

**Vérifier la  version**

Merci de vérifier que vous avez bien téléchargé la version d'Ink/Stitch compatible avec votre version macOS ([Télécharger](#télécharger)).

### J'ai installé Ink/Stitch mais le menu est grisé (désactivé)

C'est souvent le cas si une mauvaise version Ink/Stitch a été installée.
Veuillez vérifier si vous avez téléchargé la bonne version Ink/Stitch pour votre système d'exploitation.

### Les fenêtres de dialogue sont affichées en anglais!

Premièrement, il est possible que tous les textes n'aient pas été traduits. Ceci est le cas si **certaines parties sont en anglais et d'autres dans votre langue maternelle**.

Si vous souhaitez terminer la traduction, consultez notre [description pour les traducteurs](/developers/localize/).

Si Ink/Stitch n'est pas sûr de la langue à prendre en charge, il choisira l'anglais.
Vous pouvez indiquer explicitement à Inkscape d'utiliser votre langue maternelle comme suit:

  * Allez à Inkscape > Preferences > Interface (Ctrl + Shift + P)
  * Choisissez votre langue
  * Redémarrez Inkscape

![Preferences > Interface](/assets/images/docs/fr/preferences_language.png)

## Désinstaller Ink/Stitch

Dans Inkscape, allez à  `Inkscape > Préférences > Système` et cherchez dans ce tableau où se trouve votre dossier `Extensions utilisateur`.

![Extensions Utilisateur](/assets/images/docs/fr/extensions-folder-location-macos.jpg)

Supprimez chaque dossier ou fichier inkstitch*.

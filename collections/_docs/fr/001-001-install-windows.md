---
title: "Install Ink/Stitch"
permalink: /fr/docs/install-windows/
excerpt: "How to quickly install Ink/Stitch."
last_modified_at: 2020-03-01
toc: true
---
## Guide vidéo

Nous fournissons aussi aux débutants des tutoriels vidéo sur notre <i class="fab fa-youtube"></i> [chaine YouTube](https://www.youtube.com/channel/UCJCDCFuT_xQoI55e10HRiRw). Les vidéos sont en anglais. Mais il y a des sous-titres en français.

* <i class="fab fa-windows"></i> [Windows](https://www.youtube.com/watch?v=U5htzWZSjA8&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=4)

## Prérequis

* [Inkscape](https://inkscape.org/) Version 0.92.2 ou supérieure

C'est tout! Toutes les librairies python et dépendances externes sont incluses (en utilisant l'excellent [pyinstaller](http://www.pyinstaller.org)), de sorte que vous ne devriez pas avoir quoi que ce soit d'autre à installer.

## Installation rapide

### Télécharger
Télécharger, en tenant compte de votre plateforme.

<i class="fa fa-download " ></i> [Français]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-fr_FR.zip) <i class="fa fa-download " ></i> [Allemand]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-de_DE.zip) <i class="fa fa-download " ></i> [Anglais]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-en_US.zip) <i class="fa fa-download " ></i> [Finnois]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-fi_FI.zip) <i class="fa fa-download " ></i> [Italien]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-windows-it_IT.zip)
{: .inline-table }

**Dernière version:** [Ink/Stitch {{ site.github.latest_release.tag_name }} ({{ site.github.latest_release.published_at | date: "%Y-%m-%d" }})](https://github.com/inkstitch/inkstitch/releases/latest)

Le `LOCALE` sélectionné affecte les menus à l'intérieur d'Inkscape. Les dialogues d'Ink/Stitch sont dans la langue de votre OS (si cette langue est supportée).<br><br>Ink/Stitch n’existe pas dans votre langue? Aidez-nous à [traduire les dialogues dans votre langue maternelle](/fr/developers/localize/).
{: .notice--info }

### Installation

Dans Inkscape, allez à  `Edition > Préferences > Systeme` et cherchez dans ce tableau où se trouve votre dossier `Extensions utilisateur`.

![Extensions folder](/assets/images/docs/fr/extensions-folder-location-windows.jpg)

Décompressez l'archive Ink/Stitch **directement** dans ce dossier.

Ce dossier doit présenter une structure semblable à l'exemple ci-dessous (avec juste un tas de fichiers en plus):
![File Structure](/assets/images/docs/en/file_structure.png)

Redémarrez Inkscape.

Vous trouverez alors Ink/Stitch sous `Extensions > Ink/Stitch`.

## Mise à jour

 * Il faut d'abord effacer tous les fichiers de l'ancienne extension:<br />
   Ouvrez le répertoire des extensions et supprimez chaque dossier ou fichier inkstitch*.
 * Puis procédez comme ci-dessus.

**Astuce:** Inscrivez-vous aux news pour avoir connaissance des mises à jour d'Ink/Stitch:<br />
 <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [GitHub Feed on new Releases](https://github.com/inkstitch/inkstitch/releases.atom)<br>
 <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [Ink/Stitch News](/feed.xml)<br />
{: .notice--info }

<p class="notice--info" style="margin-top: -3.5em !important;">Or watch the project on GitHub:<br /><iframe style="display: inline-block;" src="https://ghbtns.com/github-btn.html?user=inkstitch&repo=inkstitch&type=watch&count=true&v=2" frameborder="0" scrolling="0" width="170px" height="20px"></iframe></p>

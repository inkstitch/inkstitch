---
title: "Install Ink/Stitch"
permalink: /fr/docs/install/
excerpt: "How to quickly install Ink/Stitch."
last_modified_at: 2020-03-01
toc: true
---
## Guide vidéo

Nous fournissons aussi aux débutants des tutoriels vidéo sur notre <i class="fab fa-youtube"></i> [chaine YouTube](https://www.youtube.com/channel/UCJCDCFuT_xQoI55e10HRiRw). Les vidéos sont en anglais. Mais il y a des sous-titres en français.

Pour le processus d'installation regarder la vidéo pour votre système d'exploitation
* <i class="fab fa-linux"></i> [Linux](https://www.youtube.com/watch?v=Dkb5UvsZUNg&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=2)
* <i class="fab fa-apple"></i> [macOS](https://www.youtube.com/watch?v=gmOVLNh9cu8&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=3)
* <i class="fab fa-windows"></i> [Windows](https://www.youtube.com/watch?v=U5htzWZSjA8&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=4)

## Prérequis

* [Inkscape](https://inkscape.org/) Version 0.92.2 ou supérieure

C'est tout! Toutes les librairies python et dépendances externes sont incluses (en utilisant l'excellent [pyinstaller](http://www.pyinstaller.org)), de sorte que vous ne devriez pas avoir quoi que ce soit d'autre à installer.

**Info:** Inkscape Version 0.92 ou supérieure, a une caractéristique vraiment essentielle: la "*boite de dialogue Objets*".<br>
Elle vous donne une liste hiérarchisée des objets de votre fichier SVG, dans leur ordre d'empilement. C'est vraiment important parce que l'ordre d'empilement dicte l'ordre dans lequel les formes seront brodées.<br><br>
Les versions 0.92.2 et supérieures vous permettent de [lier une touche](/fr/docs/customize/#shortcut-keys) aux nouvelles commandes, “monter” et “descendre”, que vous pouvez assigner aux touches "page haut", "page bas". Cela vous permettra de réordonner les objets dans le fichier SVG directement dand l'ordre de broderie. Cela marche beaucoup mieux que les anciennes commandes "monter" et "descendre".
{: .notice--info }

## Installation rapide

### 1. Télécharger
Télécharger, en tenant compte de votre plateforme.

Le `LOCALE` sélectionné affecte les menus à l'intérieur d'Inkscape. Les dialogues d'Ink/Stitch sont dans la langue de votre OS (si cette langue est supportée).

**Tip:** Ink/Stitch n’existe pas dans votre langue?<br>Aidez-nous à [traduire les dialogues dans votre langue maternelle](/fr/developers/localize/).
{: .notice--info }

Langage|Linux (64bit)|Windows|macOS (Catalina) [[?]](#macos)
---|---|---|---
**Allemand**|<i class="fa fa-download " ></i> [Linux]({{ site.github.releases_url }}/latest/download/inkstitch-refs-tags-{{ site.github.latest_release.tag_name }}-linux-de_DE.zip)|<i class="fa fa-download " ></i> [Windows]({{ site.github.releases_url }}/latest/download/inkstitch-refs-tags-{{ site.github.latest_release.tag_name }}-windows-de_DE.zip)|<i class="fa fa-download " ></i> [macOS]({{ site.github.releases_url }}/latest/download/inkstitch-refs-tags-{{ site.github.latest_release.tag_name }}-osx-de_DE-2413e616807472808f5ce86132e58016.zip)|
**Anglais**|<i class="fa fa-download " ></i> [Linux]({{ site.github.releases_url }}/latest/download/inkstitch-refs-tags-{{ site.github.latest_release.tag_name }}-linux-en_US-ff55eccaa4069d9cbcd2dd74890e3797.zip)|<i class="fa fa-download " ></i> [Windows]({{ site.github.releases_url }}/latest/download/inkstitch-refs-tags-{{ site.github.latest_release.tag_name }}-windows-en_US.zip)|<i class="fa fa-download " ></i> [macOS]({{ site.github.releases_url }}/latest/download/inkstitch-refs-tags-{{ site.github.latest_release.tag_name }}-osx-en_US.zip)|
**Finnois**|<i class="fa fa-download " ></i> [Linux]({{ site.github.releases_url }}/latest/download/inkstitch-refs-tags-{{ site.github.latest_release.tag_name }}-linux-fi_FI.zip)|<i class="fa fa-download " ></i> [Windows]({{ site.github.releases_url }}/latest/download/inkstitch-refs-tags-{{ site.github.latest_release.tag_name }}-windows-fi_FI.zip)|<i class="fa fa-download " ></i> [macOS]({{ site.github.releases_url }}/latest/download/inkstitch-refs-tags-{{ site.github.latest_release.tag_name }}-osx-fi_FI.zip)|
**Français**|<i class="fa fa-download " ></i> [Linux]({{ site.github.releases_url }}/latest/download/inkstitch-refs-tags-{{ site.github.latest_release.tag_name }}-linux-fr_FR.zip)|<i class="fa fa-download " ></i> [Windows]({{ site.github.releases_url }}/latest/download/inkstitch-refs-tags-{{ site.github.latest_release.tag_name }}-windows-fr_FR.zip)|<i class="fa fa-download " ></i> [macOS]({{ site.github.releases_url }}/latest/download/inkstitch-refs-tags-{{ site.github.latest_release.tag_name }}-osx-fr_FR.zip)|
{: .inline-table }

**Dernière version:** [Ink/Stitch {{ site.github.latest_release.tag_name }} ({{ site.github.latest_release.published_at | date: "%Y-%m-%d" }})](https://github.com/inkstitch/inkstitch/releases/latest)

### 2. Installation
 * Dans Inkscape, aller à  `Edition > Préferences > Systeme` et cherchez où se trouve votre dossier `Extensions`.
 * Decompresser l'archive Ink/Stitch **directement** dans ce dossier.<br />
  Ce dossier doit présenter une structure semblable à l'exemple ci-dessous (avec juste un tas de fichiers en plus):
   ![File Structure](/assets/images/docs/en/file_structure.png)
 * Redémarrez Inkscape.
 * Vous trouverez alors Ink/Stitch sous `Extensions > Ink/Stitch`.

#### Linux:

 ```
 $ cd ~/.config/inkscape/extensions
 $ unzip ~/Downloads/inkstitch-refs-tags-{{ site.github.latest_release.tag_name }}-linux-fr_FR.zip
 ```

#### macOS

macOS nécessite une méthode de téléchargement spéciale. Si vous téléchargez la version Ink/Stitch via le navigateur, vous recevrez des messages tels que **"Impossible d'ouvrir 'xxxx', car cette app provient d'un développeur non identifié"**. Ce message apparaît car nous n'avons pas acheté de certificat auprès d'Apple. Vous pouvez éviter ces messages en téléchargeant Ink/Stitch avec `curl`:

```
$ cd ~/.config/inkscape/extensions
$ curl -LJO {{ site.github.releases_url }}/latest/download/inkstitch-refs-tags-{{ site.github.latest_release.tag_name }}-osx-fr_FR.zip
$ unzip inkstitch-refs-tags-{{ site.github.latest_release.tag_name }}-osx-fr_FR.zip
```

**Info:** Ink/Stitch pour macOS fonctionne actuellement seulement avec Catalina (10.15) et supérieur.
Pour les anciennes versions de macOS, utilisez Ink/Stitch 1.26.2 (2019-08-20):
<br>**Allemand:**
<i class="fa fa-download " ></i> [Sierra]({{ site.github.releases_url }}/v1.26.2/download/inkstitch-v1.26.2-osx-sierra-x86_64-de_DE.tar.gz),
<i class="fa fa-download " ></i> [High Sierra]({{ site.github.releases_url }}/v1.26.2/download/inkstitch-v1.26.2-osx-high_sierra-x86_64-de_DE.tar.gz),
<i class="fa fa-download " ></i> [Mojave]({{ site.github.releases_url }}/v1.26.2/download/inkstitch-v1.26.2-osx-mojave-x86_64-de_DE.tar.gz)
<br>**Anglais:**
<i class="fa fa-download " ></i> [Sierra]({{ site.github.releases_url }}/v1.26.2/download/inkstitch-v1.26.2-osx-sierra-x86_64-en_US.tar.gz),
<i class="fa fa-download " ></i> [High Sierra]({{ site.github.releases_url }}/v1.26.2/download/inkstitch-v1.26.2-osx-high_sierra-x86_64-en_US.tar.gz),
<i class="fa fa-download " ></i> [Mojave]({{ site.github.releases_url }}/v1.26.2/download/inkstitch-v1.26.2-osx-mojave-x86_64-en_US.tar.gz)
<br>**Français:**
<i class="fa fa-download " ></i> [Sierra]({{ site.github.releases_url }}/v1.26.2/download/inkstitch-v1.26.2-osx-sierra-x86_64-fr_FR.tar.gz),
<i class="fa fa-download " ></i> [High Sierra]({{ site.github.releases_url }}/v1.26.2/download/inkstitch-v1.26.2-osx-high_sierra-x86_64-fr_FR.tar.gz),
<i class="fa fa-download " ></i> [Mojave]({{ site.github.releases_url }}/v1.26.2/download/inkstitch-v1.26.2-osx-mojave-x86_64-fr_FR.tar.gz)
{: .notice--warning }

#### Windows

 * Faites afficher le répertoire caché AppData (aller à  `C:\Users\%USERNAME%\`, par exemple `C:\Users\Janet`)
 * Dézippez dans `C:\Users\%USERNAME%\AppData\Roaming\inkscape\extensions`

## Mise à jour

 * Il faut d'abord effacer tous les fichiers de l'ancienne extension:<br />
   Ouvrez le répertoire des extensions et supprimez chaque dossier ou fichier inkstitch*.
 * Puis procédez comme ci-dessus.

**Astuce:** Inscrivez-vous aux news pour avoir connaissance des mises à jour d'Ink/Stitch:<br />
 <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [GitHub Feed on new Releases](https://github.com/inkstitch/inkstitch/releases.atom)<br>
 <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [Ink/Stitch News](/feed.xml)<br />
{: .notice--info }

<p class="notice--info" style="margin-top: -3.5em !important;">Or watch the project on GitHub:<br /><iframe style="display: inline-block;" src="https://ghbtns.com/github-btn.html?user=inkstitch&repo=inkstitch&type=watch&count=true&v=2" frameborder="0" scrolling="0" width="170px" height="20px"></iframe></p>

## Installation manuelle

C'est possible d'installer Ink/Stitch manuellemnt. Ce n'est cependant pas recommandé - A moins que vous vouliez participer au développement de l'extension.
Dans ce cas jetez un coup d'oeil à la section [documentation développeur](/fr/developers/inkstitch/manual-setup/).

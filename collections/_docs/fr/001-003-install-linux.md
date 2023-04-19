---
title: "Installer Ink/Stitch pour linux"
permalink: /fr/docs/install-linux/
excerpt: "Comment installer rapidement Ink/Stitch."
last_modified_at: 2022-01-12
toc: true
---
{% comment %}
## Guide vidéo

Nous fournissons aussi aux débutants des tutoriels vidéo sur notre <i class="fab fa-youtube"></i> [chaine YouTube](https://www.youtube.com/c/InkStitch). Les vidéos sont en anglais. Mais il y a des sous-titres en français.

* <i class="fab fa-linux"></i> [Linux](https://www.youtube.com/watch?v=Dkb5UvsZUNg&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=2)
{% endcomment %}

## Prérequis

Ink/Stitch est une extension pour Inkscape. Téléchargez et installez  [Inkscape](https://inkscape.org/release/) Version 1.0.2 ou supérieure avant d'installer Ink/Stitch.

## Installation

{% assign tag_name = site.github.latest_release.tag_name %}
Téléchargez la dernière version disponible pour Linux (Ink/Stitch {{ tag_name }}).

{% assign tag_name = tag_name | slice: 1,tag_name.size %}

<div class="instructions">
  <p class="download-button"><a href="{{ site.github.releases_url }}/latest/download/inkstitch_{{ tag_name }}_amd64.deb" class="btn btn--info btn--large"><i class="fa fa-download " ></i> Télécharger le paquet DEB </a></p>
  <input type="checkbox" id="deb-instructions" />
  <label for="deb-instructions"> Instructions  d'installation<p class="down">▿</p><p class="up">▵</p></label>
  <section>
    <p class="headline">Installation du paquet deb </p>
    <p>Double cliquez sur le fichier deb téléchargé et suivez le processus d'installation.</p>
  </section>
</div>

<div class="instructions">
  <p class="download-button"><a href="{{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-1.x86_64.rpm" class="btn btn--info btn--large"><i class="fa fa-download " ></i> Télécharger le paquet RPM </a></p>
  <input type="checkbox" id="rpm-instructions" />
  <label for="rpm-instructions">Instructions d'installation <p class="down">▿</p><p class="up">▵</p></label>
  <section>
    <p class="headline">Installer le paquet rpm </p>
    <p>Double cliquez sur le fichier rpm téléchargé et suivez le processus d'installation.</p>
    <p><a href="/assets/files/inkstitch.gpg">GPG-Key</a></p>
  </section>
</div>

<div class="instructions">
  <p class="download-button"><a href="{{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-linux.sh" class="btn btn--info btn--large"><i class="fa fa-download " ></i> Télécharger le script d'installation </a></p>
  <input type="checkbox" id="installer-instructions" />
  <label for="installer-instructions">Instructions  d'installation <p class="down">▿</p><p class="up">▵</p></label>
  <section>
    <p class="headline"> Installer avec le script d'installation</p>
    <p>Utilisez cette version si vous utilisez la version AppImage d'Inkscape ou si vous voulez installer  Ink/Stitch uniquement pour votre propre utilisateur. Ce script est aussi utile si votre système ne supporte pas les paquets deb ou rpm.</p>
    <p>Ouvrez votre terminal et naviguez jusqu'au répertoire qui contient le script que vous avez téléchargé, par exemple</p>
    <div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>cd Downloads</code></pre></div></div>
    <p>Exécutez la commande suivante</p>
    <div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>sh inkstitch-{{ tag_name }}-linux.sh</code></pre></div></div>
    <p><b>Option pour les experts</b></p>
    <p> Ce script va tenter de déterminer automatiquement où installer les extensions utilisateurs d'Inkscape. S'il se trompe, vous pouvez modifier une de ces variables d'environnement:</p>
    <ul>
      <li>
        <p><code class="language-plaintext highlighter-rouge">INKSCAPE_PATH (ex: /usr/bin/inkscape)</code></p>
        <p> Le chemin vers l'exécutable inkscape.  Le script demandera à ce programme où installer les extensions en lui transmettant l'argument --user-data-directory.</p>
      </li>
      <li>
        <p><code class="language-plaintext highlighter-rouge">INKSCAPE_EXTENSIONS_PATH (ex: $HOME/.config/inkscape/extensions)</code></p>
        <p>Le chemin vers le repertoire d'extensions inkscape.  Utilisez cela pour contourner la methode  --user-data-directory  et spécifier vous même le repertoire.</p>
      </li>
    </ul>
    <p>Si vous preferrez l'installer vous même, exécutez ce script avec  <code class="language-plaintext highlighter-rouge">--extract</code> pour produire le fichier original inkstitch-&lt;version&gt;.tar.xz dans le répertoire courant.</p>
  </section>
</div>

<div class="instructions">
  <p class="download-button"><a href="{{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-linux.tar.xz" class="btn btn--info btn--large"><i class="fa fa-download " ></i> Télécharger l'archive tar.xz </a></p>
  <input type="checkbox" id="archive-instructions" />
  <label for="archive-instructions">Instructions d'installation <p class="down">▿</p><p class="up">▵</p></label>
  <section>
  <p class="headline">Installer avec l'archive  tar.xz </p>
  <p>Allez à  <code class="language-plaintext highlighter-rouge">Edition > Préférences > Système</code> et vérifiez où se trouve votre dossier <code class="language-plaintext highlighter-rouge"> Extensions utilisateur</code>.</p>
  <p><img alt="Extensions folder location" src="/assets/images/docs/fr/extensions-folder-location-linux.jpg" /></p>
  <p>Décompressez l'archive Ink/Stitch dans ce dossier.</p>
  <div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>$ cd ~/.config/inkscape/extensions
$ tar -xvf ~/Downloads/inkstitch-{{ tag_name }}-linux.tar.xz</code></pre></div></div>
  </section>
</div>

**Dernière version:** [Ink/Stitch {{ site.github.latest_release.tag_name }} ({{ site.github.latest_release.published_at | date: "%Y-%m-%d" }})](https://github.com/inkstitch/inkstitch/releases/latest)

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

### Les dialogues Ink/Stitch disparaissent après quelques secondes

Ce problème peut être causé par wayland. Démarrez Inkscape avec la commande suivante: `export GDK_BACKEND=x11 && inkscape`.

Cette solution de contournement doit être utilisé jusqu'à ce que nous ayons déployées toutes les applications Ink/Stitch dans l'environnement electron.


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

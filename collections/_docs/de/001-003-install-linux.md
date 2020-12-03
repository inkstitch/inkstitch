---
title: "Installation von Ink/Stitch"
permalink: /de/docs/install-linux/
excerpt: "Wie wird Ink/Stitch installiert."
last_modified_at: 2020-12-03
toc: true
---
## Video-Anleitung

Wir stellen Anfänger-Tutorials auf unserem <i class="fab fa-youtube"></i> [YouTube Kanal](https://www.youtube.com/channel/UCJCDCFuT_xQoI55e10HRiRw) zur Verfügung. Die Videos sind in englischer Sprache. Deutsche Untertitel können zugeschaltet werden. Schaue den Installationsprozess für <i class="fab fa-linux"></i> [Linux](https://www.youtube.com/watch?v=Dkb5UvsZUNg&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=2) an.

## Vorraussetzung

* [Inkscape](https://inkscape.org/) Version 0.92.2 oder höher (einschließlich [Inkscape](https://inkscape.org/release/inkscape-1.0/?latest=1) Version 1.0 RC)

Das ist alles! Alle Python-Bibliotheken und externen Abhängigkeiten werden mitgeliefert (durch den ausgezeichneten [pyinstaller](http://www.pyinstaller.org)), so dass keine weiteren Installationen notwendig sind.

## Installation

### Herunterladen
Lade das passende Archiv für deine Sprache herunter.

<i class="fa fa-download " ></i> [Deutsch]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-linux-de_DE.zip) <i class="fa fa-download " ></i> [Englisch]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-linux-en_US.zip) <i class="fa fa-download " ></i> [Finnisch]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-linux-fi_FI.zip) <i class="fa fa-download " ></i> [Französisch]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-linux-fr_FR.zip) <i class="fa fa-download " ></i> [Italienisch]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-linux-it_IT.zip)

**Aktuelle Version:** {{ site.github.latest_release.published_at | date: "%d.%m.%Y" }} [Ink/Stitch {{ site.github.latest_release.tag_name }})](https://github.com/inkstitch/inkstitch/releases/latest)

Die ausgewählte Sprache bezieht sich nur auf die Menüs von Inkscape. Ink/Stitch-Dialogfenster werden in der Sprache des Betriebssystems dargestellt (sofern diese unterstützt wird).<br><br>Deine Sprache ist nicht verfügbar oder unvollständig? Hilf uns [die Dialoge und Menüs in deine Muttersprache zu übersetzen](/de/developers/localize/).
{: .notice--info }

### Dateien entpacken

Öffne Inkscape. Unter `Bearbeiten > Einstellungen > System` (Inkscape 0.9) oder `Inkscape > Einstellungen > System > Benutzererweiterungen` (Inkscape 1.0) kannst du einsehen, wo sich der Installationsordner befindet.

Entpacke das Ink/Stitch-Archiv **direkt** in diesen Ordner.

 ```
 $ cd ~/.config/inkscape/extensions
 $ unzip ~/Downloads/inkstitch-{{ site.github.latest_release.tag_name }}-linux-de_DE.zip
 ```

Die Dateistruktur sollte ungefähr dem Bild unten entsprechen (aber ein paar mehr Dateien enthalten):

![File Structure](/assets/images/docs/en/file_structure.png)

### Ink/Stitch öffnen
Starte Inkscape neu.

Ink/Stitch befindet sich nun unter `Erweiterungen > Ink/Stitch`.

## Aktualisierung

Lösche zunächst die alte Ink/Stitch Installation. Gehe in das Erweiterungsverzeichnis und entferne alle Dateien und Ordner, die mit inkstitch* beginnen.

Dann folge erneut der Installationsbeschreibung auf dieser Seite.

**Tipp:** Abonniere den News-Feed-Kanal, um die Aktualisierungen von Ink/Stitch zu verfolgen:<br>
 <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [GitHub Feed on new Releases](https://github.com/inkstitch/inkstitch/releases.atom)<br>
 <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [Ink/Stitch News](/feed.xml)<br> 
{: .notice--info }

<p class="notice--info" style="margin-top: -3.5em !important;">Oder schaue das Projekt auf GitHub an:<br><iframe style="display: inline-block;" src="https://ghbtns.com/github-btn.html?user=inkstitch&repo=inkstitch&type=watch&count=true&v=2" frameborder="0" scrolling="0" width="170px" height="20px"></iframe></p>

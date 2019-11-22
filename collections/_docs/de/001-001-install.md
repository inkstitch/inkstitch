---
title: "Installation von Ink/Stitch"
permalink: /de/docs/install/
excerpt: "Wie wird Ink/Stitch installiert."
last_modified_at: 2019-11-22
toc: true
---

**Info:** Wir stellen auch Anfänger-Tutorials auf unserem <i class="fab fa-youtube"></i> [YouTube Kanal](https://www.youtube.com/channel/UCJCDCFuT_xQoI55e10HRiRw) zur Verfügung.
Für den Installationsprozess, wähle das Video für
<i class="fab fa-linux"></i>&nbsp;[Linux](https://www.youtube.com/watch?v=Dkb5UvsZUNg&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=2),
<i class="fab fa-apple"></i>&nbsp;[macOS](https://www.youtube.com/watch?v=gmOVLNh9cu8&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=3) oder
<i class="fab fa-windows"></i>&nbsp;[Windows](https://www.youtube.com/watch?v=U5htzWZSjA8&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=4).<br /><br />
Die Videos sind in englischer Sprache. Deutsche Untertitel können zugeschaltet werden.
{: .notice--info }

## Vorraussetzung

* [Inkscape](https://inkscape.org/) Version 0.92.2 oder höher
* Moderner Browser für die Druckvorschau

Das ist alles! Alle Python-Bibliotheken und externen Abhängigkeiten sind schon dabei (durch den ausgezeichneten [pyinstaller](http://www.pyinstaller.org)), so dass nichts weiteres eingerichtet werden muss.

**Info:** Inkscape in der Version 0.92 oder höher hat eine wirklich wichtige Funktion: *Objekte*.<br>
Dies zeigt eine hierarchische Liste von Objekten in der SVG-Datei an, die in ihrer Stapelfolge aufgeführt sind. Dies ist sehr wichtig, da die Auflistung die Reihenfolge bestimmt, in der die Formen gestickt werden.<br><br>
Inkscape Versionen 0.92.2 und höher lassen [Kurzbefehle](/de/docs/customize/#tastenkürzel) zu, "nach oben" und "nach unten", denen Pfeil-Oben und Pfeil-Unten zugwiesen werden können. Dadurch ist es moglich, Objekte in der SVG-Datei beliebig neu zu ordnen, wodurch man direkt die Reihenfolge ändern kann. Es funktioniert viel einfacher als die Standardbefehle "nach oben" und "nach unten".
{: .notice--info}

## Schnelleinrichtung

### 1. Herunterladen
Lade das passende Archiv für deine Plattform herunter.

Die ausgewählte `SPRACHE` bezieht sich nur auf die Menüs von Inkscape. Ink/Stitch-Dialogfenster werden in der Sprache des Betriebssystems dargestellt (sofern diese unterstützt wird).

**Tip:** Deine Sprache ist nicht verfügbar oder unvollständig?<br>Hilf uns [die Dialoge und Menüs in deine Muttersprache zu übersetzen](/de/developers/localize/).
{: .notice--info }

Sprache|Linux (64bit)|Windows|macOS
---|---|---|---
**Deutsch**|<i class="fa fa-download " ></i> [Linux]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-linux-x86_64-de_DE.tar.gz)|<i class="fa fa-download " ></i> [Windows]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-win32-de_DE.zip)|<i class="fa fa-download " ></i> [Sierra]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-sierra-x86_64-de_DE.tar.gz)<br><i class="fa fa-download " ></i> [High Sierra]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-high_sierra-x86_64-de_DE.tar.gz)<br><i class="fa fa-download " ></i> [Mojave + Catalina]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-mojave-x86_64-de_DE.tar.gz)|
**Englisch**|<i class="fa fa-download " ></i> [Linux]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-linux-x86_64-en_US.tar.gz)|<i class="fa fa-download " ></i> [Windows]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-win32-en_US.zip)|<i class="fa fa-download " ></i> [Sierra]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-sierra-x86_64-en_US.tar.gz)<br><i class="fa fa-download " ></i> [High Sierra]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-high_sierra-x86_64-en_US.tar.gz)<br><i class="fa fa-download " ></i> [Mojave + Catalina]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-mojave-x86_64-en_US.tar.gz)|
**Französisch**|<i class="fa fa-download " ></i> [Linux]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-linux-x86_64-fr_FR.tar.gz)|<i class="fa fa-download " ></i> [Windows]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-win32-fr_FR.zip)|<i class="fa fa-download " ></i> [Sierra]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-sierra-x86_64-fr_FR.tar.gz)<br><i class="fa fa-download " ></i> [High Sierra]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-high_sierra-x86_64-fr_FR.tar.gz)<br><i class="fa fa-download " ></i> [Mojave + Catalina]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-mojave-x86_64-fr_FR.tar.gz)|
{: .inline-table }

**Info:** Ink/Stitch für macOS funktioniert derzeit nur mit Sierra (10.12) oder höher.
{: .notice--warning }

*Aktuelle Version: [Ink/Stitch {{ site.github.latest_release.tag_name }} ({{ site.github.latest_release.published_at | date: "%d.%m.%Y"  }})](https://github.com/inkstitch/inkstitch/releases/latest)*

### 2. Installation
 * Öffne Inkscape. In `Bearbeiten > Einstellungen > System` kannst du sehen, wo sich der Ordner "Benutzererweiterungen" befindet.
 * Entpacke das Ink/Stitch-Archiv **direkt** in diesen Ordner.
   Die Dateistruktur sollte ungefähr dem Bild unten entsprechen (aber ein paar mehr Dateien enthalten):
   ![File Structure](/assets/images/docs/en/file_structure.png)
 * Starte Inkscape neu.
 * Ink/Stitch befindet sich nun unter `Erweiterungen > Ink/Stitch`.

#### Beispiel unter Linux und macOS:

```
$ cd ~/.config/inkscape/extensions
$ tar zxf ~/Downloads/inkstich-v1.0.0-Linux-x86_64.tar.gz
```

#### Beispiel unter Windows

* Öffne das AppData-Verzeichnis (gehe zu `C:\Users\%USERNAME%\`, zum Beispiel `C:\Users\Janet`
* Entpackt wird die Zip-Datei unter `C:\Benutzer\%USERNAME%\AppData\Roaming\inkscape\extensions`

## Aktualisierung

 * Möglicherweise muss man zuerst die alten Ink/Stitch-Dateien löschen:<br>
   Gehe in das Erweiterungsverzeichnis und entferne die alle Dateien und Ordner, die mit inkstitch* beginnen.
 * Dann gehe wie oben vor.

**Tipp:** Abonniere den News-Feed-Kanal, um die Aktualisierungen von Ink/Stitch zu verfolgen:<br>
 <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [GitHub Feed on new Releases](https://github.com/inkstitch/inkstitch/releases.atom)<br>
 <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [Ink/Stitch News](/feed.xml)<br> 
{: .notice--info }

<p class="notice--info" style="margin-top: -3.5em !important;">Oder schaue das Projekt auf GitHub an:<br><iframe style="display: inline-block;" src="https://ghbtns.com/github-btn.html?user=inkstitch&repo=inkstitch&type=watch&count=true&v=2" frameborder="0" scrolling="0" width="170px" height="20px"></iframe></p>

## Manuelle Installation

Es ist auch möglich Ink/Stitch manuell zu installieren. Es wird jedoch nicht empfohlen - es sei denn, man möchte bei der Entwicklung der Erweiterung helfen.
In diesem Fall lies den Abschnitt [Manuelle Installation](/de/developers/inkstitch/manual-setup/).


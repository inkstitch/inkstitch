---
title: "Installation von Ink/Stitch für macOS"
permalink: /de/docs/install-macos/
excerpt: "Wie wird Ink/Stitch installiert."
last_modified_at: 2020-12-03
toc: true
---
## Video-Anleitung

Wir stellen Anfänger-Tutorials auf unserem <i class="fab fa-youtube"></i> [YouTube Kanal](https://www.youtube.com/channel/UCJCDCFuT_xQoI55e10HRiRw) zur Verfügung. Die Videos sind in englischer Sprache. Deutsche Untertitel können zugeschaltet werden.

Schaue den Installationsprozess für <i class="fab fa-apple"></i> [macOS](https://www.youtube.com/watch?v=gmOVLNh9cu8&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=3) an.

**Warnung:** Das Video für macOS-Nutzer ist nicht mehr aktuell. Bitte beachte ["Zusätzliche Schritte für Catalina / Big Sur"](#zusätzliche-schritte-für-catalina--big-sur).
{: .notice--warning }

## Vorraussetzung

* [Inkscape](https://inkscape.org/) Version 0.92.2 oder höher (einschließlich [Inkscape](https://inkscape.org/release/inkscape-1.0/?latest=1) Version 1.0 RC)

Das ist alles! Alle Python-Bibliotheken und externen Abhängigkeiten werden mitgeliefert, so dass keine weiteren Installationen notwendig sind.

## Installation

### Herunterladen
Lade das passende Archiv für deine Sprache.

Sprache|macOS Catalina / Big Sur | Sierra* | High Sierra* | Mojave*
---|---|---|---
**English**|<i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-en_US.zip)|<i class="fa fa-download " ></i> [Sierra]({{ site.github.releases_url }}/download/v1.26.2/inkstitch-v1.26.2-osx-sierra-x86_64-en_US.tar.gz)|<i class="fa fa-download " ></i> [High Sierra]({{ site.github.releases_url }}/download/v1.26.2/inkstitch-v1.26.2-osx-high_sierra-x86_64-en_US.tar.gz)|<i class="fa fa-download " ></i> [Mojave]({{ site.github.releases_url }}/download/v1.26.2/inkstitch-v1.26.2-osx-mojave-x86_64-en_US.tar.gz)|
**Finnish**|<i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-fi_FI.zip)|
**French**|<i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-fr_FR.zip)|<i class="fa fa-download " ></i> [Sierra]({{ site.github.releases_url }}/download/v1.26.2/inkstitch-v1.26.2-osx-sierra-x86_64-fr_FR.tar.gz)|<i class="fa fa-download " ></i> [High Sierra]({{ site.github.releases_url }}/download/v1.26.2/inkstitch-v1.26.2-osx-high_sierra-x86_64-fr_FR.tar.gz)|<i class="fa fa-download " ></i> [Mojave]({{ site.github.releases_url }}/download/v1.26.2/inkstitch-v1.26.2-osx-mojave-x86_64-fr_FR.tar.gz)|
**German**|<i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-de_DE.zip)|<i class="fa fa-download " ></i> [Sierra]({{ site.github.releases_url }}/download/v1.26.2/inkstitch-v1.26.2-osx-sierra-x86_64-de_DE.tar.gz)|<i class="fa fa-download " ></i> [High Sierra]({{ site.github.releases_url }}/download/v1.26.2/inkstitch-v1.26.2-osx-high_sierra-x86_64-de_DE.tar.gz)|<i class="fa fa-download " ></i> [Mojave]({{ site.github.releases_url }}/download/v1.26.2/inkstitch-v1.26.2-osx-mojave-x86_64-de_DE.tar.gz)|
**Italian**|<i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-it_IT.zip)|
{: .inline-table }

\* Es gibt keine aktuelle Ink/Stitch Version für Sierra, High Sierra or Mojave. Die hier angebotenen Dateien stammen aus der Ink/Stitch Version v1.26.2 (20.08.2019).

**Aktuelle Version:** {{ site.github.latest_release.published_at | date: "%d.%m.%Y"  }} [Ink/Stitch {{ site.github.latest_release.tag_name }}](https://github.com/inkstitch/inkstitch/releases/latest)

Die ausgewählte Sprache bezieht sich nur auf die Menüs von Inkscape. Ink/Stitch-Dialogfenster werden in der Sprache des Betriebssystems dargestellt (sofern diese unterstützt wird).<br><br>Deine Sprache ist nicht verfügbar oder unvollständig? Hilf uns [die Dialoge und Menüs in deine Muttersprache zu übersetzen](/de/developers/localize/).
{: .notice--info }

### Dateien entpacken
Öffne Inkscape. Unter `Bearbeiten > Einstellungen > System` (Inkscape 0.9) oder `Inkscape > Einstellungen > System > Benutzererweiterungen` (Inkscape 1.0) kannst du einsehen, wo sich der Installationsordner befindet.

Entpacke das Ink/Stitch-Archiv **direkt** in diesen Ordner. Die Dateistruktur sollte ungefähr dem Bild unten entsprechen (aber ein paar mehr Dateien enthalten):

![File Structure](/assets/images/docs/en/file_structure.png)

### Zusätzliche Schritte für Catalina / Big Sur

Neuere macOS Versionen rufen eine Fehlermeldung hervor, wenn Ink/Stitch durch das Browserfenster geöffnet wird: `'xxxx' kann nicht geöffnet werden, weil es von einem nicht verifizierten Entwickler stammt`.

Um diese Fehlermeldung zu vermeiden, öffne die Terminal App. Klicke auf die kleine Lupe am oberen rechten Rand der Menüleiste (oder <key>Cmd (⌘)</key>+<key>Leerzeichen</key>). Suche nach `Terminal` und öffne die Anwendung.

Anschließend muss in die Befehlszeile folgende Zeile eingegeben werden:

```
xattr -r -d com.apple.quarantine ~/Library/Application\ Support/org.inkscape.Inkscape/config/inkscape/extensions/
```

Falls dein Installationspfad für Erweiterungen vom Standard abweicht, ersetzte `~/Library/Application\ Support/org.inkscape.Inkscape/config/inkscape/extensions/` durch den Pfad der in Inkscape unter `Inkscape > Preferences > System` eingetragen ist).

Nutzer von **Big Sur** müssen noch weitere Befehle eingeben um die Installation abzuschließen:

```
cd ~/Library/Application\ Support/org.inkscape.Inkscape/config/inkscape/extensions/
cd inkstitch/bin
ln -s libpython2.7.dylib libc.dylib
```

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

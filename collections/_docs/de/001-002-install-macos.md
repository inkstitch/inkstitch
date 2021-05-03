---
title: "Installation von Ink/Stitch für macOS"
permalink: /de/docs/install-macos/
excerpt: "Wie wird Ink/Stitch installiert."
last_modified_at: 2021-05-03
toc: true
---
## Video-Anleitung

Wir stellen Anfänger-Tutorials auf unserem <i class="fab fa-youtube"></i> [YouTube Kanal](https://www.youtube.com/channel/UCJCDCFuT_xQoI55e10HRiRw) zur Verfügung. Die Videos sind in englischer Sprache. Deutsche Untertitel können zugeschaltet werden.

Schaue den Installationsprozess für <i class="fab fa-apple"></i> [macOS](https://www.youtube.com/watch?v=gmOVLNh9cu8&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=3) an.

**Warnung:** Das Video für macOS-Nutzer ist nicht mehr aktuell. Bitte beachte ["Zusätzliche Schritte für Catalina / Big Sur"](#zusätzliche-schritte-für-catalina--big-sur).
{: .notice--warning }

## Vorraussetzung

* [Inkscape](https://inkscape.org/) Version 0.92.2 oder höher (einschließlich [Inkscape](https://inkscape.org/release/inkscape-1.0/?latest=1) Version 1.0.1)

Das ist alles! Alle Python-Bibliotheken und externen Abhängigkeiten werden mitgeliefert, so dass keine weiteren Installationen notwendig sind.

## Installation

### Herunterladen
Lade das passende Archiv für deine Sprache herunter.

Sprache| Catalina & Big Sur | High Sierra & Mojave | Sierra & El Capitan
---|---|---|---
**Deutsch** | <i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-de_DE.zip) | <i class="fa fa-download " ></i> [High Sierra / Mojave]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-mojave-de_DE.zip)|<i class="fa fa-download " ></i> [Sierra / El Capitan]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-sierra-de_DE.zip)
**Englisch** | <i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-en_US.zip) | <i class="fa fa-download " ></i> [High Sierra / Mojave]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-mojave-en_US.zip)|<i class="fa fa-download " ></i> [Sierra / El Capitan]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-sierra-en_US.zip)
**Finnisch** | <i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-fi_FI.zip) | <i class="fa fa-download " ></i> [High Sierra / Mojave]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-mojave-fi_FI.zip)|<i class="fa fa-download " ></i> [Sierra / El Capitan]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-sierra-fi_FI.zip)
**Französisch** | <i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-fr_FR.zip) | <i class="fa fa-download " ></i> [High Sierra / Mojave]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-mojave-fr_FR.zip)|<i class="fa fa-download " ></i> [Sierra / El Capitan]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-sierra-fr_FR.zip)
**Italienisch** | <i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-it_IT.zip) | <i class="fa fa-download " ></i> [High Sierra / Mojave]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-mojave-it_IT.zip)|<i class="fa fa-download " ></i> [Sierra / El Capitan]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-sierra-it_IT.zip)
**Japanisch** | <i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-ja_JP.zip) | <i class="fa fa-download " ></i> [High Sierra / Mojave]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-mojave-ja_JP.zip)|<i class="fa fa-download " ></i> [Sierra / El Capitan]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-sierra-ja_JP.zip)
**Niederländisch** | <i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-nl_NL.zip) | <i class="fa fa-download " ></i> [High Sierra / Mojave]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-mojave-nl_NL.zip)|<i class="fa fa-download " ></i> [Sierra / El Capitan]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-sierra-nl_NL.zip)
**Russisch** | <i class="fa fa-download " ></i> [Catalina / Big Sur]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-ru_RU.zip) | <i class="fa fa-download " ></i> [High Sierra / Mojave]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-mojave-ru_RU.zip)|<i class="fa fa-download " ></i> [Sierra / El Capitan]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx-sierra-ru_RU.zip)
{: .inline-table }

**Aktuelle Version:** {{ site.github.latest_release.published_at | date: "%d.%m.%Y"  }} [Ink/Stitch {{ site.github.latest_release.tag_name }}](https://github.com/inkstitch/inkstitch/releases/latest)

Die ausgewählte Sprache bezieht sich nur auf die Menüs von Inkscape. Ink/Stitch-Dialogfenster werden in der Sprache des Betriebssystems dargestellt (sofern diese unterstützt wird).<br><br>Deine Sprache ist nicht verfügbar oder unvollständig? Hilf uns [Ink/Stitch in deine Muttersprache zu übersetzen](/de/developers/localize/).
{: .notice--info }

### Dateien entpacken
Öffne Inkscape.

Unter `Bearbeiten > Einstellungen > System > Benutzererweiterungen` kannst du einsehen, wo sich der Installationsordner befindet.

![](/assets/images/docs/de/extensions-folder-location-macos.jpg)

Entpacke das Ink/Stitch-Archiv in diesen Ordner.

### Zusätzliche Schritte für Catalina / Big Sur

Neuere macOS Versionen rufen eine Fehlermeldung hervor, wenn Ink/Stitch durch das Browserfenster geöffnet wird: `'xxxx' kann nicht geöffnet werden, weil es von einem nicht verifizierten Entwickler stammt`.

Um diese Fehlermeldung zu vermeiden, öffne die Terminal App. Klicke auf die kleine Lupe am oberen rechten Rand der Menüleiste (oder <key>Cmd (⌘)</key>+<key>Leerzeichen</key>). Suche nach `Terminal` und öffne die Anwendung.

Anschließend muss in die Befehlszeile folgende Zeile eingegeben werden:

```
xattr -r -d com.apple.quarantine ~/Library/Application\ Support/org.inkscape.Inkscape/config/inkscape/extensions/
```

Falls dein Installationspfad für Erweiterungen vom Standard abweicht, ersetzte `~/Library/Application\ Support/org.inkscape.Inkscape/config/inkscape/extensions/` durch den Pfad der in Inkscape unter `Inkscape > Preferences > System` eingetragen ist).

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

## Fehlerbehebung

### Ink/Stitch startet nicht / Menüpunkte sind grau

**Installationspfad überprüfen**

Überprüfe noch einmal, ob du den richtigen Installationspfad gewählt hast. Sollte Ink/Stitch unter `Benutzererweiterungen` nicht funktionieren, kannst du auch versuchen, es unter `Inkscape Erweiterungen` zu platzieren.
Der Pfad kann auch unter `Bearbeiten > Einstellungen > System` nachgeschaut werden.

**Ink/Stitch-Version überprüfen**

Bitte überprüfe noch einmal, ob du die richtige Ink/Stitch Version für dein Betriebssytsem heruntergeladen hast.
Für macOS findest du den Download-Link unter [Herunterladen](#herunterladen) oben auf dieser Seite.

**Nutzer/Nutzerrechte überprüfen**

Einige Nutzer berichten, dass falsche Nutzereinstellungen, bzw. Nutzerrechte der Ink/Stitch-Dateien dieses Problem herbeiführen.

### 'xxxx' kann nicht geöffnet werden, da es von einem nicht verifizierten Entwickler stammt

In der Installationsbeschreibung haben wir unter ["Zusätzliche Installationsschritte für Catalina und Bg Sur"](#zusätzliche-schritte-für-catalina--big-sur) notwenige Schritte zur Beseitigung dieser Fehlermeldung zusammengefasst.

### ValueError: Null geometry supports no operations

Ink/Stitch mit macOS kann folgende Fehlermeldung hervorrufen:  `[...] ValueError: Null geometry supports no operations`.

Diese Fehlermeldung entsteht durch eine Inkompatibilität mit der speedups-Bibliothek von shapely, die mit Ink/Stitch mitgeliefert wird.
Um Ink/Stitch wieder nutzen zu können, muss die Bibliothek aus der Ink/Stitch Installation entfernt werden.

* Öffne den Ordner, in dem du Ink/Stitch installiert hast (meisten ist das: `~/Library/Application\ Support/org.inkscape.Inkscape/config/inkscape/extensions/`)
* Öffne auch den Ink/Stitch Unterordner, sofern du einen angelegt hast
* Halte die `Strg`-Taste gedrücl während du auf die Ink/Stitch Applikations-Datei klickst und wähle `Show Package Contents`

  ![Show Package Contents](/assets/images/docs/en/macOS-nogeometry.png)

* Öffne anschließend die Ordner `Contents > MacOS`, dort befindet sich der Ordner `shapely`.
  Der shapely-Ordner kann komplett gelöscht werden.

### Ich habe Ink/Stitch in meiner Muttersprache installiert, aber die Dialog-Fenster sind englisch

**Unvollständige Übersetzung**

Es möglich, dass die Übersetzung unvollständig ist. Das erkennt man daran, dass in einem Fenster sowohl englische, als auch anderssprachige Texte erscheinen.
Wenn du helfen willst, die Übersetzung zu vervollständigen, lese unsere [Beschreibung für Übersetzer](/de/developers/localize/).


**Spracheinstellungen**

Die Dialog-Fenster von Ink/Stitch richten sich nach der Sprache deines Betriebssytsems. Nur die eigentlichen Menüpunkte unter Erweiterungen werden von der installierten Ink/Stitch Sprachversion beeinflusst.
Ink/Stitch wird bei unklarar Spracheinstellung immer auf die englisch Standardsprache zurückgreifen.
In Inkscape kann die Spracheinstellung manuell angepasst werden:
  * Öffne Bearbeiten > Einstellungen > Benutzeroberfläche (Strg + Shift + P)
  * Wähle deine Sprache
  * Schließe Inkscape und starte es erneut

![Einstellungen > Benutzeroberfläche](/assets/images/docs/de/preferences_language.png)

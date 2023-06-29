---
title: "Installation von Ink/Stitch für macOS"
permalink: /de/docs/install-macos/
excerpt: "Wie wird Ink/Stitch installiert."
last_modified_at: 2023-04-28
toc: true
---
{% comment %}
## Video-Anleitung

Wir stellen Anfänger-Tutorials auf unserem <i class="fab fa-youtube"></i> [YouTube Kanal](https://www.youtube.com/c/InkStitch) zur Verfügung. Die Videos sind in englischer Sprache. Deutsche Untertitel können zugeschaltet werden.

Schaue den Installationsprozess für <i class="fab fa-apple"></i> [macOS](https://www.youtube.com/watch?v=gmOVLNh9cu8&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=3) an.
{% endcomment %}

## Herunterladen
Lade die aktuelle Version für dein macOS System herunter.

<p><a href="{{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx.pkg" class="btn btn--info btn--large"><i class="fa fa-download " ></i> Download Ink/Stitch {{ site.github.latest_release.tag_name }} for macOS<br><span style="color:lightblue;">Monterey</span></a></p>
<p><a href="{{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-high-sierra-catalina-osx.pkg" class="btn btn--info btn--large"><i class="fa fa-download " ></i> Download Ink/Stitch {{ site.github.latest_release.tag_name }} for macOS<br><span style="color:lightblue;">High Sierra / Mojave / Catalina / Big Sur</span></a></p>

**Aktuelle Version:** [Ink/Stitch {{ site.github.latest_release.tag_name }} ({{ site.github.latest_release.published_at | date: "%Y-%m-%d"  }})](https://github.com/inkstitch/inkstitch/releases/latest)

## Installation

Ink/Stitch ist eine Inkscape Erweiterung, deshalb **muss <span style="text-decoration:underline;">vor</span> der Ink/Stitch-Installation [Inkscape](https://inkscape.org/release/) Version 1.0.2 oder höher <span style="text-decoration:underline;">installiert und mindestens einmal geöffnet</span> worden sein**. Sonst schlägt die Installation fehl.<br><br>
Inkscape 1.2 funktioniert nicht mit **El Capitan** und **Sierra**. Für diese macOS-Versionen bitte [Inkscape 1.1.2](https://inkscape.org/release/1.1.2/platforms/) installieren.
{: .notice--warning .bold--warning }

**Monterey:** Öffne die heruntergeladene Datei mit Klick.

**El Capitan - Big Sur:** `Strg+Klick` auf die heruntergeladene Installations-Datei und klicke auf `Öffnen`.

Klicke auf `Weiter`.

![Install Ink/Stitch](/assets/images/docs/de/macos-install/installer01.png)

Klicke auf `Installieren`.

![Install Ink/Stitch](/assets/images/docs/de/macos-install/installer02.png)

Eine Passwortabfrage öffnet sich. Gib dein Benutzerpasswort ein und klicke anschließend auf `Software installieren`.

![Install Ink/Stitch](/assets/images/docs/de/macos-install/installer03.png)

In einigen Fällen wird dein System nachfragen, ob du erlaubst, dass Dateien in deinem Nutzerverzeichnis gespeichert werden dürfen. Ink/Stitch muss in den Ordner für Inkscape Erweiterungen gespeichert werden. Darum beantworte diese Frage mit `Ja`.
{: .notice--info }

Deine Installation ist abgeschlossen.

![Install Ink/Stitch](/assets/images/docs/de/macos-install/installer04.png)

Nur noch eine kleine Frage ...

Willst du die heruntergeladene Installations-Datei behalten? Das ist deine Wahl. Ink/Stitch braucht diese Datei nun nicht mehr.

![Install Ink/Stitch](/assets/images/docs/de/macos-install/installer05.png)

## Ink/Stitch öffnen
Öffne Inkscape. Du findest Ink/Stitch unter `Erweiterungen > Ink/Stitch`.

![Ink/Stitch menu](/assets/images/docs/de/macos-install/inkstitch-extensions-menu.png)

## Aktualisierung

Wenn eine neue Ink/Stitch Version erscheint, lade sie herunter und installiere sie wie oben beschrieben. Die alte Version wird dabei automatisch entfernt.

Installationen die älter sind als Ink/Stitch 2.1.0 müssen von Hand entfernt werden.
Öffne den Ordner für Inkscape Erweiterungen und entferne die alte Ink/Stitch Installation, bevor du das Installationskript aufrufst.

**Tipp:** Abonniere den News-Feed-Kanal, um die Aktualisierungen von Ink/Stitch zu verfolgen:<br>
 <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [GitHub Feed on new Releases](https://github.com/inkstitch/inkstitch/releases.atom)<br>
 <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [Ink/Stitch News](/feed.xml)<br> 
{: .notice--info }

<p class="notice--info" style="margin-top: -3.5em !important;">Oder schaue das Projekt auf GitHub an:<br><iframe style="display: inline-block;" src="https://ghbtns.com/github-btn.html?user=inkstitch&repo=inkstitch&type=watch&count=true&v=2" frameborder="0" scrolling="0" width="170px" height="20px"></iframe></p>

## Fehlerbehebung

### 'xxxx' kann nicht geöffnet werden, da es von einem nicht verifizierten Entwickler stammt

Das kann passieren, wenn du eine Entwickler-Versionen nutzt.

`Strg+Klick` auf die heruntergeladene Installations-Datei und klicke auf `Öffnen`.

### Installation fails

We also provide a zip download file which can be extraced in the the user extensions folder (see below: confirm installation path).

For Big Sur and Monterey [dowload ZIP]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-osx.zip)

For older macOS versions [download ZIP]({{ site.github.releases_url }}/latest/download/inkstitch-{{ site.github.latest_release.tag_name }}-capitan-cataline-osx.zip)

### Ink/Stitch startet nicht / Menüpunkte sind grau

**M1-Prozessoren (Apple Silicon Mac)**

Dieser Fehler tritt meistens dann auf, wenn Rosetta nicht installiert ist. Um das Problem zu beheben, öffne das Terminal und führe folgenden Befehl aus: `softwareupdate --install-rosetta --agree-to-license` 

**Installationspfad überprüfen**

Überprüfe noch einmal, ob du den richtigen Installationspfad gewählt hast. Sollte Ink/Stitch unter `Benutzererweiterungen` nicht funktionieren, kannst du auch versuchen, es unter `Inkscape Erweiterungen` zu platzieren.
Der Pfad kann auch unter `Inkscape > Einstellungen > System` nachgeschaut werden.

**Ink/Stitch-Version überprüfen**

Bitte überprüfe noch einmal, ob du die richtige Ink/Stitch Version für dein Betriebssytsem heruntergeladen hast.
Für macOS Versionen findest du den Download-Link unter [Herunterladen](#herunterladen) oben auf dieser Seite.

**Nutzer/Nutzerrechte überprüfen**

Einige Nutzer berichten, dass falsche Nutzereinstellungen, bzw. Nutzerrechte der Ink/Stitch-Dateien dieses Problem herbeiführen.

### Ink/Stitch wird auf englisch angezeigt

**Unvollständige Übersetzung**

Es möglich, dass die Übersetzung unvollständig ist. Das erkennt man daran, dass in einem Fenster sowohl englische, als auch anderssprachige Texte erscheinen.
Wenn du helfen willst, die Übersetzung zu vervollständigen, lese unsere [Beschreibung für Übersetzer](/de/developers/localize/).

**Spracheinstellungen**

In Inkscape kann die Spracheinstellung manuell angepasst werden:
  * Öffne `Inkscape > Einstellungen > Benutzeroberfläche` (Strg + Shift + P)
  * Wähle deine Sprache
  * Schließe Inkscape und starte es erneut

![Einstellungen > Benutzeroberfläche](/assets/images/docs/de/preferences_language.png)

## Ink/Stitch entfernen

Öffne den Ordner für Inkscape Erweiterungen. Unter `Inkscape > Einstellungen > System > Benutzererweiterungen` kannst du einsehen, wo dieser sich befindet.

![Inkscape extensions folder](/assets/images/docs/de/extensions-folder-location-macos.jpg)

Entferne alle Dateien und Ordner die mit `inkstitch` beginnen.

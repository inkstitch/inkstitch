---
title: "Installation von Ink/Stitch für Linux"
permalink: /de/docs/install-linux/
excerpt: "Wie wird Ink/Stitch installiert."
last_modified_at: 2025-06-17
toc: true
after_footer_scripts:
  - /assets/js/copy_code.js
---
{% comment %}
## Video-Anleitung

Wir stellen Anfänger-Tutorials auf unserem <i class="fab fa-youtube"></i> [YouTube Kanal](https://www.youtube.com/c/InkStitch) zur Verfügung. Die Videos sind in englischer Sprache. Deutsche Untertitel können zugeschaltet werden. Schaue den Installationsprozess für <i class="fab fa-linux"></i> [Linux](https://www.youtube.com/watch?v=Dkb5UvsZUNg&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=2) an.
{% endcomment %}

## Vorraussetzung

Ink/Stitch ist eine Inkscape Erweiterung. Installiere [Inkscape](https://inkscape.org/release/) Version 1.0.2 oder höher, bevor du Ink/Stitch installierst.

## Installation

{% assign tag_name = site.github.latest_release.tag_name %}
Lade die neueste Version für Linux herunter (Ink/Stitch {{ tag_name }})

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

**Aktuelle Version:** {{ site.github.latest_release.published_at | date: "%d.%m.%Y" }} [Ink/Stitch {{ site.github.latest_release.tag_name }})](https://github.com/inkstitch/inkstitch/releases/latest)

### RPM und DEB installieren

Führe einen Doppelklick auf die deb-Datei aus und folge den Installationsanweisungen deines Betriebssystems.

RPM: [GPG-Key](/assets/files/inkstitch.gpg)

### SH installieren

Benutze dieses Skript, wenn du die AppImage Version von Inkscape benutzt oder wenn du Ink/Stitch nur für deinen Benutzer installieren willst. Unterstützt dein System weder deb noch rpm, dann kannst du auch dieses Skript verwenden.

Öffne das Terminal und navigiere in den Ordner, in den du das Skript heruntergeladen hast und führe es aus, z.B.

```
cd Downloads
sh inkstitch-{{ tag_name }}-linux.sh
```

#### Experten Optionen

Dieses Skript versucht automatisch den richtigen Installationsort für Inkscape Erweiterungen herauszufinden. Sollte dies nicht funktionieren, kannst du die Umgebungsvariablen auch selbst setzen:

* `INKSCAPE_PATH` (z.B.: /usr/bin/inkscape)

  Der Pfad zum ausführbaren Inkscape Programm. Das Skript befragt dieses Programm mit dem --user-data-directory Argument danach, wo Erweiterungen installiert werden sollen.

* `INKSCAPE_EXTENSIONS_PATH` (z.B.: $HOME/.config/inkscape/extensions)

  Der Pfad zum Ordner für Inkscape Erweiterungen. Benutze dies, um die --user-data-directory Methode zu umgehen und den Zielordner selbst zu definieren.

Wenn du Ink/Stitch lieber selbst installieren willst, nutze das Argument `--extract` um die ursprüngliche tar.xz Version zu erhalten.

### TAR.XZ installieren

Unter `Bearbeiten > Einstellungen > System` kannst du einsehen, wo sich der Installationsordner befindet.

![Extensions folder location](/assets/images/docs/de/extensions-folder-location-linux.jpg)

Entpacke das Ink/Stitch-Archiv in diesen Ordner.

```
$ cd ~/.config/inkscape/extensions
$ tar -xvf ~/Downloads/inkstitch-{{ tag_name }}-linux.tar.xz
```

## Ink/Stitch öffnen

Starte Inkscape.

Ink/Stitch befindet sich nun unter `Erweiterungen > Ink/Stitch`.

## Aktualisierung

## Aktuelle Ink/Stitch Versionen

DEB und RPM Packet Installationen erkennen zuvor installierte Versionen und ersetzen diese automatisch mit der aktuellen Version. Auch das Installationsskript kann alte Versionen erkennen und ersetzen.
Das gilt jeweils nur, wenn auch die Vorgängerversion auf diese Weise installiert wurde. Ansonsten bitte der Anleitung für ältere Versionen folgen.

## Ink/Stitch Versionen älter als 2.1.0 und tar.xz Version

Lösche zunächst die alte Ink/Stitch Installation. Gehe in das Erweiterungsverzeichnis und entferne alle Dateien und Ordner, die mit inkstitch* beginnen.

Dann folge erneut der Installationsbeschreibung auf dieser Seite.

Die Verzeichnisse für Erweiterungen können unter `Bearbeiten > Einstellungen > System` eingesehen werden.

## Updateinfo

Abonniere den News-Feed-Kanal, um die Aktualisierungen von Ink/Stitch zu verfolgen:<br>
* <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [GitHub Feed on new Releases](https://github.com/inkstitch/inkstitch/releases.atom)
* <i class="fas fa-fw fa-rss-square" aria-hidden="true" style="color: #ffb400;"></i> [Ink/Stitch News](/feed.xml)
* <p>Oder folge dem Projekt auf GitHub <iframe style="display: inline-block;" src="https://ghbtns.com/github-btn.html?user=inkstitch&repo=inkstitch&type=watch&count=true&v=2" frameborder="0" scrolling="0" width="170px" height="20px"></iframe></p>

## Fehlerbehebung

### Ink/Stitch startet nicht / Menüpunkte sind grau

**Installationspfad überprüfen**

Überprüfe noch einmal, ob du den richtigen Installationspfad gewählt hast. Sollte Ink/Stitch unter `Benutzererweiterungen` nicht funktionieren, kannst du auch versuchen, es unter `Inkscape Erweiterungen` zu platzieren.
Der Pfad kann auch unter `Bearbeiten > Einstellungen > System` nachgeschaut werden.

**Ink/Stitch-Version überprüfen**

Bitte überprüfe noch einmal, ob du die richtige Ink/Stitch Version für dein Betriebssytsem heruntergeladen hast.
Für Linux findest du den Download-Link unter [Herunterladen](#herunterladen) oben auf dieser Seite.

**Nutzer/Nutzerrechte überprüfen**

Einige Nutzer berichten, dass falsche Nutzereinstellungen, bzw. Nutzerrechte der Ink/Stitch-Dateien dieses Problem herbeiführen.

### Einige Ink/Stitch Dialoge verschwinden kurz nach dem Aufruf wieder oder erscheinen gar nicht

#### Nutze X11

Dieser Fehler kann durch wayland verursacht werden. Starte Inkscape mit folgendem Befehl:

```
export GDK_BACKEND=x11 && inkscape
```

Bei Nutzung des Inkscape flatpak-Packets, sieht der Befehl folgendermaßen aus:

```
flatpak --env=GDK_BACKEND=x11 run org.inkscape.Inkscape
```

#### Verlängere Timeout für mutter

In den Versions von mutter ≥ 3.35.92 ist es möglich, die timeout-Zeit zu verlängern.
Das ist auch für X-forwarding über ssh mit hoher Latenz hilfreich.

Um den Timeout auf 60 s (60000 ms) zu setzen, nutze folgenden Befehl:

```gsettings set org.gnome.mutter check-alive-timeout 60000```

### ImportError: libnsl.so.1: cannot open shared object file. No such file or directory

Installiere die fehlende Bibliothek.

Für **Fedora** wird libnsl beispielsweise mit dem folgenden Befehl installiert

```
sudo dnf install libnsl
```

### AttributeError: 'NoneType' object has no attribute 'title' in inkstitch.py

Dieser Fehler wird von Nutzern berichtet, die Inkscape über snap installiert haben. Die Installation mit snap verhindert die Kommunikation zwischen Inkscape und Ink/Stitch.
Versuche Inkscape mit einer anderen Methode zu isntallieren. Alle auf [https://inkscape.org/](https://inkscape.org/de/releases/latest/) beschriebenen Methoden sollten funktionieren.

### Ich habe Ink/Stitch in meiner Muttersprache installiert, aber die Dialog-Fenster sind englisch!

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

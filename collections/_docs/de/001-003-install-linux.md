---
title: "Installation von Ink/Stitch für Linux"
permalink: /de/docs/install-linux/
excerpt: "Wie wird Ink/Stitch installiert."
last_modified_at: 2023-10-22
toc: true
---
{% comment %}
## Video-Anleitung

Wir stellen Anfänger-Tutorials auf unserem <i class="fab fa-youtube"></i> [YouTube Kanal](https://www.youtube.com/c/InkStitch) zur Verfügung. Die Videos sind in englischer Sprache. Deutsche Untertitel können zugeschaltet werden. Schaue den Installationsprozess für <i class="fab fa-linux"></i> [Linux](https://www.youtube.com/watch?v=Dkb5UvsZUNg&list=PLvlbfDmZyXG1ORmeqHdp4aP7J71e7icJP&index=2) an.
{% endcomment %}

## Vorraussetzung

Ink/Stitch ist eine Inkscape Erweiterung. Installiere [Inkscape](https://inkscape.org/release/) Version 1.0.2 oder höher, bevor du Ink/Stitch installierst.

## Installation

{% assign tag_name = site.github.latest_release.tag_name %}
Download the latest release (Ink/Stitch {{ tag_name }}) for Linux

{% assign tag_name = tag_name | slice: 1,tag_name.size %}

<div class="instructions">
  <p class="download-button"><a href="{{ site.github.releases_url }}/latest/download/inkstitch_{{ tag_name }}_amd64.deb" class="btn btn--info btn--large"><i class="fa fa-download " ></i> Download DEB Packet</a></p>
  <input type="checkbox" id="deb-instructions" />
  <label for="deb-instructions">Installationsanweisung <p class="down">▿</p><p class="up">▵</p></label>
  <section>
    <p class="headline">Installation deb Packet</p>
    <p>Führe einen Doppelklick auf die deb-Datei aus und folge den Installationsanweisungen deines Betriebssystems.</p>
  </section>
</div>

<div class="instructions">
  <p class="download-button"><a href="{{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-1.x86_64.rpm" class="btn btn--info btn--large"><i class="fa fa-download " ></i> Download RPM Packet</a></p>
  <input type="checkbox" id="rpm-instructions" />
  <label for="rpm-instructions">Installationsanweisung <p class="down">▿</p><p class="up">▵</p></label>
  <section>
    <p class="headline">Installation rpm Packet</p>
    <p>Führe einen Doppelklick auf die rpm-Datei aus und folge den Installationsanweisungen deines Betriebssystems.</p>
    <p><a href="/assets/files/inkstitch.gpg">GPG-Key</a></p>
  </section>
</div>

<div class="instructions">
  <p class="download-button"><a href="{{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-linux.sh" class="btn btn--info btn--large"><i class="fa fa-download " ></i> Download Installationsskript</a></p>
  <input type="checkbox" id="installer-instructions" />
  <label for="installer-instructions">Installationsanweisung <p class="down">▿</p><p class="up">▵</p></label>
  <section>
    <p class="headline">Installation mit dem Installationsskript</p>
    <p>Benutze dieses Skript, wenn du die AppImage Version von Inkscape benutzt oder wenn du Ink/Stitch nur für deinen Benutzer installieren willst. Unterstützt dein System weder deb noch rpm, dann kannst du auch dieses Skript verwenden.</p>
    <p>Öffne das Terminal und navigiere in den Ordner, in den du das Skript heruntergeladen hast, z.B.</p>
    <div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>cd Downloads</code></pre></div></div>
    <p>Anschließend kannst du mit folgendem Befehl das Skript ausführen</p>
    <div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>sh inkstitch-{{ tag_name }}-linux.sh</code></pre></div></div>
    <p><b>Experten Optionen</b></p>
    <p>Dieses Skript versucht automatisch den richtigen Installationsort für Inkscape Erweiterungen herauszufinden. Sollte dies nicht funktionieren, kannst du die Umgebungsvariablen auch selbst setzen:</p>
    <ul>
      <li>
        <p><code class="language-plaintext highlighter-rouge">INKSCAPE_PATH (z.B.: /usr/bin/inkscape)</code></p>
        <p>Der Pfad zum ausführbaren Inkscape Programm. Das Skript befragt dieses Programm mit dem --user-data-directory Argument danach, wo Erweiterungen installiert werden sollen.</p>
      </li>
      <li>
        <p><code class="language-plaintext highlighter-rouge">INKSCAPE_EXTENSIONS_PATH (z.B.: $HOME/.config/inkscape/extensions)</code></p>
        <p>Der Pfad zum Ordner für Inkscape Erweiterungen. Benutze dies, um die --user-data-directory Methode zu umgehen und den Zielordner selbst zu definieren.</p>
      </li>
    </ul>
    <p>Wenn du Ink/Stitch lieber selbst installieren willst, nutze das Argument <code class="language-plaintext highlighter-rouge">--extract</code> um die ursprüngliche tar.xz Version zu erhalten.</p>
  </section>
</div>

<div class="instructions">
  <p class="download-button"><a href="{{ site.github.releases_url }}/latest/download/inkstitch-{{ tag_name }}-linux.tar.xz" class="btn btn--info btn--large"><i class="fa fa-download " ></i> Download tar.xz Archiv</a></p>
  <input type="checkbox" id="archive-instructions" />
  <label for="archive-instructions">Installationsanweisung <p class="down">▿</p><p class="up">▵</p></label>
  <section>
  <p class="headline">Installation mit dem tar.xz Archiv</p>
  <p>Unter <code class="language-plaintext highlighter-rouge">Bearbeiten > Einstellungen > System</code> kannst du einsehen, wo sich der Installationsordner befindet.</p>
  <p><img alt="Extensions folder location" src="/assets/images/docs/de/extensions-folder-location-linux.jpg" /></p>
  <p>Entpacke das Ink/Stitch-Archiv in diesen Ordner.</p>
  <div class="language-plaintext highlighter-rouge"><div class="highlight"><pre class="highlight"><code>$ cd ~/.config/inkscape/extensions
$ tar -xvf ~/Downloads/inkstitch-{{ tag_name }}-linux.tar.xz</code></pre></div></div>
  </section>
</div>

**Aktuelle Version:** {{ site.github.latest_release.published_at | date: "%d.%m.%Y" }} [Ink/Stitch {{ site.github.latest_release.tag_name }})](https://github.com/inkstitch/inkstitch/releases/latest)

### NixOS

Eine Version für NixOS wird extern betreut und kann unter [https://codeberg.org/tropf/nix-inkstitch](https://codeberg.org/tropf/nix-inkstitch) heruntergeladen werden.

### Arch Linux

ArchLinux-Nutzer können ein AUR-Packet nutzen: [https://aur.archlinux.org/packages/inkstitchhttps://aur.archlinux.org/packages/inkstitch](https://aur.archlinux.org/packages/inkstitchhttps://aur.archlinux.org/packages/inkstitch)

## Ink/Stitch öffnen
Starte Inkscape neu.

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

### Ink/Stitch Fenster verschwinden kurz nach dem Aufruf wieder

Dieser Fehler kann durch wayland verursacht werden. Starte Inkscape mit folgendem Befehl: `export GDK_BACKEND=x11 && inkscape`

Nutze diesen Workaround bis wir die gesamte Oberfläche auf electron umgestellt haben.

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

---
title: Ink/Stitch auf dem Android Smartphone oder Tablet installieren
permalink: /de/tutorials/inkstistch-on-android/
last_modified_at: 2024-09-29
language: de
excerpt: "Ink/Stitch auf Android mit Termux installieren"
image: "/assets/images/tutorials/android/android_inkstitch.png"

tutorial-typ:
  - Text
after_footer_scripts:
  - /assets/js/copy_code.js
classes:
  - wide
---
![The simulator on a phone screen](/assets/images/tutorials/android/android_inkstitch_full.png)

Dies ist ein kleines Spaß-Tutorial. Der Nutzen Ink/Stitch auf einem Smartphone zu installieren mag fragwürdig erscheinen. Es kann sein, dass die Installation häufig abstürzt. Wir geben keinen Support für Ink/Stitch Installationen auf Android Systemen.
{: .notice--warning }

Dieses Tutorial ist ein bisschen technisch und an erfahrene Nutzer gerichtet. Wir nutzen Termux um einen Linux Desktop aufzusetzen über den wir Inkscape und Ink/Stitch laufen lassen können.

Auf dieser Seite findest du eine einfache Beschreibung einer möglichen Installation. Tiefergreifende Informationen gibt es bei: [Termux](https://github.com/LinuxDroidMaster/Termux-Desktops), [Termux X11](https://github.com/termux/termux-x11)

Wir wollen unseren Dank an [LinuxDroidMaster](https://github.com/LinuxDroidMaster) für die harte Arbeit und das Erstellen des Skripts richten, ohne das dieses Spaß-Projekt nicht funktionieren würde.

## Installation

In unserem Beispiel nutzen wir proot, Archlinux und den XFCE-Desktop. Für andere Optionen, folge den Anweisungen unter den oben genannten Links.
{: .notice--info }

* Zunächst müssen wir [Termux](https://termux.dev/) installieren.

* In Termux benötigen wir ein paar Pakete um Linux erfolgreich installieren zu können. Dafür müssen wir folgende Befehle ausführen:

  ```
  pkg update
  pkg upgrade
  ```

  ```
  pkg install x11-repo termux-x11-nightly tur-repo pulseaudio proot-distro wget git vim
  ```

* Lade termux-x11 für Android herunter und installiere es. [termux-x11 nightly release](https://github.com/termux/termux-x11/releases/tag/nightly). Nutze die Datei `debug-universal.apk`.

* Um Linux mit proot zu installieren, führe folgenden Befehl aus

  ```
  proot-distro install archlinux
  ```

* Einloggen in den Archlinux Kontainer

  ```
  proot-distro login archlinux
  ```

* Nun sind wir in der Archlinux-Installation. Zunächst aktualisieren wir das System

  ```
  pacman -Syu
  ```

* sudo installieren

  ```
  pacman -S sudo
  ```

* Nutzer erstellen

  ```
  useradd -m -G wheel username
  passwd username
  ```

  Insert the following line into `/etc/sudoers`

  ```
  username ALL=(ALL) ALL
  ```

* XFCE und Inkscape installieren.

  ```
  pacman -S xfce4 inkscape
  ```

* Verlasse den Archlinux Kontainer

  ```
  exit
  ```

* Zurück in Termux lade das Skript um XFCE in Termux zu starten herunter

  ```
  wget https://raw.githubusercontent.com/LinuxDroidMaster/Termux-Desktops/main/scripts/proot_arch/startxfce4_arch.sh
  ```

  Mache das Skript ausführbar

  ```
  chmod +x startxfce4_arch.sh
  ```

  Bearbeite das Skript um es an den oben festgelegten Nutzernamen anzupassen

  ```
  vim startxfce4_arch.sh
  ```

  In untenstehender Zeilte den Nutzernamen `droidmaster` mit deinem eigenen ersetzen:

  ```
  proot-distro login archlinux --shared-tmp -- /bin/bash -c  'export PULSE_SERVER=127.0.0.1 && export XDG_RUNTIME_DIR=${TMPDIR} && su - droidmaster -c "env DISPLAY=:0 startxfce4"'
  ```

  Auf einigen Geräten kann es beim Start des Skripts schwarze Bildschirme geben.
  Sollte das bei dir der Fall sein, ersetze `termux-x11 :0 >/dev/null &` mit

  ```
  termux-x11 :0 -legacy-drawing >/dev/null &
  ```

  Speichern und Vim verlassen

* Nutze das Skript um XFCE zu starten

  ```
  ./startxfce4_arch.sh
  ```

* Wir haben Inkscape bereits installiert. Öffne es einmal und schließe es direkt wieder.

  [Lade Ink/Stitch für arm64](https://github.com/inkstitch/inkstitch-linux-arm64/releases/latest) herunter und installiere es wie gewohnt (in den Ordner für Inkscape-Erweiterungen kopieren).

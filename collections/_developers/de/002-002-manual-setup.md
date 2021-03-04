---
title: "Manualle Installation"
permalink: /de/developers/inkstitch/manual-setup/
last_modified_at: 2021-03-04
toc: false
---
Eine manuelle Installation ermöglicht es am Quellcode zu arbeiten und die Änderungen

Wenn du die Erweiterung unter **Windows** debuggen willst, sind ein paar [zusätzliche Schritte](/developers/inkstitch/windows-manual-setup/) nötig (englisch).

## How to Install Ink/Stich Manually

### 1. Ink/Stitch herunterladen

```
git clone https://github.com/inkstitch/inkstitch
```

### 2. Install Pyembroidery

```
git clone https://github.com/inkstitch/pyembroidery.git
pip install -e pyembroidery/
```

We recommend to use `pyenv` to avoid the need of root privileges for `pip`.

### 3.  Installiere Python Abhängigkeiten

Es werden ein paar Python Module gebraucht. In einigen Fällen benutzt Ink/Stitch Funktionen, die nicht automatisch durch die Distributionen mit Python mitgeliefert werden.
Deshalb empfehlen wir sie mit pip zu installieren:

```
pip install -r requirements.txt
```

**Info:** Evtl. musst du auf einigen Plattformen wxPython entfernen und ein platform-spezifisches Paket [installieren](https://wiki.wxpython.org/How%20to%20install%20wxPython):<br />
   ⚫ Debian `python-wxgtk3.0`<br />
   ⚫ Ubuntu 16.04: `pip install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-16.04 wxPython`
{: .notice--info }

**Info:** Wenn du nur Python 2 installiert hast, kannst du evtl. auch einfach `pip` anstelle von `pip2` benutzen.
{: .notice--info }

### 4.  Installiere Abhängigkeiten für Electron

Die grafische Oberfläche von Ink/Stitch nutzt Electron.  Dazu brauchst du eine funktionsfähige Installation von NodeJS (Version 10 oder höher).  Sofern nicht vorhanden, installiere yarn mit `npm install yarn`.

Installiere Electron mit den dazugehörigen Abhängigkeiten wie folgt:

```
cd electron
yarn install
cd ..
```

### 4.  INX-Dateien vorbereiten

```
make inx
```

Das erstellt `*.inx` Dateien für jede Sprache in `inx/<locale>`.

Navigiere zum neu erstellten inx-Ordner und lösche alle Sprachen, bis auf eine oder nutze folgenden Befehl:
```
find inx/ -mindepth 1 -maxdepth 1 -type d -not -name de_DE -exec rm -rf {} +
```
Ersetze `de_DE` mit deiner bevorzugten Sprache (sofern vorhanden).

Die Wahl der Sprache der inx-Dateien beeinflusst lediglich die Sprache im Inkscape Menü.
Für die Ink/Stitch Dialoge wird die Systemsprache genutzt.
{: .notice--info }

### 5.  Symbolische Links in den Inkscape extensions-Order setzen

```
cd ~/.config/inkscape/extensions
ln -s /path/to/inkstitch
```

### 6.  Inkscape starten

Änderungen am Python-Code werden wirksam, sobald die Erweiterung das nächste Mal gestartet wird. Änderungen an den Inkscape-Menü Dateien (`*.inx`) zeigen sich erst, nachdem Inkscape neu gestartet wurde.

## Fehlerbehebung

### ImportError: No module named shapely

Wenn Ink/Stitch `ImportError: No module named shapely` ausgibt, dann ist es gut möglich, dass Inkscape eine andere Python Version benutzt,
als die in den installierten Abängigkeiten.

* Schließe Inkscape, sonst werden alle Änderungen wieder überschrieben
* Öffne `preferences.xml`.<br>
  Wo sich die Datei befindet kann unter `Bearbeiten > Einstellungen > System > Benutzereinstellungen` eingesehen werden
* Suche nach dem Begriff `<group id="extensions" />` und füge den richtigen Python-Interpreter ein.

  **Beispiel:** Benutze `<group id="extensions" python-interpreter="/usr/local/bin/python3" />` wobei `/usr/local/bin/python3` der Wert ist, der von `which python3` zurückgegeben wird.

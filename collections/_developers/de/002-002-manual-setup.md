---
title: "Manuelle Installation"
permalink: /de/developers/inkstitch/manual-setup/
last_modified_at: 2025-10-19
toc: false
after_footer_scripts:
  - /assets/js/copy_code.js
---
Eine manuelle Installation ermöglicht es am Quellcode zu arbeiten und die Änderungen

## Ink/Stitch manuell installieren

Wir empfehlen die Nutung von `pyenv` mit python 3.11.

### 1. Ink/Stitch herunterladen

```
git clone https://github.com/inkstitch/inkstitch
```

### 2. Installiere Python Abhängigkeiten

Es werden ein paar Python Module gebraucht. In einigen Fällen benutzt Ink/Stitch Funktionen, die nicht automatisch durch die Distributionen mit Python mitgeliefert werden.
Deshalb empfehlen wir sie mit pip zu installieren.

```
python -m pip install -r inkstitch/requirements.txt
```

### 4.  INX-Dateien vorbereiten

Jetzt werden die Dateien für das Inkscape-Menü erstellt.

```
cd inkstitch
make manual
```

Für spätere Updates der Templates kann folgender Befehl ausgeführt werden:

```
make inx
```

### 5. Symbolische Links in den Inkscape extensions-Order setzen

```
cd ~/.config/inkscape/extensions
ln -s /path/to/inkstitch
```

### 6.  Inkscape starten

Änderungen am Python-Code werden wirksam, sobald die Erweiterung das nächste Mal gestartet wird. Änderungen an den Inkscape-Menü Dateien (`*.inx`) zeigen sich erst, nachdem Inkscape neu gestartet wurde.

## Fehlerbehebung

### ImportError: No module named shapely

Wenn Ink/Stitch `ImportError: No module named shapely` ausgibt, dann ist es gut möglich, dass Inkscape eine andere Python Version benutzt, als die in den installierten Abängigkeiten.

* Schließe Inkscape, sonst werden alle Änderungen wieder überschrieben
* Öffne `preferences.xml`.<br>
  Wo sich die Datei befindet kann unter `Bearbeiten > Einstellungen > System > Benutzereinstellungen` eingesehen werden
* Suche nach dem Begriff `<group id="extensions" />` und füge den richtigen Python-Interpreter ein.

  **Beispiel:** Benutze `<group id="extensions" python-interpreter="/usr/local/bin/python3" />` wobei `/usr/local/bin/python3` der Wert ist, der von `which python3` zurückgegeben wird.

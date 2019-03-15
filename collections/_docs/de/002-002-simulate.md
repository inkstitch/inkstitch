---
title: "Simulation"
permalink: /de/docs/simulate/
excerpt: ""
last_modified_at: 2019-03-15
toc: false
---

Wähle die Objekte aus, die in der simulierten Vorschau angezeigt werden sollen. Wenn das gesamtes Design simuliert werden soll, wähle alles (`Strg + A`) oder nichts aus.

Dann starte `Erweiterungen -> Ink/Stitch -> Simulation` und genieße.

### Tastenkombinationen der Simulation

tastenkombination | Beschreibung
-------- | --------
<key>→</key> | vorwärts
<key>←</key> | rückwärts
<key>↑</key> | schneller
<key>↓</key> | langsamer
<key>+</key> | ein Frame vorwärts
<key>-</key> | ein Frame rückwärts
<key>p</key> | Animation anhalten
<key>r</key> | Animation neu starten
<key>q</key> | Beenden

Es ist auch möglich die Simulation mit der Maus zu **zoomen** und zu **verschieben**.

## Simulator unabhängig von Inkscape verwenden

Der Simulator kann auf jedes von Ink/Stitch unterstütze Dateiformat angewendet werden:

```
PYTHONPATH=/usr/share/inkscape/extensions python -m lib.simulator Pfad/zur/Datei.Dateiendung
```

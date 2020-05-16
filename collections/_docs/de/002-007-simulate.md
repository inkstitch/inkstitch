---
title: "Visualisierung"
permalink: /de/docs/visualize/
excerpt: ""
last_modified_at: 2020-05-12
toc: false
---

Wähle die Objekte aus, die in der simulierten Vorschau angezeigt werden sollen. Wenn das gesamtes Design simuliert werden soll, wähle alles (`Strg + A`) oder nichts aus.

Dann starte `Erweiterungen -> Ink/Stitch -> Simulation`.

### Tastenkombinationen der Simulation

tastenkombination | Beschreibung
-------- | --------
<key>→</key> | vorwärts
<key>←</key> | rückwärts
<key>↑</key> | schneller
<key>↓</key> | langsamer
<key>+</key> | ein Frame vorwärts
<key>-</key> | ein Frame rückwärts

Es ist auch möglich die Simulation mit der Maus zu **zoomen** und zu **verschieben**.

## Simulator unabhängig von Inkscape verwenden

Der Simulator kann auf jedes von Ink/Stitch unterstütze Dateiformat angewendet werden:

```
PYTHONPATH=/usr/share/inkscape/extensions python -m lib.simulator Pfad/zur/Datei.Dateiendung
```

## Stich-Plan Vorschau

Führe den Befehl `Erweiterungen > Ink/Stitch > Visualisierung und Export > Stich-Plan Vorschau` aus.
Dies fügt den Stichplan direkt am rechten Rand deines Dokuments ein.
Dort kannst du das Ergebnis untersuchen und anschließend wieder entfernen.
You can inspect it from there and delete it afterwards.

---
title: "Addons für Inkscape installieren"
permalink: /de/docs/install-addons/
last_modified_at: 2025-03-29
toc: true
---
{% include upcoming_release.html %}

Installiert Farbpaletten oder Motiv-Symbol-Bibiotheken für Inscape

* `Erweiterungen > Ink/Stitch > Addons für Inkscape installieren`
* Wähle was installiert werden soll (Garn-Farbpaletten und/oder Symbol-Bibliotheken)
* Klicke auf `Anwenden`
* Start Inkscape neu

## Garn-Farbpaletten

Ink/Stitch liefert viele Farbpaletten gängiger Garnhersteller mit, die in Inkscape installiert werden können.
So können Stickdesign direkt mit den richtigen Farben erstellt werden.
Die Farben werden sowohl für die PDF-Ausgabe, als auch direkt in die Stickdateien eingespeichert - sofern das gewählte Dateiformat Farbinformationen zulässt.

[Wie Farbpaletten angewandt werden](/de/docs/thread-color/#mit-farbpaleten-arbeiten)

## Symbol-Bibliotheken

Symbole sind wiederverwendbare Elemente, die in ein Dokument eingefügt werden können. Sie können einfache Pfade, als auch ganze Stickdesigns enthalten.

Ink/Stitch liefert eine Symbol-Bibliothek mit Motif-Stichen. Diese Symbole können mit dem Pfadeffekt `Muster entlang Pfad` dafür genutzt werden, um einfach gemusterte Geradstiche zu erzeugen.

### Funktionsweise

* Öffne den Symbol-Dialog `Objekt > Symbole` (Shift+Ctrl+Y)
* Wähle die Ink/Stitch Motif-Bibliothek (inkstitch-motif-library)
* Ziehe eins der Symbole auf die Leinwand (drag & drop)

Für die Anwendung mit dem Pfadeffekt

* Wähle das Symbol aus und drücke `Strg + C` um das Symbol zu kopieren (alternativ: Rechtsklick > Kopieren)
* Wähle den Pfad auf den das Motif angewandt werden soll
* Öffne den Pfadeffekt-Dialog `Pfad > Pfadeffekte...` und wähle als Pfadeffekt `Muster entlang Pfad`
* Bei `Quelle des Musters` klicke auf das Symbol `Mit Pfad in der Zwischenablage verknüpfen`
* `Musterkopien` sollte auf `Wiederholt` oder auf `Wiederholt, gestreckt` gesetzt werden
* Das ursprüngliche Symbol kann nun gelöscht werden

---
title: Verformen mit Pfad-Effekten
permalink: /de/tutorials/distort/
last_modified_at: 2024-05-24
language: de
excerpt: "Formen und Schriften mit Inkscape Pfad-Effekten verformen"
image: "/assets/images/galleries/fonts/multiple/multifont3.jpg"

tutorial-typ:
  - Sample File
stichart: 
  - Satin Stitch
techniken:
   -Lettering
field-of-use:
schwierigkeitsgrad: 
---
{% include upcoming_release.html %}

![Verzerr Effekt](/assets/images/galleries/fonts/multiple/multifont3.jpg)

Stickobjekte mit Inkscape Pfadeffekten zu verformen macht Spaß. Inkscape bietet hierfür verschiedene Pfadeffekte an:

* Biegen
* Hüllenverformung
* Gitterverformung
* Perspektive/Umhüllung

Für gute Resultate sollte folgendes beachtet werden:

* Pfade sollten so gut wie möglich vereinfacht werden
* Sehr kleine Elemente eignen sich nicht für diese Technik

Satinsäulen stellen eine Herausforderung dar: es gibt keine spezielle Kennzeichnung für Richtungsvekotren und Außenkonturen in der SVG-Pfad-Beschreibung. Ink/Stitch muss aus allen Unterpfaden die Außenkonturen herausfiltern.

Um Ink/Stitch bei diesem Prozess zu unterstützen und das Ergebnis nach der Verformung konstant zu halten:

* Außenkonturen sollten sich nach Möglichkeit nicht überschneiden
* Richtungsvekotren sollten die Außenkonturen an beiden Seiten klar kreuzen
* Die Satinsäulen sollte Richtungsvekotren haben, aber nicht exakt zwei

Wenn diese Regeln befolgt werden, ist die Chance groß, dass Ink/Stitch die Satinsäulen auch nach der Verformung noch richtig erkennen kann.

Die meisten Ink/Stitch Schriften sind dazu optimiert worden mit leichten Verformungen gut zu funktionieren.
Wenngleich extreme Verformungen möglicherweise zu Problemen beim Sticken führen können.

## Biegen

Der Pfadeffekt `Biegen` ist sehr einfach auf Schriften anzuwenden

* Wähle eine komplette Text-Gruppe
* Füge den Pfadeffekt `Biegen` hinzu
* Klicke im Pfadeffekt-Dialog auf `Auf der Arbeitsfläche bearbeiten` und verforme nun erschienenen grünen Pfad

  Da es sich um einen Pfadeffekt handelt, kann der grüne Pfad auch später immer wieder angepasst werden

Für mehrzeilige Texte lohnt es sich den Pfadeffekt auf jede Zeile einzelnd anzuwenden.

![Text Biegen Beispiel](/assets/images/tutorials/distort/peace_dove.svg)

[Herunterladen](/assets/images/tutorials/distort/peace_dove.svg){: download="peace_dove.svg" }

Natürlich ist diese Methode nicht auf Schriften begrenzt. In diesem Beispiel wurde aus einem einzigen gezeichneten Rochen ein ganzer Schwarm.

![Mantas Bend Example](/assets/images/tutorials/distort/Mantas.svg)

[Herunterladen](/assets/images/tutorials/distort/Mantas.svg){: download="Mantas.svg" }

## Hüllenverformung

Die Hüllenverformung funktioniert im Wesentlichen genauso wie der Biegen-Pfadeffekt. Hier ist eine Bearbeitung auf der Arbeitsfläche für alle 4 Seiten möglich.

In diesem Beispiel wurde die Hüllenverformung auf jede Textzeile getrennt angwendet.

![Manger Enveloppe deformation example](/assets/images/tutorials/distort/manger.svg)

[Download](/assets/images/tutorials/distort/manger.svg){: download="manger.svg" }

## Perspektive/Umhüllung

Dieser Pfadeffekt ist sehr nützlich um ... einer Form eine Perspektive zu geben.

Nach der Anwendung des Effekts können die vier Ecken mit dem Knotenwerkzeug verschoben werden.

![perspective example](/assets/images/tutorials/distort/perspective.svg)

[Download](/assets/images/tutorials/distort/manger.svg){: download="perspective.svg" }


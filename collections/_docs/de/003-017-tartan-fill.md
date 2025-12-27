---
title: "Tartan Fill"
permalink: /de/docs/stitches/tartan-fill/
last_modified_at: 2024-05-14
toc: true
---
## Beschreibung

[![Tartan Fill Sample](/assets/images/docs/tartan-fill.jpg){: width="200x"}](/assets/images/docs/tartan-fill.svg){: title="Download SVG File" .align-left download="tartan-fill.svg" }
Tartan ist ein gemusterter Stoff mit farbigen horizontalen und vertikalen Streifen. Man kennt es typischerweise von schottischen Kilts. Diese Stichart versucht, das typische Muster nachzuahmen.

## Funktionsweise

* Erstelle einen **geschlossenen Pfad mit Füllfarbe**. Die Form darf Löcher enthalten.
* Öffne den Tartn-Muster Editor unter `Erweiterungen > Ink/Stitch > Werkzeuge: Füllung > Tartan` und erstelle ein Tartan-Muster
* Weitere Stickparameter können im Anschluß im Parameter-Dialog eingestellt werden (`Erweiterungen > Ink/Stitch  > Parameter`)

## Tartan-Muster bearbeiten

Der Tartan-Muster Editor befindet sich unter `Erweiterungen > Ink/Stitch > Werkzeuge: Füllung > Tartan`

[Erfahre mehre über den Tartan-Muster Editor](/de/docs/fill-tools#tartan)

## Parameter

Öffne das Parameter-Dialogfenster (`Erweiterungen > Ink/Stitch  > Parameter`, um die Einstellungen zu verfeinern.

Einstellung                     ||Beschreibung
---|---|---
Automatisch geführte Füllstiche | ☑ |Muss aktiviert sein, damit diese Einstellungen wirksam werden.
Füllmethode                     | Tartanfüllung | Hier bitte `Tartanfüllung` auswählen
Erweitern                       |![Expand example](/assets/images/docs/params-fill-expand.png) | Erweitern der Form vor dem Füllstich, um Lücken zwischen den Formen auszugleichen.
Winkel der Stichlinien          || Relativ zur Rotation des Tartanmusters
Maximale Füll-Stichlänge        |![Stitch length example](/assets/images/docs/params-fill-stitch_length.png) | Die Stichlänge in einer Reihe. Ein kürzerer Stich kann am Anfang oder am Ende einer Reihe verwendet werden.
Reihenabstand                   |![Spacing example](/assets/images/docs/params-fill-spacing_between_rows.png) | Abstand zwischen den Stichreihen.
Versatz                         |![Stagger example](/assets/images/docs/params-fill-stagger.png) | Die Einstellung bestimmt, wie viele Reihen die Stiche voneinander entfernt sind, bevor sie in die gleiche Position münden.  Fractional values are allowed and can have less visible diagonals than integer values.
Stichlänge                      |![Running stitch length example](/assets/images/docs/params-fill-running_stitch_length.png) | Stichlänge für Geradstiche beim Übergang von Abschnitt zu Abschnitt.
Geradstich-Toleranz             ||Alle Stiche müssen innerhalb dieses Abstandes zum Pfad befinden. Ein niedrigerer Toleranzwert führt zu kürzeren Stichen. Ein höherer Wert könnte Ecken abrunden. Dezimalzahlen führen ggf. zu weniger deutlichen Diagonalen als Ganzzahlen.
Mehrfachgeradstich Anzahl der Wiederholungen || ◦ Jeden Stich vervielfachen.<br/>◦ Ein Wert von 1 würde jeden Stich verdreifachen (vorwärts, rückwärts, vorwärts).<br/>◦ Ein Wert von 2 würde jeden Stich fünffach ausführen, usw.<br/>◦ Gilt nur für den Geradstich.
Reihen pro Tartan-Faden         || Aufeinanderfolgende Reihen gleicher Farbe
Fischgrätenmuster-Breite        || Definiert die Breite des Frischgrätenmusters. Nutze 0 für das klassische Tartanmuster. Es wird empfohlen ein mehrfaches oder einen teilbaren Wert der Streifen-Breite zu nutzen. Ein schönes Ergebnis lässt sich auch erzielen, wenn für Kette und Schuss jeweils nur eine Farbe definiert wurde.
Minimale Stichlänge             || Überschreibt die globale Einstellung für die minimale Stichlänge. Stiche, die kleiner sind als dieser Wert werden entfernt.
Minimale Länge für Sprungstiche || Überschreibt die globale Einstellung für die minimale Länge für Sprungstiche. Kleinere Entfernungen zum nächsten Objekt haben keine Vernähstiche
Vernähen erlauben               || Vernäht bei Bedarf an den ausgewählten Positionen
Vernähen erzwingen              || Vernäht den Faden nach diesem Element, auch dann, wenn der Abstand zum Folgeobjekt geringer ist als in den [Ink/Stitch Einstellungen](/de/docs/preferences/) definiert.
Anstecher                       || Wähle die [Anstecher](/de/docs/stitches/lock-stitches) Variante (Anfang).
Verstecher                      || Wähle die [Verstecher](/de/docs/stitches/lock-stitches) Variante (Ende).
Stopp                           || Stoppt die Maschine nachdem dieses Objekt genäht wurde und springt zur Stopp-Position (sofern vorhanden)
Fadenschnitt                    || Schneidet den Faden nachdem dieses Objekt genäht wurde
{: .params-table }

## Unterlage

Die Unterlage nutzt den Stickwinkel der in den [Parametern der Unterlage](/de/docs/params/#füllung-unterlage) eingestellt werden kann.

## Beispieldateien mit Tartanfüllung

{% include tutorials/tutorial_list key="stichart" value="Tartanfüllung" %}

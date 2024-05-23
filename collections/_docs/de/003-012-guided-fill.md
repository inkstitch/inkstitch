---
title: "Kurvenfüllung"
permalink: /de/docs/stitches/guided-fill/
last_modified_at: 2024-05-22
toc: true
---
## Beschreibung

Kurvige Füllflächen mit Hilfe von Führungslinien.

![Fill stitch detail](/assets/images/docs/guided-fill-detail.jpg)

## Funktionsweise

* Erstelle einen geschlossenen Pfad mit einer Füllung.
* Erstelle eine Führungslinie um die Stickrichtung zu definieren:
    * zeichne eine Linie mit einer Kontur (ohne Füllung)
    * wähle die Linie aus
    * Öffne `Erweiterungen > Ink/Stitch > Bearbeiten > Auswal zu Fürhungslinie`
* Wähle beide Elemente aus und gruppiere sie (`Strg + G`)
  Jede Gruppe kann mehrere Füllobjekte enthalten, aber nur eine Führungslinie.
  Weitere Führungslinien werden ignoriert.
* Öffne den Parameter-Dialog (`Erweiterungen > Ink/Stitch > Parameter`) und wähle `Kurvenfüllung` als Methode aus.

![Guided Fill Group](/assets/images/docs/guided-fill-group.svg)
[Beispieldatei herunterladen](/assets/images/docs/guided-fill-group.svg){: download="guided-fill-group.svg" }

![Guided fill group](/assets/images/docs/guided-fill-complex.svg)
[Beispieldatei herunterladen](/assets/images/docs/guided-fill-complex.svg){: download="guided-fill-complex.svg" }

### Strategie

Ink/Stitch bietet zwei verschiedene Füllstrategien für Kurvenfüllungen an. Dabei hat jede Strategie Vor- und Nachteile.

#### Kopieren

Kopieren ist die Standardeinstellung. Mit dieser Methode werden Kopien der Führungslinie über die Füllfläche verschoben, dadurch können können die Abstände im Füllmuster variieren.

#### Parallelverschiebung

Die Methode Parallelverschiebung stellt sicher, dass die Abstände zwischen den einzelnen Reihen immer gleich bleiben. Dabei können scharfe Ecken entstehen.

## Anfangs- und Endpunkt festlegen

Ink/Stitch erlaubt es über visuelle Befehle den [Anfangs- und Endpunkt eines Füllobjekts](/de/docs/commands) zu kennzeichnen.

## Parameter

Öffne `Erweiterungen > Ink/Stitch  > Parameter` um das Stickbild deinen Bedürfnissen anzupassen.

Einstellung                                 ||Beschreibung
---|---|---
Automatisch geführte Füllstiche             | ☑ |Muss aktiviert sein
Füllmethode                                 | Kurvenfüllung|Für diesen Stichtyp bitte Kurvenfüllung auswählen
Strategie                                   | ![Guided Fill Strategies](/assets/images/docs/guidedfillstrategies.svg)| Kopieren (Standard), oben, füllt die Form mit Hilfe von Kopien der Führungslinie. Parallelverschiebung, unten, stellt sicher, dass die Abstände gleich bleiben (dies kann zu scharfen Kanten führen).
Erweitern                                   || Erweitert die Form um beim Sticken Lücken zu benachbarten Formen zu vermeiden.
Maximale Füllstichlänge                     || Stichlänge des Füllstiches. Am Start oder am Ende der Reihe können auch kürzere Stiche enstehen (deshab "maximal")
Reihenabstand                               || Abstand zwischen den Reihen
Stichversatz                                | ![Stagger example](/assets/images/docs/params-fill-stagger.png) | Die Einstellung bestimmt, wie viele Reihen die Stiche voneinander entfernt sind, bevor sie in die gleiche Position münden.   Dezimalzahlen führen ggf. zu weniger deutlichen Diagonalen als Ganzzahlen.
Letzten Stich in jeder Reihe überspringen   || Der letzte Stich in jeder Reihe ist dem darauffolgenden Stich sehr nah. Ihn zu überspringen verringert die Stichanzahl und Dichte.
Verbindungsstiche innerhalb des Objektes    || Verbindungsstiche werden innerhalb des Objektes versteckt (aktiv) oder am äußeren Rand entlang gestickt (inaktiv
Stichlänge (zwischen den Abschnitten)       || Länge der Stiche zwischen den Füllstich-Sektionen (Verbindungsstiche)
Geradstich-Toleranz                         || Alle Stiche müssen innerhalb dieses Abstandes zum Pfad befinden. Ein niedrigerer Toleranzwert führt zu kürzeren Stichen. Ein höherer Wert könnte Ecken abrunden.
Zufällige Stiche                            |☑|Anstatt einer gleichmäßigen Verteilung, erfolgt die Stichlänge und -phase nach dem Zufallsprinzip. Dies wird besonders für eng beieinander liegende Kurvenfüllungen empfohlen, um Moiré-Artefakte zu vermeiden.
Zufallsabweichung von der Stichlänge        ||Maximale randomisierte Abweichung der Stichabstände in Prozent.
Zufallszahl                                 ||Zufallswert für randomisierte Attribute. Verwendet die Element-ID, falls leer.
Minimale Stichlänge                         || Überschreibt die globale Einstellung für die minimale Stichlänge. Stiche, die kleiner sind als dieser Wert werden entfernt.
Minimale Länge für Sprungstiche             || Überschreibt die globale Einstellung für die minimale Länge für Sprungstiche. Kleinere Entfernungen zum nächsten Objekt haben keine Vernähstiche.
Vernähen erlauben                           || Vernäht bei Bedarf an den ausgewählten Positionen
Vernähen erzwingen                          || Vernäht den Faden nach diesem Element, auch dann, wenn der Abstand zum Folgeobjekt geringer ist als in den [Ink/Stitch Einstellungen](/de/docs/preferences/) definiert.
Anstecher                                   ||Wähle die [Anstecher](/de/docs/stitches/lock-stitches) Variante (Anfang).
Verstecher                                  ||Wähle die [Verstecher](/de/docs/stitches/lock-stitches) Variante (Ende).
Fadenschnitt                                || Schneidet den Faden nachdem dieses Objekt genäht wurde
Stopp                                       || Stoppt die Maschine nachdem dieses Objekt genäht wurde und springt zur Stopp-Position (sofern vorhanden)

## Unterlage

Die Unterlage für geführte Füllstiche folgt nicht der Führungslinie sondern nutzt den Füllwinkel der in den [Unterleger-Parametern](/de/docs/stitches/fill-stitch/#unterlage) festgelegt werden kann.

## Beispiele mit Kurvenfüllung

{% include tutorials/tutorial_list key="stichart" value="Kurvenfüllung" %}

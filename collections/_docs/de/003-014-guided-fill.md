---
title: "Kurvenfüllung"
permalink: /de/docs/stitches/guided-fill/
last_modified_at: 2024-05-22
toc: true
---
## Beschreibung

Kurvige Füllflächen mit Hilfe von Führungslinien.

{% include folder-galleries path="butterfly-fill-project/guided/" captions="1:Kurvenfüllung mit mehrfarbigem Garn;2:Übereinandergelagerte Flächen mit loser Kurvenfüllung für einen Wasserfarben-Effekt;3:Kurvenfüllung mit der Buffer-Methode" %}

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

Ink/Stitch bietet drei verschiedene Füllstrategien für Kurvenfüllungen an. Dabei hat jede Strategie Vor- und Nachteile.

#### Kopieren

Kopieren ist die Standardeinstellung. Mit dieser Methode werden Kopien der Führungslinie über die Füllfläche verschoben, dadurch können können die Abstände im Füllmuster variieren.

#### Parallelverschiebung

Die Methode Parallelverschiebung stellt sicher, dass die Abstände zwischen den einzelnen Reihen immer gleich bleiben. Dabei können scharfe Ecken entstehen.

#### Buffer

{% include upcoming_release.html %}

Die Buffer-Methode ist ein fortgeführter Vesatz zur Führungslinie und erlaubt auch, dass die Führungslinie aus mehreren Unterpfaden besteht.

## Anfangs- und Endpunkt festlegen

Ink/Stitch erlaubt es über visuelle Befehle den [Anfangs- und Endpunkt eines Füllobjekts](/de/docs/commands) zu kennzeichnen.

## Parameter

Öffne `Erweiterungen > Ink/Stitch  > Parameter` um das Stickbild deinen Bedürfnissen anzupassen.

{% include params.html stitch_type='guided_fill'%}

## Unterlage

Die Unterlage für geführte Füllstiche folgt nicht der Führungslinie sondern nutzt den Füllwinkel der in den [Unterleger-Parametern](/de/docs/stitches/fill-stitch/#unterlage) festgelegt werden kann.

## Beispiele mit Kurvenfüllung

{% include tutorials/tutorial_list key="stichart" value="Kurvenfüllung" %}

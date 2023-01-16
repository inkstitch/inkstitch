---
title: "Kurvenfüllung"
permalink: /de/docs/stitches/guided-fill/
excerpt: ""
last_modified_at: 2022-12-08
toc: true
---
## Beschreibung

Kurvige Füllflächen  mit Hilfe von Führungslinien.

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

Run `Extensions > Ink/Stitch  > Params` to tweak the settings to your needs.

Einstelung||Beschreibung
Automatically routed fill stitching| ☑ |Must be enabled for these settings to take effect.
Expand||Expand the shape before fill stitching, to compensate for gaps between shapes.
Maximale Füll-Stichlänge|| Die Stichlänge in einer Reihe. Ein kürzerer Stich kann am Anfang oder am Ende einer Reihe verwendet werden.
Reihenabstand|| Abstand zwischen den Stichreihen.
Running stitch length||Length of stitches used when moving from section to section
Skip last stitch in each row||The last stitch in each row is quite close to the first stitch in the next row. Skipping it decreases stitch count and density.
Underpath||Must be enabled to let running stitches travel inside shape instead of around the border when moving from section to section
Force lock stitches||Sew lock stitches after sewing this element, even if the distance to the next object is shorter than defined by the collapse length value in the Ink/Stitch preferences.
Allow lock stitches||Enables lock stitches in only desired positions

## Underlay

Underlay in Guided Fill doesn't follow the guide line, but uses the fill angle which can be defined in the underlay [params](/de/docs/fill-stitch#unterlage).

## Samples Files Including Guided Fill Stitches
{% include tutorials/tutorial_list key="stichart" value="Kurvenfüllung" %}

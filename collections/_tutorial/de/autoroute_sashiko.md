---
permalink: /de/tutorials/autoroute_sashiko/
title: "Sashiko "
language: de
last_modified_at: 2025-02-17
excerpt: "Automatisch Geführter Geradstich und Sashiko-Erweiterung"
image: "/assets/images/tutorials/sashiko/sashiko.jpg"
tutorial-typ:
  - Beispieldatei
stichart:
  - Mehrfach-Geradstich
werkzeug:
  - Linie
techniken:
schwierigkeitsgrad: 
  - mittel
---
![Sample](/assets/images/tutorials/sashiko/sashiko.jpg)

[Die inkscape  für Ink/stitch-Erweiterung Sashiko](https://gitlab.com/kaalleen/sashiko-inkscape-extension) in Verbindung mit dem Werkzeug  `Automatisch Geführter Geradstich` (oder  mit "Redwork" Erweiterung) ermöglicht es, Sashiko-Stil-Stickdateien mit Mehrfach-Geradstich auf eine so einfache Weise zu produzieren, dass es fast unanständig ist.

Anmerkung: diese Erweiterung unterscheidet sich von der ursprünglichen [Shashiko Inkscape Erweiterung](https://inkscape.org/~FractalLotus/%E2%98%85sashiko-stitching-patterns), indem sie es vermeidet, doppelte Linien zu produzieren.Außerdem fügt sich ein paar wenige Muster zur Auswahl hinzu.

Dazu muss natürlich die Sashiko-Erweiterung installiert werden. 

Wenn du die Erweiterung installiert hast, navigiere zu ihr:

`Erweiterungen > Rendern > Sashiko`. 

![ScreeShot](/assets/images/tutorials/sashiko/Sashiko1.jpg)

Wenn du auf "Vorschau" klickst, kannst du ganz einfach das Muster, die Anzahl der Zeilen und die Anzahl der Spalten sehen und auswählen.

Wenn du deine Wahl getroffen hast, klicke auf "Anwenden", dann kannst du das Sashiko-Fenster schließen.

Du kannst nun das Dialogfenster der Sashiko Erweiterung schließen.

## Muster, die nicht direkt verbunden sind (z.B. Offset Crosses)

Um von der Zeichnung zu einer Stickerei mit Dreifach-Geradstich zu gelangen:
* Wähle alle Pfade aus, die die Erweiterung gerade erstellt hat (es gibt viele).
  * `Erweiterungen > Ink/Stitch > Parameter`. 
    * Die Länge des Geradstichs wählen (2 mm im gestickten Beispiel).
     * Die Anzahl der Wiederholungen des Mehrfach-Geradstiches wählen (1 im gestickten Beispiel, also Dreifach-Geradstich).
  * `Erweiterungen > Ink/Stitch > Werkzeuge:Linie > Automatisch Geführter Geradstich`. 
    * Häkchen setzen bei "Knoten an Überschneidungen hinzufügen".
    * Deaktiviere den Haken bei "Reihenfolge der Laufstiche beibehalten".

** und das ist alles !!!!**.

Du hast nun eine automatisch erstellte Gruppe, die eine Mischung aus folgenden Elementen beinhaltet:

* Pfade mit dreifachem Geradstich, deren Namen mit "Auto-Geradstich" beginnen und die der gewählten Zeichnung entsprechen.
* Einfache Geradstichpfade, deren Namen mit "Auto-Geradstich-Verbindung" beginnen, die hinzugefügt wurden, um dir zu ermöglichen, ein Ergebnis ohne Fadensprünge zu erhalten.

Die so erstellte Gruppe kannst du nun so skalieren wie du möchtest, die oben gewählte Länge des Geradstichs bleibt erhalten. 

## Verbundene Muster (z.B. Blue Ocean Waves)

Nutze die `Redwork` Erweiterung:

Passe die Einstellungen an (0.5mm für die ersten zwei Parameter ist in der Regel eine gute Wahl).

Mit der aktivierten Option `Kombiniere Elemente des gleichen Typs` ohne Einstellungen für einen Mehrfachgeradstich, entsteht eine einzige durchgehende Linie, die alle Abschnitte genau zwei mal passiert.
Ist ein Wert für Mehrfachgeradstiche gesetzt, alternieren Unterpfade und Mehrfachgeradstiche.

Ist die Option zum Kombinieren der Pfade deaktiviert, entstehen automatisch mehr Pfade. Dies ist nur dann empfohlen, wenn die Pfade noch weiter bearbeitet werden sollen.

# Weitere Erweiterungen

* [Bobbinlace Erweiterung](https://d-bl.github.io/inkscape-bobbinlace)
* [Tiling extension](https://inkscape.org/fr/~cwant/%E2%98%85inkscape-tiling-extension+2) versuchen.

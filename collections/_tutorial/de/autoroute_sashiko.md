---
permalink: /de/tutorials/autoroute_sashiko/
title: "Sashiko "
language: de
last_modified_at: 2024-02-15
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

Note that this extension is different for  the  original [Sashiko Inkscape extension](https://inkscape.org/~FractalLotus/%E2%98%85sashiko-stitching-patterns), as it never generates two copies of the same path one on  top of the other.


Dazu muss natürlich die Sashiko-Erweiterung installiert werden. 

Wenn du die Erweiterung installiert hast, navigiere zu ihr:

`Erweiterungen > Rendern > Sashiko`. 

![ScreeShot](/assets/images/tutorials/sashiko/Sashiko1.jpg)

Wenn du auf "Vorschau" klickst, kannst du ganz einfach das Muster, die Anzahl der Zeilen und die Anzahl der Spalten sehen und auswählen.

Wenn du deine Wahl getroffen hast, klicke auf "Anwenden", dann kannst du das Sashiko-Fenster schließen.

Du kannst nun das Dialogfenster der Sashiko Erweiterung schließen.

## If you have chosen a pattern that yields a non conected result (for instance Offset Crosses) 

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

## If you have chosen a pattern that yields a connected result (for instance Blue Ocean Weaves) 

Use now the "Redwork"  extension :

Chose your  parameters (0.5mm for the first two parameters is usually a good choice).

{% include upcoming_release.html %}

If you chose  to combine  and no  bean stitches repeat then you will get a single path that travel everything twice.
If you chose to combine  and have a non null bean stitches repeat value, you will get an alternate sequence of underpath and bean stitch path.

If you do not combine you will get more paths, this should only be done if you want to further work with the result.



Du könntest es auch mit dieser [Bobbinlace Erweiterung](https://d-bl.github.io/inkscape-bobbinlace)  oder [Tiling extension](https://inkscape.org/fr/~cwant/%E2%98%85inkscape-tiling-extension+2) versuchen.

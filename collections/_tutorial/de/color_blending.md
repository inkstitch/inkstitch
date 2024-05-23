---
title: Color Blending
permalink: /de/tutorials/color-blending/
last_modified_at: 2024-05-23
language: de
excerpt: "Farbübergänge"
image: "/assets/images/tutorials/tutorial-preview-images/blend.png"
werkzeug:
  - Füllung
tutorial-typ:
  - Beispieldatei
stichart: 
  - Füllstich
techniken:
schwierigkeitsgrad:
---
Füllungen müssen nicht flach sein, denn Farbübergänge sind möglich und willkommen.

## Lineare Farbverlaufsfüllung

{% include upcoming_release.html %}

Farbverläufe in Ink/Stitch zu erstellen ist leicht geworden. Die beste Qualität erreicht man mit der [Linearen Farbverlaufsfüllung](/de/docs/stitches/linear-gradient-fill/), einer Füllstichart. Da der Farbverlauf hier als Ganzes behandelt wird ist es möglich Reihenabstände und Stichpositionen trotz Farbwechsel konstant zu halten.

* Erstelle eine Form mit einer linearen Farbverlaufsfüllung in Inkscape
* Wähle in den Ink/Stitch Parametern "Lineare Farbverlaufsfüllung" als Füllmethode aus

## Farbverlauf in Blöcke aufteilen

Ink/Stitch hat ein Werkzeug um Farbverläufe in einzelne Blöcke aufzuteilen. Mit dieser Funktion kann nicht die Gleiche Qualität erreicht werden wir mit der Farbverlaufs-Stichart, aber sie kann für experimentelle Zwecke dienen. Wir sprechen über die Erweiterung [Farbverlauf in Blöcke aufteilen](/de/docs/fill-tools/#farbverlauf-in-blöcke-aufteilen).

* Erstelle eine Form mit einer linearen Farbverlaufsfüllung in Inkscape
* Wähle als Füllmethode "Automatische Füllung" in den Ink/Stitch Parameter-Einstellungen
* `Erweiterungen > Ink/Stitch > Werkzeuge: Füllung > Farbverlauf in Blöcke aufteilen`

![Download Sample File](/assets/images/tutorials/samples/inkstitch_gradient_extension.svg)

[Beispieldatei herunterladen](/assets/images/tutorials/samples/inkstitch_gradient_extension.svg).

In jedem Block erhöht sich der Reihenabstand vom Anfang zum Ende, während der Reihenabstand der nächsten Farbe verringert wird. So entsteht ein Farbübergang von einer zur nächsten Farbe.

Die Richtung des Farbübergangs bestimmt den *Füllwinkel*.

### Wie wird die Varianz im Reihenabstand erzeugt?

Ist ein Wert für `Reihenabstand (Ende)` gesetzt, ändert sich der Reihenabstand kontinierlich hin zu diesem Wert. Senkrecht zum Füllwinkel betrachtet, beginnt der Reihenabstand beim Wert `Reihenabstand (Ende)` und endet beim Wert `Reihenabstand`, wobei er linear angepasst wird.

Die übereinanderliegenden Farbblöcke die mit „Farbverlauf in Blöcke aufteilen“ erstellt wurden, haben die gleichen Werte für *Reihenabstand* und *Reihenabstand (Ende)*, aber entgegengesetzte Füllwinkel, wodurch der Verlaufseffekt erzielt wird. 

### Das Ergebnis anpassen

Die Erweiterung spart im Vergleich zur manuellen Methode viel Zeit. Die Werte für die Reihenabstände können im Nachinein weiter angepasst werden um das Ergebnis zu verändern. Dabei sollte man immer die Dichte aller übereinanderliegenden Blöcke im Auge behalten.

Die Dichte ist immer dem Wert Reihenabstand entgegengesetzt. Wenn wir einen bestimmten *Gesamtreihenabstand* **sbr** anstreben (beide Farben), dann muss die Summe des Kehrwerts des *Reihenabstandes* der beiden Farbverlaufsblöcke gleich **1/sbr** sein sowie die Summe des Kehrwerts ihres Wertes für *Reihenabstand (Ende)*.

Dies ist ein Teil einer Datei mit 100 Rechtecken. Jedes Rechteck zeigt einen Verlauf von Rot nach Blau mit verschiedenen Parametern.

![Download Sample File](/assets/images/tutorials/samples/end_row_spacing_2_colors_blending.svg)

[Beispieldatei herunterladen](/assets/images/tutorials/samples/end_row_spacing_2_colors_blending.svg) 

## Manuelle Farbverläufe

Farbverläufe können auch manuell erstellt werden.

### Falscher Farbübgergang (Faux Fill Blend)

1. Ein falscher Farbübergang hat eine unterste Ebene mit Standard-Füllstich, jede darüberliegende Ebene variiert in ihrer Dichte
2. Jede Ebene sollte den selben Stich-Winkel haben, so kann der Farbübergang-Effekt erzielt werden
3. Solltest du mehr als 2 Ebenen nutzen, muss jede folgende Ebene eine geringere Dichte aufweisen
4. Am Besten sollte jede Ebene am selben Punkt starten und am selben Punkt enden.
5. Eine Unterlage ist nicht unbedingt nötig. Das hängt jedoch immer von dem individuellen Projekt ab.
6. Normalerweise macht es Sinn mit den helleren Farben zu beginnen. Auch das hängt natürlich von dem jeweiligen Projekt ab.
7. Obwohl dies kein echter Farbübergang ist, reicht diese Methode in den meisten Fällen vollkommen aus, um den gewünschten Effekt zu erzielen.
8. Die Werte für die Dichte in diesem Beispiel sind nicht in Stein gemeißelt, es soll nur das Konzept demonstrieren. Die Werten hängen von verschiedenen Faktoren, wie z.B. Stoffart und Designgröße, ab.

[Download Sample File](/assets/images/tutorials/samples/Faux_Fill_Blend.svg){: download="Faux_Fill_Blend.svg" }

### Echter Farbübergang (True Blend)

1. Viele Konditionen des falschen Farbübergangs sind auch auf den echten übertragbar.  Stichwinkel, Start- und Endpunkte, sowie Farbreihenfolge hängen vom individuellen Design ab.
2. Der größte Unterschied ist, dass gerechnet werden muss: die Gesamtdichte für jeden Bereich sollte bei 100% liegen.
3. Das kann bedeuten, dass mehr Farb-Ebenen und Dichte-Variationen erforderlich sind. Der größte Faktor ist die Größe und Form des Designs, sowie die Besonderheiten des einzelnen Projekts.
4. Was diese Methode zu einem echten Farbbergang macht, ist, dass sich die Farben tatsächlich miteinander "vermischen".

[Download Sample File](/assets/images/tutorials/samples/True_Blend.svg){: download="True_Blend.svg" }

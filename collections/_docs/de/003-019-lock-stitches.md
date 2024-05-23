---
title: "Vernähstiche"
permalink: /de/docs/stitches/lock-stitches/
last_modified_at: 2023-02-27
toc: true
---
An- und Verstecher sind kleine Stiche am Anfang (Anstecher) oder am Ende (Verstecher) eines Farbblocks oder vor und nach einem Sprungstich oder Fadenschnitt-Befehl. Sie helfen den Faden zu sichern.

Fadenscnittbefehle können auf zwei Arten eingefügt werden:

* entweder als visueller Befehl übr `Erweiterungen > Ink/Stitch > Befehle > Objektbefehle hinzufügen ...`
* oder im Parameter-Dialog mit dem aktivieren der `Fadenschnitt`-Checkbox

Die Stickdatei enthält mehere Elemente die hintereinander gestickt werden sollen.

Ist der Abstand zwischen dem letzten Stich des einen Elementes und dem ersten Stich des nächsten Elementes größer als der Wert `Minimale Sprungstichlänge` (`Erweiterungen > Ink/Stitch > Einstellungen`), dann wird ein Sprungstich zwischen den Elementen generiert. In diesem Fall kommen auch Vernähstiche am Ende des ersten Elements und Anfang des nächsten Elements zur Anwendung (wenn dies nicht durch die Option `Vernähen erlauben` explizit unterbunden wird).

Ist der Abstand zwischen den Elementen kleiner als der Wert `Minimale Sprungstichlänge` erstellt das Stickprogramm einen normalen Stich und zwischen den Elementen werden keine Vernähstiche generiert.

Ink/Stitch bietet die Möglichkeit auch bei kleinen Distanzen Vernähstiche zu erzwingen. Dies geschieht durch die Option `Vernähstiche erzwingen` in den Parametern. Hierdurch werden unabhängig von Abständen Vernähstiche zwischen den beiden Objekten erzeugt. Diese Option überschreibt auch die Einstellung `Vernähen erlauben`.

Ink/Stitch bietet verschiedene Vernähstich-Typen an und erlaubt sogar die Definition eigener Vernähstiche.

## Standard-Vernähstiche

![Lock stitch variants](/assets/images/docs/lock-stitches.png)
{: .img-half }

1. Halbstich. Dies ist der Standartwert und die einzige Option für Vernähstiche älterer Ink/Stitch Versionen. Eine Skalierung ist nicht möglich, da sich dieser Stich an der Stichlänge des Elements orientiert: zwei halbe Stiche zurück, zwei halbe Stiche nach vorn.
2. Pfeil, skaliert in %
3. Vor und zurück, skaliert in mm
4. Schleife, skaliert in %
5. Kreuz, skaliert in %
6. Stern, skaliert in %
7. Dreieck, skaliert in %
8. Zick-Zack, skaliert in %
9. Benutzerdefiniert. Skaliert in % oder mm abhängig von der eingegebenen Pfad-Variante.

## Benutzerdefinierte Vernähstiche

Benutzerdefinierte Vernähstiche können entweder als SVG-Pfad definiert werden (skaliert in %) oder durch relative Schritte die sich nach der mm Angabe skalieren.

### Benutzerdefinierter SVG-Pfad

Der SVG-Pfad wird immer so abgebildet, als ob er ein Pfad für einen Anstecher ist. Wird er als Verstecher genutzt dreht sich der Pfad automatisch um. Der letzte Knoten des Pfades wird nicht gestickt, sondern dient lediglich als Richtungsangabe wie sich der Pfad an den Ursprungspfad anschließen soll.

or instance the triangle lock stitches corresponds to the custom path  M -0.26,0.33 H 0.55 L 0,0.84 V 0 L 0.34,0.82 (this is the d attribute of the path). 
On next image, this are the black paths, on one copy its last segment is colored green for clarity.

![Triangle lock stitch](/assets/images/docs/triangle_lock.png)

Both red and blue path have a triangle tack down.

The custom svg path is rotated in such away that its last segment (green) has the same direction as the begining of red and blue paths. It is only used to compute this rotation angle, and is not part of the actual tack down, and will not be embroidered.


### Benutzerdefinierter Pfad in mm

Benutzerdefinierte Werte für die absolute Skalierung in mm werden mit einem Leerzeichen getrennt. Beispielsweise wird ein Pfad mit den Werten 1 1 -1 -1 und einer Skalierungsangabe von 0.7 mm zweimal 0.7 mm vorwärts wandern und zweimal 0.7 mm rückwärts. Dezimalwerth-Angaben sind möglich (z.B. 0.5 2.2 -0.5 - 2.2).

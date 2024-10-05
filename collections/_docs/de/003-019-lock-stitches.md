---
title: "Vernähstiche"
permalink: /de/docs/stitches/lock-stitches/
last_modified_at: 2024-09-05
toc: true
---
## Beschreibung

An- und Verstecher sind kleine Stiche am Anfang (Anstecher) oder am Ende (Verstecher) eines Farbblocks oder vor und nach einem Sprungstich oder Fadenschnitt-Befehl. Sie helfen den Faden zu sichern.

## Einflussfaktoren (Wann werden Vernähstiche gesetzt)

Eine Stickdatei enthält eine Abfolge an Stickobjekten, die nacheinander ausgestickt werden. Vernähstiche werden gesetzt, wenn zwischen den Objekten ein Farbwechsel, ein Fadenschnittbefehl oder ein großer Abstand besteht. Mit `Vernähstiche zulassen` kann die Verwendung von Vernähstichen verhindert werden, mit „Vernähstiche erzwingen“ wird sichergestellt, dass diese vorhanden sind.

### Minimum Jump Stitch Length

Der Wert für die `Minimale Sprungstichlänge` kann unter `Erweiterungen > Ink/Stitch > Einstellungen` oder objektbezogen im Parameterdialog eingestellt werden.

Der Wert definiert, ob der Stich zwischen zwei Objekten ein Sprungstich oder ein normaler Stich ist.
Nur wenn der Abstand zwischen zwei Objekten größer ist, als der Wert für die `Minimale Sprungstichlänge`, wird ein Sprungstich angewendet. Nur wenn ein Sprungstich verwendet wird, werden am Ende des ersten Objekts Verstecher und am Anfang des zweiten Objekts Anstecher hinzugefügt.

![Drei Linien, der erste Abstand beträgt 1mm, der Zweite 3mm, die minimale Sprungstichlänge ist 2. Es gibt keine Vernähstiche für den ersten Abstand, beim Zweiten schon.](/assets/images/docs/lock_stitch_min_jump.svg)
{: .border-shadow }

Es gibt jedoch noch weitere Parameter, die Einfluss darauf haben können, ob Vernähstiche verwendet werden.

### Farbwechsel

Vor und nach einem Farbwechsel werden Verriegelungsstiche gesetzt.

### Fadenschnittbefehle

Ink/Stitch fügt in das Objekt mit dem Fadenschnittbefehl Verstecher und in das darauf folgende Objekt Anstecher ein.

![Drei Linien. Die Abstände sind 1mm breit. Die minimale Sprungstichlänge ist auf 2 eingestellt. Die mittlere Linie hat einen Fadenschnittbefehl, der Verstecher darauf setzt und Anstecher auf das nächste Objekt](/assets/images/docs/lock_stitch_trim.svg)
{: .border-shadow }

Fadenschnittbefehle können auf zwei Arten eingefügt werden:

* entweder als visueller Befehl übr `Erweiterungen > Ink/Stitch > Befehle > Objektbefehle hinzufügen ...`
* oder im Parameter-Dialog mit dem aktivieren der `Fadenschnitt`-Checkbox

### Vernähstiche erlauben

`Vernähstiche erlauben` kann An- und/oder Verstecher unterdrücken, wenn sie normalerweise angewendet würden.
{: .notice--info }

![Drei Linien. Die Abstände sind 3 mm breit. Die minimale Sprungstichlänge ist auf 2 eingestellt. Die mittlere Linie ist so eingestellt, dass nur am Ende Verstecher zulässig sind. Daher hat sie keine Anstecher.](/assets/images/docs/lock_stitch_allow.svg)
{: .border-shadow }

Der Parameter `Vernähstiche erlauben` kann Vernähstiche vor oder nach dem Objekt (oder beides) verhindern. Wenn also der Abstand zwischen zwei Objekten groß genug für einen Sprungstich ist, aber das erste Objekt den Parameter `Vernähstiche erlauben` auf `Anfang` eingestellt hat, werden am Ende dieses Objekts keine Verstecher gesetzt.

### Vernähstiche erzwingen

Es ist jedoch möglich, An- und Verstecher auch für Objekte mit geringen Abständen zu erzwingen. Aktiviere den Parameter „Vernähstiche erzwingen“, um Verriegelungsstiche zu erzwingen. Das folgende Objekt erhält dadurch automatisch auch Anstecher.

![Drei Linien. Die Abstände sind 1 mm breit. Die minimale Sprungstichlänge ist auf 2 eingestellt. Bei der mittlere Linie ist die Option Vernähstiche erzwingen aktiviert. Dadurch erhält das Objekt Verstecher. Das folgende Objekt erhält Anstecher.](/assets/images/docs/lock_stitch_force.svg)
{: .border-shadow }

Achten Sie darauf, dass Sie „Vernähstiche erzwingen“ nicht für das zweite Objekt aktivieren, da Sie dann die „Verriegelungsstiche“ dafür erzwingen würden, nicht die „Heftstiche“, und Sie würden außerdem Verriegelungsstiche für das nächste Objekt erzwingen, unabhängig von dessen Abstand zum Objekt nach dem Sprung.

`Vernähstiche erzwingen` wendet unabhöngig vom Abstand immer Verstecher an. Diese Option überschreibt auch die Einstellungen für `Vernähen erlauben`.
{: .notice--info }

## Arten von Vernähstichen

Ink/Stitch bietet verschiedene Vernähstich-Typen an und erlaubt sogar die Definition eigener Vernähstiche.

### Standard-Vernähstiche

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

### Benutzerdefinierte Vernähstiche

Benutzerdefinierte Vernähstiche können entweder als SVG-Pfad definiert werden (skaliert in %) oder durch relative Schritte die sich nach der mm Angabe skalieren.

#### Benutzerdefinierter SVG-Pfad

Der SVG-Pfad wird immer so abgebildet, als ob er ein Pfad für einen Anstecher ist. Wird er als Verstecher genutzt dreht sich der Pfad automatisch um. Der letzte Knoten des Pfades wird nicht gestickt, sondern dient lediglich als Richtungsangabe wie sich der Pfad an den Ursprungspfad anschließen soll.

or instance the triangle lock stitches corresponds to the custom path  M -0.26,0.33 H 0.55 L 0,0.84 V 0 L 0.34,0.82 (this is the d attribute of the path). 
On next image, this are the black paths, on one copy its last segment is colored green for clarity.

![Triangle lock stitch](/assets/images/docs/triangle_lock.png)

Both red and blue path have a triangle tack down.

The custom svg path is rotated in such away that its last segment (green) has the same direction as the begining of red and blue paths. It is only used to compute this rotation angle, and is not part of the actual tack down, and will not be embroidered.

#### Benutzerdefinierter Pfad in mm

Benutzerdefinierte Werte für die absolute Skalierung in mm werden mit einem Leerzeichen getrennt. Beispielsweise wird ein Pfad mit den Werten 1 1 -1 -1 und einer Skalierungsangabe von 0.7 mm zweimal 0.7 mm vorwärts wandern und zweimal 0.7 mm rückwärts. Dezimalwerth-Angaben sind möglich (z.B. 0.5 2.2 -0.5 - 2.2).

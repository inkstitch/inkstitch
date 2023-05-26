---
title: "Vernähstiche"
permalink: /de/docs/stitches/lock-stitches/
excerpt: ""
last_modified_at: 2023-02-27
toc: true
---
An- und Verstecher sind kleine Stiche am Anfang (Anstecher) oder am Ende (Verstecher) eines Farbblocks oder vor und nach einem Sprungstich oder Fadenschnitt-Befehl. Sie helfen den Faden zu sichern.

Ink/Stitch bietet verschiedene Vernähstich-Typen an und erlaubt sogar die Definition eigener Vernähstiche.

## Standart-Vernähstiche

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

### Benutzerdefinierter Pfad in mm

Benutzerdefinierte Werte für die absolute Skalierung in mm werden mit einem Leerzeichen getrennt. Beispielsweise wird ein Pfad mit den Werten 1 1 -1 -1 und einer Skalierungsangabe von 0.7 mm zweimal 0.7 mm vorwärts wandern und zweimal 0.7 mm rückwärts. Dezimalwerth-Angaben sind möglich (z.B. 0.5 2.2 -0.5 - 2.2).

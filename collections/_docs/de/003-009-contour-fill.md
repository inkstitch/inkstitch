---
title: "Konturfüllung"
permalink: /de/docs/stitches/contour-fill/
excerpt: ""
last_modified_at: 2022-05-16
toc: true
---
## Beschreibung

![Konturfüllung Detail](/assets/images/docs/contour-fill-detail.jpg)

Konturfüllung füllt eine Fläche der Kontur folgend.

### Funktionsweise

Erstelle einen geschlossenen Pfad mit einer Füllfarbe.

### Anfangs- und Endpunkt festlegen

Ink/Stitch erlaubt es über visuelle Befehle den [Anfangs- und Endpunkt eines Füllobjekts](/de/docs/commands) zu kennzeichnen.

### Parameter

Öffne `Erweiterungen > Ink/Stitch > Parameter`. Setze die Füllmethode auf `Konturfüllung` und passe die restlichen Einstellungen den jeweiligen Bedürfnissen an.

Einstellung||Beschreibung
Automatisch geführte Füllstiche | ☑ |Muss aktiviert sein, damit diese Einstellungen wirksam werden.
Füllmethode|Contour Fill|Contour Fill must be selected to sew spiral lines of the contour
Contour Fill Strategy|![Inner to Outer](/assets/images/docs/contour-fill-innertoouter-bottlenecks.jpg)<br>![Contour spirals](/assets/images/docs/contour-fill-spirals.jpg)|**Innter to outer** (default) is able to fill shapes with bottlenecks<br>**Single spiral** fills a shape with a single spiral from the outside to the inside<br>**Double spiral** fills a shape with a double spiral, starts and ends at the outside border of the shape.
Join Style|Round, Mitered, Beveled|Method to handle the edges when the size the contour is reduced for the inner spirals
Avoid self-crossing|![Avoid self crossing effect](/assets/images/docs/contour-fill-self-crossing.jpg)|Wheter inner to outer is allowed to cross itself or not
Clockwise||Direction to move around the contour
Maximale Füll-Stichlänge|| Die Stichlänge in einer Reihe. Ein kürzerer Stich kann am Anfang oder am Ende einer Reihe verwendet werden.
Reihenabstand|| Abstand zwischen den Stichreihen.
Vernähen erzwingen||Sew lock stitches after sewing this element, even if the distance to the next object is shorter than defined by the collapse length value in the Ink/Stitch preferences.
Vernähen erlauben|| Vernäht bei Bedarf an den ausgewählten Positionen

### Unterlage

Die Unterlage einer Konturfüllung folgt nicht der Kontur, aber nutzt den Stickwinkel, der in den [Parametern der Unterlage](/de/docs/params/#füllung-unterlage) eingestellt werden kann.

### Beispieldateien für Konturfüllung
{% include tutorials/tutorial_list key="stichart" value="Konturfülllung" %}

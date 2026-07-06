---
title: "Konturfüllung"
permalink: /de/docs/stitches/contour-fill/
last_modified_at: 2025-04-12
toc: true
---
## Beschreibung

Konturfüllung füllt eine Fläche der Kontur folgend.

{% include folder-galleries path="butterfly-fill-project/contour/" captions="1:Konturfüllung auf die Gesamtform;2:Konturfüllung mit Unterteilungen" %}

[<i class="fa fa-download"></i> Beispieldateien herunterladen](/assets/images/stitch-type-butterflies/contour_fill.zip)

### Funktionsweise

Erstelle einen geschlossenen Pfad mit einer Füllfarbe.

### Anfangs- und Endpunkt festlegen

Für die Konturfüllung kann nur der Startpunkt über [visuelle Befehle](/docs/commands/) festgelegt werden. Der Befehlt für Endpunkte hat bei dieser Stichart keinen Effekt.

### Parameter

Öffne `Erweiterungen > Ink/Stitch > Parameter`. Setze die Füllmethode auf `Konturfüllung` und passe die restlichen Einstellungen den jeweiligen Bedürfnissen an.

{% include params.html stitch_type='contour_fill'%}

### Unterlage

Die Unterlage einer Konturfüllung folgt nicht der Kontur, aber nutzt den Stickwinkel, der in den [Parametern der Unterlage](/de/docs/params/#füllung-unterlage) eingestellt werden kann.

### Beispieldateien für Konturfüllung

{% include tutorials/tutorial_list key="stichart" value="Konturfüllung" %}

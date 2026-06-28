---
title: "Spiralfüllung"
permalink: /de/docs/stitches/circular-fill/
last_modified_at: 2024-06-07
toc: true
---
## Beschreibung

Eine Spiralfüllung füllt eine Form mit einer gestickten Spirale. Der Mittelpunkt der Spirale liegt im Mittelpunkt des Elements. Eine Zielposition kann definiert werden um den Spiralmittelpunkt zu verschieben.

{% include folder-galleries path="butterfly-fill-project/circular/" captions="1:Spiralfüllung in mehreren Schichten;2:Spiralfüllung mit unauffälligem Farbverlauf" %}

## Funktionsweise

* Erstelle einen geschlossenen Pfad mit einer Füllung. Aussparungen innerhalb der Form sind möglich.
* In den Parametereinstellungen (`Erweiterungen > Ink/Stitch > Parameter`) `Spiralfüllung` als Füllmethode auswählen.
  Die restlichen Parameter können nach Belieben angepasst werden.

## Spiralmittelpunkt festlegen

Standartmäßig ist der Spiralmittelpunkt im geometrischen Schwerpunkt des Elements (Flächenschwerpunkt).
Das entspricht nicht in jedem Fall dem Mittelpunkt des Begrenzungsrahmens. 

Der Spiralmittelpunkt lässt sich mit einem [Zielpositions-Befehl](/de/docs/commmands/) manuell definieren:

* Wähle ein Element mit einer Spiralfüllung aus 
* Öffne `Erweiterungen > Ink/Stitch > Befehle > Befehle mit gewählten Objekten verknüpfen...`
* Wähle `Zielposition` und klicke auf Anwenden
* `Strg + Klick` auf das Symbol des Befehls um es auszuwählen, dann bewege es zur gewünschten Position

## Anfangs- und Endpunkt festlegen

Ink/Stitch erlaubt es über visuelle Befehle den [Anfangs- und Endpunkt eines Füllobjekts](/de/docs/commands) zu kennzeichnen.

## Parameter

Öffne `Erweiterungen > Ink/Stitch  > Parameter` um das Stickbild deinen Bedürfnissen anzupassen.

{% include params.html stitch_type='circular_fill'%}

## Unterlage

Die Unterlage der Spiralfüllung ist keine Spirale, sondern nutzt den Stichwinkel der [Parametereinstellungen](/de/docs/fill-stitch/#unterlage)

## Beispieldateien mit Spiralfüllung

{% include tutorials/tutorial_list key="stichart" value="Spiralfüllung" %}

---
title: "Lineare Farbverlaufsfüllung"
permalink: /de/docs/stitches/linear-gradient-fill/
last_modified_at: 2024-05-07
toc: true
---
## Beschreibung

Die lineare Verlaufsfüllung nutzt die in Inkscape gesetzte Farbe "linearer Verlauf" um einen nahtlosen Verlauf mit guter Stichpositionierung zu schaffen.

{% include folder-galleries path="butterfly-fill-project/linear_gradient/" captions="1:Blau-Lila-Farbverlauf;2:Rot-Gelb-Farbverlauf" %}

## Funktionsweise

* Erstelle einen geschlossenen Pfad. Der Pfad darf Löcher enthalten.
* Im Dialog `Füllung und Kontur` wähle als Füllfarbe einen linearen Farbverlauf und passe die Farben deinen Wünschen entsprechend an.
  Auf der Arbeitsfläche wird der Farbverlauf durch eine Linie dargestellt mit der die Farbpositionen und die Verlaufsrichtung direkt bearbeitet werden könne.
  Die Verlaufsrichtung bestimmt auch den Stichwinkel der Füllung (90° entgegengesetzt der Verlaufslinie).
  ![linear gradient](/assets/images/docs/en/linear-gradient.png)
* Öffne den Parameterdialog (`Erweiterungen > Ink/Stitch > Parameter`) und wähle als Füllmethode `Lineare Farbverlaufsfüllung`.
  Setze die anderen Parameter deinen Wünschen entsprechend.

### Anfangs- und Endpunkt festlegen

Ink/Stitch erlaubt es über visuelle Befehle den [Anfangs- und Endpunkt eines Füllobjekts](/de/docs/commands) zu kennzeichnen.

### Parameter

Öffne das Parameter-Dialogfenster (`Erweiterungen > Ink/Stitch  > Parameter`, um die Einstellungen zu verfeinern.

{% include params.html stitch_type='linear_gradient_fill'%}

## Unterlage

Die Unterlage nutzt den Stickwinkel der in den [Parametern der Unterlage](/de/docs/params/#füllung-unterlage) eingestellt werden kann.

## Beispieldateien mit linearer Farbverlaufsfüllung

{% include tutorials/tutorial_list key="stichart" value="Lineare Farbverlaufsfüllung" %}

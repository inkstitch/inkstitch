---
title: "Manuelle Stichplatzierung"
permalink: /de/docs/stitches/manual-stitch/
last_modified_at: 2026-04-08
toc: true
---
## Beschreibung

Im manuellen Stichmodus stellt jeder Knoten des Pfades einen Nadeleinstich dar. So ist es möglich jeden Stich genau zu planen.

{% include folder-galleries path="butterfly-fill-project/manual/" captions="1:Manueller Pfad - jeder Knotenpunkt ein Stich" %}

## Funktionsweise

1. Erstelle einen Pfad mit mehreren Knoten. Breite und Strichlinien-Einstellung haben keine Auswirkungen im manuellen Stichmodus.
2. Öffne `Erweiterungen > Ink/Stitch  > Parameter`.
3. Wähle als Methode `Manuelle Stichpositionierung`.

Jeder Knoten repräsentiert einen Nadeleinstich. Kurven werden dementsprechend nicht berechnet.

![Manual Stitch Placement](/assets/images/docs/manual-stitch-placement.png)

Für eine genaue Planung macht es deshalb Sinn, schon beim Zeichnen Kurven direkt ganz zu vermeiden, oder den Pfad vor dem Sticken entsprechend zu bearbeiten:
1. Wähle alle Knotenpunkte an (`F2` dann `Ctrl`+`A`)
2. Klicke auf ![Die gewählten Knoten in Ecken umwandeln](/assets/images/docs/tool-controls-corner.jpg){: title="Die gewählten Knoten in Ecken umwandeln" } in der `Werkzeugeinstellungsleiste`.g

## Parameter

Über `Erweiterungen > Ink/Stitch  > Parameter` können Einstellungen an den Stickparametern vorgenommen werden.

{% include params.html stitch_type='manual-stitch'%}

## Tipps

### Faden vernähen

Im manuellen Modus muss auch das Vernähen von Hand angelegt werden. Wenn du den Faden vernähen willst, plane den Pfad entsprechend.

## Beispieldateien die den manuellen Stichmodus beinhalten

{% include tutorials/tutorial_list key="stichart" value="Manueller Stich" %}


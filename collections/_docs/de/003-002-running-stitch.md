---
title: "Geradstich / Mehrfachgeradstich"
permalink: /de/docs/stitches/running-stitch/
last_modified_at: 2026-06-18
toc: true
---
## Beschreibung

Der Geradstich produziert eine Serie von kleinen Stichen entlang einer Kurve.
Häufig ist eine einfache Wiederholung zu dünn und der Geradstich wird stattdessen als Mehrfachgeradstich ausgeführt. So wird die Linie breiter und deutlicher.

{% include folder-galleries path="butterfly-fill-project/running/" captions="1:Geradstich Mandala (Redwork)" %}

[<i class="fa fa-download"></i> Beispieldateien herunterladen](/assets/images/stitch-type-butterflies/running_stitch.zip)

## Funktionsweise

Geradstich wird durch einen Pfad mit einer Konturfarbe erstellt.

Die Stickrichtung wird durch die [Pfadrichtung](/de/docs/customize/#pfadkonturen--pfadrichtungen) bestimmt. Wenn du die Richtung ändern willst, führe die Funktion `Pfad > Richtung umkehren` aus.

Wenn ein Objekt aus mehreren Pfaden besteht, werden diese der Reihe nach mit einem Sprungstich verknüpft.

### Mehrfachgeradstich

Der Mehrfachgeradstich wird durch die Eingabe eines Wertes für die Parameter-Option `Mehrfachgeradstich Anzahl der Wiederholungen` aktiviert.
Bei dieser Stichart wird jeder Stich entsprechend der Anzahl des eingegebenen Wertes vor und zurück gestickt.

## Parameter

Über [`Erweiterungen > Ink/Stitch  > Parameter`](/de/docs/params/#linie) können folgende Einstellungen vorgenommen werden.

{% include upcoming_release_params.html %}

{% include params.html stitch_type='running-stitch'%}

## Anordnen

Für eine bessere Stickreihenfolge lohnt es sich das [Linien-Werkzeug](/de/docs/stroke-tools/) `Automatisch geführter Geradstich` oder `Redwork` auszuprobieren.

Redwork sorgt für eine einheitliche Linienbreite und endet immer am Anfangspunkt. Für den automatisch geführten Geradstich kann sowohl eine Start- als auch eine Endposition festgelegt werden.

## Gemusterter Geradstich

In einem [Tutorial](/de/tutorials/patterned-unning-stitch/) erklären wir, wie mit einem Inkscape Pfadeffekt schnell und einfach ein gemusterter Geradstich entstehen kann.

![patterned running stitch](/assets/images/tutorials/pattern-along-path/copy-paste.png)

## Beispieldateien, die Geradstich enthalten

{% include tutorials/tutorial_list key="stichart" value="Geradstich" %}

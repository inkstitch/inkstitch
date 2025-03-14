---
title: "Ink/Stitch in der Shell"
permalink: /de/docs/command-line/
last_modified_at: 2024-07-13
---
Ink/Stitch kann bequem über die Shell ausgeführt werden.

## Beispiele für die Befehlszeile

### Zip-Export

Um ein Zip-Archiv (mit dst, pes und Garnliste) zu erstellen, führe folgenden Befehl aus:

```
./inkstitch --extension=zip --format-dst=True --format-pes=True --format-threadlist=True input-file.svg > output-file.zip
```

### Stichplan

Hier ein Beispiel für die Erstellung eines SVG mit dem Stichplan für zwei spezifische Objekte. Das Original-Design wird versteckt, die Nadelpunkte werden angezeigt und der Stichplan direkt über dem Originaldeisgn platziert.

```
./inkstitch --extension=stitch_plan_preview --id=path1 --id=path2 --move-to-side=False --layer-visibility=hidden --needle-points=True input.svg > output.svg
```

## Inkscape Optionen für die Befehlszeile

Für eine komplette Übersicht möglicher Optionen, gibt es eine [man page](https://inkscape.org/doc/inkscape-man.html) auf der Inkscape Webseite.

Ink/Stitch Erweiterungen können so zusammen mit anderen "Inkscape actions" ausgeführt werden. Eine komplette Übersicht über mögliche `actions` gibt es über folgende Abfrage

```
inkscape --action-list
```

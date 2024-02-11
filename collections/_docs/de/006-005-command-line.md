---
title: "Ink/Stitch in der Shell"
permalink: /de/docs/command-line/
last_modified_at: 2023-12-31
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
./inkstitch --extension=stitch_plan_preview --id=path1 id=path2 --move-to-side=False --layer-visibility=hidden --needle-points=True input.svg > output.svg
```

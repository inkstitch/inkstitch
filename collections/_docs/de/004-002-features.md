---
title: "Versteckte Funktionen"
permalink: /de/docs/features/
excerpt: ""
last_modified_at: 2019-03-15
toc: true
---
## Farbverlauf

Die Version 1.4.0 hat eine neue Funktion für Farbverläufe eingeführt. Sie funktioniert noch nicht 100% zuverlässig und ist deshalb etwas versteckt.

Öffne den XML-Editor und füge `embroider_end_row_spacing_mm` hinzu. Dann erhälst du einen Effekt, wie er in [#78](https://github.com/inkstitch/inkstitch/issues/78) beschrieben ist.

Objekte mit komplizierten Formen und Löchern lassen anscheinend die Funktion in eine Endlosschleife laufen, so dass der Prozess manuel beendet werden muss. Aber für die meisten Formen funktionert der Algorhitmus. Kombiniere zwei solcher Objekte in gegensätzlicher Richtung, dann erhälst du einen Farbverlauf.

![image](https://user-images.githubusercontent.com/11083514/38469632-dc97b73c-3b4f-11e8-9044-c03d1f5d17ab.png)


Hier gibt es eine Tutorial-Datei:

[Tutorial-embroider_end_row_spacing_mm.zip](https://github.com/inkstitch/inkstitch/files/1887652/Tutorial-embroider_end_row_spacing_mm.zip)

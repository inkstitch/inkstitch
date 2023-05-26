---
title: Füllstich Werkzeuge
permalink: /de/docs/fill-tools/
excerpt: ""
last_modified_at: 2023-05-11
toc: true
---
## Füllstich-Objekte zerlegen

Füllstich Objekte sollten aus Objekten bestehen, deren Randlinien sich nicht kreuzen. Manchmal ist es wirklich nicht einfach, diese Regel zu erfüllen, denn oft entstehen winzige Schleifen, die man in Inkscape gar nicht sehen kann. Aus diesem Grund können Füllstiche oft ärgerliche Fehlermeldungen hervorrufen.

Diese Erweiterung soll dir helfen, kaputte Objekte zu repaireren. Nutze diese Funktion einfach für alle Füllstich-Bereiche die eine Fehlermeldung ausgeben. Sie wird kleine Schleifen entfernen und wenn nötig, deine Form in kleinere Unterabschnitte unterteilen.

### Funktionsweise

* Wähle ein oder mehrere Füllobjekte aus
* Öffne das Dialogfenster unter `Erweiterungen > Ink/Stitch  > Füllstich Werkzeuge  > Füllstich-Objekte zerlegen`

## Einfach oder Komplex

* *Einfach* kann mit Löchern, unverbundenen Objekten und sich überkreuzenden Rändern arbeiten. Kombinierte Pfade werden in einzelne Pfade zerlegt.

* *Komplex* agiert genauso wie "einfach", kann aber zusätzlich mit Objekten mit mehreren sich überschneidenden Pfaden umgehen.

![Break apart fill objects](/assets/images/docs/en/break_apart.jpg)
[Download SVG](/assets/images/docs/en/break_apart.svg)

## Farbverlauf in Blöcke aufteilen

Diese Erweiterung teilt ein Füllobjekt mit einem linearen Farbverlauf in mehrere einfarbige Blöcke auf und setzt den zuvor bestimmten Wert für `Reihenabstand Ende`.

### Anwendung

1. Setze einen linearen Farbverlauf

   ![linear gradient](/assets/images/docs/en/linear-gradient.png)
2. `Erweiterungen > Ink/Stitch > Werkzeuge: Füllung > Farbverlauf in Blöcke aufteilen...`

   ![color blocks](/assets/images/docs/color_blocks.png)
3. Setze einen Wert für den Reihenabstand am Ende der Füllung. Bei einem Wert von 0.00 wird der doppelte Wert des ursprünglichen Reihenabstandes angenommen.

## Tutorials zu Füllwerkzeugen

{% include tutorials/tutorial_list key="werkzeug" value="Füllung" %}

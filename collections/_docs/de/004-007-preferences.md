---
title: "Einstellungen"
permalink: /de/docs/preferences/
excerpt: ""
last_modified_at: 2023-02-21
toc: false
---
Die Version 2.2.0 hat noch keine globalen Einstellungsmöglichkeiten.

{% include upcoming_release.html %}

Die Einstellungen können über `Erweiterungen > Ink/Stitch > Einstellungen` abgerufen werden.

Globale Einstellungen werden direkt auf jedes neue SVG-Dokument angewendet, während die Einstellungen im ersten Reiter dokumentspezifisch sind.

## Ausgabeeinstellungen

* Maximaler Abstand zwischen zwei Objekten ohne vernähen (mm): Sprungstiche die kleiner als der angegebene Wert sind, werden als normale Stiche behandelt und nicht vernäht.
* Minimale Stichlänge (mm): Stiche die kleiner sind als dieser Wert, werden gelöscht und nicht exportiert (Ausnahme: Vernähstiche).

* Nur als globale Einstellung: **Cache Größe:** Bestimme wieviel Platz der Festplatte dafür verwendet werden darf, Stichpläne in den Cache zu speichern. Gespeicherte Stichpläne müssen nicht erneut gerendert werden. Dadurch wird die Berechnungszeit erheblich verkürzt. Je höher dieser Wert ist, desto mehr Stichpläne können gespeichert werden. Standartwert: 100
  
**W6 Maschinenbesitzer:** Setze den globalen Wert für die minimale Stichlänge auf mindestens 0.3 mm. Ansonsten kann es passieren, dass an unerwarteten Stellen Stiche fehlen werden.
{: .notice--warning }

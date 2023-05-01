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

<!--

* Maximaler Abstand zwischen zwei Objekten ohne vernähen (mm): Sprungstiche die kleiner als der angegebene Wert sind, werden als normale Stiche behandelt und nicht vernäht.
* Minimale Stichlänge (mm): Stiche die kleiner sind als dieser Wert, werden gelöscht und nicht exportiert (Ausnahme: Vernähstiche).
-->

* **Minimum jump stitch length (mm)**: 
  *  Any shorter jump between subpaths of a composite path will be treated as a normal stitch (no lock stitches added)
  *  In case of a jump beetween two succcesive paths, if the jump between the two paths is shorter than this value, lock stitches at ending point and tack stiches at starting point are only created if Force lock stitches is enabled in the corresponding path.  If the jump is longer, lock stitches and tack stitches are true to their settings.
  
* **Minimum stitch length (mm)**: Stitches smaller than this value will be dropped (exception: lock stitches). This value is only used at the very end of the stitch plan computation to filter too short stitches. Be aware that the behavior is may be not what you expected : for instance if Minimum stitch length is set to 2mm and you have running stitches with maximum stitch length of 1.5mm, every other stich is dropped, yielding a running path  with 3mm stiches. 

Simulation take these parameters into account.

* Nur als globale Einstellung: **Cache Größe:** Bestimme wieviel Platz der Festplatte dafür verwendet werden darf, Stichpläne in den Cache zu speichern. Gespeicherte Stichpläne müssen nicht erneut gerendert werden. Dadurch wird die Berechnungszeit erheblich verkürzt. Je höher dieser Wert ist, desto mehr Stichpläne können gespeichert werden. Standartwert: 100
  
**W6 Maschinenbesitzer:** Setze den globalen Wert für die minimale Stichlänge auf mindestens 0.3 mm. Ansonsten kann es passieren, dass an unerwarteten Stellen Stiche fehlen werden.
{: .notice--warning }

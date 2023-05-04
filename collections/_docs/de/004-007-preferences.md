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

* **Minimale Länge für Sprungstiche (mm)**:
  * Jeder Sprung zwischen Unterpfaden, der kleiner ist als dieser Wert, wird als normaler Stich gestickt (ohne zusätzliche Vernähstiche)
  * Sollten für einen kürzeren Abstand trotzdem Vernähstiche erwünscht sein, kann die Funktion `Vernähstiche erzwingen` aktiviert werden.
  * Längere Sprungstiche verhalten sich gemäß den Vernähstich-Einstellungen des einzelnen Objektes

* **Minimale Stichlänge (mm)**: Stiche die kleiner sind als dieser Wert, werden gelöscht (Ausnahme: Vernähstiche).
  Dieser Wert wird auf den gerenderten Stichplan angewendet und verhält sich evtl. anders als erwartet:
  Ist die minimale Stichlänge auf 2 mm gesetzt und die Geradstichlänge auf 1.5 mm eingestellt, ergibt dies im Ergebnis eine Stichlänge von durchschnittlich 3 mm. 

* Nur als globale Einstellung: **Cache Größe:** Bestimme wieviel Platz der Festplatte dafür verwendet werden darf, Stichpläne in den Cache zu speichern.
  Gespeicherte Stichpläne müssen nicht erneut gerendert werden. Dadurch wird die Berechnungszeit erheblich verkürzt.
  Je höher dieser Wert ist, desto mehr Stichpläne können gespeichert werden. Standartwert: 100
  
**W6 Maschinenbesitzer:** Setze den globalen Wert für die minimale Stichlänge auf mindestens 0.3 mm. Ansonsten kann es passieren, dass an unerwarteten Stellen Stiche fehlen werden.
{: .notice--warning }

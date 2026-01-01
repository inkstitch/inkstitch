---
title: "Einstellungen"
permalink: /de/docs/preferences/
last_modified_at: 2024-05-22
toc: true
---
Die Einstellungen können über `Erweiterungen > Ink/Stitch > Einstellungen` abgerufen werden.

Globale Einstellungen werden direkt auf jedes neue SVG-Dokument angewendet, während die Einstellungen im ersten Reiter dokumentspezifisch sind.

Einstellungen für das geöffnete Dokument können mit einem Klick auch auf die globalen Werte übertragen werden.

Diese Einstellungen werden auf alle Elemente des Dokuments angewendet.
{: .notice--info }

## Minimale Länge für Sprungstiche (mm)

* Jeder Sprungstich zwischen zwei Pfaden der gleichen Farbe, der kleiner ist als dieser Wert, wird als normaler Stich gestickt (ohne zusätzliche Vernähstiche)
* Sollten für einen kürzeren Abstand trotzdem Vernähstiche erwünscht sein, kann die Funktion `Vernähstiche erzwingen` aktiviert werden.
* Längere Sprungstiche verhalten sich gemäß den Vernähstich-Einstellungen des einzelnen Objektes

Ab der Version 3.1.0 kann der globale Wert bei einzelnen Elementen durch eine Einstellung in den [Parametern](/docs/params) überschrieben werden.

## Minimale Stichlänge (mm)

* Stiche die kleiner sind als dieser Wert, werden gelöscht (Ausnahme: Vernähstiche).
* Setze den globalen Wert für die minimale Stichlänge auf mindestens 0.3 mm. Ansonsten kann es bei manchen Maschinen (z.B. W6-Stickeinheiten) passieren, dass an unerwarteten Stellen Stiche fehlen werden.

Ab der Version 3.1.0 kann der globale Wert bei einzelnen Elementen durch eine Einstellung in den [Parametern](/docs/params) überschrieben werden.

### Auswirkung auf den Stichplan

Die Minimale Stichlänge wird auf den fertig gerenderten Stichplan angewendet und verhält sich evtl. anders als erwartet. Ist beispielsweise die minimale Stichlänge auf 2 mm gesetzt und die Geradstichlänge auf 1.5 mm eingestellt, ergibt dies im Ergebnis eine Stichlänge von durchschnittlich 3 mm.

![simulation](/assets/images/docs/preference_msl_paths.png)

*Geradstiche mit einer Sitchlänge 0,5 mm. 1: Minimale Sitchlänge 0,5 mm. 2: Minimale Stichlänge 2 mm*

Ist die minimale Stichlänge kleiner als der `Reihenabstand` fällt der Effekt bei **Füllstichen** ganz besonders an den Seitenrändern der Füllung auf (ganz wie der Wert `Letzten Stich überspringen`).
Bei **Geradstichen** zeigen sich Veränderungen insbesondere bei `engen Kurven` und niedrigem Toleranzwert.

*Minimale Stichlänge* | Füllung mit 0,25 mm Reihenabstand | Kurvenfüllung mit 0,25 mm Reihenabstand | Geradstich mit einer Stichlänge von 1.5 mm bei kleiner Designgröße (10 mm Breite)
---|---|---|---
0   |![square 0](/assets/images/docs/preference_fill_0.png)     |![square 0](/assets/images/docs/preference_guided_0.png)     |![running_0](/assets/images/docs/preference_running_stitch_0.png)
0,5 |![square 0.5](/assets/images/docs/preference_fill_half.png)|![square 0.5](/assets/images/docs/preference_guided_half.png)|![running_0](/assets/images/docs/preference_running_stitch_half.png)
1   |![square 1](/assets/images/docs/preference_fill_1.png)     |![square 1](/assets/images/docs/preference_guided_1.png)     |![running_0](/assets/images/docs/preference_running_stitch_1.png)

Die minimale Stichlänge kann sich dementsprechend auch auf **Satinsäulen** auswirken. Der Wert sollte bei der Verwendung kleiner Schriften wie beispielsweise *Ink/Stitch small* oder *Glacial Tiny* nicht zu hoch gesetzt sein:

*Minimale Stichlänge* | *Ink/Stitch Small* | *Glacial Tiny*
---|---|---
0 or 0,5 |![ink_stitch_O](/assets/images/docs/preference_ink_small_0.png)|![glacial_O](/assets/images/docs/preference_glacial_0.png)
1        |![ink_stitch_1](/assets/images/docs/preference_ink_small_1.png)|![glacial_1](/assets/images/docs/preference_glacial_1.png)

Stiche mit **manueller Stichpositionierung** werden ebenfalls entsprechend dieser Einstellung angepasst. Dies kann von Nutzen sein, wenn die Stiche versehentlich zu eng gesetzt wurden.

### Rotiere bei Export (nur dokumentbezogen)

{% include upcoming_release.html %}

Diese Option rotiert das Stickbild beim Export um 90°. Dies ist nützlich, wenn eine Stickmaschine ein Design nicht automatisch dreht um es in den Stickrahmen einzupassen.

## Cache Größe (MB)

* Dieser Wert kann nur global gesetzt werden.
* Er definiert, wie viel Platz auf der Festplatte zum Speichern der Stichpläne zur Verfügung steht.
  Die Standardgröße für den Cache-Speicher ist 100 MB.
* Je größer der Wert ist, desto mehr Stichpläne können im Cache gespeichert werden.
  Ein im Cache gespeicherter Stichplan muss nicht erneut gerendert werden. Dies beschleunigt den Vorgang erheblich.
* Der Cache kann über einen Knopf im Reiter `globale Einstellungen` geleert werden.

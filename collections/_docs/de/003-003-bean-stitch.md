---
title: "Mehrfach Geradstich"
permalink: /de/docs/stitches/bean-stitch/
excerpt: ""
last_modified_at: 2023-01-16
toc: true
---
## Beschreibung

[![Bean Stitch Dog](/assets/images/docs/bean-stitch-example.jpg){: width="200x"}](/assets/images/docs/bean-stitch.svg){: title="Download SVG File" .align-left download="bean-stitch.svg" }
Mehrfachgeradstich oder "Bean stitch" beschreibt eine Wiederholung von Geradstichen (vor und zurück). Durch die Wiederholungen wird der Faden dicker und die Linie deutlicher.

![Bean Stitch Detail](/assets/images/docs/bean-stitch-detail.jpg){: width="350x" }

## Funktionsweise

1. Markiere eine **gestrichelte Linie** und öffne `Erweiterungen > Ink/Stitch  > Parameter`.

2. Im [Geradstich-Modus](/de/docs/stitches/running-stitch) gibt es die Option `Geradstich Anzahl der Wiederholungen`. Wird eine Zahl gesetzt, aktiviert dies gleichzeitig den Mehrfach-Geradstich-Modus.

   ![Bean Stitch Params](/assets/images/docs/en/params-bean-stitch.jpg)

   * Ein Wert von 1 verdreifacht jeden Stich (vor, zurück, vor), es entsteht ein Dreifach-Geradstich.
   * Ein Wert von 2 verfünfacht jeden Stich (vor, zurück, vor, zurück, vor), es entsteht ein Fünffach-Geradstich, etc.
   * Durch die Eingabe mehrerer durch ein Leerzeichen getrennter Werte  ein Muster zu erzeugen (z.B ergibt der Wert `1 0` folgendes Muster: `≡-≡-≡`)

## Parameter

Einstellung|Beschreibung
---|---
Geradstich                            | Muss aktiviert sein, damit diese Einstellungen wirksam werden.
Methode                               | Der Mehrfachgeradstich kann sowohl auf Geradstiche als auch auf Ripple-Stiche angewendet werden
Manuelle Stichpositionierung          | Aktiviert den [manuellen Stichmodus](#manuelle-füllung)
Wiederholungen                        | ◦ Legt fest, wie oft der Pfad durchlaufen werden soll<br/>◦ Standard: 1 (einmal vom Anfang bis zum Ende des Pfades)<br/>◦ Ungerade Zahl: Stiche enden am Ende des Pfades<br/>◦ Gerade Zahl: Die Naht kehrt zum Anfang des Pfades zurück
**Mehrfach Geradstitch Anzahl der Wiederholungen** | ◦ Jeden Stich vervielfachen.<br/>◦ Ein Wert von 1 würde jeden Stich verdreifachen (vorwärts, rückwärts, vorwärts).<br/>◦ Ein Wert von 2 würde jeden Stich fünffach ausführen, usw.<br/>◦ Durch die Eingabe mehrerer durch ein Leerzeichen getrennte Werte, kann ein Wiederholungsmuster erstellt werden.
Stichlänge                            | Länge der Stiche
Geradstich Toleranz                   | Alle Stiche müssen innerhalb dieser Distanz zum Pfad liegen. Eine niedrigere Toleranz verkürzt die Stiche. Eine höhere Toleranz kann scharfe Ecken abrunden.
Zick-Zack Abstand (Spitze zu Spitze)  | ◦ Stichabstand im [Zick-Zack-Modus](/de/docs/stitches/zigzag-stitch/)<br>◦ Die Höhe wird durch die Breite der Linie definiert
Vernähen erlauben                     | Vernäht bei Bedarf an den ausgewählten Positionen
Vernähen erzwingen                    | Vernäht den Faden nach diesem Element, auch dann, wenn der Abstand zum Folgeobjekt geringer ist als in den [Ink/Stitch Einstellungen](/de/docs/preferences/) definiert.
Tack stitch                           |Chose your [favorite style](/docs/stitches/lock-stitches/)
Lock stitch                           |Chose your [favorite style](/docs/stitches/lock-stitches/)
Fadenschnitt                          | Schneidet den Faden nachdem dieses Objekt genäht wurde
Stopp                                 | Stoppt die Maschine nachdem dieses Objekt genäht wurde und springt zur Stopp-Position (sofern vorhanden)

{% include upcoming_release.html %} 
By entering a sequence of space separated integers in Bean stitch number of repeats, it is possible to define a custom stitch. For instance the sequence 0 1 will yield alternating simple and triple stitches.

## Beispieldateien mit Mehrfachgeradstich

{% include tutorials/tutorial_list key="stichart" value="Mehrfachgeradstich" %}

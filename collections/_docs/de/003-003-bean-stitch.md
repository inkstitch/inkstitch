---
title: "Mehrfachgeradstich"
permalink: /de/docs/stitches/bean-stitch/
last_modified_at: 2024-05-07
toc: true
---
## Beschreibung

[![Bean Stitch Dog](/assets/images/docs/bean-stitch-example.jpg){: width="200x"}](/assets/images/docs/bean-stitch.svg){: title="Download SVG File" .align-left download="bean-stitch.svg" }
Mehrfachgeradstich oder "Bean stitch" beschreibt eine Wiederholung von Geradstichen (vor und zurück). Durch die Wiederholungen wird der Faden dicker und die Linie deutlicher.

![Bean Stitch Detail](/assets/images/docs/bean-stitch-detail.jpg){: width="350x" }

## Funktionsweise

1. Markiere eine Linie und öffne `Erweiterungen > Ink/Stitch  > Parameter`.

2. Im [Geradstich-Modus](/de/docs/stitches/running-stitch) gibt es die Option `Geradstich Anzahl der Wiederholungen`. Wird eine Zahl gesetzt, aktiviert dies gleichzeitig den Mehrfach-Geradstich-Modus.

   ![Bean Stitch Params](/assets/images/docs/en/params-bean-stitch.jpg)

   * Ein Wert von 1 verdreifacht jeden Stich (vor, zurück, vor), es entsteht ein Dreifach-Geradstich.
   * Ein Wert von 2 verfünfacht jeden Stich (vor, zurück, vor, zurück, vor), es entsteht ein Fünffach-Geradstich, etc.
   * Die Eingabe mehrerer durch ein Leerzeichen getrennte Werte erzeugt ein Muster (z.B ergibt der Wert `1 0` einen Wechsel von einfachen Geradstichen und Dreifachstichen: `≡-≡-≡`)

## Parameter

{% include upcoming_release_params.html %}

Einstellung|Beschreibung
---|---
Geradstich                            | Muss aktiviert sein, damit diese Einstellungen wirksam werden.
Methode                               | Der Mehrfachgeradstich kann sowohl auf Geradstiche, Ripple-Stiche oder die manuelle Stichpositionierung angewendet werden
Wiederholungen                        | ◦ Legt fest, wie oft der Pfad durchlaufen werden soll<br/>◦ Standard: 1 (einmal vom Anfang bis zum Ende des Pfades)<br/>◦ Ungerade Zahl: Stiche enden am Ende des Pfades<br/>◦ Gerade Zahl: Die Naht kehrt zum Anfang des Pfades zurück
**Mehrfach Geradstitch Anzahl der Wiederholungen** | ◦ Jeden Stich vervielfachen.<br/>◦ Ein Wert von 1 verdreifacht jeden Stich (vorwärts, rückwärts, vorwärts).<br/>◦ Ein Wert von 2 verfünffacht jeden Stich, usw.<br/>◦ Durch die Eingabe mehrerer durch ein Leerzeichen getrennter Werte, kann ein Wiederholungsmuster erstellt werden.
Stichlänge                            | Länge der Stiche. Durch Eingabe mehrerer Werte kann ein Stichlängenmuster erstellt werden. Beispielsweise werden bei einem Wert von `2 4` eine Abfolge von Stichen erstellt, die abwechselnd eine Länge von 2mm und 4mm haben.
Geradstich Toleranz                   | Alle Stiche müssen innerhalb dieser Distanz zum Pfad liegen. Eine niedrigere Toleranz verkürzt die Stiche. Eine höhere Toleranz kann scharfe Ecken abrunden.
Zufällige Stichlänge                  | Anstatt einer gleichmäßigen Verteilung, erfolgt die Stichlänge und -phase nach dem Zufallsprinzip. Dies wird besonders für eng beieinander liegende Kurvenfüllungen empfohlen, um Moiré-Artefakte zu vermeiden.
Zufallsabweichung von der Stichlänge  | Maximale randomisierte Abweichung der Stichabstände in Prozent. Zufällige Stichlänge randomisieren muss aktiviert sein.
Zuffalszahl                           | Zufallswert für randomisierte Attribute. Verwendet die Element-ID, falls leer.
Minimale Stichlänge                   | Überschreibt die globale Einstellung für die minimale Stichlänge. Stiche, die kleiner sind als dieser Wert werden entfernt.
Minimale Länge für Sprungstiche       | Überschreibt die globale Einstellung für die minimale Länge für Sprungstiche. Kleinere Entfernungen zum nächsten Objekt haben keine Vernähstiche.
Vernähen erlauben                     | Vernäht bei Bedarf an den ausgewählten Positionen
Vernähen erzwingen                    | Vernäht den Faden nach diesem Element, auch dann, wenn der Abstand zum Folgeobjekt geringer ist als in den [Ink/Stitch Einstellungen](/de/docs/preferences/) definiert.
Anstecher                             | Wähle die [Anstecher](/de/docs/stitches/lock-stitches) Variante (Anfang).
Verstecher                            | Wähle die [Verstecher](/de/docs/stitches/lock-stitches) Variante (Ende).
Fadenschnitt                          | Schneidet den Faden nachdem dieses Objekt genäht wurde
Stopp                                 | Stoppt die Maschine nachdem dieses Objekt genäht wurde und springt zur Stopp-Position (sofern vorhanden)

## Beispieldateien mit Mehrfachgeradstich

{% include tutorials/tutorial_list key="stichart" value="Mehrfachgeradstich" %}

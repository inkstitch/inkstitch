---
title: "Geradstich"
permalink: /de/docs/stitches/running-stitch/
excerpt: ""
last_modified_at: 2023-04-19
toc: true
---
## Beschreibung

[![Running Stitch Butterfly](/assets/images/docs/running-stitch.jpg){: width="200x"}](/assets/images/docs/running-stitch.svg){: title="Download SVG Datei" .align-left download="running-stitch.svg" }

Der Geradstich produziert eine Serie von kleinen Stichen entlang einer Kurve.

![Running Stitch Detail](/assets/images/docs/running-stitch-detail.jpg)

## Funktionsweise

Geradstich kann durch eine **gestichelte Linie** erstellt werden. Jede Strichlinienart erfüllt diesen Zweck. Die Linienbreite spielt dabei keine Rolle.

![Running Stitch Dashes](/assets/images/docs/running-stitch-dashes.jpg){: .align-left style="padding: 5px"}
* Wähle eine Linie aus und öffne das Dialogfeld `Objekte > Küllung und Kontur...`.
* Im Reiter `Muster der Kontur` eine Strichlinie aktivieren.

Die Stickrichtung wird durch die Pfadrichtung bestimmt. Wenn du die Richtung ändern willst, führe die Funktion `Pfad > Richtung umkehren` aus.

Wenn ein Objekt aus mehreren Pfaden besteht, werden diese der Reihe nach mit einem Sprungstich verknüpft.

**Info:** Um abgerundete Ecken zu vermeiden, wird an jeder scharfen Ecke ein zusätzlicher Stich eingefügt.
{: .notice--info style="clear: both;" }

## Parameter

Über [`Erweiterungen > Ink/Stitch  > Parameter`](/de/docs/params/#linie) können folgende Einstellungen vorgenommen werden.

Einstellung|Beschreibung
---|---
Geradstich                            | Muss aktiviert sein, damit diese Einstellungen wirksam werden.
Methode                               | Geradstich auswählen
Manuelle Stichpositionierung          | Aktiviert den [manuellen Stichmodus](#manuelle-füllung)
Wiederholungen                        | ◦ Legt fest, wie oft der Pfad durchlaufen werden soll<br/>◦ Standard: 1 (einmal vom Anfang bis zum Ende des Pfades)<br/>◦ Ungerade Zahl: Stiche enden am Ende des Pfades<br/>◦ Gerade Zahl: Die Naht kehrt zum Anfang des Pfades zurück
Bean stitch Anzahl der Wiederholungen | ◦ Jeden Stich vervielfachen.<br/>◦ Ein Wert von 1 würde jeden Stich verdreifachen (vorwärts, rückwärts, vorwärts).<br/>◦ Ein Wert von 2 würde jeden Stich fünffach ausführen, usw.<br/>◦ Gilt nur für den Geradstich.
Stichlänge                            | Länge der Stiche
Geradstich Toleranz                   | Alle Stiche müssen innerhalb dieser Distanz zum Pfad liegen. Eine niedrigere Toleranz verkürzt die Stiche. Eine höhere Toleranz kann scharfe Ecken abrunden.
Vernähen erlauben                     | Vernäht bei Bedarf an den ausgewählten Positionen
Vernähen erzwingen                    | Vernäht den Faden nach diesem Element, auch dann, wenn der Abstand zum Folgeobjekt geringer ist als in den [Ink/Stitch Einstellungen](/de/docs/preferences/) definiert.
Anstecher                             |Wähle die [Anstecher](/de/docs/stitches/lock-stitches) Variante (Anfang).
Verstecher                            |Wähle die [Verstecher](/de/docs/stitches/lock-stitches) Variante (Ende).
Fadenschnitt                          | Schneidet den Faden nachdem dieses Objekt genäht wurde
Stopp                                 | Stoppt die Maschine nachdem dieses Objekt genäht wurde und springt zur Stopp-Position (sofern vorhanden)

## Anordnen

Für eine bessere Stickreihenfolge lohnt es sich das [Linien-Werkzeug](/de/docs/stroke-tools/) `Automatisch geführter Geradstich` auszuprobieren.

## Gemusterter Geradstich

In einem [Tutorial](/de/tutorials/patterned-unning-stitch/) erklären wir, wie mit einem Inkscape Pfadeffekt schnell und einfach ein gemusterter Geradstich entstehen kann.

![patterned running stitch](/assets/images/tutorials/pattern-along-path/copy-paste.png)

## Beispieldateien, die Geradstich enthalten

{% include tutorials/tutorial_list key="stichart" value="Geradstich" %}

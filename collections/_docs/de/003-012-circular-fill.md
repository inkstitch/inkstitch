---
title: "Spiralfüllung"
permalink: /de/docs/stitches/circular-fill/
excerpt: ""
last_modified_at: 2023-05-01
toc: true
---
{% include upcoming_release.html %}

## Beschreibung

Eine Spiralfüllung füllt eine Form mit einer gestickten Spirale. Der Mittelpunkt der Spirale liegt im Mittelpunkt des Elements. Eine Zielposition kann definiert werden um den Spiralmittelpunkt zu verschieben.

![Circular stitch detail](/assets/images/docs/circular-fill-detail.png)

## Funktionsweise

* Erstelle einen geschlossenen Pfad mit einer Füllung. Aussparungen innerhalb der Form sind möglich.
* * In den Parametereinstellungen (`Erweiterungen > Ink/Stitch > Parameter`) `Spiralfüllung` als Füllmethode auswählen. Die restlichen Parameter können nach eigenem Belieben angepasst werden.

## Spiralmittelpunkt festlegen

Definiere eine Zielposition mit einem [visuellen Befehl](/de/docs/commmands/):

* Wähle ein Element mit einer Spiralfüllung aus 
* Öffne `Erweiterungen > Ink/Stitch > Befehle > Befehle mit gewählten Objekten verknüpfen...`
* Wähle `Zielposition` und clicke auf Anwenden
* `Strg + Klick` auf das Symbol des Befehls um es auszuwählen, dann bewege es zur gewünschten Position

Wenn keine Zielposition definiert wurde, liegt der Spiralmittelpunkt in der Mitte des Objektes.

## Anfangs- und Endpunkt festlegen

Ink/Stitch erlaubt es über visuelle Befehle den [Anfangs- und Endpunkt eines Füllobjekts](/de/docs/commands) zu kennzeichnen.

## Parameter

Öffne `Erweiterungen > Ink/Stitch  > Parameter` um das Stickbild deinen Bedürfnissen anzupassen.

Einstellung          ||Beschreibung
---|---|---
Automatisch geführte Füllstiche | ☑ |Muss aktiviert sein
Füllmethode          | Spiralfüllung|Für diesen Stichtyp bitte Spiralfüllung auswählen
Erweitern            |![Expand example](/assets/images/docs/params-fill-expand.png)  |Erweitert die Ursprungsform. Diese Option kann genutzt werden um Lücken zwischen angrenzenden Objekten zu verringern. Negative Werte verkleinern die Form.
Stichlänge           ||Definiert die maximale Stichlänge. Minimale Stichlänge bitte über die Geradstich-Toleranz festlegen.
Geradstich-Toleranz  ||Alle Stiche müssen innerhalb dieser Distanz vom Ursprungspfad liegen. Ein geringerer Toleranzwert bedeutet, dass Stiche enger zusammenliegen. Ein höherer Wert kann zu abgerundeten Ecken führen.
Verbindungsstiche innerhalb des Objektes|![Skip example](/assets/images/docs/params-fill-underpathing.png)| Muss aktiviert sein, um Geradstiche zum Verbinden der Abschnitte innerhalb des Objekts verlaufen zu lassen, anstatt sie am Rand entlang zu führen.
Vernähen erlauben    || Vernäht bei Bedarf an den ausgewählten Positionen
Vernähen erzwingen   || Vernäht den Faden nach diesem Element, auch dann, wenn der Abstand zum Folgeobjekt geringer ist als in den [Ink/Stitch Einstellungen](/de/docs/preferences/) definiert.
Anstecher            ||Wähle die [Anstecher](/docs/stitches/lock-stitches) Variante (Anfang).
Verstecher           ||Wähle die [Verstecher](/docs/stitches/lock-stitches) Variante (Ende).
Fadenschnitt         || Schneidet den Faden nachdem dieses Objekt genäht wurde
Stopp                || Stoppt die Maschine nachdem dieses Objekt genäht wurde und springt zur Stopp-Position (sofern vorhanden)

## Unterlage

Die Unterlage der Spiralfüllung ist keine Spirale, sondern nutzt den Stichwinkel der [Parametereinstellungen](/de/docs/fill-stitch/#unterlage)

## Beispieldateien mit Spiralfüllung

{% include tutorials/tutorial_list key="stitch-type" value="Spiralfüllung" %}

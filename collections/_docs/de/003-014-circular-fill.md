---
title: "Spiralfüllung"
permalink: /de/docs/stitches/circular-fill/
last_modified_at: 2024-06-07
toc: true
---
## Beschreibung

Eine Spiralfüllung füllt eine Form mit einer gestickten Spirale. Der Mittelpunkt der Spirale liegt im Mittelpunkt des Elements. Eine Zielposition kann definiert werden um den Spiralmittelpunkt zu verschieben.

![Circular stitch detail](/assets/images/docs/circular-fill-detail.png)

## Funktionsweise

* Erstelle einen geschlossenen Pfad mit einer Füllung. Aussparungen innerhalb der Form sind möglich.
* In den Parametereinstellungen (`Erweiterungen > Ink/Stitch > Parameter`) `Spiralfüllung` als Füllmethode auswählen.
  Die restlichen Parameter können nach Belieben angepasst werden.

## Spiralmittelpunkt festlegen

Standartmäßig ist der Spiralmittelpunkt im geometrischen Schwerpunkt des Elements (Flächenschwerpunkt).
Das entspricht nicht in jedem Fall dem Mittelpunkt des Begrenzungsrahmens. 

Der Spiralmittelpunkt lässt sich mit einem [Zielpositions-Befehl](/de/docs/commmands/) manuell definieren:

* Wähle ein Element mit einer Spiralfüllung aus 
* Öffne `Erweiterungen > Ink/Stitch > Befehle > Befehle mit gewählten Objekten verknüpfen...`
* Wähle `Zielposition` und klicke auf Anwenden
* `Strg + Klick` auf das Symbol des Befehls um es auszuwählen, dann bewege es zur gewünschten Position

## Anfangs- und Endpunkt festlegen

Ink/Stitch erlaubt es über visuelle Befehle den [Anfangs- und Endpunkt eines Füllobjekts](/de/docs/commands) zu kennzeichnen.

## Parameter

Öffne `Erweiterungen > Ink/Stitch  > Parameter` um das Stickbild deinen Bedürfnissen anzupassen.

Einstellung          ||Beschreibung
---|---|---
Automatisch geführte Füllstiche | ☑ |Muss aktiviert sein
Füllmethode          | Spiralfüllung|Für diesen Stichtyp bitte Spiralfüllung auswählen
Erweitern            |![Expand example](/assets/images/docs/params-fill-expand.png)  |Erweitert die Ursprungsform. Diese Option kann genutzt werden um Lücken zwischen angrenzenden Objekten zu verringern. Negative Werte verkleinern die Form.
Reihenabstand        |![Spacing example](/assets/images/docs/params-fill-spacing_between_rows.png) | Abstand zwischen den Stichreihen.
Reihenabstand (Ende) |![End row spacing example](/assets/images/docs/params-fill-end_row_spacing.png) | Erhöht oder verringert den Reihenabstand zum Ende hin.
Unterpfad            |![Skip example](/assets/images/docs/params-fill-underpathing.png)| Muss aktiviert sein, um Geradstiche zum Verbinden der Abschnitte innerhalb des Objekts verlaufen zu lassen, anstatt sie am Rand entlang zu führen.
Stichlänge           ||Definiert die maximale Stichlänge.
Geradstich-Toleranz  ||Alle Stiche müssen innerhalb dieser Distanz vom Ursprungspfad liegen. Ein geringerer Toleranzwert bedeutet, dass Stiche enger zusammenliegen. Ein höherer Wert kann zu abgerundeten Ecken führen. Zu eng beieinander liegende Stiche werden allerdins durch die minimale Stichlänge (globale oder objektbasierte Einstellung, s.u.) wieder entfernt.
Zufällige Stiche     |☑ |Anstatt einer gleichmäßigen Verteilung, erfolgt die Stichlänge und -phase nach dem Zufallsprinzip. Dies wird besonders für eng beieinander liegende Kurvenfüllungen empfohlen, um Moiré-Artefakte zu vermeiden.
Zufallsabweichung von der Stichlänge| |Maximale randomisierte Abweichung der Stichabstände in Prozent.
Zuffalszahl| |Zufallswert für randomisierte Attribute. Verwendet die Element-ID, falls leer.
Minimale Stichlänge  | |Überschreibt die [globale Einstellung für die minimale Stichlänge](/de/docs/preferences/#minimale-stichlänge-mm). Stiche, die kleiner sind als dieser Wert werden entfernt.
Minimale Sprungstichlänge | |Überschreibt die [globale Einstellung für die minimale Sprungstichlänge](/de/docs/preferences/#minimale-länge-für-sprungstiche-mm). Kleinere Entfernungen zum nächsten Objekt haben keine Vernähstiche.
Wiederholungen       ||◦ Definiert wie oft der Pfad hoch und runter gestickt wird.<br />Standart: 1 stickt einmal von Anfang bis Ende<br />◦ Ungerade Anzahl: der Stickpfad endet am Ende des Pfades<br />◦ Gerade Anzahl: der Stickpfad endet dort, wo er gestartet ist
Mehrfachgeradstich Anzahl der Wiederholungen ||◦ Aktiviert den [Mehrfachgeradstich](/de/docs/stitches/bean-stitch/)<br/>◦ Ein Wert von 1 verdreifacht jeden Stich (vorwärts, rückwärts, vorwärts).<br/>◦ Ein Wert von 2 verfünffacht jeden Stich, usw.<br/>◦ Durch die Eingabe mehrerer durch ein Leerzeichen getrennter Werte, kann ein Wiederholungsmuster erstellt werden.
Vernähen erlauben    || Vernäht bei Bedarf an den ausgewählten Positionen
Vernähen erzwingen   || Vernäht den Faden nach diesem Element, auch dann, wenn der Abstand zum Folgeobjekt geringer ist als in den [Ink/Stitch Einstellungen](/de/docs/preferences/) definiert.
Anstecher            ||Wähle die [Anstecher](/docs/stitches/lock-stitches) Variante (Anfang).
Verstecher           ||Wähle die [Verstecher](/docs/stitches/lock-stitches) Variante (Ende).
Fadenschnitt         || Schneidet den Faden nachdem dieses Objekt genäht wurde
Stopp                || Stoppt die Maschine nachdem dieses Objekt genäht wurde und springt zur Stopp-Position (sofern vorhanden)

## Unterlage

Die Unterlage der Spiralfüllung ist keine Spirale, sondern nutzt den Stichwinkel der [Parametereinstellungen](/de/docs/fill-stitch/#unterlage)

## Beispieldateien mit Spiralfüllung

{% include tutorials/tutorial_list key="stichart" value="Spiralfüllung" %}

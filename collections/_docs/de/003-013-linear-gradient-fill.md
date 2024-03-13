---
title: "Lineare Farbverlaufsfüllung"
permalink: /de/docs/stitches/linear-gradient-fill/
last_modified_at: 2024-03-13
toc: true
---
 {% include upcoming_release.html %}

## Beschreibung

[![Linear Gradient Fill Sample](/assets/images/docs/linear-gradient.jpg){: width="200x"}](/assets/images/docs/linear-gradient.svg){: title="SVG Datei herunterladen" .align-left download="linear-gradient.svg" }
Die lineare Verlaufsfüllung nutzt die in Inkscape gesetzte Farbe "linearer Verlauf" um einen nahtlosen Verlauf mit guter Stichpositionierung zu schaffen.

## Funktionsweise

* Erstelle einen geschlossenen Pfad. Der Pfad darf Löcher enthalten.
* Im Dialog `Füllung und Kontur` wähle als Füllfarbe einen linearen Farbverlauf und passe die Farben deinen Wünschen entsprechend an.
  Auf der Arbeitsfläche wird der Farbverlauf durch eine Linie dargestellt mit der die Farbpositionen und die Verlaufsrichtung direkt bearbeitet werden könne.
  Die Verlaufsrichtung bestimmt auch den Stichwinkel der Füllung (90° entgegengesetzt der Verlaufslinie).
  ![linear gradient](/assets/images/docs/en/linear-gradient.png)
* Öffne den Parameterdialog (`Erweiterungen > Ink/Stitch > Parameter`) und wähle als Füllmethode `Lineare Farbverlaufsfüllung`.
  Setze die anderen Parameter deinen Wünschen entsprechend.

### Anfangs- und Endpunkt festlegen

Ink/Stitch erlaubt es über visuelle Befehle den [Anfangs- und Endpunkt eines Füllobjekts](/de/docs/commands) zu kennzeichnen.

### Parameter

Öffne das Parameter-Dialogfenster (`Erweiterungen > Ink/Stitch  > Parameter`, um die Einstellungen zu verfeinern.

Einstellung                     ||Beschreibung
---|---|---
Automatisch geführte Füllstiche | ☑ |Muss aktiviert sein, damit diese Einstellungen wirksam werden.
Füllmethode                     | Lineare Verlaufsfüllung | Hier bitte `Lineare Verlaufsfüllung` auswählen
Erweitern                       |![Expand example](/assets/images/docs/params-fill-expand.png) | Erweitern der Form vor dem Füllstich, um Lücken zwischen den Formen auszugleichen.
Maximale Füll-Stichlänge        |![Stitch length example](/assets/images/docs/params-fill-stitch_length.png) | Die Stichlänge in einer Reihe. Ein kürzerer Stich kann am Anfang oder am Ende einer Reihe verwendet werden.
Reihenabstand                   |![Spacing example](/assets/images/docs/params-fill-spacing_between_rows.png) | Abstand zwischen den Stichreihen.
Reihenanzahl bis sich das Muster wiederholt |![Stagger example](/assets/images/docs/params-fill-stagger.png) | Die Einstellung bestimmt, wie viele Reihen die Stiche voneinander entfernt sind, bevor sie in die gleiche Position münden.  Fractional values are allowed and can have less visible diagonals than integer values.
Verbindungsstiche innerhalb des Objektes|![Skip example](/assets/images/docs/params-fill-underpathing.png)| Muss aktiviert sein, um Geradstiche zum Verbinden der Abschnitte innerhalb des Objekts verlaufen zu lassen, anstatt sie am Rand entlang zu führen.
Letzten Stich in jeder Reihe überspringen | Der letzte Stich in jeder Reihe ist dem darauffolgenden Stich sehr nah. Ihn zu überspringen verringert die Stichanzahl und Dichte.
Am Endpunkt enden               | ☑ |Ist diese Option deaktivert, gibt der Endpunkt nur eine generelle Stickrichtung an. Bei aktivierter Option endet der letzte Farbabschnitt genau an diesem Punnkt.
Geradstichlänge                 |![Running stitch length example](/assets/images/docs/params-fill-running_stitch_length.png) | Stichlänge für Geradstiche beim Übergang von Abschnitt zu Abschnitt.
Geradstich-Toleranz             ||Alle Stiche müssen innerhalb dieses Abstandes zum Pfad befinden. Ein niedrigerer Toleranzwert führt zu kürzeren Stichen. Ein höherer Wert könnte Ecken abrunden. Dezimalzahlen führen ggf. zu weniger deutlichen Diagonalen als Ganzzahlen.
Vernähen erlauben               || Vernäht bei Bedarf an den ausgewählten Positionen
Vernähen erzwingen              || Vernäht den Faden nach diesem Element, auch dann, wenn der Abstand zum Folgeobjekt geringer ist als in den [Ink/Stitch Einstellungen](/de/docs/preferences/) definiert.
Anstecher                       || Wähle die [Anstecher](/de/docs/stitches/lock-stitches) Variante (Anfang).
Verstecher                      || Wähle die [Verstecher](/de/docs/stitches/lock-stitches) Variante (Ende).
Stopp                           || Stoppt die Maschine nachdem dieses Objekt genäht wurde und springt zur Stopp-Position (sofern vorhanden)
Fadenschnitt                    || Schneidet den Faden nachdem dieses Objekt genäht wurde
{: .params-table }

## Unterlage

Die Unterlage nutzt den Stickwinkel der in den [Parametern der Unterlage](/de/docs/params/#füllung-unterlage) eingestellt werden kann.

## Beispieldateien mit linearer Farbverlaufsfüllung

{% include tutorials/tutorial_list key="stitch-type" value="Linear Gradient Fill" %}

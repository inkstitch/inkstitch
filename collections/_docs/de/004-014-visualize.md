---
title: "Visualisierung"
permalink: /de/docs/visualize/
last_modified_at: 2026-04-06
toc: true
---
## Simulator

Wähle die Objekte aus, die in der simulierten Vorschau angezeigt werden sollen. Wenn das gesamtes Design simuliert werden soll, wähle alles (`Strg + A`) oder nichts aus.

Dann starte `Erweiterungen -> Ink/Stitch -> Simulation -> Visualisieren und Exportieren` und lehne dich zurück.

![Simulator](/assets/images/docs/de/simulator_de.jpg)
{: style="border: 2px solid gray; padding: 5px;"}

### Schaltflächen und Tastenkombinationen

Schaltfläche  | Wirkung | Tastenkombinationen
-------- | -------- | --------
**Steuerung**||
|<img src="/assets/images/docs/icons/backward_command.png" >|Gehe einen Befehl zurück| <key>Bild ↓</key>
|<img src="/assets/images/docs/icons/backward_stitch.png" >|Gehe einen Stich zurück| <key>←</key>
|<img src="/assets/images/docs/icons/forward_stitch.png" >|Gehe einen Stich vor| <key>→</key>
|<img src="/assets/images/docs/icons/forward_command.png" >|Gehe einen Befehl vor| <key>Bild ↑</key>
|<img src="/assets/images/docs/icons/direction.png" >|Richtung wechseln| 
|<img src="/assets/images/docs/icons/play.png"> | Abspielen/Pausieren |<key>space</key> / <key>p</key>
|<img src="/assets/images/docs/icons/restart.png" >|Neustart| <key>r</key>
**Geschwindigkeit**||
|<img src="/assets/images/docs/icons/slower.png" >|langsamer| <key>↓</key>
|<img src="/assets/images/docs/icons/faster.png" >|schneller| <key>↑</key>
**Zeige**||
|<img src="/assets/images/docs/icons/npp.png" >|Nadeleinstichposition| <key>o</key>
|<img src="/assets/images/docs/icons/jump.png" >|Sprungstiche|
|<img src="/assets/images/docs/icons/trim.png" >|Fadenschnittbefehle|
|<img src="/assets/images/docs/icons/stop.png" >|Stoppbefehle|
|<img src="/assets/images/docs/icons/color_change.png" >|Farbwechsel|
**Info**||
|<img src="/assets/images/docs/icons/info.png" >|Infobox öffnen|
**Einstellungen**||
|<img src="/assets/images/docs/icons/change_background.png" >|Hintergrundfarbe wechseln|
|<img src="/assets/images/docs/icons/cursor.png" >|Fadenkreuz aneigen|
|<img src="/assets/images/docs/icons/page.png" >|Seite anzeigen|
|<img src="/assets/images/docs/icons/settings.png" >|Einstellungen öffnen|

Es ist auch möglich die Simulation mit der Maus zu **zoomen** und zu **verschieben**.

## Stichplan Vorschau

Die Stichplan-Vorschau zeigt den Stichplan direkt auf der Arbeitsfläche an. Abhängig von den Einstellungen wird der Stichplan direkt über dem Design oder am
rechten Rand der Arbeitsfläche dargestellt (Option: Stickplan an der Seite platzieren).

Die Stichplan-Vorschau befindet sich unter dem Menüpunkt `Erweiterungen > Ink/Stitch > Visualisierung und Export > Stichplan Vorschau ...`.

### Optionen

![simple and realistic render modes](/assets/images/docs/stitch-plan-preview-modes.jpg)

<i>V.l.n.r.: 1. Render-Modus einfach 2. Render-Modus einfach mit Nadeleinstichstellen 3. Render-Modus realistisch<br>
Bildquelle: [Pixabay](https://pixabay.com/vectors/fox-red-fox-creature-mammal-svg-2530031/)</i>

- **Design-Layer Sichtbarkeit** definiert die Sichtbarkeit, bzw. Transparenz der Design-Layer
  - **unverändert** die Design-Layer bleiben unverändert
  - **versteckt** das Original-Design wird versteckt
  - **Verrinerte Deckkraft** das Original wird mit 40%-Transparenz dargestellt
- **Render Modus**
  ![simple and realistic render modes](/assets/images/docs/stitch-plan-preview-modes.jpg)

  <i>Original image from [Pixabay](https://pixabay.com/vectors/fox-red-fox-creature-mammal-svg-2530031/)</i>
  - **Einfach**: einfache Liniendarstellung
  - **Realistisch**: Realistische Vorschau als in Inkscape eingebundene PNG-Bilddatei (8-bit)
  - **Realistisch (hohe Qualität)** Realistische Vorschau als in Inkscape eingebundene PNG-Bilddatei (16-bit)
  - **Realistisch Vektor (langsam)** Vektor-Ausgabe mit realistischen Filtern

- **Stickplan an der Seite platzieren** Der Stichplan wird rechts neben dem Canvas abgebildet.
  Ist diese Option nicht aktiviert, wird der Stichplan direkt über das Design gelegt.
  In diesem Fall ist es nützlich die Sichtbarkeit des Designs anzupassen.
- **Nadeleinstichstellen** zeigt Punkte an den Einstichstellen
- **Stichplan-Ebene sperren** Stichplan reagiert nicht auf Mausinteraktionen. Das ist praktisch, wenn mit aktiviertem Stichplan das Original-Design bearbeitet werden soll
- **Zeige visuelle Befehle**
- **Sprungstitche anzeigen**

- **Ebene ignorieren Befehl einfügen**
- **Letzten Stichplan überschreiben**
  Überschreibt den letzten Stichplan wenn aktiviert. Soll der alte Stichplan erhalten bleiben, deaktiviere diese Option.

### Verbesserter Worfklow mit Tastenkürzeln

Nutze [Tastenkürzel](/docs/customize/#shortcuts) für beides, `Stichplan-Vorschau` und `Stichplanvorschau aufheben` (s.u.) um deinen Workflow zu verbessern.

* Wir empfehlen die Tatenkürzel auf die Methoden mit dem Zusatz `Keine Einstellungen` zu legen.
  So wird die Funktion direkt ausgeführt (ohne das Einstellungsfenster). Dabei werden die zuletzt genutzen Einstellungen verwendet.
* Aktiviere die Option `Stichplan-Ebene sperren` um alle Pfade ohne Interferenzen mit dem aktivierten Stichplan verändern zu können.
* Achte darauf, dass die Option `Letzten Stichplan überschreiben` aktiviert ist. Andernfalls werden sich die Stichpläne auf der Arbeitsfläche häufen.

{% include video id="vyTMwLvkkiw4vgwDcTJS6e" provider="diode" %}

## Stichplan Vorschau aufheben

Wird der Stichplan über dem Design mit verringerter Deckkraft angezeigt, hilft es eine visuelle Idee zu bekommen, wie das Design am Ende aussehen wird. Manchmal ist es hilfreich, in einen angezeigten Stichplan hineinzuarbeiten. Dies jedoch, kann es schwieriger machen, den Stichplan wieder zu entfernen und da auch die Deckkraft wieder zurückgesetzt werden muss. Mit dieser Erweiterung kann auch der Stichplan nach erfolgten Änderungen am Dokument einfach wieder entfernt werden.

`Erweiterungen > Ink/Stitch > Visualisieren und Exportieren > Stich-Plan Vorschau aufheben`

## Dichte Indikator

Zeigt Punkte in frei wählbaren Farben (Standart: rot, gelb, grün) über dem Design. Sie helfen Stellen mit hoher Dichte ausfindig zu machen.

* Wähle die Objekte aus, bei denen die Dichte angezeigt werden soll. Wird keine Auswahl getroffen, analysiert diese Erweiterung das gesamte Dokument
* Öffne `Erweiterungen > Ink/Stitch > Visualisieren und Exportieren > Dichte Indikator`
* Setze die Farben wie gewünscht und klicke auf `Anwenden`
* Untersuche das Design (evtl. ist es nötig stärker in das Design hineinzuzoomen)
* Entferne die Dichte-Punkte mit `Ctrl + Z` (rückgängig machen)

### Optionen

* Rot / gelbe Markierungen

  Definiere ab vielen Stichen in welchem Radius die Markerungen rot / gelb gefärbt werden sollen
* Design-Layer Sichtbarkeit

  Definiere ob Ink/Stitch die Design-Ebene unverändert belassen soll, sie verstecken oder die Deckkraft verringern soll
* Indikator-Größe

  Lege die Größe der eingefügten Markierungen in Dokumenteinheit fest

## Stickreihenfolge anzeigen

Diese Erweiterung fügt nummerierte Beschriftungen für ausgewählte Elemente in das Dokument ein, um die Stichreihenfolge zu visualisieren.

* Öffne `Erweiterungen > Ink/Stitch > Visualisieren und Exportieren > Stickreihenfolge anzeigen...`
* Wähle die Schriftgröße
* Klicke auf "Anwenden".

![Display stacking order](/assets/images/docs/stacking_order.png)

## PDF-Export

Die Informationen zum PDF-Export sind auf einer gesonderten Seite zusammengefasst: [mehr Informationen zum PDF-Export](/de/docs/print-pdf)

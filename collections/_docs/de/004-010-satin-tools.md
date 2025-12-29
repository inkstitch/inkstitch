---
title: "Satin Werkzeuge"
permalink: /de/docs/satin-tools/
last_modified_at: 2025-04-15
toc: true
---
Unter `Erweiterungen > Ink/Stitch  > Satin Tools` befindet sich eine kleine Anzahl nützlicher Helfer, die das Arbeiten mit [Satinsäulen](/docs/stitches/satin-column/) erleichtern sollen.

**Beispiel:**
* Erzeuge einen Pfad mit dem Beziér-Kurven Werkzeug (`B`)
* Benutze "[Linie zu Satin](/de/docs/satin-tools/#linie-zu-satin)"
* Aktiviere im [Parameter Dialogfenster](/de/docs/params/#satinsäule) eine oder mehrere Unterlagen
* Führe "[Automatische Satinsäulenführung](/docs/satin-tools/#automatische-satinsäulenführung)" aus, um optimal geführte Satinsäulen zu erhalten

[![Stroke to Satin](/assets/images/docs/en/satin-tools.svg)](/assets/images/docs/en/satin-tools.svg){: title="Download SVG File" download="satin-tools.svg" }

**Tip:** Setze [Tastenkürzel](/docs/customize/) um die einzelnen Satin-Werkzeuge schneller ausführen zu können.
{: .notice--info}

## Automatisch geführte Satinsäulen...

Dieses Werkzeug ersetzt deine Satinsäulen mit einem Set von neuen Satinsäulen in logischer Reihenfolge. Sprungstiche werden hinzugefügt, falls nötig, optional werden stattdessen Fadenschneide-Befehle eingesetzt. Um Sprungstiche zu vermeiden werden Satinsäulen getrennt und versteckte Geradstiche hinzugefügt. Die neuen Satinsäulen behalten alle Einstellungen bei, die zuvor über den Paramter-Dialog gesetzt wurden, einschließlich Unterlage, Zick-Zack-Abstand, etc.

### Funktionsweise

1. Wähle eine Satinsäule an (fertig vorbereitet mit Unterlage, etc.)
2. Führe `Erweiterungen > Ink/Stitch  > Satin Tools > Auto-Route Satin Columns...` aus
3. Aktiviere die gewünschten Optionen und klicke auf "Anwenden"

**Tip:** Standardmäßig beginnen automatisch geführte Satinsäulen links und enden rechts. Du kannst dieses Verhalten mit den Befehlen "[Start- und Enpunkt für automatisch geführte Satinsäulen](/de/docs/visual-commands/#--start--und-endposition-für-automatisch-geführte-satinsäulen)" überschreiben.
{: .notice--info }

### Optionen

* Aktiviere **Schneide Faden bei Sprungstichen** um anstelle von Sprungstichen den Faden zu trennen. Jeder Sprungstich über einem Milimeter wird getrennt. Fadenschneide-Befehle werden der SVG-Datei hinzugefügt, somit ist es auch nachträglich noch möglich sie zu modifizieren.

* Solltest du es bevorzugen die vorher gesetzte Objekt-Reihenfolge beizubehalten (das könnte der Fall sein, wenn sich die Satinsäulen überschneiden), benutze die Option **Behalte Reihenfolge der Satinsäulen bei**.

* **Satinsäulen behalten** definiert, ob die ausgewählten Elemente nach der Umwandlnug gelöscht werden oder für spätere Korrekturen erhalten bleiben.

## Linie zu Satin

Diese Erweiterung konvertiert einen einfachen Pfad in eine Satinsäulen. Dabei wird die Linienbreite übernommen. Nach der Konvertierung wirst du zwei "Holme" und (möglicherweise) viele Sprossen (wie bei einer Leiter). Wieviele Sprossen es gibt hängt ganz von der Form der Linie ab.

### Funktionsweise

1. Zeichne eine Beziér-Kurve (`B`)
2. Stelle die Linienbreite ein (`Ctrl+Shift+F)
2. Führe `Erweiterungen > Ink/Stitch  > Satin Tools > Linie zu Satin` aus


## Satinsäule schneiden

Diese Option schneidet eine Satinsäule an einem vordefiniertem Punkt. Alle Parameter die der Säule zuvor zugewiesen wurden werden auf beide Teile übertragen. Auch alle Sprossen bleiben erhalten. Sollte eine der beiden Säulen keine Sprossen beinhalten, wird eine Neue hinzugefügt.

### Funktionsweise

1. Wähle eine Satinsäule an (eine Zick-Zack-Linie funktioniert hier nicht)
2. Füge über `Erweiterungen > Ink/Stitch  > Befehle > Befehle mit gewählten Objekten verknüpfen > Satin cut point` einen "Satin-Schnittstelle"-Befehl ein
3. Bewege das Symbol zur gewünschten Stelle. Der Zeiger muss genau auf die Stelle treffen, wo die Satinsäule geschnitten werden soll
4. Wähle die Satinsäule erneut an
5. Führe `Erweiterungen > Ink/Stitch  > Satin Tools > Satinsäule schneiden` aus
6. Der Satin-Schnittstelle-Befehl und sein Zeiger sind verschwunden. Wähle die Satinsäule aus: es sind jetzt zwei.

You can use multiple commands on the same satin column to split it into multiple pieces in a single action.
## Füllung zu Satin

Füllung zu Satin hilft bei der Umwandlung von Füllflächen zu Satinsäulen. Es ist eine halbautomatische Funktion und benötigt ein wenig Handarbeit.

### Funktionsweise

* Bereite die Füllobjekte vor. Es kann nötig sein, die Füllflächen mit dem Shape-Builder
  Werkzeug oder anderen Pfadbearbeitungswerkzeugen in Inkscape in einfachere Formen aufzuteilen.
* Überprüfe, ob die Füllfläche nur eine Füllfarbe hat (keine Konturfarbe)
* Erstelle die Richtungsvektoren. Die Richtungsvektoren haben keine Füllfarbe und nur eine Konturfarbe.
  Sie zerteilen die Füllfläche in Teilbereiche und legen außerdem später den Stichwinkel fest.

  Es ist wichtig, dass eine ausreichende Anzahl an Richtnugsvektoren gesetzt ist.
  Besonders dann, wenn die Funktion `Beginne / Ende an Richtungsvektor` aktiviert ist, da diese Option die Enden der Satinsäule auslässt.
  {: .notice--warning }
* Wähle sowohl die Füllung als auch die Richtungsvektoren aus
* Öffne den Dialog `Erweiterungen > Ink/Stitch > Werkzeuge: Satin > Füllung zu Satin...`
* Aktiviere die gewünschten Optionen
* Klicke auf `Anwenden`

### Optionen

Option                             | Beschreibung
-----------------------------------|-------------
Beginne / Ende an Richtungsvektor  | Ist diese Funktion aktiviert, werden offene Enden von der Satinsäule entfernt. Hierfür ist es wichtig, dass ausreichend Richtungsvektoren für jeden Teilabschnitt gesetzt wurden. Ansonsten kann es zu fehlenden Bereichen führen. Diese Option ist ein gutes Mittel, die Satinsäulen zu verkürzen, da sie sich beim Aussticken wieder verlängern.
Mittellinien Unterlage             | Fügt eine Mittellinien-Unterlage hinzu
Konturunterlage                    | Fügt eine Konturunterlage hinzu
Zick-Zack Unterlage                | Fügt eine Zick-Zack-Unterlage hizu
Original behalten                  | Behalte oder verwerfe die ausgewählten Original-Pfade

### Brücken

Definiere die Verbindungen zwischen den Satinsäulen mit Hilfe von Brücken.
Ist eine Kreuzung nicht überbrückt, entsteht hier einfach eine Lücke.

Brücken müssen innerhalb des Füllelements verlaufen und dürfen die Außenlinie nicht überkreuzen.
{: .notice--info}

![Convert to satin with and without bridge](/assets/images/docs/fill_to_satin_bridge.png)

### Beispieldatei

[Füllung zu Satin Playground herunterladen](/assets/images/docs/fill_to_satin_playground.svg){: title="Download SVG File" download="fill_to_satin_playground.svg" }

## Satinsäule umkehren

Dies ist ein kleines Werkzeug, mit dem der Stichpfad genau geplant werden kann. Bei Anwendung kehrt es eine Satinsäule, die auf der linken Seite beginnt und auf der rechten Seite endet, um. Diese wird nun auf der rechten Seite beginnen und auf der linken Seite enden.
Sonst wird nichts an der Satinsäule verändert.

![Flip Satin Columns](/assets/images/docs/en/flip-satin-column.jpg)

### Funktionsweise

* Wähle eine oder mehrere Satinsäule(n) aus
* Starte `Erweiterungen -> Ink/Stitch -> Satinsäule umkehren`

## Mehrfarbige Satinsäule

Diese Erweiterung generiert Kopien der ausgewählten Satinsäule um einen mehrfarbigen Effekt zu erzeugen

![Multicolor Satin](/assets/images/tutorials/multicolor_satin/solution.png)

Für nähere Infos über die Funktionsweise dieser Erweiterung gibt es im [Tutorial für mehrfarbige Satinsäulen](/de/tutorials/multicolor_satin).

### Funktionsweise

* Wähle eine oder mehrere Satinsäulen
* Öffne `Erweiterungen > Ink/Stitch > Werkzeuge: Satin > Mehrfarbige Satinsäule`
* Setze alle bevorzugten Präferenzen in `Farben`
* Klicke auf `Anwenden`

### Optionen

#### Allgemeine Einstellungen

* Gleichmäßige Abstände: Wähle ob die Farben gleiche Breiten und Abstände haben sollen oder nicht.
  * Ist die Option aktiviert, kann die Breite aller Farben über die Option `Monochrome Farbbreite` eingestellt werden.
  * Ist die Option deaktiviert, kann für jede Farbe sowohl die Breite der reinen Farbe als auch die Breite des darauf folgenden zweifarbigen Bereichs über die einzelnen Farben definiert werden.
* Überlauf links (%): Fügt einen gezackten Rand links der Satinsäule hinzu
* Überlauf rechts (%): Fügt einen gezackten Rand rechts der Satinsäule hinzu
* Zugausgleich (mm): Verbreitert die Satinsäulen und überlappt sie. So können Lücken zwischen den Farben vermieden werden.
* Zufallswert: Passe den Wert an, um das Erscheinungsbild der Zufallsparameter zu ändern

* Satinsäulen behalten: legt fest, ob die ursprüngliche Satinsäule gelöscht werden soll oder nicht
* Unterlage pro Farbe anpassen: findet nur Anwendung, wenn die ursprüngliche Satinsäule Unterlagen enthält
  * Ist die Option aktiviert, wird die Unterlagen auf die verschiedenen Farben aufgeteilt. Mehrfarbige Bereiche bleiben ohne Unterlage
  * Ist die Option deaktiviert, erhält nur die erste Farbe eine Unterlage die den gesamten Bereich abdeckt

#### Farben

Width values are given in percentages. Make sure all numbers for all colors add up to 100%.

Bitte beachte, dass das erste Eingabefeld die Breite für die einfarbigen Bereiche definiert. Das zweite Eingabefeld definiert die Breite des zweifarbigen Abschnitts bis zur nächsten Farben.
Ist die Option `Gleichmäßige Abstände` aktiviert, reduziere den Wert für `Monochrome Farbbreite` um ein breiteres zweifarbiges Feld zu erhalten.
{: .notice--info}

![Multicolor satin ui](/assets/images/docs/en/multicolor_satin_ui_01.png)

![Multicolor satin ui](/assets/images/docs/en/multicolor_satin_ui_02.png)

## Linie zu Pfadeffekt-Satin

Konvertiert eine Linie in eine Satinsäule mit Hilfe von Pfadeffekten. Dies macht es einfacher Form und Breite auch im Nachhinein noch anzupassen.

**Verwende keine spitzen Ecken.** Genauso wie bei normalen Satinsäulen, sollten spitze Ecken in verschiedene Pfade aufgespalten werden. Um eine konstante Breite zu erzielene, kann es nötig sein, die Anfasser der Knoten zu ziehen oder mehr Knoten hinzuzufügen.
{: .notice--warning }

### Funktionsweise

1. Wähle eine Linie oder einen Pfadeffekt-Satin
2. Öffne `Erweiterungen > Ink/Stitch > Werkzeuge: Satin > Linie zu Pfadeffekt-Satin...`
3. Setze die ungefähren Maße für die Satinsäule
4. Klicke auf `Anwenden`

## Options

--|--
Pattern             | ![LPE-Patterns](/assets/images/docs/lpe_patterns.png) | Musters, das wiederholt auf die Satinsäule aufgetragen werden soll
Min Width (mm)      | ![Min width](/assets/images/docs/lpe_min_width.png)   | Musterbreite an der schmalsten Stelle
Max Width (mm)      | ![Max width](/assets/images/docs/lpe_max_width.png)   | Musterbreite an der breitesten Stelle
Pattern Length (mm) | ![Length](/assets/images/docs/lpe_length.png)         | Länge des Musters
Stretched           | ![Stretched](/assets/images/docs/lpe_stretched.png)   | Wenn diese Option aktiviert ist, wird das Muster so gestreckt, dass seine Musterwiederholungen genau die Länge der Linie einnehmen, andernfalls kann am Ende der Linie eine Lücke entstehen
Add rungs           | ![Rungs](/assets/images/docs/lpe_rungs.png)           | Da die Muster (i.d.R.) alle die gleiche Knotenanzahl auf beiden Seiten der Außenkontur haben, sind die Richtungslinien optional.
Path specific       |                                                       | ● Wenn diese Option aktiviert ist, hat die Satinsäule ein eigenes Muster. Eine Modifikation der Optionen beeinflusst nur diese Satinsäule. Element-Transformationen können berücksichtigt werden.<br> ● Ist die Option deaktiviert, wird das gleiche Muster auf alle ausgewählten Pfade angewendet. Wenn das Muster für eine Satinsäule geändert wird, wird es für alle geändert. Element-Transformationen können zu unerwarteten Breiten führen.

### Muster anpassen

Es ist möglich auch im Nachhinein das Muster zu personalisieren, bzw. ein andere Muster anzuwenden.

* Mit dem Knotenwerkzeug kann der Ursprungspfad auch weiterhin geändert und angepasst werden
* Das Muster kann manuell über die Pfadeffekt-Einstellungen geändert werden (`Pfad > Padeffekte...`)
  * Mit der Einstellung `Breite` kann das Muster schmaler oder breiter gemacht werden
  * Das Muster selbst kann über `Auf der Arbeitsfläche bearbeiten` unter `Quelle des Musters` nach Belieben geändert werden.
    
    ![edit on canvas](/assets/images/tutorials/pattern-along-path/edit.png)
* Um eine andere vordefinierte Form zu verwenden, kann dieses Werkzeug einfach erneut auf den Pfad angewendet werden
* Um weitere Bearbeitungsmöglichkeiten wie z.B. eine Anpassung der Richtungslinien zu erreichen, kann der Pfad mit `Strg + Umstelltaste + C` auch in einen herkömmlichen Pfad umgewandelt werden (er verliert dabei aber die Funktionalität des Pfadeffekts)

### Pfadeffekt anwenden

Nutze die Funktion `Pfad > Objekt in Pfad umwandeln` um eine "normale" Satinsäule zu erhalten.


## Zickzack-Linie zu Satin

Wenn du manuell eine Form für einen Satinstich nachzeichnen willst, kann dieses Tool hilfreich sein.
Anstatt zunächst beide Außenlinien und dann die Richtungsvektoren zu erstellen, kann die Form mit einer einzigen Linie generiert werden.

### Funktionsweise

* Zeichne die Form mit Hilfe des bevorzugten Pfadstils (Muster) s.u.
* Wähle diese Form an und öffne `Erweiterungen > Ink/Stitch > Werkzeuge: Satin > Zickzack-Linie zu Satin...`
  * Wähle den benutzen Pfadstil (Muster). Ist nicht das richtige Muster ausgewählt, kann es zu komischen Effekten führen.
  * Wähle ob der resultierende Pfad geglättet werden soll oder nicht
  * Wähle ob der Pfad Richtungslinien enthalten soll oder nicht. Der so erstellte Pfad hat immer die gleiche Anzahl an Knoten auf beiden Außenlinien.

### Muster

* Alle Muster müssen mit einer Richtungslinie beginnen und enden.
* Für die Muster **Rechteck (1)** und **Sägezahn (2)** werden der Reihe nach die Richtungslinien gezeichnet.
* Bei dem Muster **Zickzack (3)** werden Richtungslinien von der jeder Spitze auf jeder Seite auf die Mittelpunkte zwischen den Spitzen der anderen Seite projiziert.

![Zigzag Line to Satin Patterns](/assets/images/docs/zigzag-line-to-satin.png)

Wenn dein Ergebnis in etwa so aussieht wie auf dem Bild unten, hast du wahrscheinlich das falsche Muster für deine Linie gewählt.

![Zigzag Line wrong pattern](/assets/images/docs/zigzag-line-to-satin-wrong-pattern.png)


## Tutorials zu Satinwerkzeugen

{% include tutorials/tutorial_list key="Werkzeug" value="Satin" %}

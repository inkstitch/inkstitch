---
title: "Satin Werkzeuge"
permalink: /de/docs/satin-tools/
excerpt: ""
last_modified_at: 2023-03-12
toc: true
---
Unter `Erweiterungen > Ink/Stitch  > Satin Tools` befindet sich eine kleine Anzahl nützlicher Helfer, die das Arbeiten mit [Satinsäulen](/docs/stitches/satin-column/) erleichtern sollen.

**Beispiel:**
* Erzeuge einen Pfad mit dem Beziér-Kurven Werkzeug (`B`)
* Benutze "[Linie zu Satin](/de/docs/satin-tools/#linie-zu-satin)"
* Aktiviere im [Parameter Dialogfenster](/de/docs/params/#satinsäule) eine oder mehrere Unterlagen
* Führe "[Automatische Satinsäulenführung](/docs/satin-tools/#automatische-satinsäulenführung)" aus, um optimal geführte Satinsäulen zu erhalten

[![Convert Line to Satin](/assets/images/docs/en/satin-tools.svg)](/assets/images/docs/en/satin-tools.svg){: title="Download SVG File" download="satin-tools.svg" }

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

* Aktiviere **Trim jump stitches** um anstelle von Sprungstichen den Faden zu trennen. Jeder Sprungstich über einem Milimeter wird getrennt. Fadenschneide-Befehle werden der SVG-Datei hinzugefügt, somit ist es auch nachträglich noch möglich sie zu modifizieren.

* Solltest du es bevorzugen die vorher gesetzte Objekt-Reihenfolge beizubehalten (das könnte der Fall sein, wenn sich die Satinsäulen überschneiden), benutze die Option **Preserve order of Satin Columns**.

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

## Satinsäule umkehren

Dies ist ein kleines Werkzeug, mit dem der Stichpfad genau geplant werden kann. Bei Anwendung kehrt es eine Satinsäule, die auf der linken Seite beginnt und auf der rechten Seite endet, um. Diese wird nun auf der rechten Seite beginnen und auf der linken Seite enden.
Sonst wird nichts an der Satinsäule verändert.

![Flip Satin Columns](/assets/images/docs/en/flip-satin-column.jpg)

### Funktionsweise

* Wähle eine oder mehrere Satinsäule(n) aus
* Starte `Erweiterungen -> Ink/Stitch -> Satinsäule umkehren`

## Linie zu Pfadeffekt-Satin

{% include upcoming_release.html %}

Konvertiert eine Linie in eine Satinsäule mit Hilfe von Pfadeffekten. Dies macht es einfacher Form und Breite auch im Nachhinein noch anzupassen.

### Funktionsweise

1. Wähle eine Linie
2. Öffne `Erweiterungen > Ink/Stitch > Werkzeuge: Satin > Linie zu Pfadeffekt-Satin...`
3. Setze die ungefähren Maße für die Satinsäule
4. Klicke auf `Anwenden`

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

{% include upcoming_release.html %}

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
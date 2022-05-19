---
title: "Satin Werkzeuge"
permalink: /de/docs/satin-tools/
excerpt: ""
last_modified_at: 2021-10-30
toc: true
---
Unter `Erweiterungen > Ink/Stitch  > Satin Tools` befindet sich eine kleine Anzahl nützlicher Helfer, die das Arbeiten mit [Satinkolumnen](/docs/stitches/satin-column/) erleichtern sollen.

**Beispiel:**
* Erzeuge einen Pfad mit dem Beziér-Kurven Werkzeug (`B`)
* Benutze "[Linie zu Satin](/de/docs/satin-tools/#linie-zu-satin)"
* Aktiviere im [Parameter Dialogfenster](/de/docs/params/#satinkolumne) eine oder mehrere Unterlagen
* Führe "[Automatische Satinkolumnenführung](/docs/satin-tools/#automatische-satinkolumnenführung)" aus, um optimal geführte Satinkolumnen zu erhalten

[![Convert Line to Satin](/assets/images/docs/en/satin-tools.svg)](/assets/images/docs/en/satin-tools.svg){: title="Download SVG File" download="satin-tools.svg" }

**Tip:** Setze [Tastenkürzel](/docs/customize/) um die einzelnen Satin-Werkzeuge schneller ausführen zu können.
{: .notice--info}

## Automatische Satinkolumnenführung...

Dieses Werkzeug ersetzt deine Satinkolumnen mit einem Set von neuen Satinkolumnen in logischer Reihenfolge. Sprungstiche werden hinzugefügt, falls nötig, optional werden stattdessen Fadenschneide-Befehle eingesetzt. Um Sprungstiche zu vermeiden werden Satinkolumnen getrennt und versteckte Laufstiche hinzugefügt. Die neuen Satinkolumnen behalten alle Einstellungen bei, die zuvor über den Paramter-Dialog gesetzt wurden, einschließlich Unterlage, Zick-Zack-Abstand, etc.

### Funktionsweise

1. Wähle eine Satinkolumne an (fertig vorbereitet mit Unterlage, etc.)
2. Führe `Erweiterungen > Ink/Stitch  > Satin Tools > Auto-Route Satin Columns...` aus
3. Aktiviere die gewünschten Optionen und klicke auf "Anwenden"

**Tip:** Standardmäßig beginnen automatisch geführte Satinkolumnen links und enden rechts. Du kannst dieses Verhalten mit den Befehlen "[Start- und Enpunkt für automatische Satinkolumnenführung](/de/docs/visual-commands/#--start--und-endposition-für-automatische-satinkolumnenführung)" überschreiben.
{: .notice--info }

### Optionen

* Aktiviere **Trim jump stitches** um anstelle von Sprungstichen den Faden zu trennen. Jeder Sprungstich über einem Milimeter wird getrennt. Fadenschneide-Befehle werden der SVG-Datei hinzugefügt, somit ist es auch nachträglich noch möglich sie zu modifizieren.

* Solltest du es bevorzugen die vorher gesetzte Objekt-Reihenfolge beizubehalten (das könnte der Fall sein, wenn sich die Satinkolumnen überschneiden), benutze die Option **Preserve order of Satin Columns**.

## Linie zu Satin

Diese Erweiterung konvertiert einen einfachen Pfad in eine Satinkolumnen. Dabei wird die Linienbreite übernommen. Nach der Konvertierung wirst du zwei "Holme" und (möglicherweise) viele Sprossen (wie bei einer Leiter). Wieviele Sprossen es gibt hängt ganz von der Form der Linie ab.

### Funktionsweise

1. Zeichne eine Beziér-Kurve (`B`)
2. Stelle die Linienbreite ein (`Ctrl+Shift+F)
2. Führe `Erweiterungen > Ink/Stitch  > Satin Tools > Linie zu Satin` aus

## Satin zu Linie

Satinkolumne zu Linie konvertiert eine Satinkolumne in ihre Mittellinie. Das ist besonders dann hilfreich, wenn du während des Designprozesses eine Satinkolumne in einen Laufstich abändern willst. Du kannst diese Funktion auch benutzen, wenn du die Breite der Satinkolumne ändern willst, aber der Parameter Zugausgleich nicht zum gewünschten Ergebnis (oder zu Überschneidungen) führt. In diesem Fall kannst du die Satinkolumne in einen Laufstich ändern, um im Anschluss die Weite im "Füllung und Kontur"-Panel anzupassen. Die Funktion ["Linie zu Satin"](#linie-zu-satin) führt den Laufstich wieder in eine Satinkolumne zurück. 

Das funktioniert am Besten mit Satinkolumnen gleicher Breite.

![Satin to Stroke example](/assets/images/docs/en/satin_to_stroke.png)

### Funktionsweise

1. Wähle eine oder mehrere Satinkolumnen aus, die in einen Laufstich umgewandelt werden sollen
2. Öffne `Erweiterungen > Ink/Stitch > Satinwerkzeuge > Satin zu Linie...`
3. Wähle, ob die ursprünglichen Satinkolumnen beibehalten oder gelöscht werden sollen
4. Klicke auf "Anwenden"

## Satinkolumne schneiden

Diese Option schneidet eine Satinkolumne an einem vordefiniertem Punkt. Alle Parameter die der Kolumne zuvor zugewiesen wurden werden auf beide Teile übertragen. Auch alle Sprossen bleiben erhalten. Sollte eine der beiden Kolumnen keine Sprossen beinhalten, wird eine Neue hinzugefügt.

### Funktionsweise

1. Wähle eine Satinkolumne an (eine Zick-Zack-Linie funktioniert hier nicht)
2. Füge über `Erweiterungen > Ink/Stitch  > Befehle > Befehle mit gewählten Objekten verknüpfen > Satin cut point` einen "Satin-Schnittstelle"-Befehl ein
3. Bewege das Symbol zur gewünschten Stelle. Der Zeiger muss genau auf die Stelle treffen, wo die Satinkolumne geschnitten werden soll
4. Wähle die Satinkolumne erneut an
5. Führe `Erweiterungen > Ink/Stitch  > Satin Tools > Satinkolumne schneiden` aus
6. Der Satin-Schnittstelle-Befehl und sein Zeiger sind verschwunden. Wähle die Satinkolumne aus: es sind jetzt zwei.

## Satinkolumne umkehren

Dies ist ein kleines Werkzeug, mit dem der Stichpfad genau geplant werden kann. Bei Anwendung kehrt es eine Satinkolumne, die auf der linken Seite beginnt und auf der rechten Seite endet, um. Diese wird nun auf der rechten Seite beginnen und auf der linken Seite enden.
Sonst wird nichts an der Satinkolumne verändert.

![Flip Satin Columns](/assets/images/docs/en/flip-satin-column.jpg)

### Funktionsweise

* Wähle eine oder mehrere Satinkolumne(n) aus
* Starte `Erweiterungen -> Ink/Stitch -> Satinkolumne umkehren`


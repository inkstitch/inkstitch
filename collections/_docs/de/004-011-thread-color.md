---
title: "Garnfarben-Verwaltung"
permalink: /de/docs/thread-color/
excerpt: ""
last_modified_at: 2021-10-23
toc: true
---
## Garnliste importieren

Ink/Stitch kann Garnlisten auf ein Design anwenden. Das ist besonders dann nützlich, wenn du mit bestehenden Stickdateien arbeitest, die keine Farbinformationen speichern (z.B. DST).

Außerdem könnte diese Funktion dazu dienen, verschiedene Farbvariationen auszuprobieren. Du kannst Garnlisten importieren und exportieren wie es dir gefällt. Wichtig ist nur, dass sich die Stickreihenfolge- und anzahl der Objekte nicht ändert. In einem solchen Fall solltest du auf das Speichern der kompletten SVG-Datei zurückgreifen (das ist auch sonst nie eine schlechte Idee).

### Importieren
Öffne `Erweiterungen > Ink/Stitch > Garnliste importieren ...` um eine von Ink/Stitch erstellte Garnliste zu importieren.

Willst du eine andere Garnliste aus einer Textdatei (txt) importieren, wähle die Option "Andere Garnliste importieren" und wähle aus der Auswahlliste eine Garnpalette aus bevor du auf "Anweden" klickst.

**Tipp:** Installiere die Addons für Ink/Stitch um mehr Garnlisten in der Auswahlliste zur Verfügung zu haben.
{: .notice--info }

### Exportieren

Garnlisten können nur über eine ZIP-Datei exportiert werden ([batch export](/de/docs/import-export/#batch-export))

## Benutzerdefinierte Farbpalette installieren

Wenn du eine `.gpl` Liste hast, die deine Garnfarben abbildet, kannst du sie mit dieser Erweiterung einfach in Inkscape verfügbar machen: `Erweiterungen > Ink/Stitch > Garnfarben Verwaltung > Benutzerdefinierte Farbpalette installieren`. Inkscape muss nach diesem Vorgang neu gestartet werden.

.gpl-Farbpaletten können mit GIMP erstellt werden.

## Farbpaletten für Insckape installieren

Ink/Stitch enthält viele Farbpaletten der üblichen Garnhersteller. Diese können installiert werden, damit sie in Inkscape nutzbar sind.
Das erlaubt dir dein Design mit den richtigen Farben zu planen. Die Farben werden in die PDF-Ausgabe übernommen und auch in der Stickdatei abgespeichert, sofern dein Stickformat dies unterstützt.

**Installation**
* Gehe zu `Erweiterungen -> Ink/Stitch -> Garnfarben Verwaltung > Installiere Erweiterungen für Inkscape`
* Wähle "Installieren"
* Starte Inkscape neu

### Handhabung der Farbpaletten

Die Inkscape Farbpaletten befinden sich unten rechts neben den Farbfeldern.

![Inkscape Farbpaletten](/assets/images/docs/palettes-location.png)

Klicke auf den kleinen Pfeil, um eine Liste der installierten Paletten zu öffnen und wähle die Herstellerfarbpalette abhängig von dem Garn, das verwendet werden soll.

Die Auswahl wirkt sich auch auf die in der Druckvorschau angezeigten Garnnamen aus.

## Farbpalette generieren

Dieses Feature ist Teil der kommenden Ink/Stitch Version und in Ink/Stitch v2.1.2 noch nicht enthalten.
{: .notice--warning }

Inkscape kann `.gpl` Farbpaletten erstellen. Aber es ist nicht möglich, die Farben zu sortieren.

Diese Erweiterung exportiert die Farben von Textelementen, während der Text selbst als Farbname und Nummer abgespeichert wird.

1. Import an image with the thread colors you want to use for the color palette.
2. Activate the text tool and copy & paste the color names (if you have them) or type them in.
   Use one line for each color.
   If the last part of a color name is a number, it will be used as the catalog number.
3. Use `Extensions > Ink/Stitch > Thread Color Management > Generate Palette > Split Text` extension to split a text block with multiple lines into separate text elements.
4. Activate the color picker tool (D) and color the text elements, while using tab to select the text elements.
5. Select the text elements and run `Extensions > Ink/Stitch > Thread Color Management > Generate Palette > Generate Color Palette ...`
6. Specify the name for your color palette and click on apply
7. Restart Inkscape to activate the new color palette

{% include video id="I5BjjG5T7qo" provider="youtube" %}

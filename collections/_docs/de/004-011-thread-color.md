---
title: "Garnfarben-Verwaltung"
permalink: /de/docs/thread-color/
last_modified_at: 2024-07-13
toc: true
---
Inkscape unterstützt den Gebrauch von Farbpaletten. Farbpaletten helfen Ink/Stitch Farbnamen zu definieren und zusätzliche Informationen wie den Namen des Garnherstellers und die Katalognummer in die Stickdatei abzuspeichern.

Abhängig von den Möglichkeiten der genutzten Maschine können Farbnamen während des Stickvorgangs vom Maschinendisplay abgelesen werden. Bitte beachte, dass nicht alle Stickdatei-Formate das Abspeichern von Farbinformationen erlauben (z.B. DST). Für andere Formate nutzen ein Mehr-Dateien-System. Für EXP-Dateien beispielsweise ist es üblich, neben der Stickdatei auch eine INF-Datei abzuspeichern, die dann die Farbinformationen enthält.

Farbinformationen werden auch in die [PDF Ausgabe](/de/docs/threadlist/) übernommen. Außerdem können auch menschenlesbare einfach Textdateien mit der Garnabfolge (sogenannte [Garnfarben-Listen](/de/docs/threadlist/)) exportiert werden.

Bevor aber mit den Garnfarben gearbeitet werden kann, müssen zunächst die Farbpaletten installiert werden. Es gibt die Möglichkeit entweder [eigene Farbpaletten](/de/docs/thread-color/#benutzerdefinierte-farbpalette-installieren) zu erstellen und zu installieren oder die von [Ink/Stitch mitgelieferten Farbpaletten](/de/docs/thread-color/#vordefinierte-farbpaletten-für-insckape-installieren) in Inkscape verfügbar zu machen.

## Farbpaletten installieren

### Vordefinierte Farbpaletten für Insckape installieren

Ink/Stitch enthält viele Farbpaletten der üblichen Garnhersteller. Diese können installiert werden, damit sie in Inkscape nutzbar sind.
Das erlaubt dir dein Design mit den richtigen Farben zu planen. Die Farben werden in die PDF-Ausgabe übernommen und auch in der Stickdatei abgespeichert, sofern dein Stickformat dies unterstützt.

**Installation**

* Gehe zu `Erweiterungen -> Ink/Stitch -> Garnfarben Verwaltung > Installiere Erweiterungen für Inkscape`
* Wähle "Installieren"
* Starte Inkscape neu

### Benutzerdefinierte Farbpalette installieren

Wenn du eine `.gpl` Liste hast, die deine Garnfarben abbildet, kannst du sie mit dieser Erweiterung einfach in Inkscape verfügbar machen: `Erweiterungen > Ink/Stitch > Garnfarben Verwaltung > Benutzerdefinierte Farbpalette installieren`.
Inkscape muss nach diesem Vorgang neu gestartet werden.

Farbpaletten können mit Ink/Stitch erstellt werden. Wie das geht wird auf dieser Seite weiter unten beschrieben.

## Farbpaletten erstellen und bearbeiten

### Farbpalette erstellen

Inkscape kann `.gpl` Farbpaletten erstellen. Aber es ist nicht möglich, die Farben zu sortieren.

Diese Erweiterung exportiert die Farben von Textelementen, während der Text selbst als Farbname und Nummer abgespeichert wird.

1. Importiere ein Bild mit den Garnfarben, die die neue Farbpalette enthalten soll.
2. Aktiviere das Text-Werkzeug und füge die Farbnamen ein (wenn vorhanden) oder tippe sie ein.
   Benutze eine Zeile pro Farbe.
   Wenn der letzte Teil des Farbnamens eine Nummer ist, wird er als Katalognummer interpretiert und abgespeichert.
3. `Erweiterungen > Ink/Stitch > Garnfarben Verwaltung > Palette erstellen > Text zerlegen` teilt den Text in einzelne Textelemente.
4. Aktiviere das Farbwahl-Werkzeug (D) und färbe die einzelnen Textelemente ein.
   Nutze dabei die Tabulator-Taste um das jeweils nachfolgende Textelement auszuwählen.
5. Wähle alle Text-Elemente aus und führe die Funktion `Erweiterungen > Ink/Stitch > Garnfarben Verwaltung > Palette erstellen > Farbpalette erstellen ...` aus.
6. Gib einen Namen für die Farbpalette ein und klicke auf Anwenden.
7. Inkscape neu starten um die neue Farbpalette verfügbar zu machen

{% include video id="4bcRVoKvzAw" provider="youtube" %}

### Farbpalette zu Text

Bereits bestehende Farbpaletten können mit Ink/Stitch als Text bearbeitet werden.

* Importiere Farben und Farbnamen mit `Erweiterungen > Ink/Stitch > Garnfarben verwalten > Palette zu Text`
* Ändere Farben, Farbnamen, Katalognummern oder füge weitere Farben hinzu.
* Exportiere die Palette mit `Erweiterungen > Ink/Stitch > Garnfarben Verwaltung > Palette erstellen > Farbpalette erstellen ...`
* Inkscape neu starten

## Mit Farbpaleten arbeiten

### Generelle Handhabung

Die Inkscape Farbpaletten befinden sich unten rechts neben den Farbfeldern.

![Inkscape Farbpaletten](/assets/images/docs/palettes-location.png)

Klicke auf den kleinen Pfeil, um eine Liste der installierten Paletten zu öffnen und wähle die Herstellerfarbpalette dem Garn entsprechend, das verwendet werden soll.

Um eine bestimmte Farbe auf ein Element anzuwenden, klicke auf die Farben am unteren Bildschirmrand. Nutze einen einfachen `Links-Klick` für eine Füllfarbe und `Umschalttaste + Links-Klick` für eine Konturfarbe. Nutze das X auf der linken Seite um eine Farbe zu entfernen.

### Farbpalette anwenden

{% include upcoming_release.html %}

Diese Erweiterung wendet die ähnlichsten Farben einer gewählten Farbpalette auf das geöffnete Design an.
Die Farben werden entsprechend in die Stickdatei gespeichert und in der PDF-Ausgabedatei angezeigt.

* Öffne `Erweiterung > Ink/Stitch > Garnfarben Verwaltung > Farbpalette anwenden`
* Wähle eine Farbpalette
* Klicke auf `Anwenden`

## Mit Garnlisten arbeiten

### Garnfarben-Liste anwenden

Ink/Stitch kann Garnlisten auf ein Design anwenden. Das ist besonders dann nützlich, wenn du mit bestehenden Stickdateien arbeitest, die keine Farbinformationen speichern (z.B. DST).

Außerdem kann diese Funktion dazu dienen, verschiedene Farbvariationen auszuprobieren. Du kannst Garnlisten importieren und exportieren wie es dir gefällt. Wichtig ist nur, dass sich die Stickreihenfolge- und anzahl der Objekte nicht ändert. In einem solchen Fall solltest du auf das Speichern der kompletten SVG-Datei zurückgreifen (das ist immer eine gute Idee).

* Öffne `Erweiterungen > Ink/Stitch > Garnfarbenverwaltung > Garnfarben-Liste anwenden`
* Wähle eine Datei mit Farbinformationen
* Definiere, ob die Datei mit Ink/Stitch erstellt wurde oder nicht

  Wenn nicht: Wähle die Farbpalette aus, die genutzt werden soll
* Klick auf anweden

### Garnliste Exportieren

Garnlisten für ein Design können nur über eine ZIP-Datei exportiert werden ([batch export](/de/docs/import-export/#batch-export))

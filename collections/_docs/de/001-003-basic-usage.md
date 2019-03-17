---
title: "Grundfunktionen"
permalink: /de/docs/basic-usage/
excerpt: ""
last_modified_at: 2018-08-26
toc: true
---
Probiere die folgenden Schritte aus, um die Erweiterung zu testen und die Grundfunktionen kennenzulernen.

**Tipp:** Wenn noch nicht mit Inkscape gearbeitet wurde, dann sieh zuerst deren [Einführung](https://inkscape.org/de/doc/tutorials/basic/tutorial-basic.html) an.
{: .notice--info }

## Schritt 1 - Objekt zeichnen

Erstelle ein Objekt, z.B. ein Kreis und stelle sicher, dass es sowohl eine Kontur als auch eine Füllung hat.

**Info:** *Die Verwendung einer Linie ist für Satinkolumnen nicht geignet*. Wir haben es dennoch hier verwendet, um ein einfaches Beispiel zu geben. Lese in der Stichbibliothek, um mehr Informationen über Stichtypen zu erhalten.
{: .notice--warning }

![Füllung und Kontur](https://edutechwiki.unige.ch/mediawiki/images/thumb/8/86/SVG-yellow-circle-stroke-fill.png/300px-SVG-yellow-circle-stroke-fill.png)

## Schritt 2 - In einen Pfad konvertieren
**Alle Objekte** umwandeln, die zu einem Pfad werden sollen:

* Markiere alle Objekte (`Strg + A`)
* `Pfad -> Objekt in Pfad umwandeln` oder `Strg + Alt + C`. <br>

**Info:** Objekte, die nicht ein Pfad sind, werden von Ink/Stitch ignoriert.
{: .notice--warning }

## Schritt 3 - SVG-Pfad mit Parametern versehen

* Wähle minimum ein Objekt aus.
* Öffne `Erweiterungen -> Ink/Stitch -> Parameter` und verändere diese gegebenenfalls.
* Akzeptiere einfach die Standardeinstellungen oder schliesse diese ohne zu speichern.

## Schritt 4 - Erstellung der Stickdatei

Es kann entweder eine Stickdatei für eine Auswahl von Objekten oder für alle Objekte erstellen werden.
So wird eine Stickdatei für das gesamte Design erstellt:

* Klicken in einen leeren Bereich (um die Auswahl aufzuheben)
* Öffne / Starte `Erweiterungen -> Ink/Stitch -> Sticken ...`
* Wähle das richtige Dateiformat für das Gerät aus
* Wähle ein Verzeichnis aus, in dem die Ausgabedateien gespeichern werden. Z.B. `C:\Benutzer\%BENUTZERNAME%\Dokumente` unter Windows. Ink/Stitch merkt sich diese Auswahl.

## Schritt 5 - Anzeige in Inkscape

Einen Kreis, den wir im Beispiel erstellt haben, wird verschwinden und durch einige Streifen und Zickzacks ersetzt. Ink/Stitch hat alle Ebenen ausgeblendet und einen neuen "Stich Plan" erstellt. Dieser wird visuallisiert dargestellt. Es hat die ausgewählte Form in zwei Objekte zerlegt: Füllung und Kontur. Eine Füllung wird mit Hilfe von Füllstichen erstellt. Eine Kontur wird durch Satinstiche entlang dieser Kontur erstellt.

Wähle die horizontalen Linien mit dem Werkzeug "Bearbeiten der Koten..." aus. Zoome etwas heran um zu sehen, dass die Linien aus vielen Punkten bestehen. Jeder Punkt repräsentiert einen Stich - eine Nadeleindringung und eine Verriegelung des Oberfadens mit dem Unterfaden. Beachte, dass die Punkte alle in Diagonalen liegen. Dies verleiht der Füllnaht eine schöne und ordentliche Optik.

Schaue jetzt die Zickzacks an. Dies sind die Satinstiche. Beachte, dass die Ecken ziemlich hässlich aussehen. Dies liegt daran, dass Satinstiche, die aus einer Form erzeugt wurden, ziemlich rudimentär sind und nicht intelligent umgesetzt werden. *Mit einer [**Satinkolumne**](/docs/stitches/satin/)* können Satinstiche viel besser erzeugt werden.
![Stitch Plan](https://edutechwiki.unige.ch/mediawiki/images/thumb/6/6a/Inkstitch-stitch-plan.png/800px-Inkstitch-stitch-plan.png)

Die Vorschau, die gerade betrachtet wird, soll nicht permanent sein. Sobald die Stiche betrachtet wurden, kann man diese mit `Strg + Z` rückgängig machen. Die eigentliche Arbeit ist eine Designdatei zu erstellen.

## Schritt 6 - Das Design sticken
Wohin wurde die Designdatei gespeichert? Einer der Parameter, die im Dialogfeld `Sticken` angeben werden konnten, war das Ausgabeverzeichnis. Das verwendete Verzeichnis ist standardmäßig der Ort, in dem Ink/Stitch installiert wurde.

Ink/Stich erstellt eine Datei mit dem Namen `irgendwas.ext`, wobei `irgendwas` der Name der SVG-Datei ist (z. B.`irgendwas.svg`). `ext` ist die Erweiterung für das ausgewählte Ausgabeformat. Wenn `irgendwas.ext` bereits existiert, wird siese in `irgendwas.ext.1` unbenannt. Es werden bis zu 5 Backup-Kopien unterstützt.

   <span style="color: #3f51b5;">↳ irgendaws.ext</span><br/>
   <span style="color: #ff9800;">↳ irgendwas.ext</span>, <span style="color: #3f51b5;">irgendwas.ext.1</span><br/>
   <span style="color: #f44336;">↳ irgendwasg.ext</span>, <span style="color: #ff9800;">irgendwas.ext.1</span>, <span style="color: #3f51b5;">irgendwas.ext.2</span>

Wenn das Design wie gewünscht erstellt wurde, speichere eine Kopie von <span style="color: #f44336;">`irgendwas.ext`</span> und übertrage diese zu der Stickmaschine.

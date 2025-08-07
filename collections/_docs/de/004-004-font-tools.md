---
title: "Schriftverwaltung"
permalink: /de/docs/font-tools/
last_modified_at: 2025-04-12
toc: true
---
Eine Sammlung von Werkzeugen für Schriftarten Entwickler oder Personen, die dem [Text-Werkzeug](/de/docs/lettering/) von Ink/Stitch zusätzliche Schriften hinzufügen wollen.

Ein Blick in das [Schriften für Ink/Stitch erstellen Tutorial](/de/tutorials/font-creation) lohnt sich auf jeden Fall, wenn du neue Schriften erstellen willst.
{: .notice--info }

## Convert SVG Font to Glyph Layers
This extension allows you to convert an svg font into glyph layers.


## Benutzerdefinierter Ordner für Schriften

Diese Erweiterung erlaubt dir, einen Ordner zu definieren, in dem du zusätzliche Schriften für das Text-Werkzeug speichern willst.

Jede Schriftart sollte in einem eigenen Unterordner gespeichert werden und sollte mindestens folgende Dateien enthalten: eine Schriftdatei (svg) und eine json-Datei.
Zusätzlich empfehlen wir eine Lizenz-Datei.

Die Schriftdatei muss nach der Stichrichtung für die sie erstellt wurde benannt werden (`→.svg`, `←.svg`, etc.). Es gibt auch die Möglichkeit Ordner mit den Pfeilnamen (`→`, `←`, etc.) anzulegen und darin mehrere Dateien für die Stickrichtung abzuspeichern.

Die JSON-Datei muss als minimale Bedingung den Namen der Schrift enthalten.

## JSON bearbeiten

Diese Erweiterung erlaubt das Bearbeiten von Schriftinformationen. Hat die Schrift noch keine JSON-Datei, erstelle sie zunächst mit [JSON-Datei erstellen](#json-datei-erstellen)

Außerdem wird bei Ausführung der Erweiterung die Liste der verfügbaren Zeichen in der JSON-Datei aktualisiert. Daher sollte sie nach dem Hinzfügen oder Löschen von Schriftzeichen auf die geänderte Schrift angewandt werden.

## Zeichentabelle

Diese Erweiterung generiert eine Liste aller Zeichen einer Schrift.
So können Schriftautoren schnell und einfach das Stickergebnis einer neuen Schrift prüfen.

### Funktionsweise

* Öffne `Erweiterungen > Ink/Stitch > Schriftverwaltung > Zeichentabelle`
* Wähle eine Schrift und setze die gewünschten Einstellungen
* Klicke auf Anwenden

### Optionen

* Schrift: die Schrift die ausgegeben werden soll
* Stickrichtung: Links nach rechts in der Standardeinstellung
* Skalieren: in Prozent
* Maximale Zeilenlänge: fügt Zeilenumbrüche entsprechend des gewählten Wertes ein
* Farbsortierung: legt fest, ob mehrfarbige Schriften sortiert werden sollen (damit das funktioniert, muss die Schrift die entsprechenden [Farbsortierindices](#farbsortierindex-festlegen) festgelegt haben)

## Vernähstiche erzwingen

Bei kleinen Schriften kann es schnell passieren, dass sich der Faden löst, wenn Sprungstiche nach der Fertigstellung geschnitten werden.

Um dies zu verhindern, ist es wichtig, dass auch I-Punkte u.ä. mit einem kleineren Abstand zum Schriftkörper als durch die minimale Sprungstichlänge definiert, vernäht werden.

Diese Erweiterung soll dabei helfen, die Stickobjekte entsprechend zu bearbeiten.

### Funktionsweise

* Öffne `Erweiterungen > Ink/Stitch > Schriftverwaltung > Vernähstiche erzwingen...`
* Setze die Einstellungen wie gewünscht passend zur geöffneten Schrift
* Klick auf Anwenden

### Optionen

* Auf Satinsäulen beschränken

* "Vernähen erzwingen" nach Abstandsparametern einfügen
  * Minimaler Abstand (mm): füge keinen Vernähstiche erzwingen Befehl ein, wenn der Abstand zum nächsten Element kleiner ist als dieser Wert
  * Maximaler Abstand (mm): füge keinen Vernähstiche erzwingen Befehl ein, wenn der Abstand zum nächsten Element größer ist als dieser Wert

* Füge das Attribut "Vernähen erzwingen" dem jeweils letzten Element eines Schriftzeichens hinzu

## JSON-Datei erstellen

Diese Erweiterung wurde entwickelt, um die Erstellung der JSON-Datei zu erleichtern.

Abhängig davon, wie du deine Schriftdatei erstellt hast, wird die Kerning Information ebenfalls in die JSON-Datei übertragen.
Lese nach [**wie man eine SVG-Schrift mit Kerning Information erstellt**](/de/tutorials/font-creation)

Wenn du deine Schrift ohne Kerning erstellt hast, kannst du mit diesem Werkzeug immer noch eine JSON-Datei mit den Grundinformationen erstellen.

### Schriftinformationen

|Option                          |Beschreibung
|--------------------------------|---------------------------------
|Name                            |Pflichfeld. Der Name der Schrift.
|Beschreibung                    |Eine kurze Beschreibung deiner Schrift
|Schriftdatei                    |Pflichtfeld. Wenn du deine Schrift mit Hilfe von FontForge erstellt hast, wird Ink/Stitch die Kerning informationen aus dieser Datei lesen und in die JSON-Datei einfügen.<br>Außerdem legt der Dateipfad den Speicherort für die neue JSON-Datei fest.<br/><br/>Die Datei `font.json` wird in demselben Ordner erstellt, in dem deine SVG-Schriftdatei liegt.
|Stichwörter                     |Aktiviere die Kategorien, die für die Schrift zutreffend sind

### Einstellungen

|Option                          |Beschreibung
|--------------------------------|---------------------------------
|Automatisch geführte Satinsäulen|▸ aktiviert<br/>Ink/Stitch generiert automatisch geführte Satinsäulen, wenn die Schrift mit dem Text Werkzeug von Ink/Stitch benutzt wird. [Mehr Informationen über automatisch geführte Satinsäulen](/de/docs/satin-tools/#automatisch-geführte-satinsäulen)<br/><br/>▸ deaktiviert<br/>Ink/Stitch benutzt die Buchstaben so wie du sie digitalisiert hast. Wennn du selbst schon für einen optimalen Stichpfad gesorgt hast, kannst du diese Funktion deaktivieren.
|Umkehrbar                      | definiere, ob deine Schrift vorwärts und rückwärts gestickt werden kann.  Wähle diese Option nur, wenn du verschiedene Schriftvarianten (bzw. Richtungen) erstellt hast.
|Sortierbar                     | legt fest, ob die Farbsortier-Option für diese Schrift aktiviert werden soll. Diese Option funktioniert nur, wenn in der Schriftdatei der [Farbsortierindex](#farbsortierindex-festlegen) festgelegt wurde.
|Indizes kombinieren| Komma getrennte Liste von Farbsortierindexen. Elemente mit dem gleichen in dieser Liste aufgeführten Farbsortierindex werden zu einem Element zusammengefügt. Dies ist hilfreich um Farbwechsel für Sitcharten mit mehreren Farben zu vermeiden (z.B. Tartan).
|Klein-/Großbuchstaben erzwingen|▸ Nein<br/>Wähle diese Option, wenn deine Schrift sowohl Großbuchstaben, als auch Kleinbuchstaben enthält.<br/><br/>▸ Großbuchstaben<br/>Wähle diese Option, wenn die Schrift nur Großbuchstaben enthält.<br/><br/>▸ Kleinbuchstaben<br/>Wähle diese Option, wenn die Schrift nur Kleinbuchstaben enthält.
|Standard-Glyphe| das Zeichen/der Buchstabe der ausgegeben werden soll, wenn der eingegebene Buchstabe nicht in der Schriftdatei vorhanden ist
|Minimale Skalierung / Maximale Skalierung| definiert, wie weit die Schrift maximal skaliert werden darf ohne beim Sticken an Qualität zu verlieren 

### Kerning

Die folgenden Felder sind nur notwendig, wenn die SVG-Schriftdatei keine Kerning Information enthält.
Wenn keine Kerning Information vorhanden ist, werden die unten stehenden Werte automatisch genutzt.

|Option                          |Beschreibung
|--------------------------------|---------------------------------
|Erzwinge nutzerdefinierte Werte | Benutze nicht die Kerning-Information aus der Schriftdatei, sondern die unten definierten Werte.
|Zeilenhöhe (px)                 | Abstand zur nächsten Zeile
|Wortabstand (px)                | Die Breite des Leerzeichens


## Buchstaben zu Schrift

"Buchstaben zu Schrift" ist ein Werkzeug, um bereits digitalisierte Buchstaben zu einer mit Ink/Stitch nutzbaren Schrift zusammenzufügen.

Die digitalisierte Schrift muss für den Import folgende **Bedingungen** erfüllen:
* Eine Datei pro Buchstabe in einem Stickformat, das Ink/Stitch lesen kann
* Der Buchstabenname muss am Ende des Dateinamens stehen. Eine gültiger Dateiname für den Großbuchstaben A könnte z.B. sein `A.pes` oder `Beispielschrift_A.pes`

Bei gekauften Schriften kommt es häufig vor, dass die Buchstaben in Unterordnern organisiert sind, da jeder Buchstabe in mehreren Dateiformaten geliefert wird. Diese Struktur muss nicht geändert werden. Ink/Stitch durchsucht auch die Unterordner nach den Buchstabendateien.
{: .notice--info }

### Funktionsweise

* Wähle das Dateiformat aus dem du die Buchstaben importieren willst (idealerweise ein Format, dass Farbinformationen speichert)
* Wähle den Ordner in dem sich die Buchstaben befinden. Wenn es Unterordner gibt, wähle den Hauptordner der Schrift.
* Wähle, ob du Befehle importieren willst oder nicht (Warnung: importierte Befehle in großem Ausmaß verlangsamen das System erheblich)
* Klicke auf Anwenden - und warte ...
* Nach dem Import muss die Grundlinie (`baseline`) an die richtige Stelle gerückt werden und die Buchstaben entsprechend positioniert. Der linke Dokumentenrand wirkt sich ebenfalls auf die Positionierung der Buchstaben durch das Textwerkzeug aus
* Speichere die Datei als `→.svg` in einem neuen Ordner in dem [Benutzerdefinierten Ordner für Schriften](#benutzerdefinierter-ordner-für-schriften)
* Erstelle mit [JSON-Datei erstellen](#json-datei-erstellen) eine JSON-Datei, die die Schrift für das Textwerkzeug von Ink/Stitch nutzbar macht. "Automatisch geführte Satinsäulen" sollte für digitalisierte Schriften nicht ausgewählt sein. Die Skalierung bleibt bei 1.

## Kerning entfernen

**⚠ Warnung**: Änderungen die von diesem Werkzeug durchgeführt werden, können nicht rückgängig gemacht werden. Speichere auf jeden Fall eine **Kopie** deiner Datei ab, bevor du die hier beschriebenen Schritte durchführst.
{: .notice--warning }

Deine Schrift ist bereits einsatzbereit. Aber wenn du sie mit FontForge erstellt hast, beinhaltet sie noch jede Menge Informationen, die wir jetzt nicht mehr brauchen. Sie können sogar die Benutzung der Schrift ein wenig verlangsamen. Ink/Stitch stellt deshalb ein Werkzeug bereit, um die Datei von überflüssigen Informationen zu bereinigen.

1. Stelle sicher, dass du eine **Kopie** deiner Schriftdatei erstellt hast. Die zusätzlichen Informationen werden zwar nicht für den Gebrauch der Schrift benötigt,
   könnten aber nützlich werden, wenn du z.B. weitere Buchstaben zu der Schrift hinzufügen willst.
2. Öffne `Erweiterungen > Ink/Stitch > Font Tools > Remove Kerning`
3. Die die zu bereinigende(n) Datei(en)
4. Klicke auf `Anwenden`

## Farbsortierindex festlegen

Legt den angebebenen Farbsortierindex für ausgewählte Elemente fest. Hierdurch wirdie Reihenfolge der Elemente für mehrfarbige Schriftarten bei der Farbsortierung festgelegt.

* Wähle einer einer Schriftdatei die Elemente mit einer bestimmten Farbe aus
* Öffne die Erweiterung `Erweiterungen > Ink/Stitch > Schriftverwaltung > Farbsortierindex festlegen`
* Stelle den Index-Wert ein
* Anwenden

In der JSON-Datei muss die Option `Sortierbar` aktiviert sein. Nutze die Erweiterung [JSON bearbeiten](#edit-json) und aktiviere die Option in den `Schrifteinstellungen`.
{: .notice--warning }

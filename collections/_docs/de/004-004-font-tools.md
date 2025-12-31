---
title: "Schriftverwaltung"
permalink: /de/docs/font-tools/
last_modified_at: 2025-09-06
toc: true
---
Eine Sammlung von Werkzeugen für Schriftarten Entwickler oder Personen, die dem [Text-Werkzeug](/de/docs/lettering/) von Ink/Stitch zusätzliche Schriften hinzufügen wollen.

Ein Blick in das [Schriften für Ink/Stitch erstellen Tutorial](/de/tutorials/font-creation) lohnt sich auf jeden Fall, wenn du neue Schriften erstellen willst.
{: .notice--info }

## SVG-Schriftart zu Glyphenebenen konvertieren ...

Diese Erweiterung erlaubt das Konvertieren einer SVG-Schriftart-Datei in Glyphen-Ebenen, so wie vom Textwerkzeug benötigt.

{% include upcoming_release.html %}
It allows font sizing by specifying the target height of specified glyph.

## Benutzerdefinierter Ordner für Schriften

Diese Erweiterung erlaubt dir, einen Ordner zu definieren, in dem du zusätzliche Schriften für das Text-Werkzeug speichern willst.

Jede Schriftart sollte in einem eigenen Unterordner gespeichert werden und sollte mindestens folgende Dateien enthalten: eine Schriftdatei (svg) und eine json-Datei.
Zusätzlich empfehlen wir eine Lizenz-Datei.

{% include upcoming_release.html %}

The font variant files used to have to be named  with an arrow, indicating the stitch direction it has been created for (`→.svg`, `←.svg`, etc.).
Now, names should be ltr.svg for left to right direction and rtl.svg for right to left direction.

It is also possible to create a folder named ltr (or rtl) instead and insert multiple font files for this specific direction.

Die JSON-Datei muss als minimale Bedingung den Namen der Schrift enthalten.

## JSON bearbeiten

Diese Erweiterung erlaubt das Bearbeiten von Schriftinformationen. Hat die Schrift noch keine JSON-Datei, erstelle sie zunächst mit [JSON-Datei erstellen](#json-datei-erstellen)

Außerdem wird bei Ausführung der Erweiterung die Liste der verfügbaren Zeichen in der JSON-Datei aktualisiert. Daher sollte sie nach dem Hinzfügen oder Löschen von Schriftzeichen auf die geänderte Schrift angewandt werden.

## Zeichentabelle

Diese Erweiterung generiert eine Liste aller Zeichen einer Schrift.
So können Schriftautoren schnell und einfach das Stickergebnis einer neuen Schrift prüfen.
{% include upcoming_release.html %}
It only render unlocked (sensitive) glyphs. This allows for partial sampling while creating the font.


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
 {% include upcoming_release.html %}
*  Add force lock stitches attribute to the last element of each group

## JSON-Datei erstellen

Diese Erweiterung wurde entwickelt, um die Erstellung der JSON-Datei zu erleichtern.

Abhängig davon, wie du deine Schriftdatei erstellt hast, wird die Kerning Information ebenfalls in die JSON-Datei übertragen.
Lese nach [**wie man eine SVG-Schrift mit Kerning Information erstellt**](/de/tutorials/font-creation)

Wenn du deine Schrift ohne Kerning erstellt hast, kannst du mit diesem Werkzeug immer noch eine JSON-Datei mit den Grundinformationen erstellen.

### Schriftinformationen
{% include upcoming_release_params.html %}
|Option                          |Beschreibung
|--------------------------------|---------------------------------
|Name                            |Pflichfeld. Der Name der Schrift.
|Beschreibung                    |Eine kurze Beschreibung deiner Schrift
|Font license          | Type of license  for this ink/stitch font
|Original Font name              |name of the underlying ttf font if any|
|Original Font URL                |url of the underlying font|
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
* Kerning-Informationen für die Buchstabenabstände können, wenn nötig, mit der Erweiterung [`Schriftverwaltung > JSON bearbeiten`](#json-bearbeiten) angepasst werden.
* Wenn deine Schrift mehrfarbig ist, können Farbabschnitte mit einem [Farbsortierindex](#farbsortierindex-festlegen) belegt werden.

## Glyphen organisieren

{% include upcoming_release.html %}

Das Ziel dieser Erweiterung ist es, die Arbeitsschritte für das Digitalisieren einer gesamten Schriftart zu ordnen.

Bei jedem Arbeitsschritt wird eine spezielle Glyphengruppe im Dokument nach oben geschoben und der Schriftenersteller muss zunächst diese Glyphen digitalisieren, bevor der nächste Schritt vollzogen werden kann.

Dieser Prozess unterteilt die Arbeit in kleinere Teilschritte und erhöht so die Möglichkeit bereits digitalisierte Buchstaben(teile) wieder zu verwenden.

Bei jedem Schritt sollten die bereits digitalisierten Glyphen ausführlich gestestet werden, da sie für andere Zeichen kopiert werden und es ist ärgerlich, wenn dies im Nachhinein wieder korrigiert werden muss:

* Nutze die [Zeichentabelle](#zeichentabelle) um alle freigeschalteten Buchstaben zu generieren
* Nutze die Erweiterung [Fehlerbehebung an Objekten](/de/docs/troubleshoot/) und korrigiere alle gefundenen Fehler
* Nutze die [Simulation](/de/docs/visualize/#simulator) um ungewünschte Sprungstiche ausfindig zu machen. Am Besten zoomt man hierfür weit in die Buchstaben rein.
* Nutze die [realistische Vorschau](/de/docs/visualize/#stich-plan-vorschau) um weitere Fehler zu entdecken
* Sticke die Buchstaben, das ist der beste Test überhaupt

### Schritt 1: Komma, Punkt und Bindestrich

Der Code entfernt stillweigend alls unerwünschten Ebenen (z.B. leere Pfade oder gar keine Pfade).

Bei diesem Schritt müssen nur Kommata, Bindestriche und Punkte digitalisiert werden.

### Schritt 2: Nicht zerlegbare Buchstaben

Bei diesem Schritt müssen alle Buchstaben digitalisiert werden, die in eine dieser drei Gruppen Fallen: Großbuchstaben, Kleinbuchstaben und Andere.

Es befinden sich kopierte Punkte in den Buchtaben wie i und j. Es liegt am Schriftautor zu entscheiden, ob dies hilfreich ist oder nicht.

Es müssen nur einfache Buchstaben digitalisiert werden (es gibt in diesen Gruppen keine Buchstaben mit diakritischen Zeichen).

### Schritt 3: Zahlen, Symbole und öffnende Satzzeichen

Bei diesem Schritt werden Zahlen, Symbole und ein paar Interpunktionen digitalisiert.

Manche Zeichen enthalten bereits kopierte Pfade.

Beispielsweise wurde für das Semikolon `;` bereits das Komma `,` und der Punkt `.` aus Schritt 1 kopiert. Diese Teilpfade können nun richtig positioniert oder aber auch gelöscht und neu erstellt werden.

Außerdem enthält die `1` die bereits digitalisierten Buchstaben `l` und `I`. Sind sie zu verschieden von der `1` um nützlich zu sein, können sie einfach gelöscht werden.

### Schritt 4: Schließende Satzzeichen

Der letzte Teil der Interpunktionen: schließende Zeichen können mit den öffnenden Zeichen erstellt werden.

Beispielsweise wird hier die sich öffnende Klammer `(` in die schließende Klammer `)` kopiert, kann positioniert und angepasst werden.

Normalerweise ist bei diesem Schritt bereits alles mit bereits digitalisierten Glyphen vorausgefüllt.

### Schritt 5: erste Diakritika (Apostrophe, Anführungszeichen und einfache Akzente)

Es gibt verschiedene Arten von Apostrophen und Anführungszeichen. Dies ist zumeist abhängig von der genutzten Sprache.

Hast du mindestens eine bereits digitalisiert, werden die anderen hier hinzugefügt.

Dasselbe gilt für die Anführungszeichen. Normalerweise gibt es hier nichts weiter zu tun.

Bei diesem Schritt werden einfache Akzente digitalisieren. Wenn möglich, sind sie mit ähnlichen Symbolen bereits vorausgefüllt.

Im schlimmsten Fall, 

Im schlimmsten Fall wird der Akzent von Buchstaben in der Schriftart verwendet, ist aber in der Schriftart nicht vorhanden. In diesem Fall wird der Buchstabe in eine Ebene eingefügt und muss nun noch digitalisiert werden.

Vergiss ncht, nicht benötigte Teile zu entfernen!

### Schritt 6: weitere Diakritika

In diesem Schritt werden die anderen diakritischen Zeichen behandelt.

Hier werden Zeichen des vorangegangenen Schrittes wiederverwendet.

Diese komplexen Akzente sind entweder doppelte Akzente oder haben die gleiche Form, aber an anderen Positionen.

Die Ebenen sind vorausgefüll, aber die Positionierung muss vorgenommen werden, darum wurden in manchen Fällen die Buchstaben zu denen dieser Akzent gehört in die Ebene hinzugefügt.

### Schritt 7: zweiteilige Buchstaben

Buchstaben mit einfachen diakritischen Zeichen:

Die Buchstaben sind mit den diakritischen Zeichen vorausgefüllt und müssen noch positioniert werden.

### Schritt 8: andere zusammengesetzte Buchstaben

Buchstaben mit zwei oder mehreren diakritischen Zeichen ... für den Fall, das es überhaupt welche in der Schriftdatei gibt.


Diese Erweiterung kann mit jeder Schriftdatei genutzt werden um sie auf
* Zeichendopplungen zu überprüfen
* die Zeichen nach Kategorien zu ordnen

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

---
title: "Text"
permalink: /de/docs/lettering/
last_modified_at: 2026-10-18
toc: true
---
## Text-Werkzeug

Das Text-Modul erzeugt mehrzeiligen Text. Wähle aus einer großen Vielfalt vordigitalisierter Schriftarten die richtige Schrift für dein Projekt aus.

![Lettrage Extensions](/assets/images/docs/de/lettering.png)

## Anwendung

* Öffne `Erweiterungen > Ink/Stitch > Text > Text`.
* Gib deinen Text ein (mehrzeilig möglich).
* Lege die Schriftart und die Skalierung fest.
* **⚠ Warnung**: Beachte die angegebenen Limitierungen auch bei späteren manuellen Skalierungen.
* Klicke auf `Anwenden und schließen`.
* Der eingegebene Text erscheint über der Seite.
* Freie Positionierung ist nun möglich.

### Schriftfilter

* **Schriftgrößenfilter**<br>
  Schriften sind für eine bestimmte Skalierung digitalisiert. Der Schriftgrößenfilter hilft dir eine Schrift mit der richtigen Größe zu finden, indem er die
  Liste der Schriftarten nach der angegebenen Größe filtert.
  Ein aktivierter Filter (nicht 0) setzt bei der Auswahl einer Schriftart automatisch die Skalierung passend zur Suchgröße.

* **Zeichen**<br>
  Wenn aktiviert, werden nur Schriften angezeigt, die alle im Textfeld genutzten Buchstaben enthalten

* **Schrifttyp**<br>
  Schriften können nach Art der Schrift oder Anwendung gefiltert werden, z.B. Applikationsschriften oder serifenlose Schriften

### Optionen

* **Maßstab**

  Definiert die Größe des Textes im Vergleich zur Originalschrift (%).
  Es wird empfohlen Text mit dieser Option zu skalieren und nicht auf der Leinwandfläche in Inkscape.
  Auf diese Weise kannst du sicher stellen, dass die Textgröße auf die Parameter abgestimmt ist, mit denen die Schrift digitalisiert wurde.

* **Buchstabenabstand**

  Fügt diesen Wert (mm) als Abstand zwischen den einzelnen Zeichen ein.

* **Wortabstand**

  Fügt diesen Wert (mm) als Abstand zwischen Wörtern ein.

* **Zeilenhöhe**

  Fügt diesen Wert (mm) als Abstand zwischen den Zeilen ein.  

* **Farbsortierung**

  Sortiert Farben von mehrfarbigen Schriften und vermeidet so eine größere Anzahl an Farbwechseln.

* **Sticke Textzeilen vor und zurück**

  Wenn diese Option aktiviert ist, wird die erste Zeile von links nach rechts gestickt und die zweite von rechts nach links usw.
  Dadurch muss die Stickmaschine weniger hin und herspringen und die Sprungstiche werden verkürzt.

* **Text ausrichten**

  Ausrichtung von mehrzeiligem Text: Links, Mitte, Rechts, Block (Standard), Block (Buchstabenabstand)

* **Schnittmarker hinzufügen**

   Wenn diese Option aktiviert ist, fügt Ink/Stitch für jeden Buchstaben Schnittbefehle hinzu.

* **Befehlssymbole benutzen**

  Wenn Schnittbefehle hinzugefügt werden, nutze dafür die Darstellung der visuellen Symbole.
  Ist die Option deaktiviert, wird der Fadenschnitt-Befehl über die Parameter realisiert.

### Voreinstellungen

Hier kann eine Liste mit den beliebtesten Schriftarten gespeichert und wieder geöffnet werden.

## Text entlang Pfad

Ink/Stitch Schriften sind liebevoll designed. Wenn sie mit Inkscape Tools verformt werden (z.B. um sie in eine Kurve zu bringen) verliert das Ergebnis womöglich an Qualität. Auf der anderen Seite ist es ein langwieriger Prozess, die Buchstaben einzelnd an eine Linie anzupassen. Dieses Werkzeug hilft dir, eine Schrift auf einen Pfad zu legen - ohne die Buchstaben zu verzerren.

![curvy text](/assets/images/docs/text_along_path.jpg)

### Anwendung

* Wähle einen Pfad und eine Ink/Stitch-Text-Gruppierung

  Die Länge des Pfades sollte der Länge des Textes angemessen sein. Dabei ist es wichtig, den Text nicht manuell, sondern mit dem Textwerkzeug zu skalieren. Das Textwerkzeug bietet ebenefalls die Option Textzwischenräume zu erweitern oder zu verkleinern. Das ist besonders hilfreich, wenn der Text nach innen gebogen werden soll.
  {: .notice--info}
* Öffne `Erweiterungen > Ink/Stitch > Text > Text entlang Pfad ...`
* Passe die Optionen deinen Wünschen entsprechend an (siehe unten).
* Klicke auf `Anwenden`

Du willst den Pfad noch einmal ändern oder die Optionen anpassen? Das geht auch mit einem bereits transformierten Text. Wende die Funktion einfach noch mal an.
{: .notice--info}

### Optionen

#### Textposition

Ink/Stitch bietet verschiedene Optionen zur Textpositionierung, um deine Beschriftung am Pfad auszurichten:
* **Links:** Platziert den Text am absoluten Anfang des Pfades.
* **Mitte:** Zentriert den Text genau in der Mitte des Pfades.
* **Rechts:** Richtet den Text am äußersten Ende des Pfades aus.
* **Ausdehnen:** Streckt die Abstände zwischen den Zeichen, sodass der Text die gesamte Länge des Pfades ausfüllt.

Dabei richtet sich die Positionierung nach zwei wichtigen Faktoren: dem **Startpunkt des Pfades** und der **Pfadrichtung**.

![Ein Text der mit den verschiedenen Optionen an einem Pfad ausgerichtet ist](/assets/images/docs/text_along_path_alignment.png)

**Beispiel: Text auf einem Kreis**

Ein typischer Anwendungsfall ist das Platzieren von Text auf einem Kreises oder Oval. Standardmäßig beginnt der Pfad eines geschlossenen Kreises in Inkscape oben und verläuft gegen den Uhrzeigersinn. 
Der Simulator zeigt, dass der Stickpfad genau diesem Verhalten folgt. Für deine Textpositionierung ist dies meist nicht die richtige Einstellung.

Um den Kreis anzupassen, musst du das Objekt zuerst in einen Pfad umwandeln:
* Gehe auf **Pfad > Objekt in Pfad umwandeln** (oder drücke `Strg + Umschalt + C`).
* Diese Aktion ändert sowohl die Pfadrichtung als auch den Startpunkt.
* Überprüfe dies im Simulator; der Stickpfad beginnt nun in der Mitte rechts und verläuft im Uhrzeigersinn.

Um deinen Text oben auf dem Kreis zu positionieren, musst du den **Startpunkt anpassen**:
* Wähle das Knoten-Werkzeug (`N`) und klicke auf den **unteren Knoten**.
* Trenne den Pfad an dieser Stelle, indem du `Umschalt + B` drückst.
* Um die Trennung zu überprüfen, klicke auf den Knoten und ziehe ihn ein Stück weg (ohne die Maustaste loszulassen). Du wirst sehen, dass sich darunter ein zweiter Knoten verbirgt.
  Drücke `Esc`, um die Bewegung abzubrechen und den Knoten wieder einrasten zu lassen.

Dein neuer Startpunkt ist nun der untere Knoten und der Text kann oben zentriert werden.

Um die Startposition eines bereits getrennten Pfades zu ändern, wähle einfach beide getrennten Knoten aus, füge sie wieder zusammen (`Umschalt + J`) und trenne den Pfad an der gewünschten neuen Stelle.
{: .notice--info}

Jetzt müssen wir noch die **Pfadrichtung** bestimmen. Hierbei ist es hilfreich, wenn du dir [die Pfadrichtung anzeigen lässt](/de/docs/customize/#pfadkonturen--pfadrichtungen). Alternativ kannst du die Pfadrichtung aber auch mit dem Simulator überprüfen.

Ist die Pfadrichtung falsch herum, drehe den Pfad mit `Pfad > Pfadrichtung umkehren` um.

Hier ein Beispiel. Gleiche Einstellungen, aber gegenläufige Pfadrichtungen. Für die Textposition wurde `Mitte` gewählt.

![Zwei Texte die an jeweils einem Pfad ausgerichtet sind. Einmal geht der Pfad von links nach rechts und der Text sitzt oben auf. Der andere Pfad geht von rechts nach links und der Text hängt unten am Pfad und führt ebenfalls von rechts nach links.](/assets/images/docs/text_along_path_path_direction.jpg)

#### Vertikale Ausrichtung

Mit der vertikalen Ausrichtung bestimmst du, ob der Text komplett oberhalb des Pfades abgebildet werden soll (`oben`), ob der Pfad als `Grundlinie` dient oder ob der Text vollständig unterhalb des Pfades angezeigt wird (`unten`). Hier ein Beispiel, in dem der Text mit den Optionen in genau dieser Reihenfolge auf einen Pfad gelegt wurde.

![Ein Text der mit den drei Ausrichtungsoptinoen ausgerichtet wurde. Der Unterschied zwischen Oben und Grundlinie wird hier besonders bei dem Buchstaben p deutlich. Die Option oben legt den Text komplett über den Pfad, während mit der Option Grundlinie der Text auf dem Pfad aufliegt und der absteigende Teil des p's die Linie kreuzt](/assets/images/docs/text_along_path_vertical_alignment.jpg)

## Schrift-Bibliothek

Eine Übersicht über alle verfügbaren Schriftarten findet sich hier [Schrift-Bibliothek](/de/fonts/font-library/)

## Batch Lettering

Mit `Batch Lettering` können mehrere Textdateien gleichzeitig erstellt werden.

![A patch with four different names](/assets/images/docs/batch-lettering.png)

* Bereite die Design-Datei vor.
  Wenn die Datei einen Pfad mit dem label `batch lettering` enthält, wird dieser Pfad genutzt, um die Position des Textes festzulegen.
  Dies funktioniert genauso, wie [Schrift entlang Pfad](/de/docs/lettering/#schrift-entlang-pfad)
* Unter `Datei > Kopie speichern ...` wähle den kleinen Pfeil im Dateiformat-Auswahlfeld, um eine Liste der verfügbaren Dateiformate zu öffnen.
* Wähle das Format `Ink/Stitch: batch lettering (.zip)`
* Wähle den Speicherort und klicke auf `Speichern`

### Optionen

* **Text:** Gib einen Text ein. Standardmäßig wird pro Textzeile eine Datei erstellt.
* **Benutzerdefiniertes Trennzeichen:** Standardmäßig wird der Text bei Zeilenumbrüchen getrennt. Für mehrzeilige Texte muss ein benutzerdefiniertes Trennzeichen definiert werden.
* **Schriftname:** Der Name der Schrift, die verwendet werden soll. Eine Liste aller in Ink/Stitch verfügbaren Schriftarten gibt es in der [Schriftbibliothek](/de/fonts/font-library/)
* **Skalierung (%):** Gibt an, wie die Schrift skaliert werden soll. Der Wert wird auf die für die jewielige Schrift zugelassenen Werte beschränkt.
* **Farbsortierung:** Legt fest, ob mehrfarbige Schriften nach Farbe sortiert werden sollen
* **Fadenschnittbefehle hinzufügen:** Legt fest, ob Fadenschnittbefehle verwendet werden sollen (nie, nach jeder Linie, jedem Word oder Buchstaben)
* **Symbole verwenden:** Legt fest, ob die Fadenschnittbefehle als Parameter oder Symbol angelegt werden (nur bei Ausgabe als SVG relevant)
* **Mehrzeiligen Text ausrichten:** Definiert wie mehrzeiliger Text ausgerichtet werden soll
* **Schrift entlang Pfad**
  * **Horizontale Textposition:** Die Ausrichtung des Textes entlang des Pfades mit dem Label `batch lettering`
  * **Vertikale Textposition:** Die Ausrichtung am Pfad in vertikaler Richtung (über, auf oder unter dem Pfad)
* **Dateiformate:** eine durch Kommata getrennte Liste von [Dateiformaten](/de/docs/file-formats/#schreiben)

[Beispieldatei herunterladen](/assets/images/docs/batch_lettering_template_example.svg){: title="Download SVG File" download="batch_lettering_template_example.svg" }

### Verwedung mit der Shell

Hier ein minimales Beispiel für die Anwendung dieser Erweiterung in der Shell

```
./inkstitch --extension=batch_lettering --text="Hello\nworld" --font="Abecedaire" --file-formats="svg,dst" input_file.svg > output_file.zip
```

#### Optionen

Option             |Eingabetyp|Wert
---------- --------|----------|------
`--text`           |string    |darf nicht leer bleiben
`--separator`      |string    |default: '\n'
`--font`           |string    |muss ein valider Schriftname sein
`--scale`          |integer   |default: 100
`--color-sort`     |string    |off, all, line, word<br>default: off
`--trim`           |string    |off, line, word, glyph<br>default: off 
`--command_symbols`|bool      |default: False
`--text-align`     |string    |left, center, right, block, letterspacing<br>default: left
`--file-formats`   |string    |muss mindestens ein valides Dateiformat enthalten (kommagetrennte Liste)

## Neue Schriftarten für Ink/Stitch erstellen

Weitere Infos zu diesem Thema findest du in einem eigenen [Schrifterstellungs Tutorial](/de/tutorials/font-creation/).

Kontaktiere uns wenn du deine Schriftart für die nächste Ink/Stitch Version zur Verfügung stellen willst: [GitHub](https://github.com/inkstitch/inkstitch/issues).

## Sample Files Including Lettering

{% include tutorials/tutorial_list key="techniken" value="Text" %}


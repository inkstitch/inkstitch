---
title: "Text"
permalink: /de/docs/lettering/
last_modified_at: 2025-03-30
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
{% include upcoming_release_params.html %}
* **Maßstab**

  Definiert die Größe des Textes im Vergleich zur Originalschrift (%).
  Es wird empfohlen Text mit dieser Option zu skalieren und nicht auf der Leinwandfläche in Inkscape.
  Auf diese Weise kannst du sicher stellen, dass die Textgröße auf die Parameter abgestimmt ist, mit denen die Schrift digitalisiert wurde.

* **Letter spacing**
  
  Add that width (mm) between letters

* **Word spacing**

  Add that width (mm) between words

* **Line height**

  Add that height (mm) between lines

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

## Schrift entlang Pfad

Ink/Stitch Schriften sind liebevoll designed. Wenn sie mit Inkscape Tools verformt werden (z.B. um sie in eine Kurve zu bringen) verliert das Ergebnis womöglich an Qualität. Auf der anderen Seite ist es ein langwieriger Prozess, die Buchstaben einzelnd an eine Linie anzupassen. Dieses Werkzeug hilft dir, eine Schrift auf einen Pfad zu legen - ohne die Buchstaben zu verzerren.

![Ein Text der mit den verschiedenen Optionen an einem Pfad ausgerichtet ist](/assets/images/docs/text_along_path_alignment.png)

### Anwendung

* Wähle eine Pfad und eine Ink/Stitch-Text-Gruppierung
* Öffne `Erweiterungen > Ink/Stitch > Text > Schrift entlang Pfad ...`
* Ist `Strecken` aktiviert, wird Ink/Stitch die Buchstaben-Zwischenräume der Pfadlänge anpassen, so dass sich der Schriftzug über den gesamten Pfad erstreckt.
  Ist diese Option deaktiviert, bleiben die Buchstaben-Abstände unverändert.
* Klicke auf `Anwenden`

Die Buchstaben folgen der Pfadrichtung. Kehre den Pfad bei Bedarf mit `Pfad > Richtung umkehren` um.
{: .notice--info}

## Schrift-Bibliothek

Eine Übersicht über alle verfügbaren Schriftarten findet sich hier [Schrift-Bibliothek](/de/fonts/font-library/)

## Farben sortieren

Werden mehrere mehrfarbige Buchstaben gestickt, kann es sinnvoll sein zu viele Farbwechsel zu vermeiden.
Hier eine kurze Anleitung wie die Farben mehrfarbiger Ink/Stitch-Schriften schnell und einfach sortiert werden können:

* Wähle einen Buchstaben über den Ebenen und Objekte-Dialog
* Wähle den zuerst zu stickenden Pfad (der letzte Pfad dieser Gruppe)
* `Bearbeiten > Das Gleiche auswählen > Konturstil`
* Gruppiere die so entstandene Auswahl (Strg + G)
* Verschiebe diese Gruppe nach oben

Wiederhole diesen Prozess bis alle Farben gruppiert sind, wobei immer der zuerst zu stickende Pfad eines Buchstaben auszuwählen ist.

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
* **Schrift entlang Pfad: Textposition:** Die Ausrichtung des Textes entlang des Pfades mit dem Label `batch lettering`
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


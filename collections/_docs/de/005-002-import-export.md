---
title: "Import und Export von Dateien"
permalink: /de/docs/import-export/
last_modified_at: 2025-03-23
toc: true
---
## Stickdateien importieren

Öffne eine fertige Stickdatei, so wie eine beliebige SVG-Datei in Inkscape geöffnet wird: `Datei -> Öffnen ...`, wähle die Datei aus und wähle `Öffnen`.

Es öffnet die Datei im [Manuellen Stich Modus](/de/docs/stitches/manual-stitch). Es können einzelne Punkte bearbeitet und das Design optimiert werden. Sobald alles erledigt ist, speichere die Datei wie unten beschrieben ab.

## Stickdateien exportieren

Exportiere Dateien direkt über den Inkscape Dialog `Datei > Kopie speichern ...` (`Strg + Umschalt + Alt + S`)

Wähle ein Dateiformat, das die Stickmaschine lesen kann, und speichere die Datei im gewünschten Ausgabeverzeichnis.

![Ausgabeformat](/assets/images/docs/en/export-selection-field.jpg)

Für zukünftige Änderungen stelle sicher, dass auch eine SVG-Version des Designs behalten wird.

## Batch-Export

Unter `Datei > Kopie speichern ...` wähle den kleinen Pfeil im Dateiformat-Auswahlfeld, um eine Liste der verfügbaren Dateiformate zu öffnen.

Navigiere zum gewünschten Ausgabeverzeichnis und wähle dort das `Ink/Stitch: Export von mehreren Formaten (.zip)` aus. Klicke auf "Speichern". Dort wird  gefragt, welche Dateiformate hinein sollen.

![Batch Export](/assets/images/docs/en/export-batch.jpg)

Ink/Stitch speichert die Dateien innerhalb der ZIP-Datei mit dem Namen der Originaldatei (!) ab. Solltest du andere Dateinamen wünschen, diesen bitte in das Feld `Benutzerdefinierter Dateiname` eintragen.

![Batch export options](/assets/images/docs/de/zip-export1.png)

Die Zip-Export Funktion bietet die Möglichkeit zur Panelisierung. Sind die Werte für Wiederholungen höher als 1, wird Ink/Stitch Kopien des Stickplans in den gewünschten Abständen einfügen.
Die Abstände berechnen sich ausgehend von der oberen linken Ecke. Die Farbblöcke werden sortiert um Farbwechsel zu vermeiden.

## Batch Lettering

{% include upcoming_release.html %}

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

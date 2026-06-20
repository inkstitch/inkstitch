---
title: Füllstich Werkzeuge
permalink: /de/docs/fill-tools/
last_modified_at: 2026-01-01
toc: true
---
## Füllstich-Objekte zerlegen

Füllstich Objekte sollten aus Objekten bestehen, deren Randlinien sich nicht kreuzen. Manchmal ist es wirklich nicht einfach, diese Regel zu erfüllen, denn oft entstehen winzige Schleifen, die man in Inkscape gar nicht sehen kann. Aus diesem Grund können Füllstiche oft ärgerliche Fehlermeldungen hervorrufen.

Diese Erweiterung soll dir helfen, kaputte Objekte zu repaireren. Nutze diese Funktion einfach für alle Füllstich-Bereiche die eine Fehlermeldung ausgeben. Sie wird kleine Schleifen entfernen und wenn nötig, deine Form in kleinere Unterabschnitte unterteilen.

### Funktionsweise

* Wähle ein oder mehrere Füllobjekte aus
* Öffne das Dialogfenster unter `Erweiterungen > Ink/Stitch  > Füllstich Werkzeuge  > Füllstich-Objekte zerlegen`

## Einfach oder Komplex

* *Einfach* kann mit Löchern, unverbundenen Objekten und sich überkreuzenden Rändern arbeiten. Kombinierte Pfade werden in einzelne Pfade zerlegt.

* *Komplex* agiert genauso wie "einfach", kann aber zusätzlich mit Objekten mit mehreren sich überschneidenden Pfaden umgehen.

![Break apart fill objects](/assets/images/docs/en/break_apart.jpg)
[Download SVG](/assets/images/docs/en/break_apart.svg)

## Farbverlauf in Blöcke aufteilen

Diese Erweiterung teilt ein Füllobjekt mit einem linearen Farbverlauf in mehrere einfarbige Blöcke auf und setzt den zuvor bestimmten Wert für `Reihenabstand Ende`.

### Funktionsweise

1. Setze einen linearen Farbverlauf

   ![linear gradient](/assets/images/docs/en/linear-gradient.png)
2. `Erweiterungen > Ink/Stitch > Werkzeuge: Füllung > Farbverlauf in Blöcke aufteilen...`

   ![color blocks](/assets/images/docs/color_blocks.png)
3. Setze einen Wert für den Reihenabstand am Ende der Füllung. Bei einem Wert von 0.00 wird der doppelte Wert des ursprünglichen Reihenabstandes angenommen.

## Kreuzstich-Assistent

Der Kreuzstich-Assistent kann bei der Erstellung von [Kreuzstichmustern](/de/docs/stitches/cross-stitch) auf verschiedene Weise unterstützen.

* Überprüfung der diagonalen Stichlänge
* Anlegen des Seitengitters
* Verpixeln von Füllflächen
* Gittergröße als Parameter auf die Füllflächen übertragen

### Funktionsweise

* Optional: Wähle ein oder mehrere Füllflächen aus
* Öffne die Erweiterung unter `Erweiterungen > Ink/Stitch > Werkzeuge: Füllung > Kreuzstich-Assistent`
* Stelle die gewünschte Gittergröße ein
* Lege die gewünschten Optionen fest, wie die Gittergröße angewendet werden soll (siehe unten)
* Klicke auf `Anwenden`

#### Das Kreuzstich-Gitter

## Cross Stitch Assistant

The cross stitch assistant can assist in various ways when creating [cross stitch patterns](/docs/stitches/cross-stitch).

![A mushroom in two versions: vector path and pixelated outline](/assets/images/docs/cross_stitch_assistant.jpg){: .align-right style="max-width: 400px" }
It helps you to:
* Check and adapt the diagonal stitch length
* Create the page grid for cross stitch alignment (and visual support while working on cross stitches)
* Pixelize and combine the outline of selected elements, to avoid jump stitches, overlaps and to receive a better representation of the cross stitch positioning
* Apply cross stitch params to selected elements
* Convert bitmap images into cross stitch fill elements

### Usage

* Optional: select fill elements and/or bitmap images. Without a selection you can adapt the page grid only.
* Open the assistant extension under `Extensions > Ink/Stitch > Tools: Fill > Cross Stitch Assistant`
* Set the parameters, the output options and the bitmap settings (see below)
* Click on `Apply`

#### Settings

* **Grid settings**

  To ensure that adjacent areas are well coordinated, cross stitches are aligned according to a grid.
  This means that the embroidery pattern may change depending on where an element is located on the canvas.
  To plan this better, it is helpful to adjust the page grid to the size of the cross stitch pattern. This makes it easier to visually estimate the stitch positions.

  **Check if the page grid is aligned at the top left corner of the page.**<br/>
  If it is not, you'll need to manually adjust the grid under `File > Document Properties... > Grids`.
  You will find an `Align to page` setting, that cannot be accessed via the Ink/Stitch plugin.
  Set it to the top left corner.
  {: .notice--warning }

  When specifying the grid size, the **stitch lengths** of the diagonal crosses are not immediately apparent.
  However, stitch lengths always play an important role in machine embroidery.
  The Cross Stitch Assistant therefore has a field for displaying and adapting the diagonal stitch lengths.

* **Params, pixelate and bitmap settings**

  You can directly set the cross stitch fill params here, according to the grid spacing.

#### Output options

* **Apply grid settings**: Here you decide most of what the assistant is going to do.

   * Parameters: If checked, the cross stitch parameters will be applied to all selected fill elements, according to the Parameters tab of the cross stitch assistant.
   * Pixelize: If checked the Cross Stitch Assistant automatically pixelate selected fill elements based on the grid settings. This makes it possible to adjust the shapes directly to the grid and visually identify the stitch positions accurately.
     * Add nodes: One can chose to add nodes at each grid intersection. This will make it easier to manually adapt the outline of the shape.
       In non-square grids, nodes may not match grid intersections in vertical direction.
* **Element handling**:
  * Remove overlaps: decide if superpositions are kept or not.

* **Setup page grid**:
  * Define whether or not to adapt the page grid
  * Define grid color
  * Chose whether or not to remove the previously set cross stitch grids from the document.
    Your manual page grids will not be removed, but disabled.

#### Bitmap settings

* **Convert bitmaps**: If checked all selected bitmap images are converted into fill shapes
* **One cross each pixel**: check if you want to convert pixel art images
* **Color selection**: chose between specifying either
  * a number of colors, in this case you can also chose the color reducing algorithm. The proposed algorithms will give different results, and the best one really depends on your image
  * a list of rgb colors
  * a gimp color palette
   * or add strokes with the colors you want to use and add them to the selection before using the assistant.
* **Saturation, Brightness and Contrast** of the original image may be tweaked here to achieve better results
* **Transparency threashold**: pixels with at least that transparency are ignored.
* **Background color**: define the background color here, will allow you to remove the background.
* **Remove background**: decide what to do with fills with background color

In our tutorial section you can find multiple in depth instructions on how to convert images into cross stitch embroideries.
{: .notice--info }

<!--

Um beieinanderliegende Flächen gut aufeinander abzustimmen, richten sich Kreuzstche nach einem Gitter.
Das heißt, je nachdem an welcher Stelle auf der Arbeitsfläche sich ein Element befindet, kann sich das Stickbild ändern.
Um dies besser planen zu können, ist es hilfreich, das Seitengitter an die Kreuzstichmustergröße anzupassen. So kann man schon visuell die Stichpositionen besser abschätzen.

Unter `Datei > Dokumenteinstellungen... > Gitter` kann das Gitter auch manuell eingestellt werden. Dort gibt es auch eine Funktion (`An der Seite ausrichten`), die nicht über Ink/Stitch-Einstellungen erreicht werden kann. Daher ist es wichtig zu überprüfen, ob sich das erstellte Gitter an der oberen linken Seitenecke ausrichtet. Ansonsten muss diese Einstellung noch manuell angepasst werden.
{: .notice--warning }

#### Außenkontur verpixeln

Der Kreuzstich-Assistent hat außerdem eine Funktion die Außenkontur ausgewählter Füllflächen automatisch anhand der gesetzen Gittereinstellungen zu verpixeln.
So ist es möglich, die Formen direkt an das Gitter anzupassen und visuell die Stichpositionen genau erkennen zu können.

#### Stickparameter setzen

Nachdem das Gitter auf die gewünschte Größe eingestellt ist, muss die Gittergröße natürlich auch in den Stickparametern eines Elements gleichgesetzt werden. Wenn die Option aktiviert ist, kann der Kreuzstich-Assistent diese Einstellungen auch direkt selbst vornehmen.

#### Stichlängenberechnung

Durch die Angabe der Gittergröße sind die Stichlängen der diagonalen Kreuze nicht direkt ersichtlich.
Die Stichlängen spielen in der Maschinenstickerei aber immer eine wichtige Rolle. Der Kreuzstich-Assistent hat daher ein Feld für die Anzeige der diagonalen Stichlängen.

## Knockdown Füllung

Hilfsmethode zur Erstellung von:
- einem Füllbereich unter allen gewählten Elementen, optional mit positivem oder negativem Versatz. Dies kann sehr nützlich sein, für das Arbeiten mit hochflorigen Stoffen (bei positivem Versatz) oder um eine globale Unterlage zu erstellen (negativer Versatz)
- einem rechteckigen oder kreisförmigen Bereich um alle ausgewählten Elemente herum, wobei die Elemente selbst ausgespart werden. Dies kann für einen Embossing-Effekt nützlich sein.

![Eine Figure mit einem sie umgebenden Knockdown-Stich](/assets/images/docs/knockdown.png)

* Elemente auswählen
* `Erweiterungen > Ink/Stitch > Werkzeuge: Füllung > Auswahl zu Knockdown-Stich`
* Einstellungen anpassen
* Auf `Anwenden` klicken
* Füllparameter im Parameterdialog anpassen (`Erweiterungen > Ink/Stitch > Parameter`)

{% include upcoming_release.html %}

Der Reihenabstand wird automatisch an die gewählte Stichlänge angepasst.
-->
<!--
  Wenn du die gleiche Struktur behalten willst, das Muster aber skalieren möchtest,
  aktualisiere den Reihenabstand für die Deckschicht, als auch für die Unterlage und berechne die maximale Stichlänge: `spacing / sin(60)`<br><br>
  **Beispiel**: Wenn der Reihenabstand 1.8 mm beträgt, ist die maximale Stichlänge `1.8 / sin(60) ≈ 2.08`
  {: .notice--info }
  -->

### Einstellungen

#### Optionen

* Löcher erhalten: bestimmt ob die neue Füllfläche Löcher enthält
* Versatz: der Versatz (mm) um die Auswahl. Offset can be positive or negative
* Methode (rund, Gehrung, Abschrägung): Beeinflusst das Ergebnis um die Ecken herum
* Gehrungslimit: Beeinflusst das Ergebnis um die Ecken herum

#### Embossing

* Form: Definiert die äußere Form des Embossing-Effekts. Optionen sind Rechteck oder Kreis. Die Form wird um alle ausgewählten Elemente herum angelegt, so dass alle umschlossen werden. Die Elemente selbst, werden dabei ausgespart.
* Form ohne Ausschnitt: gibt die Form (Rechteck oder Kreis) ohne Motivausschnitt aus
* Versatz (Form): Ein positiver Wert erweitert den Embossing Bereich. Der Versatz berechnet sich auf die ausgesparte Form und bezieht den Versatz unter Optionen mit ein.
* Methode (rund, Gehrung, Abschrägung): Beeinflusst das Ergebnis um die Ecken herum

Anmerkung: wenn Embossing-Formen verwendet werden, ist der ausgesparte Bereich genauso angelegt, wie die Knockdown-Füllung sonst gewesen wäre. Der Versatz unter Optionen beeinflusst also die Größe der Embossing-Form.

## Tartan

Der Farbeditor ist unter `Erweiterungen > Ink/Stitch > Werkzeuge: Füllung > Tartan` zu finden.

![Ein Seepferdchen mit einem Tartan-Muster](/assets/images/docs/de/tartan_stripe_editor.png)

### Muster anpassen

#### Position

Das Muster kann als Ganzes rotiert, skaliert (%) und verschoben (mm) werden.

#### Muster Einstellungen

* Symmetrie: Muster können gespiegelt (symmetrisch) oder wiederholt (asymmetrisch) werden.
  * Ein gespiegeltes Muster kehrt die Farbreihenfolge in jeder zweiten Iteration um (ohne den äußeren Streifen, den Drehpunkt, zu wiederholen)
    Dies würde ein Muster mit drei Farben (grün, schwarz, gelb) wie folgt ausgeben: grün, schwarz, gelb, schwarz, grün, schwarz, gelb, ...
  * Ein wiederholtes Muster wird das gesamte Muster einfach immer wieder wiederholen: grün, schwarz, gelb, grün, schwarz, gelb, grün, ...
* Gleiche Farbkombination für Kette und Schuss
  * Ist diese Funktion deaktiviert, können für Kette und Schuss jeweils unterschiedliche Farben festgelegt werden
  * Ist diese Funktion deaktiviert, folgen Kette und Schuss der gleichen Farbkombination

#### Streifen

* Farben können über die Schaltfläche `Hinzufügen` hinzugefügt werden
* Hinter jedem Farbstreifen befindet sich ein `X` mit dem Farben gelöscht werden können
* Die Streifenpositionen kann durch Klicken und Ziehen auf der Schaltfläche `⁝` geändert werden (mit Vorsicht verwenden).
* Soll eine Farbe nur als Platzhalter dienen, kann die Ausgabe als Stickpfad über das Kontrollkästchen deaktiviert werden (☑)
* Soll Kette und Schuss nicht gleich sein, so werden die Farben für die Kettfäden vertikal und für Schussfäden horiztonal ausgegeben
* Über das Farbfeld kann die Farbe des jeweiligen Streifens geändert werden
* Gleiche Farben können gleichzeitig geändert werden, wenn das Kontrollkästchen `Farben verlinken` aktiviert ist

### Palettencode

Der Ink/Stitch Code ist die Information die in die SVG-Datei eingespeichert wird. Hierüber können alle Parameter des Tartanmusters direkt angepasst werden.

Ein Palettencode sieht beispielsweise so aus: `(#000000)/5.0 (#FFFFFF)/?5.0`. 

* Streifen sind durch Leerzeichen getrennt
* Jede Farbdefinition ist in runde Klammern eingeschlossen `(#000000)`
* Ein Schrägstrich (`/`) definiert das Muster als symmetrisch (gespiegelt), während drei Punkte (`...`) ein sich wiederholendes (asymmetrisches) Muster repräsentieren `...(#000000)5.0 (#FFFFFF)?5.0...`.
* Ein senkrechter Strich (`|`) trennt Kette von Schuss und wird nur dann eingesetzt wenn diese nicht gleich sind.

**Hinweis**: Das [Scottish Register of Tartans](https://www.tartanregister.gov.uk/) hatte eine große Sammlung and registrierten Tartan-Mustern. Ink/Stitch ist fähig den Code den man sich per Mail zuschicken lassen kann in Ink/Stitch Palettencode umzusetzen. Bitte beachtet dabei die entsprechenden Lizenz-Regulierungen. 

Das [Scottish Register of Tartans](https://www.tartanregister.gov.uk/) hat eine große Sammlung mit registrierten Tartanmustern. Ink/Stitch kann den dort ausgegebenen Code interpretieren und in den Ink/Stitch spezifischen Farbcode umwandeln. Wir bitten darum, die Lizenzbestimmungen zu beachten. Definiere die Breite eines Tartanfadens, bevor du auf „Code anwenden“ klickst.<br><br>Hier ist ein Beispiel zum Ausprobieren: `...B24 W4 B24 R2 K24 G24 W2...` ([Quelle](https://www.tartanregister.gov.uk/threadcount))
{: .notice--info}

### Stickeinstellungen

In den Stickeinstellungen kann festgelegt werden, ob das Tartanmuster als ein einziges Stickelement ausgegeben werden soll oder ob es in SVG-Elemente umgewandelt wird, die im Anschluss einzelnd bearbeitet werden können.

#### Füllstich-Element

Tartan als Stickelement führt zu einem einheitlichen Erscheinungsbild mit optimaler Stichplatzierung. Es können verschiedene Parameter eingestellt werden, die im Anschluss im Parameterdialog verfeinert werden können.

Die Parameter sind auf der Seite für die [Tartanfüllung](/de/docs/stitches/tartan-fill/) genauer beschrieben.

Der einzige Parameter der nur über dieses Menu eingestellt werden kann ist `Minimale Streifenbreite für Füllstich`. Streifen die schmaler sind als dieser Wert werden als Geradstich ausgegeben.

#### SVG Elemente

* Definiere die Stichart (veraltete Füllung oder Füllstich) und setzte die Parameter den persönlichen Vorlieben entsprechend. Streifen die schmaler sind als `Minimale Streifenbreite für Füllstich` werden als Geradstich ausgegeben. Die einzelnen Elemente können nach einem Klick auf `Anwenden` in Inkscape bearbeitet werden.

**Hinweis**: Für Füllstich-Elemente wird der Stickpfad nach dem Anwenden etwas optimiert und nicht so viele Sprungstiche enthalten wie in der Tartan-Simulation. Trotzdem können Anpassungen nötig sein.
{: .notice--info}

## Tutorials zu Füllwerkzeugen

{% include tutorials/tutorial_list key="werkzeug" value="Füllung" %}

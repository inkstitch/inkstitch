---
title: "Arbeitsablauf"
permalink: /docs/workflow/
excerpt: ""
last_modified_at: 2018-08-26
toc: true
---
## Schritt 1: Zeichnung oder ein Bild als Designvorlage

Wenn ein Design von einem vorhandenen Bild oder auf einer vorhandenen Grafik basiert, lade es in Inkscape in eine eigene Ebene. Einige Grafiken sind über die Inkscape-Funktion [Bitmap nachzeichnen](https://inkscape.org/en/doc/tutorials/tracing/tutorial-tracing.html) zugänglich, besonders wenn das Bild zuerst in einem Grafikeditor vereinfacht wurde (z. B. mit [GIMP](https://www.gimp.org/)).

**Tipp:** Wenn Linux verwendet wird und eine Linie vektorisieren müssen, kann man ein anderes Inkscape-Plugin verwenden, das [centerline tracing](https://github.com/fablabnbg/inkscape-centerline-trace). Für Stickereien kann es nur für einfache Formen genutzt werden.
{: .notice--info }

Eine Bereinigung der Vektorformen erreicht man mit `Pfad -> Vereinfachen` (`Strg + L`) danach lösche andere Knoten von Hand, wenn es möglich ist. Ziel ist es, so wenig Bezierkurven wie möglich zu verwenden, um das Bild darzustellen.

Wenn das Bild von Hand nachgezeichnet werden muss, verwende das Freihandlinien Werkzeug. Dieses Werkzeug erstellt Pfade mit vielen Bezierknoten, also vereinfache die Kurven so weit wie möglich.

**Tipp:** Durch eine schon vorhandene SVG-Datei, kann eine Menge Zeit gespart werden. Verwende daher die Google-Bildsuche mit dem Filter SVG.
{: .notice--info }

Wähle für einen **Text** die Schriftart sorgfältig aus. Es ist ziemlich schwer, Satinkolummnen gut aussehen zu lassen, wenn diese nur 1 mm breit oder dünner sind. Sans-Serif-Schriften sind in der Regel am einfachsten. Bei Texten, die kleiner als 4 mm sind, wird es sehr schwer, die Kleinbuchstaben gut aussehen zu lassen. Denke also an die Blockkappen. Kursive- oder Script-Schriftarten können gut funktionieren, aber es wird nicht so einfach sein, wie man denkt.

## Schritt 2: Plane den Stichpfad und die Farbwechsel

Ab diesem Punkt haben wir eine Vektorgrafik des Bildes. Als nächstes müssen die Vektoren in etwas konvertieren, die Ink/Stitch versteht und diese dann in eine richtige Reihenfolge bringen.

Wenn die benutzte Stickmaschine den Faden nicht in der Mitte näht oder die Farben automatisch wechseln kann, sollte der Stichpfad optimiert werden, um Sprungstiche zu reduzieren oder zu verbergen und mache nur minimale Farbwechsel. Versuche auch, Stiche über Sprungstiche zu vermeiden, wenn es möglich ist, weil es ein totaler Aufwand ist, sie später von Hand abzuschneiden.

Die Stichreihenfolge beeinflusst auch, wie der Stoff gezogen und geschoben wird. Jeder Stich verzerrt den Stoff, und deshalb muss dies berücksichtigt und entsprechend kompensiert werden. [Weitere Informationen](/tutorials/push-pull-compensation/)

## Schritt 3: Erstellung der Stickvektoren

Wir empfehlen an dieser Stelle verstärkt mit Ebenen und Gruppen zu arbeiten. Wenn ein Bild nachgezeichnet wurde, behalte es als unterste Ebene und stelle es über die Ebenen- oder Objektpalette als unsichtbar ein. Jede Ebene, Gruppe oder Vektorform, die als unsichtbar festgelegt wurde, wird von Ink/Stitch ignoriert.

Behalte die initial hinterlegten Vektoren in einer eigenen Ebene und verwende diese als Referenz beim Entwerfen von Stickvektoren. Kopiere und füge diese bei Bedarf in eine höhere Ebene ein und arbeite mit den Kopien.

Stelle die Parameter unter `Erweiterungen -> Ink/Stitch -> Parameter` ein. Weitere Informationen zu Sticharten und deren Anwendung findet man im Abschnitt [Parameter](/docs/params/) dieser Dokumentation. Jedes Mal, wenn Parameterwerte geändert werden, wird das simulierte Ergebnis in dem Vorschaufenster sichtbar. Wenn das Ergebnis zufriedenstellend ist, klicke auf "Anwenden und schließen", um die Werte in der SVG-Datei zu speichern.

Für eine detaillierte Ansicht des Ergebnisses wähle einen Vektorpfad und führe `Erweiterungen -> Ink/Stitch -> Sticken ...` aus, wodurch ein Stichplan nur für die ausgewählten Objekte angezeigt wird. Untersuche den resultierenden Stichplan mit dem Werkzeug Knoteneditor. Jeder Punkt ist ein einzelner Stich; Die Nadel dringt in das Gewebe ein und verriegelt sich an dieser Stelle mit dem Unterfaden. Nachdem der Stichplan geprüft wurde, mache den Stickvorgang rückgängig (`Strg + Z`), um den Stichplan zu verwerfen und die Vektoren wieder sichtbar zu machen.

An dieser Stelle speichere die SVG-Datei. Wenn Inkscape langsam wird (aufgrund eines Inkscape-Speicherlecks), starte es neu, bevor fortgefahren wird.

## Step 4: Reihenfolge

Sobald alle Vektoren erstellt und einzeln geprüft haben, ist es an der Zeit alles in die richtige Reihenfolge zu bringen. Hier kommt das Objektwerkzeug von Inkscape zum Einsatz. Optimiere die Reihenfolge, um Farbänderungen zu minimieren und Sprungstiche zu reduzieren oder diese zu verstecken.

In Ink/Stitch werden Objekte in genau der Reihenfolge zusammengefügt, in der sie in der SVG-Datei erscheinen, von der niedrigsten bis zur höchsten Stapelfolge. Wenn der Abstand zwischen zwei Objekten zu lang ist, fügt Ink/Stitch automatisch einen Sprungstich dazwischen ein. Es verwendet die Farbe des Objekts, um die Garnfarbe zu bestimmen, so dass Änderungen der Farbe von einem Objekt zum nächsten zu einem Farbwechsel führt, die der Stickdatei hinzugefügt wird.

**Tipp:** Inkscape bietet die Möglichkeit, Objekte in der Reihenfolge mit den Tasten BildHoch und BildRunter anzuheben und zu senken. Die neuen Funktionen "StackUp" und "StackDown" bieten eine bessere Kontrolle über diese Reihenfolge. Wir empfehlen daher, BildHoch und Bildrunter an diese Funtionen zu knüpfen. [Tastenkombinationen](/docs/customize/#Tastenkombinationen)
{: .notice--info }

** Info:** Die SVG-XML-Struktur kann auch manuell bearbeitet werden, indem der XML-Editor von Inkscape verwendet (`Strg + Umschalt + X`) wird. Die Schaltflächen "Raise" und "Lower" beeinflussen direkt die Reihenfolge der XML-Tags in der SVG-Datei und unterliegen nicht den gleichen Einschränkungen wie das ursprüngliche BildHoch und BildRunter. Beachte dabei, dass die Reihenfolge der XML-Tags im XML-Editor die _umgekehrte_ Reihenfolge der Objekte im Objektfenster ist.
{: .notice--info }

## Schritt 5: Ausgabeformat

Sobald alles in der richtigen Reihenfolge ist, deaktiviere alle Objekte und führe *Sticken ...* erneut aus. Dies stickt alle sichtbaren Objekte in der Datei. Wähle in den Erweiterungseinstellungen ein Dateiformat, das von der Stickmaschine unterstützt wird. Die meisten Maschinen unterstützen DST, und einige Brother-Maschinen bevorzugen PES.

*Sticken* erstellt eine Datei im angegebenen Ausgabeverzeichnis, die nach Ihrer SVG-Datei benannt ist, jedoch mit der Dateierweiterung `.DST`,` .PES` oder einem anderen gewählten Format. Es wird eine vorhandene Datei dort gespeichert und bis zu 5 alte Kopien jeder Datei erstellt.

## Schritt 6: Ausgabe

Es kann entweder eine Stickdatei für eine Auswahl von Objekten oder für alle Objekte erstellt werden. So wird eine Stickdatei für das gesamte Design erstellt:

* Klicke in einen leeren Bereich (um die Auswahl aufzuheben)
* Wähle `Erweiterungen -> Ink/Stitch -> Sticken ...`
* Wähle das richtige Dateiformat für die Maschine
* Gebe einen Verzeichnisnamen ein, in dem die Ausgabedateien gespeichern werden sollen. Z.B. `C:\Benutzer\%BENUTZERNAME%\Dokumente` unter Windows. Ink/Stitch wird sich an diese Information erinnern.

## Schritt 7: Sticktest

Es gibt immer Möglichkeiten für Verbesserungen! Um das Design zu testen, bereite ein Stück Teststoff vor, dass so genau wie möglich zu dem endgültigen Stoff passt. Verwende den gleichen Stabilisator und den gleichen Stoff wenn es möglich ist. Versuche für T-Shirts einen ähnlichen Stoff (normalerweise Knit) zu finden. Knit braucht viel Stabilisierung.

Nähe das Design und beobachte die Maschine um sicherzustellen, dass es keine Überraschungen gibt. Achte auf Lücken, die darauf hinweisen dass der Stoff verzerrt wurde. Beobachte auch Bereiche, in denen sich die Stiche zu sehr aufstauen und die Maschine Probleme damit hat, was darauf hinweist, dass die Stichdichte zu hoch ist.

## Step 8+: Optimierung

Optimiere das Design. Eventuell sind einige Versuche nötig, um das zu bekommen, wie es gewünscht wurde. Wenn es fertig ist, kopiere die endgültige Stickdatei aus dem Ausgabeverzeichnis, um zu verhindern, dass diese versehentlich zu einem andern Zeitpunkt überschrieben wird.

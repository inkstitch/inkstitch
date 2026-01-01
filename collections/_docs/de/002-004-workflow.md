---
title: "Arbeitsablauf"
permalink: /de/docs/workflow/
last_modified_at: 2025-03-13
toc: true
---
![Ink/Stitch workflow](/assets/images/docs/en/workflow-chart.svg)

## ![Create Icon](/assets/images/docs/workflow-icon-create.png) Schritt 1: Vektorgrafik erstellen

Zuerst brauchst du eine Idee oder ein Bild, dass du in eine Stickdatei umsetzen willst. Du kannst es mit dem Zeichenwerkzeug selbst erstellen oder ein bereits existierenden Bild nutzen.

### Mit Inkscape zeichnen

#### Pfade erstellen

Inkscape bietet verschiedene Werkzeuge zur Erstellung von Vektorgrafiken an.
Hier eine Auswahl an Werkzeugen, die du sehr viel einsetzen wirst:

* ![freehand lines icon](/assets/images/docs/inkscape-tools-freehand.png) Freihandlinie zeichnen (<key>P</key>)
* ![freehand lines icon](/assets/images/docs/inkscape-tools-bezier.png) Bezierkurven und gerade Linien zeichnen (<key>B</key>)

Mit anderen Werkzeugen können sehr schnell geometrische Grundelemente erstellt werden:

* ![square icon](/assets/images/docs/inkscape-tools-square.png) Recheck
* ![circle icon](/assets/images/docs/inkscape-tools-circle.png) Kreis
* ![polygon icon](/assets/images/docs/inkscape-tools-polygon.png) Sterne und Polygone
* ![spiral icon](/assets/images/docs/inkscape-tools-spiral.png) Spirale

#### Pfade bearbeiten

Bearbeite Objekte und Pfade mit:
* ![node tool icon](/assets/images/docs/inkscape-tools-select.png) Auswahlwerkzeug (<key>S</key>) and
* ![node tool icon](/assets/images/docs/inkscape-tools-node.png) Knoten bearbeiten (<key>N</key>)

Skalieren, rotierend und Objekte bewegen kann man mit dem Auswahlwerkzeug. Das Knotenwerkzeug dient zum manipulieren der Pfade eines Elements.

Zusätzlich gibt es eine Reihe an Pfadeffekten (`Pfad > Pfadeffekte...`) die ebenfalls nur Bearbeitung genutzt werden können.

### Eine existierende Grafik verwenden

Um dein Design an ein bereits existierendes Bild anzulehnen, muss es zunächst in Inkscape in eine eigene Ebene importiert werden. Einige Grafiken lassen sich sehr gut mit der [Inkscape Option](https://inkscape.org/de/doc/tutorials/tracing/tutorial-tracing.html) `Pfad > Bitmap nachzeichnen` in eine Vektorgrafik verwandeln. Das trifft besonders dann zu, wenn du die Grafik zuvor mit einem Grafikprogramm wie zum Beispiel [GIMP](https://www.gimp.org/) vereinfachst hast.  

Nach der Vektorisierung ist es oft notwendig, die Datei etwas aufzuräumen. Nutze zum Beispiel `Pfad > Vereinfachen`(`Strg+L`) oder lösche einige Knoten von Hand so weit wie möglich. Oft gibt es auch kleine Bildfragmente, die es sich lohnt zu entfernen. Nutze dafür z.B. die Funktion `Erweiterungen > Ink/Stitch > Troubleshoot > Cleanup document...`.

Manche Bilder sollten besser von Hand nachgezeichnet werden. Dazu kann man die Freihandlinien oder das Werkzeug für Bezierkurven verwenden. Freihandlinien erzeugen eine große Anzahl an Knotenpunkten, die anschließend mit Strg + L vereinfacht werden sollten.

**Tip:** Eine existierende Vektorgrafik zu benutzen, kann dir eine Menge Arbeit ersparen. Benutze dafür den SVG-Filter in deiner Suchmaschine oder https://openclipart.org/.
{: .notice--info }

### Text

Wähle für einen Text die Schriftart sorgfältig aus. Es ist ziemlich schwer, Satinkolummnen gut aussehen zu lassen, wenn diese nur 1 mm breit oder dünner sind. Sans-Serif-Schriften sind in der Regel am einfachsten. Bei Texten, die kleiner als 4 mm sind, wird es sehr schwer, die Kleinbuchstaben gut aussehen zu lassen. Denke also an die Blockkappen. Kursive- oder Script-Schriftarten können gut funktionieren, aber es wird nicht so einfach sein, wie man denkt.

Darüber hinaus bietet Ink/Stitch inzwischen fertige Schriftarten an. Sie können über `Erweiterungen > Ink/Stitch > Text` abgerufen werden.

## ![Vectorize](/assets/images/docs/workflow-icon-vectorize.png) Schritt 2: In Stickvektoren umwandeln & Parametrisieren

An diesem Punkt hast du bereits eine Vektorgrafik deines Bildes. Als nächstes müssen die Vektoren so angepasst werden, dass Ink/Stitch sie auch versteht.

### Objekte-Dialog

Wir empfehlen mit Ebenen und Gruppen zu arbeiten. Im Objekt-Dialog (`Objekte > Objekte...` oder `Strg + Umschalt + O`) kannst du Ebenen, Gruppen und Objekte verwalten.

Speichere dein Bild in einer duplizierten Ebene:

* Rechtsklick auf die Ebene (wenn du den Namen nicht verändert hast, heißt sie `Ebene 1`)
* Klicke auf `Duplizieren`
* Klicke auf das Auge, die Ebene wird unsichtbar und das Auge schließt sich

Jede Ebene, Gruppe und jedes Objekt das unsichtbar gemacht wurde, wird von Ink/Stitch ignoriert.
Wir arbeiten nun mit der duplizierten Ebene weiter.

![Objects panel](/assets/images/docs/en/objects-panel.png)

### Gruppen

Benutze Gruppen um deine Datei zu strukturieren.

* Markieren Objekte mit der Maus
* Füge Objekte hinzu oder entferne sie mit `Shift + Klick`
* Drücke `Strg + G` um sie zu gruppieren

Gruppierungen können mit `Strg + Umschalt + G` aufgehoben werden

### Sticharten

Ink/Stitch bietet verschiedene Sticharten an. Davon abhängend, welchen Stichtyp du verwenden willst, musst du Füllfarbe, Konturfarbe und Muster der Kontur verwenden. Die Einstellungen dafür befinden sich unter `Objekte > Füllung und Kontur...` (`Strg + Umschalt + F`).

Schau die in der untenstehenden Tabelle die einzelnen Sticharten an. Klicke auf die Links, um sie dir genauer anzuschauen und zu lernen, wie sie funktionieren.

Pfad Objekt | Stichart
---|---
(Gestrichelte) Linie |[Geradstich](/de/docs/stitches/running-stitch/), [Manueller Stich](/de/docs/stitches/manual-stitch/), [Zick-Zack-Stich](/de/docs/stitches/zigzag-stitch/), [Bohnen-Stich](/de/docs/stitches/bean-stitch/)
Zwei kombinierte Linien (mit optionalen Querstreben) oder eine einfache Linie mit einer Breite über 0.3 mm| [Satinsäule](/de/docs/stitches/satin-column), [E-Stitch](/de/docs/stitches/e-stitch)
Pfad mit Füllung | [Automatische Füllung](/de/docs/stitches/fill-stitch/), [Kurvenfüllung](/docs/stitches/guided-fill/),  [Konturfüllung](/docs/stitches/contour-fill/), [Mäanderfüllung](/docs/stitches/meander-fill/), [Spiralfüllung](/docs/stitches/circular-fill/), [cross stitch fill](/docs/stitches/cross-stitch/)
{: .equal-tables }

### Parametrisieren

Setze Stickparameter mit `Erweiterungen > Ink/Stitch > Parameter`. Du findest eine Beschreibung für jede Option unter [Parameter](/de/docs/params) auf dieser Webseite.
Jedes Mal, wenn du einen Wert änderst, erneuert sich die Stickvorschau. Wenn du mit dem Ergebnis zufrieden bist, klicke auf `Anwenden und schließen` um die Werte in die SVG-Datei zu speichern.

Speichere deine SVG-Datei regelmäßig.

## ![Create Icon](/assets/images/docs/workflow-icon-order.png) Schritt 3: Stichreihenfolge & Befehle

### Stickreihenfolge

Wenn du ein Stickdesign erstellst, ist es wichtig die Stickpfade zu optimieren. Du willst so wenig Sprungstiche wie möglich erzeugen und Farbwechsel mit sinnvoller Planung reduzieren. Sind einmal alle Vektoren erstellt, ist es jetzt Zeit die richtige Reihenfolge festzulegen. Hier ist das Objekt-Fenster (`Objekte > Objekte ...`) sehr nützlich. Hier kannst du Objekte, Gruppen und Ebenen in ihrer Position verschieben. Außerdem kannst du von der Ink/Stitch [Sortierfunktion](/de/docs/edit/#objekte-in-auswahlreihenfolge-sortieren) gebrauch machen.

Ink/Stitch wird die Objekte in genau der Reihenfolge sticken, in der sie im Dokument angelegt sind. Dabei wird stets das unterste Objekte zuerst gestickt und das oberste zuletzt. Ist der Abstand zum nächsten Objekt zu lamg, werden automatisch Sprungstiche eingefügt. Die Objektfarbe legt auch die Garnfarbe fest. Farbwechsel resultieren dementsprechend in einen Farbwechsel-Anweisung in der Stickdatei.

Die Stickreihenfolge wirkt sich außerdem auf Stoffverzerrungen aus. Jeder Stich schiebt oder drückt den Stoff. Deshalb muss schon im Design dieser Effekt entsprechend kompensiert werden. [Mehr Informationen](/de/tutorials/push-pull-compensation/)

**Tip:** Inkscape bietet die Möglichkeit, Objekte in der Reihenfolge mit den Tasten BildHoch und BildRunter anzuheben und zu senken. Die neuen Funktionen “StackUp” und “StackDown” bieten eine bessere Kontrolle über diese Reihenfolge. Wir empfehlen daher, BildHoch und Bildrunter an diese Funtionen zu knüpfen. [Tastenkombinationen](/de/docs/customize/#Tastenkombinationen)
{: .notice--info }

**Info:**  Die SVG-XML-Struktur kann auch manuell bearbeitet werden, indem der XML-Editor von Inkscape verwendet (Strg + Umschalt + X) wird. Die Schaltflächen “Raise” und “Lower” beeinflussen direkt die Reihenfolge der XML-Tags in der SVG-Datei und unterliegen nicht den gleichen Einschränkungen wie das ursprüngliche BildHoch und BildRunter. Beachte dabei, dass die Reihenfolge der XML-Tags im XML-Editor die umgekehrte Reihenfolge der Objekte im Objektfenster ist.
{: .notice--info }

### Befehle

[Befehle](/de/docs/commands/) können zur Pfadoptimierung beitragen. Du kannst Start- und Endpunkte festlegen, den Rahmen in eine bestimmte Position rücken oder Faden trennen, etc. 


## ![Create Icon](/assets/images/docs/workflow-icon-visualize.png) Schritt 4: Visualisierung

Ink/Stitch unterstützt drei Wege um sich ein Bild des entstehenden Designs zu machen:

* [Simulator](/de/docs/visualize/)
* [PDF Vorschau](/de/docs/print-pdf/)
* [Stichplan Vorschau](/de/docs/visualize/#stich-plan-vorschau) (Undo with <key>Ctrl</key><key>Z</key>)

## ![Create Icon](/assets/images/docs/workflow-icon-export.png) Schritt 5: Stickdatei speichern

Ist die Stickreihenfolge festgelegt, [exportiere](/de/docs/import-export/) dein Design über `Datei > Kopie speichern...` in das richtige Dateiformat für deine Stickmaschine. Die meisten Maschinen unterstützen DST, zusätzlich gibt es aber meistens noch ein weiteres Format. Brother Maschinen z.B. bevorzugen PES. Vergiss nicht die Datei auch im SVG-Format abzuspeichern. Sonst wird es später schwierig, das Motiv im Nachhinein weiter zu bearbeiten und kleine Details anzupassen.

## ![Create Icon](/assets/images/docs/workflow-icon-testsew.png) Schritt 7: Test-Sticken

Es gibt immer Raum für Verbesserung! Um dein Design zu testen, benutze am Besten ein Stück Stoff, dass dem Material so weit wie möglich ähnelt, für das du dein Motiv vorgesehen hast. Nutze auch das gleiche Stickvlies.

Beobachte deine Maschine, während sie stickt. Achte dabei auf Lücken zwischen den Objekten die auf Stoffverzerrungen hindeuten. Suche auch nach Stellen, an denen die Stiche zu eng sind und der Maschine Probleme bereiten.

## ![Create Icon](/assets/images/docs/workflow-icon-optimize.png) Schritt 8+: Optimieren

Gehe anschließend zurück an die Bearbeitung des Designs. Es kann mehrere Anläufe benötigen, bis alles glatt läuft. Aber die Mühe lohnt sich und du erreichst am Ende eine gute Qualität.

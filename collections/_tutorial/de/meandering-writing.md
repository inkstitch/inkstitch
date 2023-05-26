---
permalink: /de/tutorials/meandering-writing/
title: "Schrift mit Mäanderfüllung"
language: de
last_modified_at: 2023-04-26
excerpt: "Mit Mäanderfüllung schreiben"
image: "/assets/images/tutorials/tutorial-preview-images/meandering_writing.jpg"
tutorial-typ:
stichart:
  - "Mäanderfüllung Fill"
  - "Mehrfachgeradstich"
techniken:
schwierigkeitsgrad:
---
![Embroidery](/assets/images/tutorials/tutorial-preview-images/meandering_writing.jpg)

Dieses Tutorial ist **nicht** über das Textmodul von Ink/Stitch sondern nutzt installierte Systemschriften (.ttf oder .otf).
{: .notice--info }

Diese Methode sollte nicht für kleine Buchstaben genutzt werden. Die Buchstaben sollten eine Höhe von mindestens 4 oder 5 cm haben.
Dafür können aber sehr große Buchstaben erstellt werden, die sich schnell sticken lassen.
{: .notice--warning }

## Schrift erstellen

* Nutze das Text-Werkzeug von Inkscape um einen kurzen Text zu schreiben.
* Lege die gewünschte Schriftart fest.
  ![Font chosing](/assets/images/tutorials/meandering_writing/font-chosing.jpg)
* Passe evtl. die Schrift an deine Bedürfnisse an. Hier wurde die Schrift [Rubik ultrabold](htps://fonts.google.com/specimen/Rubik) verwendet.
  Die Höhe wurde bei gleichbleibender Breite etwas vergrößert.

## Schrift im positiven Raum

* Wähle den Schriftzug an und führe die Option `Pfad > Objekt in Pfad umwndeln` aus
* Im `Ebenen und Objekte`-Dialog befindet sich der Text nun als eine Gruppe mit mehreren Pfaden
* Wähle die Textgruppe aus und öffne die Ink/Stitch Parameter (`Erweiterungen > Ink/Stitch > Parameter`)
* Im Parameter-Dialog:
  * Deaktiviere die Unterlage für Füllstiche
  * Bevorzugst du Fadenschnitt-Befehle anstelle von Sprungstichen, aktiviere die Option `Fadenschnitt`.
  * Wähle als Füllmethode `Mäanderfüllung` und spiele mit den Parametereinstellungen, bis du dein favorisiertes Ergebnis erreichst
  * Es können auch einzelne Buchstaben angewählt werden, um die Mäander-Parameter individuell anzupassen.
    Manche Buchstaben sind schwieriger zu füllen als andere, eine individuelle Anpassung kann hier Abhilfe schaffen.
  * Die Mäanderfüllung beinhaltet ein Randomisier-Funktion. Um das Ergebnis zu Ändern, kann der Würfel ganz unten im Parameter-Dialog gewürfelt werden.
    Dies kann auch helfen unerwünschte Aussparungen in der Form zu verhindern.
    Auch die Größe des Mäander-Musters kann reduziert werden, sollte es Schwierigkeiten geben, die Form in Gänze auszufüllen.

    ![Params](/assets/images/tutorials/meandering_writing/meandering-parameter.jpg)

* Klicke auf `Anwenden und Schließen`. Die Schrift ist nun stickfähig.

## Schrift im negativen Raum

Mäanderfüllung ist eine gute Methode um auch größere Flächen schnell zu sticken, aber die Berechnung des Stickpfades kann einige Zeit in Anspruch nehmen.
Je größer der Stickbereich, desto länger lässt das Ergebnis auf sich warten. Es macht also Sinn, nicht mit zu großen Sitckflächen zu beginnen.

In unserem Beispiel für das Sticken im negativen Raum gibt es zwei Stickelemente. Ein Dreifachgeradestich um die Buchstaben herum und die Mäanderfüllung, die den Hintergrund füllt.

* Zeichne ein Rechteck (oder eine andere Form) um den Text. Lege die Füllfarbe fest. Die Form braucht keine Konturfarbe.
  Es ist erlaubt, die Deckkraft herunter zu setzen, dies ändert das Endergebnis nicht.
* Dupliziere den Text und wandle beide Kopien in einen Pfad um (`Pfad > Objekt in Pfad umwandeln`)

### Dreifachgeradstich

* Wähle eine der beiden Kopien des Textes an
* Entferne die Füllfarbe und setze eine Konturfarbe
* Öffne den Parameter-Dialog (`Erweiterungen > Ink/Stitch > Parameter`)
* Setze die entsprechenden Parameter für einen Mehrfachgeradstich
  ![Bean stitch Parameter](/assets/images/tutorials/meandering_writing/bean-parameter.jpg)
* Der Parameter-Simulator zeigt Sprungestiche innerhalb der Buchstaben an. Solltest du stattdessen Fadenschnitt-Befehlt bevorzugen, führe die Funktion `Pfad > Aufspalten`.
  Aktiviere anschließend in den Parametern die Option `Fadenschnitt`.

### Mäander im negativen Raum

Wähle die andere Kopie des Textes aus
* `Pfad > Kombinieren`
* Im `Ebenen und Objekte`-Dialog kann überprüft werden, ob der Text über dem Rechteck liegt.
  Wenn nötig kann die Reihenfolge hier angepasst werden.
* Wähle den Text als auch das Rechteck an
* `Pfad > Differenz`
* Wähle das resultierende Rechteck an und öffne den Parameter-Dialog
* Wähle als Füllmethode `Mäanderfüllung`
* `Anwenden und Schließen`.

Das Ergebnis kann jetzt gestickt werden.

## Die richtige Schrift wählen

Wähle eine breite, dicke Schrift. Vermeide Schriften mit schmalen Bereichen.

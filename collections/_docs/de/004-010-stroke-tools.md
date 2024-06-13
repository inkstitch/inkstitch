---
title: "Werkzeuge: Linie"
permalink: /de/docs/stroke-tools/
last_modified_at: 2024-06-13
toc: true
---
## Automatisch geführter Geradstich

Dieses Werkzeug **ersetzt** eine Auswahl von Geradstichen mit neuen Geradstichen in logischer Reihenfolge um so viele Sprungstiche wie möglich zu vermeiden.
Dabei werden Teilbereiche mit einem einfachen Geradstich unterlegt um weitere Sprungstiche zu unterbinden. Das Ergebnis erhält zuvor gesetzte Stickparameter wie beispielsweise Stichkänge, Anzahl der Wiederholungen, etc.

### Funktionsweise

- Wähle alle Geradstiche aus, die in einem möglichst zusammenhängenden Pfad gestickt werden sollen
- Führe die Funktion unter `Erweiterungen > Werkzeuge: Linie > Automatisch geführter Geradstich` aus
- Stelle die Optionen wie gewünscht ein und klicke auf `Anwenden`

Tipp: Standardmäßig wird die Stelle als Startpunkt ausgewählt, die am weitesten links liegt and der Punkt am rechten Rand ist der Enpunkt (auch, wenn sich diese Punkte nicht am Ende eines Pfades befinden). Dieses Verhalten kann durch die Befehle "Start-/Endposition für automatisch geführte Satinsäulen" angepasst werden.
{: .notice--info }

### Optionen

- Aktiviere **Knoten an Überschneidungen hinzufügen** um ein besseres Endergebnis zu erzielen. Deaktiviere diese Option nur, wenn bereits manuell Knoten an den Schnittpunkten der Linien hinzugefügt wurden.
- Aktiviere **Reihenfolge der Geradstiche beibehalten** wenn die ursprüngliche Reihenfolge beibehalten werden soll.
- Aktiviere **Schneide Faden bei Sprungstichen** um Fadenschnitt-Befehle zu den Objekten inzuzufügen auf die sonst ein Sprungstich folgen würde.


## Satin zu Geradstich

Satin zu Geradstich konvertiert eine Satinsäule in ihre Mittellinie. Das kann beispielsweise dann nützlich sein, wenn nach der Verkleinerung eines Designs ein Geradstich besser passen würde als eine Satinsäule - oder wenn eine Dickenanpassung einer Satinsäule vorgenommen werden soll und eine Verbreiterung über den Zugausgleich kein zufriedenstellendes Ergebnis liefert. Ist dies der Fall, dann konvertiere die Satinsäule mit diesem Toll in einen Geradstich, setze die Linienbreit über `Füllung und Kontur` und im Anschluss ["Linie zu Satinsäule"](/docs/satin-tools/#convert-line-to-satin)

![Satin to Stroke example](/assets/images/docs/en/satin_to_stroke.png)

### Funktionsweise

1. Wähle eine oder mehrere Satinsäulen aus, die in einen Geradstich umgewandelt werden sollen
2. Öffne `Erweiterungen > Ink/Stitch > Werkzeuge: Linie > Satin zu Linie...`
3. Wähle, ob die ursprünglichen Satinsäulen beibehalten oder gelöscht werden sollen
4. Klicke auf "Anwenden"

### Anwendung

1. Wähle eine oder mehrere Satinsäulen aus die in einen Geradstich umgewandelt werden sollen
2. Öffne die Erweiterung `Erweiterungen > Ink/Stitch > Werkzeuge: Linie > Satin zu Geradstich ...`
3. Wähle aus ob die Satinsäulen eralten bleiben oder ersetzt werden sollen
4. Klicke auf `Anwenden`


## Füllung zu Mittellinie

Füllstiche sind für Umrandungen selten gut geeignet - aber es ist eine Menge Arbeit die Umrandungen in eine Satinsäule oder in Geradstiche zu verwandeln. Dieses Werkzeug nimmt dir einen Teil der Arbeit ab.

Die Funktion ist vergleichbar mit der Inkscape Funktion unter `Pfad > Bitmap nachzeichen ...` mit dem Erkennungsmodus `Strichzeichnung vektorisieren (autotrace)` und weist kommt mit ähnlichen Schwierigkeiten einher. Die Unterschiede sind:

1. Dieses Werkzeug findet die Mittellinie nicht von Bilddateien sondern von gefüllten Vektorflächen.
2. Es gibt einen Schwellwert um kurze Linien zu entfernen. Dieser Wert sollte auf die ungefähre Linienbreite eingestellt werden.
3. Ink/Stitch bietet die Möglichkeit sogenannte Schnittlinien zu definieren. Das erfordert ein bisschen Übung, verbessert aber das Ergebnis um Längen. Die Schnittlinien müssen so angelegt sein, dass sie einen Teilbereich komplett abtrennen. Eine nur teilweise angeschnittene Füllfläche wird wieder zu einem Ganzen zusammengefügt und zeigt keinen Effekt. Das bedeutet auch, dass die Reihenfolge der Schnittlinien einen Effekt auf das Ergebnis haben kann.

![Fill to Stroke](/assets/images/docs/en/fill_to_stroke.png)

### Anwendung

*  (Optional) Zeichne Schnittlinien an Schnittpunkten. Schnittlinien sind einfache Bezier-Linien, ohne weitere Kennzeichnung. Normalerweise wird bei der Mittenberechnung an Schnittstellen eine kleine Delle entstehen. Wird die Ursprungsform aber von einer Schnittlinie unterteilt, kann diese Delle vermieden werden. Bitte beim Erstellen darauf achten, dass immer ein ganzer Teilbereich der Füllfäche abgetrennt werden muss. Dabei spielt auch die Reihenfolge der Schnittlinien ggf. eine Rolle.
* Wähle ein oder mehrere Füllobjekte die in ihre Mittellinie umgewandelt werden sollen zusammen mit ihren Schnittlinien aus.
* Öffne `Erweiterungen > Ink/Stitch > Werkzeuge: Linie > Füllung zu Mittellinie`
* Setze die gewünschten Optionen (siehe unten) und klicke auf `Anwenden`
* Nutze das Knotenwerkzeug um ggf. Stellen nachzukorrigieren

### Optionen

* Original behalten: aktiviere diese Option, wenn die originalen Pfade nicht entfernt werden sollen.
* Grenzwert für Sackgassen (mm): Entfernt kurze Linien. In den meisten Fällen ist hier der Wert der ungefähren Linienbreite des Originals in Milimetern einzutragen.
* Gestrichelte Linie: aktiviere diese Option, wenn das Endergebnis ein Geradstich werden soll (sonst: Zick zack oder Weiterverarbeitung zu Satin)
* Linienbreite (mm): wird eine Weiterverarbeitung zu Satinsäulen angestrebt, kann hier direkt die Linienbreite angegeben werden. In den meisten Fällen ist aber eine Überprüfung des Ergebnisses notwendig, dafür diesen Wert klein halten.
* Schnittlinien: Lücken schließen: Bei der Nutzung von Schnittlinien entstehen an der Stelle des Schnitts Lücken, die durch diese Option geschlossen werden können. Diese Option nur anwählen, wenn keine Weiterverarbeitung in Satinsäulen geplant ist.


## Sprungstich zu Geradstich

Dieses Werkzeug erstellt Geradstiche von der Endposition des ersten Elements zu der Startposition des zweiten. Leite den hier generierten Geradstich versteckt unter später folgenden Stickflächen entlang und vermeide so unnötige Sprungstiche.

### Anwendung

* Wähle zwei oder mehr Objekte aus
* Öffne `Erweiterungen > Ink/Stitch > Werkzeuge: Linie > Sprungstich zu Geradstich`

### Optionen

{% include upcoming_release.html %}

* Konvertiere nur Sprungstitch die länger sind als der angegebene Wert
* Konvertiere nur Sprungstitche die kürzer sind als der angegebene Wert
* Verbinde nur Elemente innerhalb einer Gruppe oder einer Ebene
* Verbinde Elemente mit Fadenschnittbefehl, Stopp-Befehl oder erzwungenen Vernähstichen nicht mit nachfolgenden Elementen

#### Ausgabe-Einstellungen

* Aufeinstanderfolgende Pfade vom gleichen Typ verschmelzen
* Unterpfade verschmelzen

Verschmolzene Pfade übernehmen die Stickeinstellungen des Urpsrungselements.
Für nicht verschmolzene Pfade gelten die folgenden Einstellungen:
* (Maximale) Stitchlänge
* Geradstichtoleranz


## Redwork

{% include upcoming_release.html %}

Redwork ist eine alte Stickkunst bei der jede Linie genau zweimal gestickt wird.

Dieses Werkzeug **ersetzt** eine Auswahl von Geradstichen mit neuen Geradstichen in logischer Reihenfolge.
Der Hauptunterschied zum `Automatisch geführtem Laufstich` ist, dass jede Linie genau zweimal gestickt wird.

### Funktionsweise

* Wähle die Geradstiche an die geführt werden sollen
* Öffne `Erweiterungen > Ink/Stitch > Werkzeuge: Linie > Redwork`
* Passe die Optionen nach Wunsch an und klicke auf `Anwenden`

### Optionen

* Verbinde Linien deren Abstand geringer ist als (mm)

  Das Redwork Werkzeug kann mehrere nicht verbundene Gruppen gleichzeitig behandeln.
  Auf der anderen Seite ist es in der Regel der Fall, dass Linien nicht genau aufeinander eingerastet sind und kleine Lücken zwischen ihnen bestehen.
  Mit dieser Option kannst du definieren, bis zu welcher Distanz diese Lücken überbrückt werden sollen.
  Linien mit einem größeren Abstand werden als unverbunden betrachtet.
  Unverbundene Gruppen haben Sprungstiche.
* Minimale Pfadlänge (mm)

  Entfernt kurze Pfade aus dem Ergebnis.
  Kurze Pfade können ein Ergebnis der automatischen Führung sein. Sie entstehen z.B. dann, wenn zwei Pfade sich minimal überschneiden.
  Pfade die kürzer sind als die definierte [minimale Sprungstichlänge](/de/docs/preferences/#minimale-länge-für-sprungstiche-mm) können üblicherweise problemlos gelöscht werden.
  Folgen mehrere kurze Pfade aufeinander, sollte der Wert aber verringert werden.
* Redwork Stichlänge(mm)

  Setzt die Stichlänge für alle Pfade auf diesen Wert
* Redwork Mehrfach-Geradstitch Anzahl der Wiederholungen

  Wendet den Wert für [Mehrfach-Geradstitch Anzahl der Wiederholungen](/de/docs/stitches/bean-stitch/) auf die Deckstiche an (nicht auf die Unterpfade).

### Anfangs- und Endposition

Redwork wird immer an der gleichen Stelle beginnen und enden. Dieser Punkt mit einem [Startbefehl für automatisch geführte Geradstiche](/de/docs/commands/#--start--und-endposition-für-automatisch-geführten-laufstich) festgelegt werden.


## Außenkontur

{% include upcoming_release.html %}

Diese Erweiterung hilft die Originalform aus einer Stickdatei wiederherzustellen.

![Stitchpath to outline](/assets/images/docs/outline.png)

### Funktionsweise

* Wähle ein oder mehrere Objekte
* Öffne `Erweiterungen > Ink/Stitch > Werkzeuge: Linie > Außenkontur`
* Aktiviere die Vorschau um das Ergebnis auf der Bildfläche zu sehen
* Passe die Parameter an, bis das Ergebnis zufriedenstellend ist
* Klicke auf `Andwenden`

## Tutorials zu Linien-Werkzeugen

{% include tutorials/tutorial_list key="werkzeug" value="Linie" %}

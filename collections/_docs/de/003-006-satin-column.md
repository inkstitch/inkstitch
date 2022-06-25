---
title: "Satinsäule"
permalink: /de/docs/stitches/satin-column/
excerpt: ""
last_modified_at: 2021-10-23
toc: true
---
## Beschreibung

Satinsäulen werden meistens für Ränder, Buchstaben oder sehr kleine Füllbereiche verwendet.

![Stitch Types - Satin Column](/assets/images/docs/stitch-type-satincolumn.jpg)

## Funktionsweise

* Füge einem Pfadobjekt eine Kontur hinzu (ohne Füllung).
* Stelle die Konturenbreite auf die Größe ein, die der Satinstich haben soll.
* Starte `Erweiterungen > Ink/Stitch > Satin Werkzeuge > Konvertierung Linie zu Satinstich`
* Optional kann auch noch die Funktion `Erweiterungen > Ink/Stitch > Satin Werkzeuge > Automatisch geführte Satinsäulen` ausgeführt werden
* Anschließend können auf Wunsch Sprossen und Holme angepasst werden

## Manuelles Erstellen von Satinsäulen
Eine Satinsäule wird aus zwei **meist parallel verlaufenden Linien** gebildet. Ink/Stitch zeichnet ein Zick-Zack Muster zwischen den beiden Linien hin und her. Die Breite der Säule kann beliebig variiert werden.

* Kombiniere zwei Linien mit `Pfad > Kombinieren` oder benutze `Strg + K`.
* [Überprüfe die Pfad-Richtungen](/docs/customize/#enabling-path-outlines--direction). Damit die Satinsäule erzeugt werden kann, müssen sie gleich sein.<br />Wenn dies nicht der Fall ist, wähle mit dem *Knoten-Werkzeug* (`N`) einen Punkt eines Unterpfads und führe ein `Pfad -> Richtung umkehren` durch. Dadurch wird nur der ausgewählte Unterpfad umgekehrt.
* Benutze die Knoten- oder die Sprossenmethode wie unten beschrieben.
* Wähle dann die Satinsäule und führe `Erweiterungen > Ink/Stitch > Paramter`, oder eine [Benutzerdefinierte Tastenkombination](/docs/customize/) aus.

### Die Knoten Methode
[![Satinsäule Boat](/assets/images/docs/satin-column.jpg){: width="200x"}](/assets/images/docs/satin-column.svg){: title="Download SVG-Datei" .align-left download="satin-column.svg" }

Abhängig von der Komplexität des Entwurfs kann diese Methode zeitaufwendig sein, da die beiden Pfade die **gleiche Anzahl an Knoten** aufweisen müssen. Dies bedeutet, dass jeder Pfad aus einer gleichen Anzahl von Bezierkurven bestehen muss. Jedes Knotenpaar fungiert als "Kontrollpunkt": Ink/Stich sorgt dafür, dass ein "Zacken" von einem Punkt zum anderen führt.

### Die Sprossen Methode

Die Sprossenmethode gibt mehr Kontrolle darüber, wie die Satinsäule erstellt wird. Eine gute Positionierung der Punkte auf jeder der beiden Linien hilft, die Stichrichtungen festzulegen. Es gibt jedoch Situationen, in denen Richtungslinien ("Sprossen") für Satinsäulen hinzugefügt werden müssen:

* Einige knifflige Eckareale
* Komplizierte Zeichnungen, bei denen das Positionieren von den Knoten schwierig und zeitaufwendig ist
* Spezielle Situationen, in denen die Stichrichtungen auf ausgefallene Weise gestaltet werden sollen

**Manuelles Hinzufügen von Sprossen**
* Stelle sicher, dass der vorhandene Satinpfad (mit den zwei Unterpfaden) mit dem Knoten-Werkzeug ausgewählt ist.
* Drücke `P` oder wähle das Freihandlinien-Werkzeug.
* Halte die Umschalttaste gedrückt.
* Klicke einmal für den Anfang der Sprosse.
* Klicke ein zweites Mal für das Ende der Sprosse.


[![Rungs in Action](https://edutechwiki.unige.ch/mediawiki/images/thumb/6/68/InkStitch-round-bird-2.png/300px-InkStitch-round-bird-2.png)](https://edutechwiki.unige.ch/mediawiki/images/6/68/InkStitch-round-bird-2.png)

Original Design von [Liv Iko](https://thenounproject.com/liv_iko/collection/birds/?i=898697) bearbeitet von [EDUTECH Wiki](https://edutechwiki.unige.ch/en/InkStitch)
{: style="font-size: 0.5rem;"}

**Info:** Wir empfehlen dringend mindestens drei "Sprossen" zu nutzen.
Wenn du genau zwei Sprossen (und zwei Holme) nutzt, ist es schwer für Ink/Stitch zu entscheiden, was Sprosse und was Holm ist.
{: .notice--warning }

## Parameter

Der Dialog `Erweiterungen > Ink/Stitch  > Parameter` gibt dir die Möglichkeit die Satinsäule genau zu justieren und entsprechende Unterlagen zu aktivieren.

Mehr Details gibt es unter [Parameter (Satinsäule)](/de/docs/params/#satinsäule).

Empfehlenswert ist auch [dieser Artikel (englisch)](https://www.mrxstitch.com/underlay/) der sich ausführlich mit dem Thema Satinsäule und Unterlagen befasst.

## Satin Werkzeuge

Für Satinsäulen stellt Ink/Stitch einige hilfreiche [Werkzeuge](/de/docs/satin-tools/) bereit, die dir das Arbeiten mit Satinsäulen erheblich erleichtern können.

## Beispieldateien, die Satinsäulen enthalten
{% include tutorials/tutorial_list key="stichart" value="Satinstich" %}

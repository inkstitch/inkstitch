---
title: "Satin Column"
permalink: /de/docs/stitches/satin-column/
excerpt: ""
last_modified_at: 2018-10-11
toc: true
---
## Beschreibung

![Stitch Types - Satin Column](/assets/images/docs/stitch-type-satincolumn.jpg)

## Funktionsweise
Eine Satinkolumne wird aus zwei **meist parallel verlaufenden Linien** gebildet. Ink/Stitch zeichnet ein Zick-Zack Muster zwischen den beiden Linien hin und her. Die Breite der Kolumne kann beliebig variiert werden.

* Kombiniere zwei Linien mit `Pfad > Kombinieren` oder benutze `Strg + K`.
* [Überprüfe die Pfad-Richtungen](/docs/customize/#enabling-path-outlines--direction). Damit die Satinkolumne erzeugt werden kann, müssen sie gleich sein.<br />Wenn dies nicht der Fall ist, wähle mit dem *Node Editor Tool* (`N`) einen Punkt eines Unterpfads und führe ein `Pfad -> Richtung umkehren` durch. Dadurch wird nur der ausgewählte Unterpfad umgekehrt.
* Benutze die Knoten- oder die Sprossenmethode wie unten beschrieben.
* Wähle dann die Satinkolumne und führe `Erweiterungen > Ink/Stitch > Paramter`, oder eine [Benutzerdefinierte Tastenkombination](/docs/customize/) aus.

## Die Knoten Methode
[![Satinkolumne Boat](/assets/images/docs/satin-column.jpg){: width="200x"}](/assets/images/docs/satin-column.svg){: title="Download SVG-Datei" .align-left download="satin-column.svg" }

Abhängig von der Komplexität des Entwurfs kann diese Methode zeitaufwendig sein, da die beiden Pfade die **gleiche Anzahl an Knoten** aufweisen müssen. Dies bedeutet, dass jeder Pfad aus einer gleichen Anzahl von Bezierkurven bestehen muss. Jedes Knotenpaar fungiert als "Kontrollpunkt": Ink/Stich sorgt dafür, dass ein "Zacken" von einem Punkt zum anderen führt.

## Die Sprossen Methode

Die Sprossenmethode gibt mehr Kontrolle darüber, wie die Satinkolumne erstellt wird. Eine gute Positionierung der Punkte auf jeder der beiden Linien hilft, die Stichrichtungen richtig zu machen. Es gibt jedoch Situationen, in denen Richtungslinien ("Sprossen") für Satinkolumnen hinzugefügt werden müssen:

* Einige knifflige Eckareale
* Komplizierte Zeichnungen, bei denen das positionieren von den Knoten schwierig und zeitaufwendig ist
* Spezielle Situationen, in denen die Stichrichtungen ausgefallen aussehen sollen

**Automatisch generierte Satinkolumne**
* Füge einem Pfadobjekt eine Kontur hinzu (ohne Füllung).
* Stelle die Konturenbreite auf die Größe ein, die der Satinstich haben soll.
* Der Pfad sollte sich nicht selbst überschneiden. Versuche bei Bedarf diesen Pfad in mehrere Pfade aufzuteilen. (Diese Regel könnte sich in zukünftigen Versionen von Ink/Stitch ändern.)
* Starte `Erweiterungen -> Ink/Stitch -> Konvertierung Linie zu Satinstich`
* Verwende diese wie vorhanden oder passe die Sprossen oder Bahnen an

**Manuelles Hinzufügen von Sprossen**
* Stelle sicher, dass der vorhandene Satinpfad (mit den zwei Unterpfaden) mit dem Node-Editor-Werkzeug ausgewählt ist.
* Drücke `P` oder wähle das Freihandlinien-Werkzeug.
* Halte die Umschalttaste gedrückt.
* Klicke einmal für den Anfang der Sprosse.
* Klicke ein zweites Mal für das Ende der Sprosse.


[![Rungs in Action](https://edutechwiki.unige.ch/mediawiki/images/thumb/6/68/InkStitch-round-bird-2.png/300px-InkStitch-round-bird-2.png)](https://edutechwiki.unige.ch/mediawiki/images/6/68/InkStitch-round-bird-2.png)

Original Design von [Liv Iko](https://thenounproject.com/liv_iko/collection/birds/?i=898697) bearbeitet von [EDUTECH Wiki](https://edutechwiki.unige.ch/en/InkStitch)
{: style="font-size: 0.5rem;"}

**Info:** Die Sprossen müssen weiter sein als die Satinkolumne selbst. Andernfalls wechselt Ink/Stitch die Richtung oder es erscheint folgende Meldung: `error: satin column: One or more of the rungs doesn't intersect both rails.  Each rail should intersect both rungs once.`
{: .notice--warning }

## Parameter

Der Dialog `Erweiterungen > Ink/Stitch  > Parameter` gibt dir die Möglichkeit die Satinkolumne genau zu justieren und entsprechende Unterlagen zu aktivieren.

Mehr Details gibt es unter [Parameter (Satinkolumne)](/de/docs/params/#satinkolumne).

Empfehlenswert ist auch [dieser Artikel (englisch)](https://www.mrxstitch.com/underlay/) der sich ausführlich mit dem Thema Satinkolumne und Unterlagen befasst.

## Satin Werkzeuge

Für Satinkolumnen stellt Ink/Stitch einige hilfreiche [Werkzeuge](/de/docs/satin-tools/) bereit, die dir das Arbeiten mit Satinkolumnen erheblich erleichtern können.

## Beispieldateien, die Satinkolumnen enthalten
{% include tutorials/tutorial_list key="stitch-type" value="Satin Stitch" %}

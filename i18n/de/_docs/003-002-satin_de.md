---
title: "Satinkolumne"
permalink: /docs/stitches/satin/
excerpt: ""
last_modified_at: 2018-08-26
toc: true
---
Definiere eine Satinkolumne mit einer Form aus **zwei meist parallel laufenden Linien**. Ink/Stitch wird ein Zick-Zack Muster zwischen den beiden Linien hin und her zeichnen. Die Dicke der Kolumne kann beliebig variiert werden.

![Stichtypen - Satinkolumne](/assets/images/docs/stitch-type-satincolumn.jpg)

* Kombiniere zwei Linien mit `Pfad -> Kombinieren` oder benutze `Strg + K`.
* [Check path directions](/docs/customize/#enabling-path-outlines--direction). Damit die Satinkolumne erzeugt werden kann, müssen sie gleich sein.<br />Wenn dies nicht der Fall ist, wähle mit dem *Node Editor Tool* (`N`) einen Punkt eines Unterpfads und führe ein `Pfad -> Richtung umkehren` durch. Dadurch wird nur der ausgewählte Unterpfad umgekehrt.
* Benutze die Knoten- oder die Sprossenmethode wie unten beschrieben.
* Wähle dann die Satinkolumne und führe `Erweiterungen -> Ink/Stitch -> Paramter`, oder eine [Benutzerdefinierte Tastenkombination](/docs/customize/) aus.

## Die Knoten Methode
[![Satinkolumne Boat](/assets/images/docs/satin-column.jpg){: width="200x"}](/assets/images/docs/satin-column.svg){: title="Download SVG-Datei" .align-left download="satin-column.svg" }

Abhängig von der Komplexität des Entwurfs kann diese Methode zeitaufwendig sein, da die beiden Pfade die **gleiche Anzahl an Knoten** aufweisen müssen. Dies bedeutet, dass jeder Pfad aus einer gleichen Anzahl von Bezierkurven bestehen muss. Jedes Knotenpaar fungiert als "Kontrollpunkt": Ink/Stich sorgt dafür, dass ein "Zacken" von einem Punkt zum anderen führt.

## Die Sprossen Methode

Die Sprossenmethode gibt mehr Kontrolle darüber, wie die Satinkolumne erstellt wird. Eine gute Positionierung der Punkte auf jeder der beiden Linien hilft, die Stichrichtungen richtig zu machen. Es gibt jedoch Situationen, in denen Richtungslinien ("Sprossen") für Satinkolumnen hinzugefügt werden müssen:

* Einige knifflige Eckareale
* Komplizierte Zeichnungen, bei denen das positionieren von den Knoten schwierig und zeitaufwendig ist
* Spezielle Situationen, in denen die Stichrichtungen ausgefallen aussehen sollen

**Schnelles Hinzufügen von Sprossen**
* Füge einem Pfadobjekt eine Kontur hinzu (ohne Füllung).
* Stelle die Konturenbreite auf die Größe ein, die der Satinstich haben soll.
* Der Pfad sollte sich nicht selbst überschneiden. Versuche bei Bedarf diesen Pfad in mehrere Pfade aufzuteilen. (Diese Regel könnte sich in zukünftigen Versionen von Ink/Stitch ändern.)
* Starte `Erweiterungen -> Ink/Stitch -> Konvertierung Linie zu Satinstich`
* Verwende diese wie vorhanden oder passe die Sprossen oder Bahnen an

** Manuelles Hinzufügen von Sprossen **
* Stelle sicher, dass der vorhandene Satinpfade (mit den zwei Unterpfaden) mit dem Node-Editor-Werkzeug ausgewählt ist.
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

![Parameter Satinkolumne.jpg](/assets/images/docs/params-satincolumn.jpg)

Einstellung|Beschreibung
---|---
Benutzerdefinierte Satinkolumne | Damit diese Einstellungen wirksam werden muss es aktiviert sein.
"E" Stich                       | Aktiviert "E" Stich anstelle von Satin. Vergiss nicht, den Zick-Zack-Abstand bei dieser Stichart zu vergrößern.
Zugkompensation                 | Satinstiche [pull the fabric together](/tutorials/push-pull-compensation/), was zu einer Kolumne führt, die schmaler ist als in Inkscape. Diese Einstellung erweitert jedes Nadeleinstichpaar von der Mitte der Satinkolumne nach außen. Es muss experimentell bestimmt werden, wie viel Kompensation für Ihre Kombination aus Stoff, Faden und Stabilisator benötigt wird.
Zick-Zack Abstand               | Spitze-zu-Spitze Abstand zwischen Zick-Zacks.
STOP (danach), TRIM (danach)    |[STOP after](/docs/params/#stop-after), [TRIM after](/docs/params/#trim-after)

**Info:** Ink/Stitch berücksichtigt jedes Paar von Bezierkurven einzeln. Es wählt den längsten der beiden aus und bestimmt, wie viele Zickzacks erforderlich sind, um die Einstellung *Zick-Zack-Abstand* zu erfüllen. Dies macht es so, dass die Außenseite einer Kurve niemals spärliche Nähte wie bei einfachem Satin haben wird.<br />Dies bedeutet jedoch, dass die Inneseite einer Kurve eine höhere Stichdichte aufweist, als angegeben wurde. Vorsicht ist bei scharfen Kurven geboten, denn *Sticken mit einer zu hohen Dichte von Einstichen, kann ein Loch in dem Stoff verursachen*!
{: .notice--info }

## Underlage
Satinkolumne unterstützt auch drei Arten von Unterlagen, von denen alle gleichzeitig benutzt verwenden können. Lese [diesen Artikel](https://www.mrxstitch.com/underlay/) zum Satinkolumnen Design.

### Mittellinien Unterlage
Dies ist eine Reihe von Laufstichen in der Mitte der Kolumne und zurück. Das kann alles sein, was für dünne Satinkolumnen benötigt wird. Es kann auch als Grundlage für komplexere Unterlagen verwendet werden.

### Konturunterlage
Dies ist eine Reihe von Laufstichen die auf einer Seite der Kolumne hoch und auf der anderen Seite wieder runter laufen. Die Reihen werden vom Rand aus der Kolumne von dem angegebenen wert bestimmt. Dies eignet sich für kleine bis mittlere Satinkolumnen.

### Zick-Zack Unterlage
Dies ist im Wesentlichen ein Satinstich mit geringerer Dichte, der an das Ende der Kolumne und zurück an den Anfang genäht wird. Wird eine Konturunterlage hinzugefügt, erhält man, wie im oben verlinkten Artikel erwähnt, die "Deutsche Unterlage". Für breite Kolumnen oder anspruchsvolle Stoffe können alle drei Unterlagentypen zusammen verwendet werden.

## Sample inklusive einer Satinkolumne
{% include tutorial_list key="stitch-type" value="Satin Stitch" %}


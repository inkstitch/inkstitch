---
title: "Satinsäule"
permalink: /de/docs/stitches/satin-column/
last_modified_at: 2024-03-13
toc: true
---
## Beschreibung

Satinsäulen werden meistens für Ränder, Buchstaben oder sehr kleine Füllbereiche verwendet.

![Stitch Types - Satin Column](/assets/images/docs/stitch-type-satincolumn.jpg)

## Funktionsweise

Ink/Stitch bietet verschiedene Möglichkeiten Satinsäulen zu erstellen. Die Methoden 1-3 konvertieren in das manuelle Setup von wo aus weitere Modifizierungen möglich sind.

![Methods](/assets/images/docs/satin_methods.svg)

1. [Linie zu Satin](#1-linie-zu-satin): für Satinsäule mit einheitlicher Breite
2. [Linie zu Pfadeffekt-Satin](#2-linie-zu-pfadeffekt-satin): leicht modifizierbare Satinsäule mit optionalem Muster
3. [Zickzack-Linie zu Satin](#3-zickzack-linie-zu-satin): für die einfache Erstellung mit Grafiktablets oder Touchscreens
4. [Manuelle Satinsäule](#4-manuelle-satinsäule): volle Kontrolle über jeden Teil der Satinsäule

### 1. Linie zu Satin

* Erstelle einen Pfad mit einer Kontur (keine Füllung)
* Lege die Breite der Kontur so fest, dass sie der Breite der zukünftigen Satinsäule entspricht
* Führe die Funktion unter `Erweiterungen > Ink/Stitch Werkzeuge: Satin > Linie zu Satinsäule` aus
* Optional kann anschließend die Funktion `Erweiterungen > Ink/Stitch > Werkzeuge: Satin > Automatisch geführter Satinstich...` auf mehrere Satinsäulen angewendet werden, um die Stickreihenfolge zu optimieren
* Die nun erstellte Satinsäule kann nun genutzt oder nach Belieben modifiziert werden

Mehr Informationen über [Linie zu Satin](/de/docs/satin-tools/#linie-zu-satin)

### 2. Linie zu Pfadeffekt-Satin

Diese Erweiterung dient dazu schnell und einfach eine Satinsäule mit gemusterter oder einheitlicher Kante zu erstellen.

Die Funktion "Automatisch geführter Satinstich" wendet den Pfadeffekt an, was eine nachträglihe Bearbeitung erschwert.

Um einen Pfadeffekt-Satin in eine normale Satinsäule umzuwandeln, nutze die Funktion `Pfad > Objekt in Pfad umwandeln`.

Mehr Informationen über [Pfadeffekt-Satins](/de/docs/satin-tools/#linie-zu-pfadeffekt-satin)

### 3. Zickzack-Linie zu Satin

Diese Methode zur Erstellung von Satinsäulen ist besonders für Grafik-Tablets oder Touch-Screens interessant.

Mehr Informationen über [Zickzack-Linie zu Satin](/de/docs/satin-tools/#zickzack-line-zu-satin)

### 4. Manuelle Satinsäule

Eine Satinsäule wird aus zwei **meist parallel verlaufenden Linien** gebildet. Ink/Stitch zeichnet ein Zick-Zack Muster zwischen den beiden Linien hin und her. Die Breite der Säule kann beliebig variiert werden.

* Kombiniere zwei Linien mit `Pfad > Kombinieren` oder benutze `Strg + K`.
* [Überprüfe die Pfad-Richtungen](/docs/customize/#enabling-path-outlines--direction). Damit die Satinsäule erzeugt werden kann, müssen sie gleich sein.<br />Wenn dies nicht der Fall ist, wähle mit dem *Knoten-Werkzeug* (`N`) einen Punkt eines Unterpfads und führe ein `Pfad -> Richtung umkehren` durch. Dadurch wird nur der ausgewählte Unterpfad umgekehrt.
* Benutze die Knoten- oder die Sprossenmethode wie unten beschrieben.
* Wähle dann die Satinsäule und führe `Erweiterungen > Ink/Stitch > Paramter`, oder eine [Benutzerdefinierte Tastenkombination](/docs/customize/) aus.

#### Die Knoten Methode

[![Satinsäule Boat](/assets/images/docs/satin-column.jpg){: width="200x"}](/assets/images/docs/satin-column.svg){: title="Download SVG-Datei" .align-left download="satin-column.svg" }

Abhängig von der Komplexität des Entwurfs kann diese Methode zeitaufwendig sein, da die beiden Pfade die **gleiche Anzahl an Knoten** aufweisen müssen. Dies bedeutet, dass jeder Pfad aus einer gleichen Anzahl von Bezierkurven bestehen muss. Jedes Knotenpaar fungiert als "Kontrollpunkt": Ink/Stich sorgt dafür, dass ein "Zacken" von einem Punkt zum anderen führt.

#### Die Sprossen Methode

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

Satinsäule unterstützt auch drei Arten von Unterlagen, die einzeln oder aber auch alle gleichzeitig benutzt verwenden können.

Empfehlenswert ist auch [dieser Artikel (englisch)](https://www.mrxstitch.com/underlay/) der sich ausführlich mit dem Thema Satinsäule und Unterlagen befasst.

Einige dieser Einstellungen sind Teil einer zukünftigen Version von Ink/Stitch und noch nicht in der derzeitigen Version enthalten.
{: .notive--info }

### Satinsäule

Einstellung||Beschreibung
---|---|---
Benutzerdefinierte Satinsäule       | ☑ |Muss aktiviert sein, damit diese Einstellungen wirksam werden.
Methode                             | |`Satinsäule` auswählen
Maximale Stichlänge                 | ![Maximum stitch length](/assets/images/docs/params-satin-maximum_stitch_length.png) | Stiche die diesen Wert übersteigen, werden geteilt.
Kurzstich-Einzug                    | ![Short Stitch example](/assets/images/docs/params-satin-short_stitch_inset.png) | Stiche in Bereichen mit hoher Dichte werden um diesen Wert verkürzt (%)
Kurzstich-Dichte                    |![Short Stitch example](/assets/images/docs/params-satin-short_stitch_distance.png)  | Verkürzt Stiche falls der Abstand zwischen den Stichen schmaler als dieser Wert ist (mm).
Zick-Zack Abstand (Spitze zu Spitze)|![Zig-zag spacing example](/assets/images/docs/params-satin-zig-zag-spacing.png)|Spitze-zu-Spitze Abstand zwischen Zick-Zacks
Zugausgleich (%)                    |![Pull compensation example](/assets/images/docs/params-satin-pull_compensation.png)|Zusätzliche Zugkompensation, die als Prozentwert der ursprünglichen Breite variiert. Zwei durch ein Leerzeichen getrennte Werte können für einen asymmetrischen Effekt verwendet werden.
Zugausgleich                        |![Pull compensation example](/assets/images/docs/params-satin-pull_compensation.png)|Satinstiche [ziehen den Stoff zusammen](/tutorials/push-pull-compensation/), was zu einer Säule führt, die schmaler ist, als in Inkscape geplant. Diese Einstellung erweitert jedes Nadeleinstichpaar von der Mitte der Satinsäule nach außen. Es muss experimentell bestimmt werden, wie viel Kompensation für deine Kombination aus Stoff, Faden und Stabilisator benötigt wird. Zwei durch ein Leerzeichen getrennte Werte können für einen asymmetrischen Effekt genutzt werden
Konturlinien umkehren               |![Reverse Rung](/assets/images/docs/satin-reverse-rung.png) | Optionen:<br /> ◦ Automatisch, die Standardeinstellung dreht eigenständig gegenläufige Außenkonturen<br />◦ Nicht umkehren, deaktiviert automatisches drehen<br />◦ Erste Konturlinie umkehren<br />◦ Zweite Konturlinie umkehren <br />◦ Beide Konturlinien umkehren
Seiten umkehren                     | | Kehrt die Seiten der Satinsäule um (links und rechts). Dies beeinflusst z.B. an welcher Seite der Faden startet und endet. Aber auch jede andere seitenbezogene Einstellung ist hiervon betroffen.
Vernähen erlauben                   | |Vernäht bei Bedarf an den ausgewählten Positionen
Vernähen erzwingen                  | |Vernäht den Faden nach diesem Element, auch dann, wenn der Abstand zum Folgeobjekt geringer ist als in den [Ink/Stitch Einstellungen](/de/docs/preferences/) definiert.
Anstecher                           | |Wähle die [Anstecher](/de/docs/stitches/lock-stitches) Variante (Anfang).
Verstecher                          | |Wähle die [Verstecher](/de/docs/stitches/lock-stitches) Variante (Ende).
Fadenschnitt                        | |Schneidet den Faden nachdem dieses Objekt genäht wurde
Stopp                               | |Stoppt die Maschine nachdem dieses Objekt genäht wurde und springt zur Stopp-Position (sofern vorhanden)
Zufälliger Prozentwert (Erweitern)  |![Random width increase](/assets/images/docs/params-satin-random-width-increase.png)| Lengthen stitch across rails at most this percent. Two values separated by a space may be used for an aysmmetric effect.
Zufälliger Prozentwert (Verkleinern)|![Random width decrease](/assets/images/docs/params-satin-random-width-decrease.png)| Shorten stitch across rails at most this percent. Two values separated by a space may be used for an aysmmetric effect.
Zufallswert Zick-Zack-Abstand (Prozent)|![Random zigzag spacing](/assets/images/docs/params-satin-random-zigzag-spacing.png)| Maximale randomisierte Abweichung der Stichabstände in Prozent
Zufälliges Zittern für Zwischenstiche|![Random split stitch jitter](/assets/images/docs/params-satin-random-split-stitch-jitter.png)| Wenn die Option für randomisierte Zwischenstiche aktiviert ist, wird die Stichlänge für Zwischenstiche randomisiert. Ist die Option deaktiviert, bezieht sich der Wert auf die Zwischenstich-Positionen
Randomisierte Zwischenstiche         |☑ | Kontrolliert ob die Zwischenstiche mittig liegen oder sich zufällig über die Stichkänge verteilen (dies kann ggf. die Stichanzahl erhöhen).
Minimale Stichlänge für randomisierte Zwischenstiche|  | Wenn leer, wird der Wert für die maximale Stichlänge verwendet. Kleinere Werte erlauben einen Übergang von Einzelstich zu Teilstich.
Zufallszahl                          | | Zufallswert für randomisierte Attribute. Falls leer wird die Element-ID verwendet.
{: .params-table }

### Mittellinien Unterlage

Dies ist eine Reihe von Geradstichen in der Mitte der Säule und zurück. Sie kann für schmale Satinsäulen vollkommen ausreichend sein, kann aber auch als Grundlage für komplexere Unterlagen verwendet werden.

![Params - Center-Walk Underlay Example](/assets/images/docs/params-center-walk-underlay-example.jpg)

Einstellung      |Beschreibung
---|---
Stichlänge       |Stichlänge (in mm)
Repeats          |Odd numbers of repeats will reverse the stitch direction of the satin column, causing it to start and end at the same position.
Position         |Position of underlay from between the rails. 0% is along the first rail, 50% is centered, 100% is along the second rail.
{: .table-full-width }

### Konturunterlage

Dies ist eine Reihe von Geradstichen die auf einer Seite der Säule hoch und auf der anderen Seite wieder runter laufen. Sie eignet sich für kleine bis mittlere Satinsäulen.

![Params - Contour Underlay Example](/assets/images/docs/params-contour-underlay-example.jpg)

Einstellung    |Beschreibung
---|---
Stichlänge     |Stichlänge (in mm)
Einzug         |Einrückung um die Unterlage vollständig von der obenliegenden Schicht zu überdecken. Negative Werte sind möglich.
Inset distance (proportional |Shrink the outline by a proportion of the column width, to prevent the underlay from showing around the outside of the satin column. Negative values are possible.


### Zick-Zack Unterlage

Dies ist im Wesentlichen ein Satinstich mit geringerer Dichte, der an das Ende der Säule und zurück an den Anfang genäht wird. Wird eine Konturunterlage hinzugefügt, die "Deutsche Unterlage". Mr. X Stitch hat einen [Artikel](https://www.mrxstitch.com/underlay/) zum Thema, der das gut erklärt. Für breite Säulen oder anspruchsvolle Stoffe können alle drei Unterlagentypen zusammen verwendet werden.

![Params - Zig-Zag Underlay Example](/assets/images/docs/params-zigzag-underlay-example.jpg)

Einstellung          ||Beschreibung
---|---|---
Einzug (proportional)||Einrückung um die Unterlage vollständig von der obenliegenden Schicht zu überdecken. Negative Werte sind möglich. Voreinstellung: Hälfte des Einzuges der Konturunterlage.
Einzug (fest)        ||Einrückung um die Unterlage vollständig von der obenliegenden Schicht zu überdecken. Negative Werte sind möglich. Voreinstellung: Hälfte des Einzuges der Konturunterlage
Maximale Stichlänge  |![Maximum stitch length](/assets/images/docs/params-satin-maximum_stitch_length.png) | Stiche die diesen Wert übersteigen, werden geteilt.
Zick-Zack Abstand    ||Der Spitze zu Spitze Abstand zwischen den Zick-Zack-Stichen.

## Satin Werkzeuge

Für Satinsäulen stellt Ink/Stitch einige hilfreiche [Werkzeuge](/de/docs/satin-tools/) bereit, die dir das Arbeiten mit Satinsäulen erheblich erleichtern können.

## Beispieldateien mit Satinsäulen

{% include tutorials/tutorial_list key="stichart" value="Satinstich" %}

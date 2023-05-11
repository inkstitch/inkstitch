---
title: "Neuerungen und Fehlerbehebungen Ink/Stitch v3.0.0"
permalink: /de/upcoming/
last_modified_at: 2023-05-11
sidebar:
  nav: pages
toc: true
---
## Allgemein

Ink/Stitch speichert bereits erstellte Stichpläne im Cacheund wird dadurch schneller.

## Neue Schriften

* [Abril En Fleur AGS](/de/fonts/abril/)

  ![Abril En Fleur AGS](/assets/images/fonts/abril_en_fleur.jpg)
* [Apex Simple AGS](/de/fonts/apex-lake/)

  ![Apex Simple AGS](/assets/images/fonts/apex_simple_AGS.jpg)
* [AGS Γαραμου Garamond](/de/fonts/AGS_greek_garamond/)

  ![AGS Γαραμου Garamond](/assets/images/fonts/garamond.png)
* [Emilio 20 simple](/de/fonts/emilio-20/)

  ![Emilio 20 simple](/assets/images/fonts/emilio_simple.png)
* [Emilio 20 bold](/de/fonts/emilio-20/)

  ![Emilio 20 bold](/assets/images/fonts/emilio_20_bold.png)
* [Emilio 20 Applique](/de/fonts/emilio-20/)

  ![Emilio 20 Applique](/assets/images/fonts/emilio_20_applique.png)

* Die Schrift `Grand Hotel` wurde in `Auberge` umbenannt

* Andere Schriftarten wurden verbesseret

## Elemente / Sticharten

### Neue Sticharten

#### Mäanderfüllung

[Meander fill](/de/docs/stitches/meander-fill) hat seinen Ursprung in Quilt-Techniken. Für das Maschinensticken ergibt sich ein schöner gemusterter Effekt. Große Bereiche können mit relativ wenigen Stichen befüllt werden.

![Meander Fill](/assets/images/tutorials/tutorial-preview-images/meandering_writing.jpg)

#### Spiralfüllung

Eine [Spiralfüllung](/de/docs/stitches/circular-fill) füllt eine Form mit einer gestickten Spirale. Der Mittelpunkt der Spirale liegt im Mittelpunkt des Elements. Eine Zielposition kann definiert werden um den Spiralmittelpunkt zu verschieben.

![Circular Fill](/assets/images/tutorials/tutorial-preview-images/circular_monogram.jpg)

### Neue Parameter

#### Fadenschnitt und Stopp-Befehle

  * Es ist nicht mehr nötig für diese Art von Befehlen Symbole zu verwenden, sie können direkt über den Parameter-Dialog aktiviert werden
  * [Befehle skalieren](/docs/commands/#scale-command-symbols): scales marker symbols as well (guide line & pattern symbols)

#### An- und Versticher (Stiche zum Vernähen)

  * Wähle aus einer Liste verschiedener An- und Verstecher
  * Skaliere Vernähstiche
  * Definiere eigene Vernähstiche

### Klone

  * Fix: Positionierung
  * Fix: automatische Berechnung der Füllwinkel

    ![Clone fill angle](/assets/images/docs/clone_fill_angle.png)

### Mehrfachgeradstich

  * Unterstütze die Eingabe von [Wiederholungsmustern](/de/docs/stitches/bean-stitch/#parameter) (1 0: ☰-☰-☰-)

    ![Bean pattern](/assets/images/docs/bean_pattern.jpg)

### Manuelle Stichpositionierung

  * Vernähstiche können über die Option `Vernähen erzwingen` aktiviert werden
  * Einstellung für maximale Stichlänge

### Füllstich

  * [Reihenanzahl bis sich das Muster wiederholt](/de/docs/stitches/fill-stitch/#parameter) erlaub nun auch Dezimalzahlen
  * [Reihenabstand (Ende)](/de/docs/stitches/fill-stitch/#parameter) ist nicht mehr versteckt, sondern über die Parametereinstellungen nutzbar (nützlich für Farbverläufe)
  * Werte für mehrere Unterlagen über den [Unterlagen Winkel](/de/docs/stitches/fill-stitch/#unterlage) werden jetzt nicht mehr durch ein Komma, sondern durch ein Leerzeichen getrennt

  * Fix: 'LineString' object has no attribute 'geoms'
  * Fix: 'Point' object has no attribute 'geoms'
  * Fix: ZeroDivisionError in intersect_region_with_grating
  * Fix: ZoneClose segments can not be changed into curves.
  * Fix: incorrect stagger in guided fill

### Satinsäule / E-Stich

  * [Optionen für Randomisierung](/de/docs/stitches/satin-column/#satin-top-layer): Stichlänge, Stichabstände, Länge/Anzahl der Teilungsstiche

    ![Bee](/assets/images/docs/random_satin.jpg)

  * [Zugkomensation](/docs/stitches/satin-column/#satin-top-layer)

    Asymmetrische Zugkomensation möglich durch die Eingabe zweier durch ein Leerzeichen getrennte Werte (mm, %)

  * Option [Konturlinien umkehren]((/docs/stitches/satin-column/#satinsäule)) direkt aus dem Parameterdialog

  * Fix: keine Fehlermeldung wenn eine Satinsäulen Füllung und Kontur hat

### Linie

  * Parameter sind jetzt flexibler. Gestrichelte Linien sind nicht mehr nötig.
    Es kann direkt in dem Parameterdialog zwischen den Sticharten gewechselt werden
  * Konsistentere Stichlänge
  * `svg:line` Elemente werden als normale Pfadelemente erkannt.

### Zickzack-Stich

  * Zugkompensation hinzugefügt

### Ripple Stitch

[Parameter](/de/docs/stitches/ripple-stitch/#parameter):
* Reihenanzahl bis sich das Muster wiederholt: Stiche werden besser platziert
* Minimaler Reihenabstand: konsistentere Dichte auch nach Skalierung eines Ripplestich-Elements (überschreibt den Wert für die Linienanzahl)

## Erweiterungen

### Neu: Farbverlauf in Blöcke aufteilen

Diese Erweiterung teilt ein Füllobjekt mit einem linearen Farbverlauf in mehrere einfarbige Blöcke auf und setzt den zuvor bestimmten Wert für Reihenabstand Ende.

![Gradient](/assets/images/docs/color_blocks.png)

Erweiterungen > Ink/Stitch > Tools: Füllung > [Convert to gradient blocks](/de/docs/fill-tools/#farbverlauf-in-blöcke-aufteilen)

### Neu: Text entlang Pfad

Platziert einen Text aus dem Text-Modul auf einen Pfad ohne die Schriftzeichen zu deformieren

![Lettering along path](/assets/images/docs/lettering_along_path.png)

Erweiterungen > Ink/Stitch > [Text entlang Pfad](/de/docs/lettering/#schrift-entlang-pfad)

### Neu: Sprungstich zu Geradstich

Generiert eine Verbindungs-Linie zwischen aufeinanderfolgenden Elementen

![Jump to Stroke](/assets/images/docs/jump_to_stroke.png)

*1: Original 2: Sprungstich zu Geradstich 3: Manuelle Anpassung des Pfadverlaufs*

Erweiterungen > Ink/Stitch > Werkzeuge: Stroke > [Sprungstich zu Geradstich](/de/docs/stroke-tools/#sprungstich-zu-geradstich)

### Neu: Füllung zu Mittellinie

Generiert die Mittellinie eines Füllobjekts

![Fill to Stroke](/assets/images/docs/fill_to_stroke.png)

Erweiterungen > Ink/Stitch > Werkzeuge: Stroke > [Füllung zu Mittellinie](/de/docs/stroke-tools/#füllung-zu-mittellinie)

### Neu: Linie zu Pfadeffekt-Satin

Konvertiert eine Linie in einen Pfadeffekt der als Satinsäule genutzt und einfach angepasst werden kann

![LPE Satins](/assets/images/docs/lpe_patterns.png)

Erweiterungen > Ink/Stitch > Werkzeuge: Satin: [Linie zu Pfadeffekt-Satin](/docs/satin-tools/#linie-zu-pfadeffekt-satin)

### Neu: Zickzack-Linie zu Satin

Konvertiert eine Zickzack-Linie in eine Satinsäule

![Zigzag to Satin](/assets/images/docs/zigzag-line-to-satin.png)

Erweiterungen > Ink/Stitch > Werkzeuge: Satin > [Zickzack-Line zu Satin](/docs/satin-tools/#zickzack-linie-zu-satin)

### Neu: Ink/Stitch SVG aktualisieren

Ink/Stitch aktualisiert alte Designdateien automatisch. Bitte verwende diese Funktion nur, wenn du weißt, was du tust.

Erweiterungen > ink/Stitch > Fehlerbehebung > [Ink/Stitch SVG aktualisieren](/docs/troubleshoot/#inkstitch-svg-aktualisieren)

### Neu: Stickelemente auswählen

Wählt Elemente nach Stichart aus (funktioniert nicht für macOS)

Erweiterungen > Ink/Stitch > Bearbeiten > [Stickelemente auswählen...](/de/docs/edit/#stickelemente-auswählen)

### Automatisch geführter Geradstich

  * Fix: Behalte Toleranz-Einstellungen für Verbindungsstiche bei

### Linie zu Satinsäule

  * Fix: kein Abbruch bei Auswahl verschiedener Sticharten
  * Fix macOS: gleichseitige Konturlinien-Richtung

### Cutwork

  * Speichere Nadelinformation in .inf Dateien, so dass Bernina/Bernette Maschinen die [richtige Nadelnummern anzeigen](/de/docs/cutwork/#cutwork-mit-berninabernette) können
  * Fix: Breche die Umwandlung nicht ab, wenn das Element ebenfalls eine Füllung hat

### Text

  * Füge einen [Filter für Schriftgrößen](/de/docs/lettering/#optionen) hinzu
  * Aktiviere Optionen für das [Einfügen von Fadenschnitt-Befehlen](/de/docs/lettering/#optionen) für alle Schriften
  * Einzelne Schriften können in mehrere Dateien aufgeteilt werden. In diesem Fall erhält der Ordnernamen den Stickrichtungspfeil.
    So können verschiedene Autoren gleichzeitig an der gleichen Schrift arbeiten oder verhindern, dass die Datei aufgrund der Größe zu langsam wird.

  * Fix: Ignoriert ungültige Schriftzeichen 
  * Fix: verhindere Fehlermeldung von automatisch geführten Satinsäulen für Füllstiche (nicht vollständig digitalisierte Schriften können direkt genutzt werden)

### Parameter Simulator

  * Lädt schneller nach Parameter-Änderungen
  * Beachtet jetzt die Einstellung für die minimale Stichlänge

### Einstellungen

  * Standardwerte für neue SVG-Dateien können für die minimale Stichlänge und minimale Sprungstichlänge gesetzt werden
  * Lege die Größe des Cache-Speichers für Stichpläne fest

### PDF-Export
  * Neue Ansicht: Vollseitige Designansicht
  * Vorauswahl des PDF-Formats beim Speichern

### Simulator

  * Nutzt Hintergrundfarbe von Inkscape
  * Füge Skalierungsoptionen hinzu

### Stichplan

  * Füge Option hinzu um den [Stichplan für Mausinteraktionen zu blockieren](/de/docs/visualize/#stich-plan-vorschau)

### Fehlerbehebung

  * Füge Skalierungsoptionen hinzu

## Stickformate

  * Füge den Namen der Stickdatei in die Header-Information einiger Stickformate ein
  * Behebt ein Problem mit Stopp-Befehlen bezüglich der Farbanzahl

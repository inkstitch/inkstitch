---
title: "Visuelle Befehle"
permalink: /de/docs/commands/
excerpt: ""
last_modified_at: 2019-03-16
toc: true
---
## Installation

Vor Benutzung [visuelle Befehle installieren](/de/docs/addons/).

### Visuelle Befehle über die Erweiterung anhängen

* Wähle ein Objekt oder mehrere Objekte
* Starte `Erweiterungen -> Ink/stitch -> Sticken -> Befehle`
* Aktiviere die gewünschten Befehle und wenden sie an
* Bei Befehlen wo die Positionierung wichtig ist: Der Endpunkt des Zeigers, der dem Objekt am nächsten ist, ist der Punkt, an dem der Befehl ausgeführt wird.

Unter `Erweiterungen -> Ink/stitch -> Sticken -> Befehle` gibt es drei Optionen: `Befehle hinzufügen...`, `Ebenenbefehle hinzufügen...` und `Befehle mit gewählten Objekten verknüpfen...`.

### Befehle hinzufügen ...

Diese Befehle wirken sich auf das gesamte Motiv aus.

![stop position](/assets/images/docs/visual-commands-stop-position.jpg) [Stopp-Position](#-stopp-position)

![origin](/assets/images/docs/visual-commands-origin.jpg) [Nullpunkt](#-nullpunkt)

#### Ebenenbefehle hinzufügen ...

Diese Befehle wirken sich auf die aktive Ebene aus.

![ignore layer symbol](/assets/images/docs/visual-commands-ignore-layer.jpg) Ebene ignorieren

#### Befehle mit gewählten Objekten verknüpfen ...

Diese Befehle hängen sich an ausgewählte Objekte.

![starting point symbol](/assets/images/docs/visual-commands-start.jpg) Füllstich Startposition

![ending point symbol](/assets/images/docs/visual-commands-end.jpg) Füllstich Endposition

![trim symbol](/assets/images/docs/visual-commands-trim.jpg) [Faden trennen](#-faden-trennen) nach diesem Object

![stop symbol](/assets/images/docs/visual-commands-stop.jpg) [Stopp](#-stopp) (pause) nach diesem Objekt (z.B. für Applikationen)

![ignore symbol](/assets/images/docs/visual-commands-ignore.jpg) Ignoriere dieses Objekt

![satin cut point symbol](/assets/images/docs/visual-commands-satin-cut-point.jpg) [Satin-Schnittstelle](#-satin-schnittstelle) (mit "Satinkolumne schneide") benutzen

![auto route satin starting position symbol](/assets/images/docs/visual-commands-auto-route-satin-stitch-start.jpg) [Startposition](#--start--und-endposition-für-automatische-satinkolumnenführung) für automatische Satinkolumnenführung

![auto route satin starting position symbol](/assets/images/docs/visual-commands-auto-route-satin-stitch-end.jpg) [Endposition](#--start--und-endposition-für-automatische-satinkolumnenführung) für automatische Satinkolumnenführung

### Visuelle Befehle manuell anhängen
* Gehe zu `Objekt -> Symbole` oder benutze `Shift+Strg+Y`, um über den Symboldialog auf die Marker zuzugreifen.
* Wähle "Ink/Stitch Commands" als Symbolsatz.
  ![Symbolsatz](/assets/images/docs/en/visual-commands-symbol-set.jpg)
* Ziehe einen Marker auf den Arbeitsbereich (egal wo).
* Verwende das Flussdiagramm-Werkzeug ("Diagramm-Konnektoren erstellen", `Strg + F2`), um eine Verbindung zwischen dem Marker und dem Füllobjekt zu erstellen, auf das es angewendet werden soll. Dies wird einen Verbindungspfad hinzufügen.
* Wenn der Marker verschoben wird, ändert sich die Position der Verknüpfung. Die Endpunkte der Verknüpfung kann auch manuell verschoben werden. Der Endpunkt der Verknüpfung, der dem Füllobjekt am nächsten ist, ist der Punkt, an dem das Sticken beginnt oder endet.
  <div style="position: relative; padding-bottom: 50%; height: 0;">
    <iframe src="/assets/video/docs/visual-commands.m4v" frameborder="0" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
  </div>
  
  [![Visuelle Befehle](/assets/images/docs/visual-commands-fill-stitch.svg)](/assets/images/docs/visual-commands-fill-stitch.svg)

  [Beispieldatei](/assets/images/docs/visual-commands-fill-stitch.svg){: download="visual-commands-fill-stitch.svg" title="Download Sample"}

### Referenz der Visuellen Befehle

### ![trim symbol](/assets/images/docs/visual-commands-trim.jpg) Faden trennen

"Trim after" tells the embroidery machine to cut the thread after the assigned object has been stitched.  Not all home machines support the trim function within a color block.  Mainly used to prevent long jump stitched between embroidery objects and to avoid post embroidery trimming by the operator.

### ![stop symbol](/assets/images/docs/visual-commands-stop.jpg) Stopp

Kommerzielle Stickmaschinen mit mehreren Nadeln laufen normalerweise von einer Farbe zur nächsten, ohne dazwischen zu pausieren. Manchmal *möchte* man eine Pause (z.B. zum Beschneiden von Applikationsstoff), so fügt "danach stoppen" einen zusätzlichen Farbwechsel hinzu, die einem speziellen Stoppbefehl unter Verwendung der Benutzerschnittstelle des Geräts (z. B. C00 auf Barudan-Maschinen) zugewiesen werden kann. Üblicher Anwendung hierfür ist, dass auflegen von Puffschaum. Benutzen von Applikationsstoff und / oder sogar verlangsamen der Maschine an einer bestimmten Stelle für verschieden Arten einer Stickerei, ohne die Maschine beaufsichtigen zu müssen.

### ![stop position](/assets/images/docs/visual-commands-stop-position.jpg) Stopp-Position

Die Stickmaschine springt nach jedem Stopp-Befehl zu diesem Punkt. Das erleichtert die Applikationsarbeit, da man so den Rahmen zum Nutzer nach vorne bringen kann.

### ![origin](/assets/images/docs/visual-commands-origin.jpg) Nullpunkt

Dieser Befehlt definiert den Ursprung (0,0) für das Dokument. Nullpunkte sind besonders für diejenigen sinnvoll, die unabhängig vom Rahmen vollen Zugang zur gesamten Arbeitsfläche der Maschine haben.

### ![starting point symbol](/assets/images/docs/visual-commands-start.jpg) ![ending point symbol](/assets/images/docs/visual-commands-end.jpg) Anfangs- und Endposition für Füllstiche

Definiert (1) die Start- und (2) die Endposition bei Objekten mit Füllstich.

### ![auto route satin starting position symbol](/assets/images/docs/visual-commands-auto-route-satin-stitch-start.jpg) ![auto route satin ending position symbol](/assets/images/docs/visual-commands-auto-route-satin-stitch-end.jpg) Start- und Endposition für automatische Satinkolumnenführung

Definiert (1) die Start- und (2) die Endposition für automatish geführte Satinkolumnen. Benutze anschließend die Funktion "[Automatische Satinkolumnenführung](/de/docs/satin-tools/#automatische-satinkolumnenführung)".

### ![satin cut point symbol](/assets/images/docs/visual-commands-satin-cut-point.jpg) Satin-Schnittstelle

Dieser Befehlt definiert an welchem Punkt die Satinkolumne geschnitten werden soll. Benutze anschließend die Funktion "[Satinkolumne schneiden](/de/docs/satin-tools/#satinkolumne-schneiden)".

